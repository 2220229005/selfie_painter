# -*- coding: utf-8 -*-
"""自动生成的 pydantic 配置模型（SDK2）。由旧 CONFIG_SCHEMA 迁移。"""
from __future__ import annotations

from typing import Any, Dict, List, Literal, Optional
from maibot_sdk import PluginConfigBase, Field


class Sec_plugin(PluginConfigBase):
    __ui_label__ = '插件启用配置'
    __ui_icon__ = 'info'
    __ui_order__ = 1

    name: str = Field(default='画家麦麦的自拍日常', description='画家麦麦的自拍日常 — 智能多模型图片生成插件，支持文生图/图生图自动识别', json_schema_extra={'label': '插件名称', 'disabled': True, 'order': 1, 'rows': 3})
    config_version: str = Field(default='3.6.11', description='插件配置版本号', json_schema_extra={'label': '配置版本', 'disabled': True, 'order': 2, 'rows': 3})
    enabled: bool = Field(default=False, description='是否启用插件。开启后麦麦可以画画，关闭则所有画图功能都不可用', json_schema_extra={'label': '启用插件', 'order': 3, 'rows': 3})


class Sec_generation(PluginConfigBase):
    __ui_label__ = '图片生成默认配置'
    __ui_icon__ = 'image'
    __ui_order__ = 2

    default_model: str = Field(default='model1', description='默认使用的模型ID（对应模型管理中的配置）。第一次画图时使用这个模型，之后可通过 /dr set 命令切换', json_schema_extra={'label': '默认模型', 'placeholder': 'model1', 'hint': '对应模型管理中的模型ID（如model1、model2）', 'order': 1, 'rows': 3, 'example': 'model1'})


class Sec_access_control(PluginConfigBase):
    __ui_label__ = '聊天流访问控制'
    __ui_icon__ = 'shield'
    __ui_order__ = 12
    # 全局聊天流黑白名单。默认黑名单模式，即默认所有聊天流都可用，只有命中黑名单才会禁用

    mode: Literal['blacklist', 'whitelist'] = Field(default='blacklist', description='全局聊天流访问模式。blacklist=黑名单（默认，名单内禁用，其他全部允许）；whitelist=白名单（仅名单内允许）', json_schema_extra={'label': '全局模式', 'order': 1, 'rows': 3})
    list: List = Field(default_factory=lambda: [], description='全局聊天流列表。格式示例：qq:114514:private、qq:1919810:group', json_schema_extra={'label': '全局聊天流列表', 'placeholder': 'qq:1919810:group', 'hint': '每行一个聊天流ID', 'order': 2, 'rows': 3})


class Sec_cache(PluginConfigBase):
    __ui_label__ = '结果缓存配置'
    __ui_icon__ = 'database'
    __ui_order__ = 5

    enabled: bool = Field(default=False, description='是否启用结果缓存。开启后，相同的画图请求会复用之前的结果，节省时间和API费用', json_schema_extra={'label': '启用缓存', 'order': 1, 'rows': 3})
    max_size: int = Field(default=10, description='最大缓存数量。缓存图片超过这个数量后，会删除最旧的。建议 5-20', ge=1, le=100, json_schema_extra={'label': '最大缓存数', 'order': 2, 'rows': 3, 'depends_on': 'cache.enabled', 'depends_value': True})


class Sec_components(PluginConfigBase):
    __ui_label__ = '组件启用配置'
    __ui_icon__ = 'puzzle-piece'
    __ui_order__ = 3

    enable_unified_generation: bool = Field(default=True, description='是否启用智能画图功能。开启后麦麦会根据对话内容自动决定是否画图（支持文生图和图生图）', json_schema_extra={'label': '智能生图', 'order': 1, 'rows': 3})
    enable_pic_command: bool = Field(default=True, description='是否启用 /dr 命令。开启后可使用 /dr 风格名、/dr 描述 等命令画图', json_schema_extra={'label': '图片生成命令', 'order': 2, 'rows': 3})
    enable_pic_config: bool = Field(default=True, description='是否启用配置管理命令（/dr list、/dr set 等）。需要管理员权限才能使用', json_schema_extra={'label': '配置管理', 'order': 3, 'rows': 3})
    enable_pic_style: bool = Field(default=True, description='是否启用风格管理命令（/dr styles、/dr style 等）', json_schema_extra={'label': '风格管理', 'order': 4, 'rows': 3})
    pic_command_model: str = Field(default='model1', description='/dr 命令使用的模型ID。可通过 /dr set 命令动态切换', json_schema_extra={'label': 'Command模型', 'placeholder': 'model1', 'order': 5, 'rows': 3})
    enable_debug_info: bool = Field(default=False, description='是否显示调试信息。开启后会显示画图参数、耗时等信息，方便排查问题', json_schema_extra={'label': '调试信息', 'order': 6, 'rows': 3})
    enable_verbose_debug: bool = Field(default=False, description='是否显示详细调试信息。开启后会打印完整的HTTP请求报文（适合开发者调试）', json_schema_extra={'label': '详细调试', 'order': 7, 'rows': 3})
    show_all_prompts: bool = Field(default=False, description='是否在后台日志中显示本次实际送去生图接口的完整提示词。开启后日志会记录完整正面提示词、负面提示词和自拍风格，不会发送到QQ聊天界面', json_schema_extra={'label': '显示全部提示词', 'order': 8, 'rows': 3})
    admin_users: List = Field(default_factory=lambda: [], description='管理员QQ号列表（字符串格式）。只有管理员才能使用 /dr set、/dr model 等配置命令', json_schema_extra={'label': '管理员列表', 'placeholder': '["用户ID1", "用户ID2"]', 'hint': '字符串形式的用户ID，如 ["12345", "67890"]', 'order': 9, 'rows': 3})
    max_retries: int = Field(default=2, description='API调用失败时的重试次数。建议 1-3 次，太多会浪费时间', ge=0, le=10, json_schema_extra={'label': '重试次数', 'order': 10, 'rows': 3})


class Sec_proxy(PluginConfigBase):
    __ui_label__ = '代理设置'
    __ui_icon__ = 'globe'
    __ui_order__ = 4

    enabled: bool = Field(default=False, description='是否启用代理。开启后所有API请求都会通过代理服务器发送（适合网络受限的环境）', json_schema_extra={'label': '启用代理', 'order': 1, 'rows': 3})
    url: str = Field(default='http://127.0.0.1:7890', description='代理服务器地址。格式：http://IP:端口 或 socks5://IP:端口。示例: http://127.0.0.1:7890', json_schema_extra={'label': '代理地址', 'placeholder': 'http://127.0.0.1:7890', 'hint': '支持 HTTP、HTTPS、SOCKS5 代理', 'order': 2, 'rows': 3, 'depends_on': 'proxy.enabled', 'depends_value': True, 'example': 'http://127.0.0.1:7890'})
    timeout: int = Field(default=60, description='代理连接超时时间（秒）。建议 30-120 秒，太小可能连接失败', ge=10, le=300, json_schema_extra={'label': '超时时间', 'order': 3, 'rows': 3, 'depends_on': 'proxy.enabled', 'depends_value': True})


class Sec_styles(PluginConfigBase):
    __ui_label__ = '风格定义'
    __ui_icon__ = 'palette'
    __ui_order__ = 10
    # 预设风格的提示词。添加更多风格请直接编辑 config.toml，格式：风格英文名 = "提示词"

    cartoon: str = Field(default='cartoon style, anime style, colorful, vibrant colors, clean lines', description='卡通风格提示词', json_schema_extra={'label': '卡通风格', 'order': 1, 'input_type': 'textarea', 'rows': 3})


class Sec_style_aliases(PluginConfigBase):
    __ui_label__ = '风格别名'
    __ui_icon__ = 'tag'
    __ui_order__ = 11
    # 风格的中文别名映射。添加更多别名请直接编辑 config.toml

    cartoon: str = Field(default='卡通', description='cartoon 风格的中文别名，支持多别名用逗号分隔', json_schema_extra={'label': '卡通别名', 'placeholder': '卡通,动漫', 'order': 1, 'rows': 3})


