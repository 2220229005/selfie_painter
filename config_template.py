# pyright: reportMissingImports=false
"""config_template: generate commented config.toml for selfie_painter."""
from __future__ import annotations
import logging
import os
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Mapping
logger = logging.getLogger('selfie_painter_v2.config_template')
CONFIG_FILE_NAME = 'config.toml'
_COMMENT_MARKER = 'selfie_painter 配置文件（自动生成）'
_FILE_HEADER = '''# ============================================================================
# selfie_painter 配置文件（自动生成）
#
# 画家麦麦的自拍日常（麦麦绘卷）- 智能多模型图片生成插件
# 支持文生图 / 图生图自动识别，兼容 OpenAI、魔搭（ModelScope）、
# 硅基流动（SiliconFlow）、豆包、Gemini、ComfyUI 等多种 API 格式。
#
# 使用提醒：
#   1. 模型配置在文件末尾的 [models.modelN] 段，按需添加 / 修改。
#   2. 每个模型段必须包含 base_url、api_key、format、model 四个字段。
#   3. format 可选值：
#        openai         - 通用 OpenAI 兼容格式（硅基流动 / NewAPI / 多数中转站）
#        openai-chat    - 通过 chat/completions 生图的服务
#        modelscope     - 魔搭（ModelScope）异步生图
#        doubao         - 豆包（火山方舟）
#        gemini         - Google Gemini
#        shatangyun     - 砂糖云（NovelAI）
#        mengyuai       - 梦羽AI
#        zai            - Gemini 转发
#        comfyui        - 本地 ComfyUI
#        tuercha-NAI    - 兔儿查（NovelAI）
#   4. api_key 统一填写 Bearer xxx 格式。
#   5. 本文件由插件自动生成；手动修改后不会被覆盖（除非删除文件）。
# ============================================================================
'''
_EXTRA_NOTES = {
    'generation': '第一次画图时使用 default_model 指定的模型，之后可通过 /dr set 命令切换。',
    'styles': '预设风格的提示词。添加更多风格请直接编辑本段。使用方式：/dr 风格英文名 描述',
    'style_aliases': '风格的中文别名映射。添加更多别名请直接编辑本段。',
    'models': '插件支持多模型。添加更多模型：复制任一 [models.modelN] 整节，把 N 改成没用过的编号（如 model4、model5），然后填入对应参数即可。',
}
_CONDITIONAL_HINTS = {
    'artist': '（仅砂糖云格式生效）',
    'cfg': '（仅砂糖云格式生效）',
    'sampler': '（仅砂糖云格式生效）',
    'nocache': '（仅砂糖云格式生效）',
    'noise_schedule': '（仅砂糖云格式生效）',
}

def _fmt(v):
    if isinstance(v, bool):
        return "true" if v else "false"
    if isinstance(v, (int, float)):
        return str(v)
    if isinstance(v, str):
        esc = v.replace(chr(92), chr(92)*2).replace(chr(34), chr(92)+chr(34))
        return chr(34) + esc + chr(34)
    if isinstance(v, (list, tuple)):
        return "[" + ", ".join(_fmt(x) for x in v) + "]"
    if isinstance(v, Mapping):
        return "{ " + ", ".join(str(k)+" = "+_fmt(x) for k,x in v.items()) + " }"
    return chr(34)*2


def _desc(fi):
    if isinstance(fi, Mapping):
        return str(fi.get("description", "") or "")
    return str(getattr(fi, "description", "") or "")


def _dflt(fi, fb=""):
    if isinstance(fi, Mapping):
        return fi.get("default", fb)
    return getattr(fi, "default", fb)


def _secs(schema_keys, config):
    ordered = []
    for k in schema_keys:
        if k and k not in ordered:
            ordered.append(k)
    def walk(d, prefix=""):
        for k, v in d.items():
            full = (prefix + "." + k) if prefix else k
            if isinstance(v, Mapping):
                if full not in ordered:
                    ordered.append(full)
                walk(v, full)
    walk(config)
    return ordered


def _nget(config, dotted):
    cur = config
    for part in dotted.split("."):
        if isinstance(cur, Mapping) and part in cur:
            cur = cur[part]
        else:
            return {}
    return dict(cur) if isinstance(cur, Mapping) else {}


