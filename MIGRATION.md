# 迁移说明：适配 maibot-plugin-sdk v2

本分支（`feature/dev-work`）将本插件从旧版 `src.plugin_system` 体系迁移到
新版 **maibot-plugin-sdk>=2.9.0**（MaiBot dev / 1.3.3）。

## 快速结论

| 项目 | 迁移前 | 迁移后 |
|---|---|---|
| 插件基类 | `BasePlugin` | `MaiBotPlugin` |
| 注册方式 | `@register_plugin` | `create_plugin()` 工厂函数 |
| Manifest | v1 | **v2**（`manifest_version: 2`） |
| 组件声明 | 独立类（`BaseAction`/`BaseCommand`/`BaseEventHandler`）| 装饰器方法（`@Action`/`@Command`/`@EventHandler`）|
| 配置读取 | `self.get_config()` | `self.get_config()`（内部改为 `ctx.config` 桥接）|
| 消息发送 | `self.send_text()` | `self.ctx.send.text(text, stream_id)` |
| 日志 | `src.common.logger.get_logger` | 标准库 `logging.getLogger` |
| src.* 依赖 | 35 处 | **0 处** |

## 一、Manifest（_manifest.json）

- 升级为 **v2**：`manifest_version: 2`，`id` 改为反向域名 `github.nguspring.selfie-painter`。
- 新增 `author` / `urls` / `host_application` / `sdk` / `capabilities` 等字段。
- v2 使用严格模型（`extra="forbid"`），多余字段会被拒绝。
- 旧 v1 备份保留为 `_manifest.v1.json.orig`。

### host / sdk 版本区间

```
host_application: 1.0.0 - 1.99.99
sdk:              2.0.0 - 2.99.99
```

## 二、插件主类（plugin.py）

### 2.1 类定义

```python
# 迁移前
@register_plugin
class SelfiePainterV2Plugin(PluginRuntimeMixin, BasePlugin):
    plugin_name = ...
    config_schema = ...
    def __init__(self, plugin_dir: str): ...
    def get_plugin_components(self): ...

# 迁移后
from maibot_sdk import MaiBotPlugin

class SelfiePainterV2Plugin(
    MaiBotPlugin,
    PluginRuntimeMixin,
    ScheduleInjectMixin,
    ScheduleCommandMixin,
    WardrobeCommandMixin,
    PicGenerationCommand,
    PicConfigCommand,
    PicStyleCommand,
    SelfiePainterActionMixin,
):
    def __init__(self) -> None:
        super().__init__()   # 必须：初始化 SDK 基类状态
        self._config_bridge = PluginConfigBridge()
        self._initialize_runtime_state()

    async def on_load(self) -> None: ...
    async def on_unload(self) -> None: ...
    async def on_config_update(self, new_config: dict, version: str) -> None: ...


def create_plugin() -> SelfiePainterV2Plugin:
    return SelfiePainterV2Plugin()
```

### 2.2 生命周期

- 旧：`ON_START` / `ON_STOP` 事件处理器（`core/lifecycle_handler.py`）→ **删除**。
- 新：直接在 `on_load()` / `on_unload()` 中实现（本插件分别调用
  `_bootstrap_runtime_tasks()` 与 `on_plugin_unload()`）。

### 2.3 配置读取桥

新增 `plugin_config_bridge.py`：

- 在 `on_load()` 中通过 `ctx.config.get_plugin()` 一次性拉取整份 `config.toml` 并缓存。
- 提供同步的 `get(key, default)` 点分键查找（保留 `self.get_config()` 兼容调用）。
- `ctx` 不可用或读取失败时**回退读取本地 config.toml**（保证独立测试/异常场景可用）。


## 三、组件迁移（共 8 个）

旧版每个组件是独立类，新版统一改为插件类上的**装饰器方法**。
为了减少改动，保留了原组件文件，但把类改造为 **mixin**，在主类中继承。