class Sec_selfie(PluginConfigBase):
    __ui_label__ = '自拍模式配置'
    __ui_icon__ = 'camera'
    __ui_order__ = 6

    enabled: bool = Field(default=False, description='是否启用自拍模式。开启后麦麦可以发自拍（会自动添加角色外观描述）', json_schema_extra={'label': '是否启用自拍模式。开启后麦麦可以发自拍（会自动添加角色外观描述）', 'rows': 3})
    reference_image_path: str = Field(default='', description='自拍参考图片路径。配置后会用这张图作为参考生成自拍（图生图模式），留空则纯文字生成', json_schema_extra={'label': '参考图片', 'placeholder': 'images/reference.png', 'order': 2, 'rows': 3, 'depends_on': 'selfie.enabled', 'depends_value': True})
    prompt_prefix: str = Field(default='', description='自拍专用外观描述。描述麦麦的样子（发色、瞳色、服装等），会自动添加到所有自拍提示词前', json_schema_extra={'label': '提示词前缀', 'placeholder': 'blue hair, red eyes, school uniform, 1girl', 'order': 3, 'input_type': 'textarea', 'rows': 2, 'depends_on': 'selfie.enabled', 'depends_value': True})
    negative_prompt: str = Field(default='', description='自拍专用负面提示词。避免生成不想要的内容（手部畸形、多指等会自动添加）', json_schema_extra={'label': '负面提示词', 'placeholder': 'lowres, bad anatomy, bad hands, extra fingers', 'order': 4, 'input_type': 'textarea', 'rows': 3, 'depends_on': 'selfie.enabled', 'depends_value': True})
    schedule_enabled: bool = Field(default=True, description='是否启用日程增强自拍。开启后自拍会结合当前日程活动生成更贴合情境的场景', json_schema_extra={'label': '日程增强', 'order': 5, 'rows': 3, 'depends_on': 'selfie.enabled', 'depends_value': True})
    default_style: Literal['standard', 'mirror', 'photo'] = Field(default='standard', description='默认自拍风格。standard=前置自拍（拿手机），mirror=对镜自拍，photo=第三人称照片', json_schema_extra={'label': '默认自拍风格', 'order': 6, 'rows': 3, 'depends_on': 'selfie.enabled', 'depends_value': True})
    show_prompt_details: bool = Field(default=False, description='是否在后台日志中完整显示自拍模式本次使用的提示词与负面提示词，仅用于排查风格是否真的切换，不会发送到QQ聊天界面', json_schema_extra={'label': '自拍显示提示词', 'order': 7, 'rows': 3, 'depends_on': 'selfie.enabled', 'depends_value': True})
    raw_mode: bool = Field(default=False, description='裸模式：开启后跳过所有固定自拍场景词（standard/mirror/photo 模板）和固定负面提示词（手部质量词、设备词），只保留 prompt_prefix、用户描述、手部动作、日程表情/光线/环境。开启后请在 prompt_prefix 或用户描述中自行补充完整的构图、视角等提示词，否则画面构图可能不稳定。', json_schema_extra={'label': '裸模式（跳过固定提示词）', 'order': 8, 'rows': 3, 'depends_on': 'selfie.enabled', 'depends_value': True})


class Sec_wardrobe(PluginConfigBase):
    __ui_label__ = '衣柜系统'
    __ui_icon__ = 'shirt'
    __ui_order__ = 11
    # 管理“穿搭(Outfit)”的配置入口：你可以在这里添加多套衣服标签，并让自拍根据日程活动自动注入合适的服装提示词；中文穿搭会优先映射或翻译成英文标签后再注入

    enabled: bool = Field(default=False, description='是否启用衣柜系统。开启后自拍会根据日程活动自动选择合适的服装', json_schema_extra={'label': '启用衣柜', 'order': 1, 'rows': 3})
    daily_outfits: List = Field(default_factory=lambda: ['哥特洛丽塔', '宽松休闲装', '黑丝JK', '白丝JK'], description="每日穿搭列表。每天随机选一套作为当日穿搭。可写简短名称（如'哥特洛丽塔'）由LLM补充细节", json_schema_extra={'label': '每日穿搭', 'order': 10, 'rows': 3, 'depends_on': 'wardrobe.enabled', 'depends_value': True})
    auto_scene_change: bool = Field(default=True, description='自动场景换装。开启后根据日程活动自动匹配场景并换装（如睡觉时换睡衣）', json_schema_extra={'label': '自动换装', 'order': 20, 'rows': 3, 'depends_on': 'wardrobe.enabled', 'depends_value': True})
    custom_scenes: List = Field(default_factory=lambda: ['睡觉的时候穿可爱睡衣', '运动的时候穿运动服'], description="自定义场景规则。一句话格式：'在XX的时候穿XX'。例如：'在实验室的时候穿实验服'", json_schema_extra={'label': '自定义场景', 'order': 30, 'rows': 3, 'depends_on': 'wardrobe.auto_scene_change', 'depends_value': True})


class Sec_auto_recall(PluginConfigBase):
    __ui_label__ = '自动撤回配置'
    __ui_icon__ = 'trash'
    __ui_order__ = 11

    enabled: bool = Field(default=False, description='是否启用自动撤回功能（总开关）。关闭后所有模型的撤回都不生效', json_schema_extra={'label': '启用撤回', 'order': 1, 'rows': 3})


class Sec_prompt_optimizer(PluginConfigBase):
    __ui_label__ = '提示词优化器'
    __ui_icon__ = 'wand-2'
    __ui_order__ = 10
    # 使用 MaiBot 主 LLM 将用户描述优化为专业绘画提示词

    enabled: bool = Field(default=True, description='是否启用提示词优化器。开启后会使用 LLM 将用户描述优化为专业英文提示词（优先使用下方自定义API，未配置则使用 MaiBot 主 LLM）', json_schema_extra={'label': '启用优化器', 'order': 1, 'rows': 3})
    mode: Literal['nai', 'sd', 'natural_language'] = Field(default='sd', description='全局优化模式，手动画图与自动自拍共用。nai=NAI标签流，sd=SD标签流，natural_language=自然英文短语。模型配置中的 optimizer_mode_override 可单独覆盖', json_schema_extra={'label': '全局优化模式', 'order': 2, 'rows': 3, 'depends_on': 'prompt_optimizer.enabled', 'depends_value': True})
    custom_api_base_url: str = Field(default='', description='自定义API地址（OpenAI兼容格式）。留空则使用 MaiBot 主 LLM。示例：https://api.deepseek.com/v1、https://api.siliconflow.cn/v1', json_schema_extra={'label': '自定义API地址', 'placeholder': 'https://api.deepseek.com/v1', 'order': 3, 'rows': 3, 'depends_on': 'prompt_optimizer.enabled', 'depends_value': True})
    custom_api_key: str = Field(default='', description='自定义API密钥。直接填密钥即可（如 sk-xxx），系统会自动添加 Bearer 前缀。留空则使用 MaiBot 主 LLM', json_schema_extra={'label': '自定义API密钥', 'placeholder': 'sk-xxx', 'order': 4, 'input_type': 'text', 'rows': 3, 'depends_on': 'prompt_optimizer.enabled', 'depends_value': True})
    custom_api_model: str = Field(default='', description='自定义模型名称。例如：deepseek-chat、gpt-4o-mini、Qwen/Qwen2.5-7B-Instruct。留空则使用 MaiBot 主 LLM', json_schema_extra={'label': '自定义模型名称', 'placeholder': 'deepseek-chat', 'order': 5, 'rows': 3, 'depends_on': 'prompt_optimizer.enabled', 'depends_value': True})


