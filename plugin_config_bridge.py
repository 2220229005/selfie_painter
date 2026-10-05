"""B2 迁移：插件配置读取桥接。

新版 SDK 中，插件配置通过 ctx.config.get_plugin()（异步 RPC）读取，
数据源为插件目录下的 config.toml。

本模块在 on_load 时一次性拉取整份配置并缓存，之后提供同步的点分键
查找接口 get(key, default)，作为旧版 self.get_config() 的等价替代，
避免 165 处调用点全部改成异步。
"""
from __future__ import annotations

import os
from typing import Any, Dict, Optional

try:
    import tomllib
except ModuleNotFoundError:  # pragma: no cover
    tomllib = None


class PluginConfigBridge:
    """插件配置读取桥接器（同步点分查找 + 本地缓存）。"""

    def __init__(self) -> None:
        self._cache: Dict[str, Any] = {}
        self._loaded: bool = False

    def load_from_dict(self, config: Optional[Dict[str, Any]]) -> None:
        self._cache = config if isinstance(config, dict) else {}
        self._loaded = True

    def load_from_toml(self, plugin_dir: str, file_name: str = "config.toml") -> None:
        config_path = os.path.join(plugin_dir, file_name)
        if tomllib is None or not os.path.exists(config_path):
            self._cache = {}
            self._loaded = True
            return
        try:
            with open(config_path, "rb") as handle:
                self._cache = tomllib.load(handle)
        except Exception:
            self._cache = {}
        self._loaded = True

    async def load_from_ctx(self, ctx: Any, plugin_dir: str = "", file_name: str = "config.toml") -> None:
        data: Optional[Dict[str, Any]] = None
        try:
            result = await ctx.config.get_plugin()
            if isinstance(result, dict) and result:
                data = result
        except Exception:
            data = None
        if data is None:
            if plugin_dir:
                self.load_from_toml(plugin_dir, file_name)
            else:
                self.load_from_dict({})
            return
        self.load_from_dict(data)

    @property
    def loaded(self) -> bool:
        return self._loaded

    @property
    def raw(self) -> Dict[str, Any]:
        return self._cache

    def get(self, key: str, default: Any = None) -> Any:
        current: Any = self._cache
        for part in str(key).split("."):
            if isinstance(current, dict) and part in current:
                current = current[part]
            else:
                return default
        return current


__all__ = ["PluginConfigBridge"]