| 旧组件类 | 旧类型 | 新声明 | 新入口方法 |
|---|---|---|---|
| `SelfiePainterAction` | Action | `@Action("draw_picture", ...)` | `handle_draw_picture_action` |
| `PicGenerationCommand` | Command | `@Command("pic_generation_command", pattern=...)` | `handle_pic_generation_command` |
| `PicConfigCommand` | Command | `@Command("pic_config_command", pattern=...)` | `handle_pic_config_command` |
| `PicStyleCommand` | Command | `@Command("pic_style_command", pattern=...)` | `handle_pic_style_command` |
| `ScheduleCommand` | Command | `@Command("schedule_command", pattern=...)` | `handle_schedule_command` |
| `WardrobeCommand` | Command | `@Command("wardrobe_command", pattern=...)` | `handle_wardrobe_command` |
| `ScheduleContextHandler` | EventHandler | `@EventHandler(..., event_type=EventType.ON_MESSAGE)` | `handle_schedule_context_event` |
| `ScheduleInjectHandler` | EventHandler | `@EventHandler(..., event_type=EventType.POST_LLM)` | `handle_schedule_inject_event` |

> 注：`@Action` 在新 SDK 中会内部转换为 `Tool` 组件（会在日志中看到 `type: TOOL`）。

### 3.1 组件类 → mixin

以 `ScheduleCommand` 为例：

```python
# 迁移前
class ScheduleCommand(BaseCommand):
    command_name = "schedule_command"
    command_description = "查看和管理麦麦的日程"
    command_pattern = r"^/(schedule|日程)\s*(?P<sub>\S+)?\s*(?P<arg>\S+)?$"
    async def execute(self):
        sub = self.matched_groups.get("sub")
        await self.send_text("...", storage_message=False)

# 迁移后（core/schedule_command.py）
class ScheduleCommandMixin:
    async def handle_schedule(
        self, stream_id: str = "", user_id: str = "",
        matched_groups: dict | None = None, message: Any = None, **kwargs: Any,
    ) -> tuple[bool, str | None, bool]:
        matched_groups = matched_groups or {}
        self._current_stream_id = stream_id
        sub = (matched_groups.get("sub") or "").strip().lower()
        await self.ctx.send.text("...", self._current_stream_id)
```

然后主类里：

```python
@Command(
    "schedule_command",
    description="查看和管理麦麦的日程",
    pattern=r"^/(schedule|日程)\s*(?P<sub>\S+)?\s*(?P<arg>\S+)?$",
)
async def handle_schedule_command(self, stream_id="", user_id="", matched_groups=None, message=None, **kwargs):
    return await self.handle_schedule(stream_id=stream_id, user_id=user_id,
                                     matched_groups=matched_groups, message=message, **kwargs)
```

### 3.2 参数 / 上下文映射

| 旧用法 | 新用法 |
|---|---|
| `self.matched_groups.get("x")` | 方法参数 `matched_groups`（字典） |
| `self.action_data.get("x")` | 方法参数 `kwargs["action_data"]`（Action 已展平） |
| `self.action_message` | 方法参数 `message` / 上下文 `_current_message` |
| `self.chat_stream` | 从 `message.chat_stream` 解析（可能有缺） |
| `self.plugin_config` | `self._config_bridge.raw` |
| `self.plugin_name` | 已删除（不再需要） |
| `self.send_text(t, storage_message=False)` | `await self.ctx.send.text(t, stream_id)` |
| `self.send_image(b64)` | `await self.ctx.send.image(b64, stream_id)` |
| `self.send_command(...)` | `await self.ctx.send.command(cmd_str, stream_id)` |
| `plugin_manager.get_plugin_instance(...)` | 直接用 `self`（组件已是插件方法） |

### 3.3 Action 元数据提取

旧 `Action` 的关键词/参数/使用说明是**类属性**，装饰器需要它们作为**参数**，
故提取到独立模块 `core/_draw_action_meta.py`，主类装饰器引用：