class Sec_search_reference(PluginConfigBase):
    __ui_label__ = '角色参考图配置'
    __ui_icon__ = 'search'
    __ui_order__ = 10
    # 通过搜索引擎获取角色参考图，VLM 提取特征后注入提示词以提升角色一致性

    enabled: bool = Field(default=False, description='是否启用角色参考图（提升角色一致性）。启用后可通过 /dr refresh <角色名> 下载参考图', json_schema_extra={'label': '启用角色参考', 'order': 1, 'rows': 3})
    character_only: bool = Field(default=True, description="仅在'画某角色'这类请求时触发特征注入（关闭则所有生图请求都会尝试匹配）", json_schema_extra={'label': '仅角色请求触发', 'order': 2, 'rows': 3})
    max_images_per_role: int = Field(default=3, description='每个角色最多保存几张参考图', ge=1, le=10, json_schema_extra={'label': '最大参考图数', 'order': 3, 'rows': 3})
    search_top_k: int = Field(default=6, description='每次搜索候选图数量（越大越慢但命中率越高）', ge=3, le=20, json_schema_extra={'label': '搜索候选数', 'order': 4, 'rows': 3})
    max_cache_size_mb: int = Field(default=100, description='参考图库总容量上限 MB（超出会自动清理旧数据）', ge=10, le=1024, json_schema_extra={'label': '缓存上限 MB', 'order': 5, 'rows': 3})
    feature_boost_weight: float = Field(default=1.25, description='特征注入权重（越高越强调角色特征，1.0=不增强，2.0=最大增强）', ge=1.0, le=2.0, json_schema_extra={'label': '特征注入权重', 'order': 6, 'rows': 3, 'step': 0.05})
    vision_prompt: str = Field(default='请用中文详细描述这张图片中主要人物的特征是什么，纯粹描述即可。输出为一段平文本，总字数最多不超过120字。', description='VLM 识图提示词（一般不需修改）', json_schema_extra={'label': '识图提示词', 'order': 7, 'input_type': 'textarea', 'rows': 3})
    hint: str = Field(default='命令：/dr refresh <角色名>、/dr status <角色名>、/dr clear <角色名>', description='使用提示', json_schema_extra={'label': '使用提示', 'disabled': True, 'order': 8, 'rows': 3})


class Sec_schedule(PluginConfigBase):
    __ui_label__ = '内置日程配置'
    __ui_icon__ = 'calendar'
    __ui_order__ = 7
    # 内置 SQLite 日程系统（模板兜底 + LLM 生成）

    auto_generate_enabled: bool = Field(default=True, description='每日自动生成日程（内置日程系统，无需外部插件）', json_schema_extra={'label': '自动生成日程', 'order': 1, 'rows': 3})
    auto_generate_time: str = Field(default='06:30', description='每日自动生成时间，格式 HH:MM', json_schema_extra={'label': '生成时间', 'placeholder': '06:30', 'order': 2, 'rows': 3})
    model_id: str = Field(default='planner', description='日程生成使用的麦麦 LLM 模型。可用值：utils（组件模型）、tool_use（工具调用模型）、replyer（首要回复模型）、planner（决策模型，推荐）、vlm（图像识别模型）', json_schema_extra={'label': '日程模型', 'placeholder': 'planner', 'order': 3, 'rows': 3})
    schedule_identity: str = Field(default='', description="身份补充，用于让日程更贴合麦麦的身份设定。例如：'是一个二次元爱好者，喜欢画画'。会与主程序的人设配置合并使用", json_schema_extra={'label': '身份补充', 'placeholder': '是一个二次元爱好者，喜欢画画', 'order': 10, 'rows': 3})
    schedule_interest: str = Field(default='', description="兴趣爱好，用于让日程活动更符合麦麦的兴趣。例如：'画画、听音乐、打游戏、看番'。日程生成时会优先安排这些活动", json_schema_extra={'label': '兴趣爱好', 'placeholder': '画画、听音乐、打游戏、看番', 'order': 11, 'rows': 3})
    schedule_lifestyle: str = Field(default='', description="生活规律，用于让日程作息更符合麦麦的习惯。例如：'习惯晚睡，经常熬夜，早上起不来'。会影响日程的时间安排", json_schema_extra={'label': '生活规律', 'placeholder': '习惯晚睡，经常熬夜', 'order': 12, 'rows': 3})
    schedule_history_days: int = Field(default=1, description='历史日程参考天数。1=仅参考昨天(默认)；2=参考前两天；0=不参考历史。参考历史可让日程有连续性，比如昨天在学Python，今天继续学', ge=0, le=7, json_schema_extra={'label': '历史参考天数', 'order': 20, 'rows': 3})
    schedule_history_retention_days: int = Field(default=-1, description='历史日程保留天数。-1=永久保留(默认，数据量很小)；7=保留一周；30=保留一个月。超期的历史日程会被自动清理', ge=-1, le=365, json_schema_extra={'label': '历史保留天数', 'order': 21, 'rows': 3})
    schedule_custom_prompt: str = Field(default='', description="自定义日程风格要求(可选)。例如：'日程安排要宽松一些'。注意：不能改变输出格式，只能追加风格要求。留空则使用默认风格", json_schema_extra={'label': '日程风格要求', 'placeholder': '日程安排要宽松一些，多安排休息时间', 'order': 30, 'rows': 3})
    schedule_multi_round: bool = Field(default=True, description='是否启用多轮生成优化。开启后如果生成的日程质量不达标会自动重试修复。建议开启，可以避免日程空档、描述过短等问题', json_schema_extra={'label': '多轮生成优化', 'order': 40, 'rows': 3})
    schedule_max_rounds: int = Field(default=2, description='最大重试轮数。当日程质量不达标时最多重试几次。建议2-3次，太多会消耗更多token', ge=1, le=5, json_schema_extra={'label': '最大重试轮数', 'order': 41, 'rows': 3, 'depends_on': 'schedule.schedule_multi_round', 'depends_value': True})
    schedule_quality_threshold: float = Field(default=0.8, description='质量分数阈值(0.0-1.0)。生成的日程分数低于此阈值时会触发重试。建议0.75-0.85，太高可能导致频繁重试', ge=0.5, le=1.0, json_schema_extra={'label': '质量阈值', 'order': 42, 'rows': 3, 'depends_on': 'schedule.schedule_multi_round', 'depends_value': True})


class Sec_schedule_inject(PluginConfigBase):
    __ui_label__ = '日程注入配置'
    __ui_icon__ = 'inject'
    __ui_order__ = 9
    # 在 LLM 生成回复前注入麦麦当前日程信息，让回复更有代入感

    enabled: bool = Field(default=True, description='是否在 LLM 生成回复前注入麦麦当前日程信息', json_schema_extra={'label': '启用日程注入', 'order': 1, 'rows': 3})
    mode: str = Field(default='smart', description='注入模式。smart=智能节流（按时间/消息数触发），always=每次都注入', json_schema_extra={'label': '注入模式', 'placeholder': 'smart', 'order': 2, 'rows': 3})
    min_messages: int = Field(default=5, description='smart 模式下，同一会话收到多少条消息后再次注入', json_schema_extra={'label': '最小消息数', 'order': 3, 'rows': 3, 'depends_on': 'schedule_inject.enabled', 'depends_value': True})
    min_seconds: int = Field(default=300, description='smart 模式下，距离上次注入多少秒后再次注入', json_schema_extra={'label': '最小间隔（秒）', 'order': 4, 'rows': 3, 'depends_on': 'schedule_inject.enabled', 'depends_value': True})
    schedule_intent_enable: bool = Field(default=True, description='是否启用意图识别。开启后系统会识别用户意图，只在相关问题上注入日程。例如：技术问答时不注入，询问日程时注入。建议开启', json_schema_extra={'label': '意图识别', 'order': 10, 'rows': 3, 'depends_on': 'schedule_inject.enabled', 'depends_value': True})
    schedule_context_cache_ttl_minutes: int = Field(default=30, description='对话上下文缓存TTL(分钟)。用于记住最近的对话内容，让连续对话更自然。建议15-60分钟', ge=5, le=120, json_schema_extra={'label': '上下文缓存TTL', 'order': 11, 'rows': 3, 'depends_on': 'schedule_inject.enabled', 'depends_value': True})
    schedule_context_cache_max_turns: int = Field(default=10, description='对话上下文最大轮数。缓存最近的N轮对话，用于连续对话理解。建议5-20轮', ge=1, le=50, json_schema_extra={'label': '上下文最大轮数', 'order': 12, 'rows': 3, 'depends_on': 'schedule_inject.enabled', 'depends_value': True})


