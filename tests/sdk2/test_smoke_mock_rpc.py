# -*- coding: utf-8 -*-
import sys, asyncio, json, traceback
sys.path.insert(0, '/tmp/MaiBot')

import tomllib

CFG = tomllib.load(open('/tmp/test_plugins/selfie_painter/config.toml','rb'))
SENT = []

async def fake_rpc(method, plugin_id, payload):
    cap = str(method)
    data = payload if isinstance(payload, dict) else {}
    if cap.endswith('config.get_plugin') or cap == 'config.get_plugin':
        return {'success': True, 'value': CFG}
    if cap.endswith('config.get') or cap == 'config.get':
        return {'success': True, 'value': data.get('default')}
    if 'send.' in cap:
        SENT.append((cap, str(data)[:120]))
        return {'success': True}
    if cap.endswith('llm.generate') or cap == 'llm.generate':
        return {'success': True, 'response': 'MOCK_LLM', 'reasoning': '', 'model': 'mock'}
    return {'success': True, 'value': None}

from src.plugin_runtime.runner.plugin_loader import PluginLoader
from maibot_sdk.context import PluginContext

async def main():
    loader = PluginLoader(host_version='1.3.3', force_plugin_compatibility=True)
    metas = loader.discover_and_load(['/tmp/test_plugins'])
    inst = metas[0].instance

    # inject a mock ctx
    ctx = PluginContext('github.nguspring.selfie-painter', fake_rpc)
    inst._set_context(ctx)
    print('CTX INJECTED:', inst._ctx is not None)

    # on_load
    try:
        await inst.on_load()
        print('ON_LOAD: OK')
    except Exception as e:
        print('ON_LOAD FAIL:', type(e).__name__, e); traceback.print_exc()

    bridge = inst._config_bridge
    print('CONFIG from ctx:', bridge.loaded, '| plugin.enabled =', bridge.get('plugin.enabled'))

    # call a command handler
    print('\n=== CALL schedule_command handler ===')
    try:
        res = await inst.handle_schedule_command(stream_id='test_stream', matched_groups={'sub':'', 'arg':''})
        print('RESULT:', res)
    except Exception as e:
        print('HANDLER FAIL:', type(e).__name__, e); traceback.print_exc()

    print('\n=== SENT MESSAGES ===')
    for s in SENT[:5]:
        print(' ', s)

asyncio.run(main())
