# pyright: reportMissingImports=false
"""config_template: generate commented config.toml for selfie_painter."""
from __future__ import annotations
import logging
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
                    hint = _CONDITIONAL_HINTS.get(fname, "")
                    for rl in (d + hint).split(NL):
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
    cfg_path = Path(plugin_dir) / CONFIG_FILE_NAME
    try:
        if cfg_path.exists():
            existing = cfg_path.read_text(encoding="utf-8")
            if _COMMENT_MARKER in existing:
                return False
        if not schema:
            return False
        text = render_commented_config(config_data, schema)
        cfg_path.parent.mkdir(parents=True, exist_ok=True)
        cfg_path.write_text(text, encoding="utf-8")
        logger.info("[SelfiePainterV2] 已生成带注释的 config.toml（%d 行）", text.count(NL))
        return True
    except Exception as exc:
        logger.warning("[SelfiePainterV2] 生成带注释配置失败: %s", exc)
        return False