class Sec_auto_selfie(PluginConfigBase):
    __ui_label__ = '自动自拍配置'
    __ui_icon__ = 'camera'
    __ui_order__ = 8
    # 定时自动生成自拍并发送到聊天流或QQ空间。发送到聊天流无需额外插件；发布到QQ空间需安装 Maizone 插件。日程数据由内置日程系统提供

    enabled: bool = Field(default=False, description='是否启用自动自拍。日程数据由内置日程系统自动提供，发送到聊天流无需额外插件（若需发布到QQ空间，则需安装 Maizone 插件）', json_schema_extra={'label': '启用自动自拍', 'order': 1, 'rows': 3})
    interval_minutes: int = Field(default=120, description='自拍间隔（分钟）。建议 60-240 分钟，太频繁可能被限制', ge=10, le=1440, json_schema_extra={'label': '自拍间隔', 'order': 2, 'rows': 3, 'depends_on': 'auto_selfie.enabled', 'depends_value': True})
    selfie_model: str = Field(default='model1', description='自拍使用的模型ID。对应模型管理中的配置（如 model1、model2）', json_schema_extra={'label': '自拍模型', 'placeholder': 'model1', 'order': 3, 'rows': 3, 'depends_on': 'auto_selfie.enabled', 'depends_value': True})
    prompt_model_id: Literal['planner', 'replyer'] = Field(default='replyer', description='自动自拍场景和配文使用的 MaiBot LLM 模型。planner=决策模型，replyer=首要回复模型。该模型只负责构思场景/动作/配文，最终图片由自拍模型生成', json_schema_extra={'label': '自动自拍提示词模型', 'order': 4, 'rows': 3, 'depends_on': 'auto_selfie.enabled', 'depends_value': True})
    quiet_hours_start: str = Field(default='00:00', description='安静时段开始时间（HH:MM）。此时段内不发自拍，避免半夜打扰', json_schema_extra={'label': '安静开始', 'placeholder': '00:00', 'order': 5, 'rows': 3, 'depends_on': 'auto_selfie.enabled', 'depends_value': True, 'example': '00:00'})
    quiet_hours_end: str = Field(default='07:00', description='安静时段结束时间（HH:MM）', json_schema_extra={'label': '安静结束', 'placeholder': '07:00', 'order': 6, 'rows': 3, 'depends_on': 'auto_selfie.enabled', 'depends_value': True})
    caption_enabled: bool = Field(default=True, description='是否为自拍生成配文。开启后会用 LLM 根据日程生成文字描述', json_schema_extra={'label': '生成配文', 'order': 7, 'rows': 3, 'depends_on': 'auto_selfie.enabled', 'depends_value': True})
    send_to_qzone: bool = Field(default=False, description='是否将自动自拍发布到 QQ 空间说说。需要安装 Maizone 插件', json_schema_extra={'label': '发送到QQ空间', 'order': 8, 'rows': 3})
    send_to_chat: bool = Field(default=False, description='是否将自动自拍发送到指定群聊和私聊', json_schema_extra={'label': '发送到群聊/私聊', 'order': 9, 'rows': 3})
    target_groups: List = Field(default_factory=lambda: [], description='目标群号列表（纯数字字符串）。每行一个群号，send_to_chat 开启时生效', json_schema_extra={'label': '目标群号', 'placeholder': '123456789', 'hint': '填群号，每行一个', 'order': 10, 'rows': 3})
    target_users: List = Field(default_factory=lambda: [], description='目标私聊QQ号列表（纯数字字符串）。每行一个QQ号，send_to_chat 开启时生效', json_schema_extra={'label': '目标私聊QQ号', 'placeholder': '987654321', 'hint': '填QQ号，每行一个', 'order': 11, 'rows': 3})
    persist_state: bool = Field(default=True, description='是否持久化自拍状态。开启后重启不会立即自拍，而是等待剩余间隔', json_schema_extra={'label': '持久化自拍状态', 'order': 12, 'rows': 3, 'depends_on': 'auto_selfie.enabled', 'depends_value': True})


class Sec_models_model1(PluginConfigBase):
    __ui_label__ = '模型1配置'
    __ui_icon__ = 'box'
    __ui_order__ = 13

    name: str = Field(default='Krea-2-Turbo', description='模型显示名称。在 /dr list 命令中显示，方便识别', json_schema_extra={'label': '模型名称', 'order': 1, 'rows': 3, 'group': 'connection'})
    base_url: str = Field(default='https://api-inference.modelscope.cn/v1', description='API服务地址。各平台地址不同：魔搭=https://api-inference.modelscope.cn/v1，硅基流动=https://api.siliconflow.cn/v1，豆包=https://ark.cn-beijing.volces.com/api/v3', json_schema_extra={'label': 'API地址', 'order': 2, 'rows': 3, 'group': 'connection'})
    api_key: str = Field(default='Bearer YOUR_MODELSCOPE_TOKEN', description="API密钥。统一填写 'Bearer xxx' 格式，部分平台会自动处理", json_schema_extra={'label': 'API密钥', 'order': 3, 'input_type': 'text', 'rows': 3, 'group': 'connection'})
    format: Literal['openai', 'openai-chat', 'tuercha-NAI', 'gemini', 'doubao', 'modelscope', 'shatangyun', 'mengyuai', 'zai', 'comfyui'] = Field(default='modelscope', description='API格式。不同平台接口不同：openai=通用格式，modelscope=魔搭，doubao=豆包，gemini=Gemini，shatangyun=砂糖云(NovelAI)，comfyui=本地ComfyUI', json_schema_extra={'label': 'API格式', 'order': 4, 'rows': 3, 'group': 'connection'})
    model: str = Field(default='krea/Krea-2-Turbo', description='模型标识。填模型ID或模型名称，如 cancel13/liaocao。ComfyUI格式填工作流文件名', json_schema_extra={'label': '模型标识', 'order': 5, 'rows': 3, 'group': 'connection'})
    fixed_size_enabled: bool = Field(default=True, description='是否固定图片尺寸。开启后强制使用 default_size，关闭则由 LLM 自动选择合适尺寸', json_schema_extra={'label': '是否固定图片尺寸。开启后强制使用 default_size，关闭则由 LLM 自动选择合适尺寸', 'rows': 3})
    default_size: str = Field(default='1024x1024', description='默认图片尺寸。格式：宽x高。常见值：1024x1024、512x768、768x512', json_schema_extra={'label': '默认尺寸', 'order': 7, 'rows': 3, 'group': 'params'})
    seed: int = Field(default=-1, description='随机种子。-1=每次随机；固定值（如 42）可复现相同结果', ge=-1, le=2147483647, json_schema_extra={'label': '随机种子', 'order': 8, 'rows': 3, 'group': 'params'})
    guidance_scale: float = Field(default=1, description="引导强度（CFG）。控制AI'听话程度'。值越高越严格遵循提示词。推荐：魔搭/硅基流动 2.5-7.5", ge=0.0, le=20.0, json_schema_extra={'label': '引导强度', 'order': 9, 'rows': 3, 'group': 'params', 'step': 0.5})
    num_inference_steps: int = Field(default=8, description='推理步数。影响质量和速度。推荐 20-50，太少质量差，太多太慢', ge=1, le=150, json_schema_extra={'label': '推理步数', 'order': 10, 'rows': 3, 'group': 'params'})
    watermark: bool = Field(default=False, description='是否添加水印。部分平台会自动添加', json_schema_extra={'label': '是否添加水印。部分平台会自动添加', 'rows': 3})
    custom_prompt_add: str = Field(default='', description='正面提示词增强。自动添加到用户描述后面，用于统一风格', json_schema_extra={'label': '正面增强词', 'order': 12, 'input_type': 'textarea', 'rows': 2, 'group': 'prompts'})
    negative_prompt_add: str = Field(default='', description='负面提示词。避免生成不想要的内容（低质量、模糊、水印等）。豆包/Gemini 不支持此参数', json_schema_extra={'label': '负面提示词', 'order': 13, 'input_type': 'textarea', 'rows': 2, 'group': 'prompts'})
    artist: str = Field(default='', description='艺术家风格标签。仅砂糖云格式生效，留空则不添加', json_schema_extra={'label': '艺术家标签', 'order': 14, 'rows': 3, 'group': 'prompts'})
    support_img2img: bool = Field(default=True, description='是否支持图生图。根据模型能力填写，不支持会自动降级为文生图', json_schema_extra={'label': '支持图生图', 'order': 15, 'rows': 3, 'group': 'prompts'})
    optimizer_mode_override: Literal['follow_global', 'nai', 'sd', 'natural_language'] = Field(default='natural_language', description='该模型对提示词优化模式的覆盖设置（手动与自动自拍共用）。follow_global=跟随全局；nai=强制 NAI 标签模式；sd=强制 SD 标签模式；natural_language=强制自然语言模式。手动画图与自动自拍链路均生效', json_schema_extra={'label': '优化模式覆盖', 'order': 16, 'rows': 3, 'group': 'prompts'})
    auto_recall_delay: int = Field(default=0, description='自动撤回延时（秒）。大于0时启用撤回，需先开启自动撤回总开关', ge=0, le=120, json_schema_extra={'label': '撤回延时', 'order': 17, 'rows': 3, 'group': 'prompts'})
    cfg: float = Field(default=0, description='CFG Rescale 参数。仅砂糖云格式生效，一般填 0', ge=0.0, le=1.0, json_schema_extra={'label': 'CFG Rescale', 'hint': '仅砂糖云格式生效', 'order': 20, 'rows': 3, 'group': 'platform', 'step': 0.1})
    sampler: Literal['Euler', 'Euler a', 'DPM++ 2M Karras', 'DPM++ 2M SDE Karras', 'DPM++ 2S a Karras', 'DPM++ SDE Karras', 'k_euler_ancestral', 'k_euler', 'k_dpmpp_2s_ancestral', 'k_dpmpp_2m_sde', 'k_dpmpp_2m', 'k_dpmpp_sde'] = Field(default='Euler', description='采样器名称。魔搭文生图会发送该字段；砂糖云和 Tuercha-NAI 使用各自支持的名称', json_schema_extra={'label': '采样器', 'hint': '魔搭使用 Euler 等界面名称；砂糖云和 Tuercha-NAI 使用 k_euler_* 等专用名称', 'order': 21, 'rows': 3, 'group': 'platform'})
    nocache: int = Field(default=0, description='是否禁用缓存。仅砂糖云格式生效。0=使用缓存，1=禁用', ge=0, le=1, json_schema_extra={'label': '禁用缓存', 'hint': '仅砂糖云格式生效', 'order': 22, 'rows': 3, 'group': 'platform'})
    noise_schedule: Literal['karras', 'native', 'exponential', 'polyexponential'] = Field(default='karras', description='噪声调度方案。仅砂糖云格式生效。推荐 karras', json_schema_extra={'label': '噪声调度', 'hint': '仅砂糖云格式生效', 'order': 23, 'rows': 3, 'group': 'platform'})