def _is_valid_toml(text):
    """校验文本是否为合法 TOML；用于识别被截断/损坏的配置文件。"""
    try:
        import tomllib

        tomllib.loads(text)
        return True
    except Exception:
        return False


def render_commented_config(config, schema):
    NL = chr(10)
    lines = []
    lines.append(_FILE_HEADER.rstrip(NL))
    lines.append("")
    lines.append("# 自动生成于 " + datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    lines.append("")
    all_sections = set(schema.keys())
    def is_sub(section, field):
        return ((section + "." + field) if section else field) in all_sections
    for section in _secs(schema.keys(), config):
        vals = _nget(config, section)
        fs = schema.get(section)
        has_schema = isinstance(fs, Mapping) and bool(fs)
        if not vals and not has_schema:
            continue
        lines.append("# " + "-" * 75)
        lines.append("# [" + section + "]")
        lines.append("# " + "-" * 75)
        if section in _EXTRA_NOTES:
            for rl in _EXTRA_NOTES[section].split(NL):
                lines.append("# " + rl)
        lines.append("[" + section + "]")
        lines.append("")
        emitted = set()
        if isinstance(fs, Mapping):
            for fname, fi in fs.items():
                if is_sub(section, fname):
                    continue
                d = _desc(fi)
                dv = _dflt(fi, "")
                val = vals.get(fname, dv)
                if d:
                    for rl in d.split(NL):
                        lines.append("# " + rl)
                lines.append(fname + " = " + _fmt(val))
                lines.append("")
                emitted.add(fname)
        for fname, val in vals.items():
            if fname in emitted or is_sub(section, fname):
                continue
            lines.append(fname + " = " + _fmt(val))
            lines.append("")
    return NL.join(lines).rstrip(NL) + NL


def ensure_commented_config(plugin_dir, config_data, schema):
    """若 config.toml 缺少注释，则用带注释版本重写。

    安全性说明：
        1. 已有本模块标记（_COMMENT_MARKER）时直接跳过，避免覆盖用户配置。
        2. 采用「临时文件 + os.replace」原子写入，杜绝写到一半（例如
           被外部编辑器/宿主并发写入打断）而产生半截损坏文件。
        3. 写入前先校验渲染结果可被 tomllib 解析，避免产出非法 TOML。

    Args:
        plugin_dir: 插件根目录。
        config_data: 当前配置数据（用于填充取值）。
        schema: 用于取注释的 CONFIG_SCHEMA。

    Returns:
        bool: 是否实际写入（True 表示已重写）。
    """
    NL = chr(10)
    cfg_path = Path(plugin_dir) / CONFIG_FILE_NAME
    tmp_path = cfg_path.with_name(cfg_path.name + ".tmp")
    try:
        if cfg_path.exists():
            existing = cfg_path.read_text(encoding="utf-8")
            if _COMMENT_MARKER in existing:
                # 有标记也要校验完整性：外部编辑器/并发写入可能把文件截断，
                # 此时必须重建，否则宿主会一直报“读取插件配置失败”。
                if _is_valid_toml(existing):
                    return False
                logger.warning(
                    "[SelfiePainterV2] 检测到 config.toml 已损坏（无法解析），将重新生成带注释版本"
                )
        if not schema:
            return False
        text = render_commented_config(config_data, schema)
        # 写入前自检：确保渲染结果确实是合法 TOML，避免污染用户的配置文件
        try:
            import tomllib

            tomllib.loads(text)
        except Exception as exc:
            logger.warning("[SelfiePainterV2] 渲染结果非法，已跳过写入: %s", exc)
            return False
        cfg_path.parent.mkdir(parents=True, exist_ok=True)
        # 原子写入：先写临时文件，fsync 后再 replace，避免出现半截文件
        with open(tmp_path, "w", encoding="utf-8") as handle:
            handle.write(text)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(tmp_path, cfg_path)
        logger.info("[SelfiePainterV2] 已生成带注释的 config.toml（%d 行）", text.count(NL))
        return True
    except Exception as exc:
        logger.warning("[SelfiePainterV2] 生成带注释配置失败: %s", exc)
        try:
            if tmp_path.exists():
                tmp_path.unlink()
        except Exception:
            pass
        return False

