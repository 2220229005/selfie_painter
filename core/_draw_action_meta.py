# Module-level metadata for @Action decorator (extracted from legacy class attrs)

DRAW_PICTURE_ACTION_DESCRIPTION = "智能图片生成：根据描述生成图片（文生图）或基于现有图片进行修改（图生图）。"
"自动检测用户是否提供了输入图片来决定使用文生图还是图生图模式。"
"支持多种API格式：OpenAI、豆包、Gemini、硅基流动、魔搭社区、砂糖云(NovelAI)、ComfyUI、梦羽AI等。"

DRAW_PICTURE_ACTIVATION_KEYWORDS = [
# 文生图关键词
"画",
"绘制",
"生成图片",
"画图",
"draw",
"paint",
"图片生成",
"创作",
# 图生图关键词
"图生图",
"修改图片",
"基于这张图",
"img2img",
"重画",
"改图",
"图片修改",
"改成",
"换成",
"变成",
"转换成",
"风格",
"画风",
"改风格",
"换风格",
"这张图",
"这个图",
"图片风格",
"改画风",
"重新画",
"再画",
"重做",
# 自拍关键词
"自拍",
"selfie",
"拍照",
"对镜自拍",
"镜子自拍",
"照镜子",
]

DRAW_PICTURE_ACTION_PARAMETERS = {
"description": "从用户消息中提取的图片描述文本（例如：用户说'画一只小猫'，则填写'一只小猫'）。必填参数。",
"model_id": "要使用的模型ID（如model1、model2、model3等，默认使用default_model配置的模型）",
"strength": "图生图强度，0.1-1.0之间，值越高变化越大（仅图生图时使用，可选，默认0.7）",
"size": "图片尺寸，如512x512、1024x1024等（可选，不指定则使用模型默认尺寸）",
"selfie_mode": "是否启用自拍模式（true/false，可选，默认false）。启用后会自动添加自拍场景和手部动作",
"selfie_style": "自拍风格，可选值：standard（标准自拍，前置摄像头视角），mirror（对镜自拍，室内镜子场景），photo（第三人称照片，他人拍摄视角，自然姿态）。仅在selfie_mode=true时生效，可选，默认standard",
"free_hand_action": "自由手部动作描述（英文，可选）。当前仅作为额外构图提示透传给最终提示词优化器，不再由本组件直接决定自拍手势或构图",
}

DRAW_PICTURE_ACTION_REQUIRE = [
"当用户明确对你提出生成或修改图片请求时使用，不要频率太高",
"群聊中必须是用户@你或叫你名字要求画图才使用，不要响应发给其他机器人的命令（如/nai、/sd等）",
"自动检测是否有输入图片来决定文生图或图生图模式",
"重点：不要连续发，如果你在前10句内已经发送过[图片]或者[表情包]或记录出现过类似描述的[图片]，就不要选择此动作",
"支持指定模型：用户可以通过'用模型1画'、'model2生成'等方式指定特定模型",
"自拍模式选择：用户要求'自拍/拍个自拍'时用standard；要求'照镜子/对镜拍'时用mirror；要求'拍张照片/画一张你在XX的照片/第三人称'等非自拍视角时用photo",
]

DRAW_PICTURE_ASSOCIATED_TYPES = ["text", "image"]