class Sec_models_model2(PluginConfigBase):

    name: str = Field(default='Z-Image-Turbo', description='模型显示名称', json_schema_extra={'label': '模型名称', 'order': 1, 'rows': 3, 'group': 'connection'})
    base_url: str = Field(default='https://api-inference.modelscope.cn/v1', description='API服务地址', json_schema_extra={'label': 'API地址', 'order': 2, 'rows': 3, 'group': 'connection'})
    api_key: str = Field(default='Bearer YOUR_MODELSCOPE_TOKEN', description='API密钥，格式：Bearer xxx', json_schema_extra={'label': 'API密钥', 'order': 3, 'input_type': 'text', 'rows': 3, 'group': 'connection'})
    format: Literal['openai', 'openai-chat', 'tuercha-NAI', 'gemini', 'doubao', 'modelscope', 'shatangyun', 'mengyuai', 'zai', 'comfyui'] = Field(default='modelscope', description='API格式', json_schema_extra={'label': 'API格式', 'order': 4, 'rows': 3, 'group': 'connection'})
    model: str = Field(default='Tongyi-MAI/Z-Image-Turbo', description='模型标识', json_schema_extra={'label': '模型标识', 'order': 5, 'rows': 3, 'group': 'connection'})
    fixed_size_enabled: bool = Field(default=True, description='是否固定图片尺寸', json_schema_extra={'label': '固定尺寸', 'order': 6, 'rows': 3, 'group': 'params'})
    default_size: str = Field(default='1024x1024', description='默认图片尺寸', json_schema_extra={'label': '默认尺寸', 'order': 7, 'rows': 3, 'group': 'params'})
    seed: int = Field(default=-1, description='随机种子', ge=-1, le=2147483647, json_schema_extra={'label': '随机种子', 'order': 8, 'rows': 3, 'group': 'params'})
    guidance_scale: float = Field(default=1, description='引导强度', ge=0.0, le=20.0, json_schema_extra={'label': '引导强度', 'order': 9, 'rows': 3, 'group': 'params', 'step': 0.5})
    num_inference_steps: int = Field(default=12, description='推理步数', ge=1, le=150, json_schema_extra={'label': '推理步数', 'order': 10, 'rows': 3, 'group': 'params'})
    watermark: bool = Field(default=False, description='是否添加水印', json_schema_extra={'label': '水印', 'order': 11, 'rows': 3, 'group': 'params'})
    custom_prompt_add: str = Field(default='', description='正面提示词增强', json_schema_extra={'label': '正面增强词', 'order': 12, 'input_type': 'textarea', 'rows': 2, 'group': 'prompts'})
    negative_prompt_add: str = Field(default='', description='负面提示词', json_schema_extra={'label': '负面提示词', 'order': 13, 'input_type': 'textarea', 'rows': 2, 'group': 'prompts'})
    artist: str = Field(default='', description='艺术家风格标签（砂糖云专用）', json_schema_extra={'label': '艺术家标签', 'order': 14, 'rows': 3, 'group': 'prompts'})
    support_img2img: bool = Field(default=True, description='是否支持图生图', json_schema_extra={'label': '支持图生图', 'order': 15, 'rows': 3, 'group': 'prompts'})
    auto_recall_delay: int = Field(default=0, description='自动撤回延时（秒）', ge=0, le=120, json_schema_extra={'label': '撤回延时', 'order': 16, 'rows': 3, 'group': 'prompts'})
    cfg: float = Field(default=0, description='CFG Rescale（仅砂糖云格式生效）', ge=0.0, le=1.0, json_schema_extra={'label': 'CFG Rescale', 'hint': '仅砂糖云格式生效', 'order': 20, 'rows': 3, 'group': 'platform', 'step': 0.1})
    sampler: Literal['Euler', 'Euler a', 'DPM++ 2M Karras', 'DPM++ 2M SDE Karras', 'DPM++ 2S a Karras', 'DPM++ SDE Karras', 'k_euler_ancestral', 'k_euler', 'k_dpmpp_2s_ancestral', 'k_dpmpp_2m_sde', 'k_dpmpp_2m', 'k_dpmpp_sde'] = Field(default='Euler', description='采样器名称。魔搭文生图会发送该字段；砂糖云和 Tuercha-NAI 使用各自支持的名称', json_schema_extra={'label': '采样器', 'hint': '魔搭使用 Euler 等界面名称；砂糖云和 Tuercha-NAI 使用 k_euler_* 等专用名称', 'order': 21, 'rows': 3, 'group': 'platform'})
    nocache: int = Field(default=0, description='是否禁用缓存（仅砂糖云格式生效）', ge=0, le=1, json_schema_extra={'label': '禁用缓存', 'hint': '仅砂糖云格式生效', 'order': 22, 'rows': 3, 'group': 'platform'})
    noise_schedule: Literal['karras', 'native', 'exponential', 'polyexponential'] = Field(default='karras', description='噪声调度方案（仅砂糖云格式生效）', json_schema_extra={'label': '噪声调度', 'hint': '仅砂糖云格式生效', 'order': 23, 'rows': 3, 'group': 'platform'})
    optimizer_mode_override: Literal['follow_global', 'nai', 'sd', 'natural_language'] = Field(default='natural_language', description='该模型对提示词优化模式的覆盖设置（手动与自动自拍共用）。follow_global=跟随全局；nai=强制 NAI 标签模式；sd=强制 SD 标签模式；natural_language=强制自然语言模式。手动画图与自动自拍链路均生效', json_schema_extra={'label': '优化模式覆盖', 'order': 16, 'rows': 3, 'group': 'prompts'})


