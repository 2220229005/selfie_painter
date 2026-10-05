# SDK2 迁移 - 运行时验证脚本

这些脚本用于在**没有完整 QQ 端到端环境**时，验证插件在真实 MaiBot 进程内的运行时行为。

## 前置

- 已克隆 MaiBot（dev 分支）到 `/tmp/MaiBot`
- 已创建 Python 3.12 venv 并安装 MaiBot 依赖（建议安装在 `/tmp/venv-validate`）
- 本插件已复制到某个 plugins 目录（如 `/tmp/test_plugins/selfie_painter`）

## 脚本

| 脚本 | 作用 |
|---|---|
| `gen_default_config.py` | 依据 `plugin_schema.CONFIG_SCHEMA` 生成一份默认 `config.toml` |
| `test_smoke_real_load.py` | 用真实 `PluginLoader` 加载插件，打印插件实例与组件列表 |
| `test_smoke_mock_rpc.py` | 注入 mock `PluginContext`（mock RPC），触发 `on_load` 并调用一个组件 handler |

## 运行示例

```bash
cd /tmp/MaiBot
/tmp/venv-validate/bin/python tests/sdk2/gen_default_config.py
/tmp/venv-validate/bin/python tests/sdk2/test_smoke_real_load.py
/tmp/venv-validate/bin/python tests/sdk2/test_smoke_mock_rpc.py
```

## 预期

- `real_load`：`FAILED: {}`，`COMPONENTS: 8`
- `mock_rpc`：`ON_LOAD: OK`，`CONFIG from ctx: True`，handler 返回合理的元组
