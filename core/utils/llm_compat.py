"""LLM 兼容层：统一封装旧版 llm_api 调用

问题：SDK 兼容层 llm_api.get_available_models() 已弃用且永远返回空 dict，
导致所有依赖该函数的模块（日程生成、自拍配文、场景生成、手部动作）全部失败。

解决方案：跳过 get_available_models 检查，直接调用 generate_with_model()。
兼容层内部的 generate_with_model() 会调用 llm.generate()，
宿主会自动使用默认模型或按 model 字符串路由。
"""
from __future__ import annotations
import logging
from typing import Any, Optional

logger = logging.getLogger("selfie_painter_v2.llm_compat")


async def call_llm_generate(
    prompt: str,
    model_id: str = "replyer",
    request_type: str = "plugin.generate",
    temperature: float | None = None,
    max_tokens: int | None = None,
) -> tuple[bool, str, str, str]:
    """统一的 LLM 生成调用（绕过已弃用的 get_available_models）

    Args:
        prompt: 提示词
        model_id: 模型任务名（planner/replyer 等），传给宿主做路由
        request_type: 请求类型标识
        temperature: 温度
        max_tokens: 最大 token
    Returns:
        (success, content, reasoning, model_name)
    """
    try:
        from maibot_sdk.compat.apis import llm_api
    except Exception as e:
        logger.warning("无法导入 llm_api: %s", e)
        return False, "", "", ""

    # SDK 兼容层的 generate_with_model 内部会调用 llm.generate()，
    # 但它不传 model 参数（使用空字符串=默认模型）。
    # model_config 参数在新版 SDK 中被忽略，传 None 即可。
    try:
        success, content, reasoning, model_name = await llm_api.generate_with_model(
            prompt=prompt,
            model_config=None,  # SDK 兼容层忽略此参数
            request_type=request_type,
            temperature=temperature,
            max_tokens=max_tokens,
        )
        if not success:
            logger.warning("LLM 生成失败 (model_id=%s): %s", model_id, content[:100] if content else "")
        return success, content, reasoning, model_name
    except Exception as e:
        logger.error("LLM 生成异常 (model_id=%s): %s", model_id, e, exc_info=True)
        return False, "", "", ""