class Sec_models_model3(PluginConfigBase):

    name: str = Field(default='WAI-illustrious-SDXL-v17', description='模型显示名称', json_schema_extra={'label': '模型名称', 'order': 1, 'rows': 3, 'group': 'connection'})
    base_url: str = Field(default='https://api-inference.modelscope.cn/v1', description='API服务地址', json_schema_extra={'label': 'API地址', 'order': 2, 'rows': 3, 'group': 'connection'})
    api_key: str = Field(default='Bearer YOUR_MODELSCOPE_TOKEN', description='API密钥，格式：Bearer xxx', json_schema_extra={'label': 'API密钥', 'order': 3, 'input_type': 'text', 'rows': 3, 'group': 'connection'})
    format: Literal['openai', 'openai-chat', 'tuercha-NAI', 'gemini', 'doubao', 'modelscope', 'shatangyun', 'mengyuai', 'zai', 'comfyui'] = Field(default='modelscope', description='API格式', json_schema_extra={'label': 'API格式', 'order': 4, 'rows': 3, 'group': 'connection'})
    model: str = Field(default='HingXuan/WAI-illustrious-SDXL-v17', description='模型标识', json_schema_extra={'label': '模型标识', 'order': 5, 'rows': 3, 'group': 'connection'})
    fixed_size_enabled: bool = Field(default=True, description='是否固定图片尺寸', json_schema_extra={'label': '固定尺寸', 'order': 6, 'rows': 3, 'group': 'params'})
    default_size: str = Field(default='1024x1024', description='默认图片尺寸', json_schema_extra={'label': '默认尺寸', 'order': 7, 'rows': 3, 'group': 'params'})
    seed: int = Field(default=-1, description='随机种子', ge=-1, le=2147483647, json_schema_extra={'label': '随机种子', 'order': 8, 'rows': 3, 'group': 'params'})
    guidance_scale: float = Field(default=6, description='引导强度', ge=0.0, le=20.0, json_schema_extra={'label': '引导强度', 'order': 9, 'rows': 3, 'group': 'params', 'step': 0.5})
    num_inference_steps: int = Field(default=30, description='推理步数', ge=1, le=150, json_schema_extra={'label': '推理步数', 'order': 10, 'rows': 3, 'group': 'params'})
    watermark: bool = Field(default=False, description='是否添加水印', json_schema_extra={'label': '水印', 'order': 11, 'rows': 3, 'group': 'params'})
    custom_prompt_add: str = Field(default='masterpiece, best quality, newest, highres, aesthetic, ', description='正面提示词增强', json_schema_extra={'label': '正面增强词', 'order': 12, 'input_type': 'textarea', 'rows': 2, 'group': 'prompts'})
    negative_prompt_add: str = Field(default='worst quality, low quality, bad hands, mutated hands, blurry, lowres', description='负面提示词', json_schema_extra={'label': '负面提示词', 'order': 13, 'input_type': 'textarea', 'rows': 2, 'group': 'prompts'})
    artist: str = Field(default='', description='艺术家风格标签（砂糖云专用）', json_schema_extra={'label': '艺术家标签', 'order': 14, 'rows': 3, 'group': 'prompts'})
    support_img2img: bool = Field(default=True, description='是否支持图生图', json_schema_extra={'label': '支持图生图', 'order': 15, 'rows': 3, 'group': 'prompts'})
    auto_recall_delay: int = Field(default=0, description='自动撤回延时（秒）', ge=0, le=120, json_schema_extra={'label': '撤回延时', 'order': 16, 'rows': 3, 'group': 'prompts'})
    cfg: float = Field(default=0, description='CFG Rescale（仅砂糖云格式生效）', ge=0.0, le=1.0, json_schema_extra={'label': 'CFG Rescale', 'hint': '仅砂糖云格式生效', 'order': 20, 'rows': 3, 'group': 'platform', 'step': 0.1})
    sampler: Literal['Euler', 'Euler a', 'DPM++ 2M Karras', 'DPM++ 2M SDE Karras', 'DPM++ 2S a Karras', 'DPM++ SDE Karras', 'k_euler_ancestral', 'k_euler', 'k_dpmpp_2s_ancestral', 'k_dpmpp_2m_sde', 'k_dpmpp_2m', 'k_dpmpp_sde'] = Field(default='Euler a', description='采样器名称。魔搭文生图会发送该字段；砂糖云和 Tuercha-NAI 使用各自支持的名称', json_schema_extra={'label': '采样器', 'hint': '魔搭使用 Euler 等界面名称；砂糖云和 Tuercha-NAI 使用 k_euler_* 等专用名称', 'order': 21, 'rows': 3, 'group': 'platform'})
    nocache: int = Field(default=0, description='是否禁用缓存（仅砂糖云格式生效）', ge=0, le=1, json_schema_extra={'label': '禁用缓存', 'hint': '仅砂糖云格式生效', 'order': 22, 'rows': 3, 'group': 'platform'})
    noise_schedule: Literal['karras', 'native', 'exponential', 'polyexponential'] = Field(default='karras', description='噪声调度方案（仅砂糖云格式生效）', json_schema_extra={'label': '噪声调度', 'hint': '仅砂糖云格式生效', 'order': 23, 'rows': 3, 'group': 'platform'})
    optimizer_mode_override: Literal['follow_global', 'nai', 'sd', 'natural_language'] = Field(default='sd', description='该模型对提示词优化模式的覆盖设置（手动与自动自拍共用）。follow_global=跟随全局；nai=强制 NAI 标签模式；sd=强制 SD 标签模式；natural_language=强制自然语言模式。手动画图与自动自拍链路均生效', json_schema_extra={'label': '优化模式覆盖', 'order': 16, 'rows': 3, 'group': 'prompts'})


class Sec_models_model4(PluginConfigBase):

    name: str = Field(default='ChenkinNoob-XL-V0.5', description='模型显示名称', json_schema_extra={'label': '模型名称', 'order': 1, 'rows': 3, 'group': 'connection'})
    base_url: str = Field(default='https://api-inference.modelscope.cn/v1', description='API服务地址', json_schema_extra={'label': 'API地址', 'order': 2, 'rows': 3, 'group': 'connection'})
    api_key: str = Field(default='Bearer YOUR_MODELSCOPE_TOKEN', description='API密钥，格式：Bearer xxx', json_schema_extra={'label': 'API密钥', 'order': 3, 'input_type': 'text', 'rows': 3, 'group': 'connection'})
    format: Literal['openai', 'openai-chat', 'tuercha-NAI', 'gemini', 'doubao', 'modelscope', 'shatangyun', 'mengyuai', 'zai', 'comfyui'] = Field(default='modelscope', description='API格式', json_schema_extra={'label': 'API格式', 'order': 4, 'rows': 3, 'group': 'connection'})
    model: str = Field(default='ChenkinNoob/ChenkinNoob-XL-V0.5', description='模型标识', json_schema_extra={'label': '模型标识', 'order': 5, 'rows': 3, 'group': 'connection'})
    fixed_size_enabled: bool = Field(default=True, description='是否固定图片尺寸', json_schema_extra={'label': '固定尺寸', 'order': 6, 'rows': 3, 'group': 'params'})
    default_size: str = Field(default='1024x1024', description='默认图片尺寸', json_schema_extra={'label': '默认尺寸', 'order': 7, 'rows': 3, 'group': 'params'})
    seed: int = Field(default=-1, description='随机种子', ge=-1, le=2147483647, json_schema_extra={'label': '随机种子', 'order': 8, 'rows': 3, 'group': 'params'})
    guidance_scale: float = Field(default=6, description='引导强度', ge=0.0, le=20.0, json_schema_extra={'label': '引导强度', 'order': 9, 'rows': 3, 'group': 'params', 'step': 0.5})
    num_inference_steps: int = Field(default=30, description='推理步数', ge=1, le=150, json_schema_extra={'label': '推理步数', 'order': 10, 'rows': 3, 'group': 'params'})
    watermark: bool = Field(default=False, description='是否添加水印', json_schema_extra={'label': '水印', 'order': 11, 'rows': 3, 'group': 'params'})
    custom_prompt_add: str = Field(default='masterpiece, best quality, newest, highres, aesthetic, ', description='正面提示词增强', json_schema_extra={'label': '正面增强词', 'order': 12, 'input_type': 'textarea', 'rows': 2, 'group': 'prompts'})
    negative_prompt_add: str = Field(default='worst quality, low quality, bad hands, mutated hands, blurry, lowres', description='负面提示词', json_schema_extra={'label': '负面提示词', 'order': 13, 'input_type': 'textarea', 'rows': 2, 'group': 'prompts'})
    artist: str = Field(default='', description='艺术家风格标签（砂糖云专用）', json_schema_extra={'label': '艺术家标签', 'order': 14, 'rows': 3, 'group': 'prompts'})
    support_img2img: bool = Field(default=True, description='是否支持图生图', json_schema_extra={'label': '支持图生图', 'order': 15, 'rows': 3, 'group': 'prompts'})
    auto_recall_delay: int = Field(default=0, description='自动撤回延时（秒）', ge=0, le=120, json_schema_extra={'label': '撤回延时', 'order': 16, 'rows': 3, 'group': 'prompts'})
    cfg: float = Field(default=0, description='CFG Rescale（仅砂糖云格式生效）', ge=0.0, le=1.0, json_schema_extra={'label': 'CFG Rescale', 'hint': '仅砂糖云格式生效', 'order': 20, 'rows': 3, 'group': 'platform', 'step': 0.1})
    sampler: Literal['Euler', 'Euler a', 'DPM++ 2M Karras', 'DPM++ 2M SDE Karras', 'DPM++ 2S a Karras', 'DPM++ SDE Karras', 'k_euler_ancestral', 'k_euler', 'k_dpmpp_2s_ancestral', 'k_dpmpp_2m_sde', 'k_dpmpp_2m', 'k_dpmpp_sde'] = Field(default='Euler a', description='采样器名称。魔搭文生图会发送该字段；砂糖云和 Tuercha-NAI 使用各自支持的名称', json_schema_extra={'label': '采样器', 'hint': '魔搭使用 Euler 等界面名称；砂糖云和 Tuercha-NAI 使用 k_euler_* 等专用名称', 'order': 21, 'rows': 3, 'group': 'platform'})
    nocache: int = Field(default=0, description='是否禁用缓存（仅砂糖云格式生效）', ge=0, le=1, json_schema_extra={'label': '禁用缓存', 'hint': '仅砂糖云格式生效', 'order': 22, 'rows': 3, 'group': 'platform'})
    noise_schedule: Literal['karras', 'native', 'exponential', 'polyexponential'] = Field(default='karras', description='噪声调度方案（仅砂糖云格式生效）', json_schema_extra={'label': '噪声调度', 'hint': '仅砂糖云格式生效', 'order': 23, 'rows': 3, 'group': 'platform'})
    optimizer_mode_override: Literal['follow_global', 'nai', 'sd', 'natural_language'] = Field(default='sd', description='该模型对提示词优化模式的覆盖设置（手动与自动自拍共用）。follow_global=跟随全局；nai=强制 NAI 标签模式；sd=强制 SD 标签模式；natural_language=强制自然语言模式。手动画图与自动自拍链路均生效', json_schema_extra={'label': '优化模式覆盖', 'order': 16, 'rows': 3, 'group': 'prompts'})


