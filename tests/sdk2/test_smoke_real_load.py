# -*- coding: utf-8 -*-
import sys, traceback
sys.path.insert(0, '/tmp/MaiBot')

from src.plugin_runtime.runner.plugin_loader import PluginLoader

loader = PluginLoader(host_version='1.3.3', force_plugin_compatibility=True)
try:
    metas = loader.discover_and_load(['/tmp/test_plugins'])
    print('\n=== RESULT ===')
    print('METAS:', [m.plugin_id for m in metas])
    print('FAILED:', loader.failed_plugins)
    for m in metas:
        print('ID:', m.plugin_id, '| VER:', m.version)
        inst = getattr(m, 'instance', None)
        print('INSTANCE:', type(inst).__name__ if inst else None)
        if inst:
            try:
                comps = inst.get_components()
                print('COMPONENTS:', len(comps))
                for c in comps:
                    print('  -', c.get('type'), c.get('name'))
            except Exception as e:
                print('get_components ERR:', type(e).__name__, e)
except Exception:
    traceback.print_exc()