```python
@Action(
    "draw_picture",
    description=DRAW_PICTURE_ACTION_DESCRIPTION,
    activation_type=ActivationType.ALWAYS,
    activation_keywords=DRAW_PICTURE_ACTIVATION_KEYWORDS,
    action_parameters=DRAW_PICTURE_ACTION_PARAMETERS,
    action_require=DRAW_PICTURE_ACTION_REQUIRE,
    associated_types=DRAW_PICTURE_ASSOCIATED_TYPES,
)
```

## 四、src.* 依赖清理（共 35 处）

新版插件运行在 IPC 隔离的子进程中，`sys.path` 被过滤，**禁止导入 `src.*`**。

| 旧导入 | 新写法 | 处数 |
|---|---|---|
| `from src.common.logger import get_logger` | `import logging` + `logging.getLogger(name)` | 20 |
| `from src.plugin_system.apis import llm_api/config_api/message_api` | `from maibot_sdk.compat.apis import ...` | 8 |
| `from src.plugin_system.core.plugin_manager import plugin_manager` | `from maibot_sdk.compat.core import ...` 或直接用 `self` | 3 |
| 动态 `import_module("src.plugin_system.apis")` | `import_module("maibot_sdk.compat.apis")` | 4 |
| `from src.config.config import global_config` | `config_api.get_global_config(key, default)` | 1 |
| `from src.common.database.database_model import Images` | `database_api.db_query("Images", filters=..., single_result=True)` | 1 |
| `from src.config.config import model_config` + `from src.llm_models.utils_model import LLMRequest` | `ctx.llm.generate(...)`（多模态） | 2 |
| `from src.plugin_system.base.component_types import PythonDependency` | `maibot_sdk.compat.base.component_types` | 1 |
| `from src.plugin_system.base.config_types import ConfigField...` | `maibot_sdk.compat.base.config_types` | 1 |

> 说明：`maibot_sdk.compat` 是官方兼容层，提供了旧 API 的同名实现，
> 底层会转发到新能力（`ctx.*`）。它依赖运行时的全局上下文注册，
> 但建议逐步将其替换为 `self.ctx.*`。

## 五、迁移中遇到的坑（重要）

### 坑 1：兼容层不会帮你兜底复杂插件

SDK 虽然提供 `maibot_sdk.compat`，但旧版 `BasePlugin` 在兼容层里是**简化空壳**（无 `__init__`、无 `get_config`）。
所以仅靠兼容层**无法**直接运行本插件，必须真正迁移主类。

### 坑 2：`__init__` 签名

- 必须**无参**，且**必须调用 `super().__init__()`**（否则 SDK 内部状态如
  `_dynamic_api_components` 缺失，`get_components()` 报错）。
- 旧代码里 `plugin_dir` 可通过 `os.path.dirname(os.path.abspath(__file__))` 自行推导，
  或使用 `self.ctx.paths`。

### 坑 3：组件类同名方法在 MRO 中互相覆盖

本插件多个 mixin 均有 `_check_permission`，但签名不同（有的带 `user_id`、有的不带），
继承到同一主类时发生**方法劫持**，运行时 `TypeError`。
解决办法：**重命名**（如 `_check_wardrobe_permission`）。

> 迁移时务必排查：所有 mixin 之间的**同名方法 / 同名属性**。

### 坑 4：`ctx.send.text()` 必须传 `stream_id`

旧版 `send_text` 只有一个必填参数，新版多了 `stream_id`。
本插件曾因部分分支漏传导致运行时 `TypeError`。建议用静态检查/冒烟测试排查。

### 坑 5：`@Action` 装饰器的参数必须是**定义时可得**的值

装饰器参数（如 `activation_keywords`）在**类定义时**求值，
无法引用类内部属性，因此旧类属性需**提升为模块级常量**（见 `core/_draw_action_meta.py`）。

### 坑 6：`ctx.config.get(key)` 读的是**宿主全局配置**