class Sec_models_model5(PluginConfigBase):

    name: str = Field(default='MiaoMiao RealSkin EPS-v1.3', description='模型显示名称', json_schema_extra={'label': '模型名称', 'order': 1, 'rows': 3, 'group': 'connection'})
    base_url: str = Field(default='https://api-inference.modelscope.cn/v1', description='API服务地址', json_schema_extra={'label': 'API地址', 'order': 2, 'rows': 3, 'group': 'connection'})
    api_key: str = Field(default='Bearer YOUR_MODELSCOPE_TOKEN', description='API密钥，格式：Bearer xxx', json_schema_extra={'label': 'API密钥', 'order': 3, 'input_type': 'text', 'rows': 3, 'group': 'connection'})
    format: Literal['openai', 'openai-chat', 'tuercha-NAI', 'gemini', 'doubao', 'modelscope', 'shatangyun', 'mengyuai', 'zai', 'comfyui'] = Field(default='modelscope', description='API格式', json_schema_extra={'label': 'API格式', 'order': 4, 'rows': 3, 'group': 'connection'})
    model: str = Field(default='mixLine/miaomiaoRealskin', description='模型标识', json_schema_extra={'label': '模型标识', 'order': 5, 'rows': 3, 'group': 'connection'})
    fixed_size_enabled: bool = Field(default=True, description='是否固定图片尺寸', json_schema_extra={'label': '固定尺寸', 'order': 6, 'rows': 3, 'group': 'params'})
    default_size: str = Field(default='1024x1024', description='默认图片尺寸', json_schema_extra={'label': '默认尺寸', 'order': 7, 'rows': 3, 'group': 'params'})
    seed: int = Field(default=-1, description='随机种子', ge=-1, le=2147483647, json_schema_extra={'label': '随机种子', 'order': 8, 'rows': 3, 'group': 'params'})
    guidance_scale: float = Field(default=6, description='引导强度', ge=0.0, le=20.0, json_schema_extra={'label': '引导强度', 'order': 9, 'rows': 3, 'group': 'params', 'step': 0.5})
    num_inference_steps: int = Field(default=30, description='推理步数', ge=1, le=150, json_schema_extra={'label': '推理步数', 'order': 10, 'rows': 3, 'group': 'params'})
    watermark: bool = Field(default=False, description='是否添加水印', json_schema_extra={'label': '水印', 'order': 11, 'rows': 3, 'group': 'params'})
    custom_prompt_add: str = Field(default='masterpiece,very aesthetic,best quality,absurdres,newest,highres,ultra detailed ,anime coloring,depth of field,pale_skin,', description='正面提示词增强', json_schema_extra={'label': '正面增强词', 'order': 12, 'input_type': 'textarea', 'rows': 2, 'group': 'prompts'})
    negative_prompt_add: str = Field(default='lowres,(bad),bad hands,limb asymmetry,bad feet,text,error,fewer,extra,missing,worst quality,jpeg artifacts,low quality,watermark,unfinished,displeasing,oldest,early,chromatic aberration,signature,simple_background,artistic error,username,scan,[abstract],english text,shiny_skin', description='负面提示词', json_schema_extra={'label': '负面提示词', 'order': 13, 'input_type': 'textarea', 'rows': 2, 'group': 'prompts'})
    artist: str = Field(default='', description='艺术家风格标签（砂糖云专用）', json_schema_extra={'label': '艺术家标签', 'order': 14, 'rows': 3, 'group': 'prompts'})
    support_img2img: bool = Field(default=True, description='是否支持图生图', json_schema_extra={'label': '支持图生图', 'order': 15, 'rows': 3, 'group': 'prompts'})
    auto_recall_delay: int = Field(default=0, description='自动撤回延时（秒）', ge=0, le=120, json_schema_extra={'label': '撤回延时', 'order': 16, 'rows': 3, 'group': 'prompts'})
    cfg: float = Field(default=0, description='CFG Rescale（仅砂糖云格式生效）', ge=0.0, le=1.0, json_schema_extra={'label': 'CFG Rescale', 'hint': '仅砂糖云格式生效', 'order': 20, 'rows': 3, 'group': 'platform', 'step': 0.1})
    sampler: Literal['Euler', 'Euler a', 'DPM++ 2M Karras', 'DPM++ 2M SDE Karras', 'DPM++ 2S a Karras', 'DPM++ SDE Karras', 'k_euler_ancestral', 'k_euler', 'k_dpmpp_2s_ancestral', 'k_dpmpp_2m_sde', 'k_dpmpp_2m', 'k_dpmpp_sde'] = Field(default='Euler a', description='采样器名称。魔搭文生图会发送该字段；砂糖云和 Tuercha-NAI 使用各自支持的名称', json_schema_extra={'label': '采样器', 'hint': '魔搭使用 Euler 等界面名称；砂糖云和 Tuercha-NAI 使用 k_euler_* 等专用名称', 'order': 21, 'rows': 3, 'group': 'platform'})
    nocache: int = Field(default=0, description='是否禁用缓存（仅砂糖云格式生效）', ge=0, le=1, json_schema_extra={'label': '禁用缓存', 'hint': '仅砂糖云格式生效', 'order': 22, 'rows': 3, 'group': 'platform'})
    noise_schedule: Literal['karras', 'native', 'exponential', 'polyexponential'] = Field(default='karras', description='噪声调度方案（仅砂糖云格式生效）', json_schema_extra={'label': '噪声调度', 'hint': '仅砂糖云格式生效', 'order': 23, 'rows': 3, 'group': 'platform'})
    optimizer_mode_override: Literal['follow_global', 'nai', 'sd', 'natural_language'] = Field(default='sd', description='该模型对提示词优化模式的覆盖设置（手动与自动自拍共用）。follow_global=跟随全局；nai=强制 NAI 标签模式；sd=强制 SD 标签模式；natural_language=强制自然语言模式。手动画图与自动自拍链路均生效', json_schema_extra={'label': '优化模式覆盖', 'order': 16, 'rows': 3, 'group': 'prompts'})


