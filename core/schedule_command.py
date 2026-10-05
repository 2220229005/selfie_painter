"""
/schedule 命令

子命令：
  /schedule          — 显示当前活动 + 当天全部日程 + 数据来源
  /schedule regen    — 用 LLM 重新生成今日日程
  /schedule inject on|off — 开启/关闭当前会话的日程注入
"""

import logging
from typing import Any, Optional, Tuple


logger = logging.getLogger(__name__)


class ScheduleCommandMixin:
    """Schedule command mixin."""

    @staticmethod
    def _format_time_range(start_min: int, end_min: int) -> str:
        """将分钟区间格式化为 HH:MM-HH:MM。"""
        start_hour, start_minute = divmod(start_min, 60)
        end_hour, end_minute = divmod(end_min, 60)
        return f"{start_hour:02d}:{start_minute:02d}-{end_hour:02d}:{end_minute:02d}"

    async def handle_schedule(
        self,
        stream_id: str = "",
        matched_groups: dict | None = None,
        **kwargs: Any,
    ) -> Tuple[bool, Optional[str], bool]:
        """执行 /schedule 命令

        Returns:
            Tuple[bool, Optional[str], bool]: (成功, 消息, 是否拦截)
        """
        matched_groups = matched_groups or {}
        self._current_stream_id = stream_id
        sub = (matched_groups.get("sub") or "").strip().lower()
        arg = (matched_groups.get("arg") or "").strip().lower()

        if not sub:
            return await self._show_schedule()
        elif sub == "regen":
            return await self._regen_schedule()
        elif sub == "inject":
            return await self._toggle_inject(arg)
        else:
            await self.ctx.send.text(
                "用法：\n"
                "/schedule — 查看当前日程\n"
                "/schedule regen — 重新生成今日日程\n"
                "/schedule inject on|off — 开关日程注入",
                self._current_stream_id,
            )
            return (True, None, True)

    async def _show_schedule(self) -> Tuple[bool, Optional[str], bool]:
        """显示当前活动和当天全部日程。"""
        try:
            from .schedule.schedule_manager import get_schedule_manager
            from datetime import date

            manager = get_schedule_manager()

            activity = await manager.get_current_activity()
            today = date.today().isoformat()
            items = await manager.list_schedule_items(today)

            lines = ["📅 麦麦的日程"]

            if activity:
                lines.append(f"🔵 现在：{activity.activity_type.value} — {activity.description}")
                if activity.mood and activity.mood != "neutral":
                    lines.append(f"   心情：{activity.mood}")
            else:
                lines.append("🔵 现在：暂无活动信息")

            if items:
                lines.append("📋 今日日程：")
                for item in items:
                    time_range = self._format_time_range(item.start_min, item.end_min)
                    lines.append(f"  {time_range} {item.description}")
            else:
                lines.append("📋 今日日程：暂无数据")

            # 数据来源
            try:
                if items:
                    source = items[0].source if hasattr(items[0], "source") else "unknown"
                    lines.append(f"📊 数据来源：{source}（共 {len(items)} 条）")
                else:
                    lines.append("📊 数据来源：无数据")
            except Exception:
                lines.append("📊 数据来源：未知")

            await self.ctx.send.text("\n".join(lines), self._current_stream_id)
            return (True, None, True)

        except Exception as e:
            logger.error(f"显示日程失败: {e}")
            await self.ctx.send.text(f"获取日程失败：{e}", self._current_stream_id)
            return (True, None, True)

    async def _regen_schedule(self) -> Tuple[bool, Optional[str], bool]:
        """用 LLM 重新生成今日日程"""
        try:
            from .schedule.schedule_manager import get_schedule_manager

            manager = get_schedule_manager()

            await self.ctx.send.text("🔄 正在用 LLM 重新生成今日日程...", self._current_stream_id)

            # regen_today_schedule_via_llm 需要一个有 get_config 方法的对象
            class _ConfigProxy:
                def __init__(self, config_dict):
                    self._config = config_dict

                def get_config(self, key, default=None):
                    keys = key.split(".")
                    current = self._config
                    for k in keys:
                        if isinstance(current, dict) and k in current:
                            current = current[k]
                        else:
                            return default
                    return current

            proxy = _ConfigProxy(self._config_bridge.raw)
            success = await manager.regen_today_schedule_via_llm(proxy)

            if success:
                await self.ctx.send.text("✅ 日程已重新生成！使用 /schedule 查看。", self._current_stream_id)
            else:
                await self.ctx.send.text("⚠️ LLM 生成失败，已回退到模板日程。", self._current_stream_id)

            return (True, None, True)

        except Exception as e:
            logger.error(f"重新生成日程失败: {e}")
            await self.ctx.send.text(f"重新生成失败：{e}", self._current_stream_id)
            return (True, None, True)

    async def _toggle_inject(self, arg: str) -> Tuple[bool, Optional[str], bool]:
        """开关当前会话的日程注入"""
        if arg not in ("on", "off"):
            await self.ctx.send.text("用法：/schedule inject on|off", self._current_stream_id)
            return (True, None, True)

        # 从 chat_stream 中获取 stream_id（MessageRecv 本身没有 stream_id 字段）
        stream_id = None
        stream_id = self._current_stream_id
        if not stream_id:
            await self.ctx.send.text("无法获取当前会话 ID", self._current_stream_id)
            return (True, None, True)

        try:
            from .schedule.schedule_manager import get_schedule_manager

            manager = get_schedule_manager()

            enabled = arg == "on"
            key = f"schedule_inject_enabled_override:{stream_id}"
            await manager.set_state(key, str(enabled).lower())

            status = "开启" if enabled else "关闭"
            await self.ctx.send.text(f"✅ 当前会话的日程注入已{status}", self._current_stream_id)
            return (True, None, True)

        except Exception as e:
            logger.error(f"切换注入状态失败: {e}")
            await self.ctx.send.text(f"操作失败：{e}", self._current_stream_id)
            return (True, None, True)
