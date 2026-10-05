"""（已废弃）组件装配逻辑；所有组件已迁移到主类的装饰器声明。"""

from __future__ import annotations

from typing import Any, List, Tuple


def build_plugin_components(plugin: Any) -> List[Tuple[Any, Any]]:
    """兼容占位：新体系下组件由装饰器声明，返回空列表。"""
    return []


__all__ = ["build_plugin_components"]