class Sec_models_model6(PluginConfigBase):

    name: str = Field(default='MiaoMiao Harem v1.9', description='模型显示名称', json_schema_extra={'label': '模型名称', 'order': 1, 'rows': 3, 'group': 'connection'})
    base_url: str = Field(default='https://api-inference.modelscope.cn/v1', description='API服务地址', json_schema_extra={'label': 'API地址', 'order': 2, 'rows': 3, 'group': 'connection'})
    api_key: str = Field(default='Bearer YOUR_MODELSCOPE_TOKEN', description='API密钥，格式：Bearer xxx', json_schema_extra={'label': 'API密钥', 'order': 3, 'input_type': 'text', 'rows': 3, 'group': 'connection'})
    format: Literal['openai', 'openai-chat', 'tuercha-NAI', 'gemini', 'doubao', 'modelscope', 'shatangyun', 'mengyuai', 'zai', 'comfyui'] = Field(default='modelscope', description='API格式', json_schema_extra={'label': 'API格式', 'order': 4, 'rows': 3, 'group': 'connection'})
    model: str = Field(default='qsdq2423432/miaomiaoHarem_v19', description='模型标识', json_schema_extra={'label': '模型标识', 'order': 5, 'rows': 3, 'group': 'connection'})
    fixed_size_enabled: bool = Field(default=True, description='是否固定图片尺寸', json_schema_extra={'label': '固定尺寸', 'order': 6, 'rows': 3, 'group': 'params'})
    default_size: str = Field(default='1024x1024', description='默认图片尺寸', json_schema_extra={'label': '默认尺寸', 'order': 7, 'rows': 3, 'group': 'params'})
    seed: int = Field(default=-1, description='随机种子', ge=-1, le=2147483647, json_schema_extra={'label': '随机种子', 'order': 8, 'rows': 3, 'group': 'params'})
    guidance_scale: float = Field(default=6, description='引导强度', ge=0.0, le=20.0, json_schema_extra={'label': '引导强度', 'order': 9, 'rows': 3, 'group': 'params', 'step': 0.5})
    num_inference_steps: int = Field(default=30, description='推理步数', ge=1, le=150, json_schema_extra={'label': '推理步数', 'order': 10, 'rows': 3, 'group': 'params'})
    watermark: bool = Field(default=False, description='是否添加水印', json_schema_extra={'label': '水印', 'order': 11, 'rows': 3, 'group': 'params'})
    custom_prompt_add: str = Field(default='masterpiece, best quality, absurdres, newest, very aesthetic, amazing quality,highres,sensitive,complex background, highres, ultra detailed, best anatomy, HDR, 8K, high detail RAW color art, high contrast, depth of field', description='正面提示词增强', json_schema_extra={'label': '正面增强词', 'order': 12, 'input_type': 'textarea', 'rows': 2, 'group': 'prompts'})
    negative_prompt_add: str = Field(default='lowres,(bad),limb asymmetry,bad feet,text,error,fewer,extra,missing,worst quality,jpeg artifacts,low quality,watermark,unfinished,displeasing,oldest,early,chromatic aberration,signature,simple_background,artistic error,username,scan,[abstract],english text,shiny_skin', description='负面提示词', json_schema_extra={'label': '负面提示词', 'order': 13, 'input_type': 'textarea', 'rows': 2, 'group': 'prompts'})
    artist: str = Field(default='', description='艺术家风格标签（砂糖云专用）', json_schema_extra={'label': '艺术家标签', 'order': 14, 'rows': 3, 'group': 'prompts'})
    support_img2img: bool = Field(default=True, description='是否支持图生图', json_schema_extra={'label': '支持图生图', 'order': 15, 'rows': 3, 'group': 'prompts'})
    auto_recall_delay: int = Field(default=0, description='自动撤回延时（秒）', ge=0, le=120, json_schema_extra={'label': '撤回延时', 'order': 16, 'rows': 3, 'group': 'prompts'})
    cfg: float = Field(default=0, description='CFG Rescale（仅砂糖云格式生效）', ge=0.0, le=1.0, json_schema_extra={'label': 'CFG Rescale', 'hint': '仅砂糖云格式生效', 'order': 20, 'rows': 3, 'group': 'platform', 'step': 0.1})
    sampler: Literal['Euler', 'Euler a', 'DPM++ 2M Karras', 'DPM++ 2M SDE Karras', 'DPM++ 2S a Karras', 'DPM++ SDE Karras', 'k_euler_ancestral', 'k_euler', 'k_dpmpp_2s_ancestral', 'k_dpmpp_2m_sde', 'k_dpmpp_2m', 'k_dpmpp_sde'] = Field(default='Euler a', description='采样器名称。魔搭文生图会发送该字段；砂糖云和 Tuercha-NAI 使用各自支持的名称', json_schema_extra={'label': '采样器', 'hint': '魔搭使用 Euler 等界面名称；砂糖云和 Tuercha-NAI 使用 k_euler_* 等专用名称', 'order': 21, 'rows': 3, 'group': 'platform'})
    nocache: int = Field(default=0, description='是否禁用缓存（仅砂糖云格式生效）', ge=0, le=1, json_schema_extra={'label': '禁用缓存', 'hint': '仅砂糖云格式生效', 'order': 22, 'rows': 3, 'group': 'platform'})
    noise_schedule: Literal['karras', 'native', 'exponential', 'polyexponential'] = Field(default='karras', description='噪声调度方案（仅砂糖云格式生效）', json_schema_extra={'label': '噪声调度', 'hint': '仅砂糖云格式生效', 'order': 23, 'rows': 3, 'group': 'platform'})
    optimizer_mode_override: Literal['follow_global', 'nai', 'sd', 'natural_language'] = Field(default='sd', description='该模型对提示词优化模式的覆盖设置（手动与自动自拍共用）。follow_global=跟随全局；nai=强制 NAI 标签模式；sd=强制 SD 标签模式；natural_language=强制自然语言模式。手动画图与自动自拍链路均生效', json_schema_extra={'label': '优化模式覆盖', 'order': 16, 'rows': 3, 'group': 'prompts'})


class SelfiePainterConfig(PluginConfigBase):
    """selfie_painter 插件配置根模型。"""

    plugin: Sec_plugin = Field(default_factory=Sec_plugin)
    generation: Sec_generation = Field(default_factory=Sec_generation)
    access_control: Sec_access_control = Field(default_factory=Sec_access_control)
    cache: Sec_cache = Field(default_factory=Sec_cache)
    components: Sec_components = Field(default_factory=Sec_components)
    proxy: Sec_proxy = Field(default_factory=Sec_proxy)
    styles: Sec_styles = Field(default_factory=Sec_styles)
    style_aliases: Sec_style_aliases = Field(default_factory=Sec_style_aliases)
    selfie: Sec_selfie = Field(default_factory=Sec_selfie)
    wardrobe: Sec_wardrobe = Field(default_factory=Sec_wardrobe)
    auto_recall: Sec_auto_recall = Field(default_factory=Sec_auto_recall)
    prompt_optimizer: Sec_prompt_optimizer = Field(default_factory=Sec_prompt_optimizer)
    search_reference: Sec_search_reference = Field(default_factory=Sec_search_reference)
    schedule: Sec_schedule = Field(default_factory=Sec_schedule)
    schedule_inject: Sec_schedule_inject = Field(default_factory=Sec_schedule_inject)
    auto_selfie: Sec_auto_selfie = Field(default_factory=Sec_auto_selfie)
    models: Dict[str, Sec_models_model1] = Field(default_factory=lambda: {"model1": Sec_models_model1()})

# 触发 pydantic 重建（from __future__ annotations 下必需）
for _cls in list(vars().values()):
    if isinstance(_cls, type) and issubclass(_cls, PluginConfigBase) and _cls is not PluginConfigBase:
        _cls.model_rebuild()