插件**自身**的 `config.toml` 需用 `ctx.config.get_plugin()`。
本插件用 `PluginConfigBridge` 在 `on_load` 一次性拉取并缓存。

### 坑 7：不是所有旧 API 都有对应新接口

例如 **VLM 图像理解**（旧 `LLMRequest.generate_response_for_image`）在新 SDK 无对应接口，
本插件改用 `ctx.llm.generate` 传多模态消息；若宿主不支持则**优雅降级**（返回空特征）。

## 六、验证方式

由于本地不一定有完整 QQ 环境，本仓库提供了**不依赖 QQ** 的验证脚本（见 `tests/sdk2/`）：

| 脚本 | 作用 |
|---|---|
| `gen_default_config.py` | 由 `CONFIG_SCHEMA` 生成默认 `config.toml` |
| `test_smoke_real_load.py` | 用真实 `PluginLoader` 加载，验证 manifest + 实例化 + 组件收集 |
| `test_smoke_mock_rpc.py` | 注入 mock `PluginContext`，触发 `on_load` 并调用 handler |

### 实测结果（本迁移）

- `PluginLoader.discover_and_load`：**成功**，`failed_plugins = {}`。
- `get_components()`：返回 **8 个组件**（1 TOOL + 5 COMMAND + 2 EVENT_HANDLER）。
- `on_load()`：成功，配置桥经 `ctx` 读到真实值，动态布局注入正常。
- 8 个 handler 逐一调用：**8/8 正常返回，零异常**。

## 七、遗留与注意事项

1. **配置 Schema 未迁到 `PluginConfigBase`**：仍用 `config_schema`（compat `ConfigField`）。
   功能上 `config.toml` 有效，但新版 WebUI 的配置页面渲染可能与旧版略有差异。
2. **VLM 特征提取降级**：若宿主不支持多模态，角色参考图特征提取会自动跳过。
3. **自动撤回（auto_recall）**：已将旧 `send_command(command_name=..., args=...)`
   改写为新 `ctx.send.command(cmd_str, stream_id)`；真机效果未验证。
4. **未做完整 QQ 端到端联调**：需真实 NapCat/协议端环境。
5. **兼容层是过渡**：`maibot_sdk.compat.*` 官方标注“未来版本可能移除”，
   建议后续逐步替换为 `self.ctx.*`。

## 八、文件变更总览

| 文件 | 变更 |
|---|---|
| `_manifest.json` | v1 → **v2** |
| `_manifest.v1.json.orig` | 新增（v1 备份） |
| `plugin.py` | 主类改写；生命周期/组件声明/装饰器注册 |
| `plugin_config_bridge.py` | **新增**（配置读取桥） |
| `core/_draw_action_meta.py` | **新增**（Action 元数据） |
| `core/lifecycle_handler.py` | **删除**（并入主类生命周期） |
| `plugin_components.py` | 降级为空占位（组件改装饰器） |
| `core/schedule_command.py` | `ScheduleCommand` → `ScheduleCommandMixin` |
| `core/wardrobe_command.py` | `WardrobeCommand` → `WardrobeCommandMixin` |
| `core/pic_command.py` | 3 个 Command 类 → mixin |
| `core/pic_action.py` | `SelfiePainterAction` → `SelfiePainterActionMixin` |
| `core/schedule_inject_handler.py` | 2 个 EventHandler → `ScheduleInjectMixin` |
| `core/utils/*.py` | 清除 `src.*`（logger/db/config 等） |
| `core/selfie/*.py` | 清除 `src.*`（llm_api/config_api 等） |
| `tests/sdk2/*` | **新增**（验证脚本） |

---

## 附：官方参考

- 迁移指南：`maibot-plugin-sdk/docs/migration-guide.md`
- API 参考：`maibot-plugin-sdk/docs/guide.md`
- 内置范例：`MaiBot/src/plugins/built_in/plugin_management/`
