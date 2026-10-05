# -*- coding: utf-8 -*-
import sys, asyncio, traceback, tomllib
sys.path.insert(0, '/tmp/MaiBot')

CFG = tomllib.load(open('/tmp/test_plugins/selfie_painter/config.toml','rb'))
SENT = []

async def fake_rpc(method, plugin_id, payload):
    cap = str(method)
    data = payload if isinstance(payload, dict) else {}
    if cap.endswith('config.get_plugin'):
        return {'success': True, 'value': CFG}
    if cap.endswith('config.get'):
        return {'success': True, 'value': data.get('default')}
    if 'send.' in cap:
        SENT.append((cap, str(data)[:100]))
        return {'success': True}
    if cap.endswith('llm.generate'):
        return {'success': True, 'response': 'MOCK_LLM', 'reasoning': '', 'model': 'mock'}
    if 'db.' in cap or 'database.' in cap:
        return {'success': True, 'value': None}
    return {'success': True, 'value': None}

from src.plugin_runtime.runner.plugin_loader import PluginLoader
from maibot_sdk.context import PluginContext

class FakeMsg:
    stream_id = 'stream_test'
    plain_text = 'hello'
    processed_plain_text = 'hello'
    llm_prompt = ''
    chat_stream = None
    message_info = None
    message_segment = None
    def modify_llm_prompt(self, v): pass

async def call(name, fn, **kw):
    try:
        r = await fn(**kw)
        print('  [OK]  %-32s -> %r' % (name, r if not isinstance(r, tuple) else r[:3]))
        return True
    except Exception as e:
        print('  [ERR] %-32s -> %s: %s' % (name, type(e).__name__, str(e)[:90]))
        return False

async def main():
    loader = PluginLoader(host_version='1.3.3', force_plugin_compatibility=True)
    metas = loader.discover_and_load(['/tmp/test_plugins'])
    inst = metas[0].instance
    ctx = PluginContext('github.nguspring.selfie-painter', fake_rpc)
    inst._set_context(ctx)
    await inst.on_load()
    print('ON_LOAD OK\n')

    msg = FakeMsg()
    print('=== COMMAND handlers ===')
    await call('schedule_command', inst.handle_schedule_command, stream_id='s1', matched_groups={'sub':'','arg':''}, message=msg)
    await call('wardrobe_command(list)', inst.handle_wardrobe_command, stream_id='s1', user_id='u1', matched_groups={'sub':'list','arg':''}, message=msg)
    await call('pic_config_command(list)', inst.handle_pic_config_command, stream_id='s1', user_id='u1', matched_groups={'action':'list','params':''}, message=msg)
    await call('pic_style_command(styles)', inst.handle_pic_style_command, stream_id='s1', matched_groups={'action':'styles','params':''}, message=msg)
    await call('pic_generation_command', inst.handle_pic_generation_command, stream_id='s1', user_id='u1', matched_groups={'content':'画一只猫'}, message=msg)

    print('\n=== EVENT handlers ===')
    await call('schedule_context_handler', inst.handle_schedule_context_event, message=msg)
    await call('schedule_inject_handler', inst.handle_schedule_inject_event, message=msg)

    print('\n=== ACTION handler ===')
    await call('draw_picture', inst.handle_draw_picture_action, stream_id='s1', platform='qq', group_id='1919810', user_id='114514', action_data={'description':'画一只猫'}, message=msg)

    print('\n=== SENT (%d) ===' % len(SENT))
    for s in SENT[:8]:
        print('  ', s)

asyncio.run(main())
