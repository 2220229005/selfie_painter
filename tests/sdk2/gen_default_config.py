# -*- coding: utf-8 -*-
import sys, os
sys.path.insert(0, '/tmp/test_plugins/selfie_painter')
sys.path.insert(0, '/tmp/test_plugins')

# import the plugin_schema module via package path
import importlib.util
spec = importlib.util.spec_from_file_location(
    'xschema', '/tmp/test_plugins/selfie_painter/plugin_schema.py')
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

SCHEMA = mod.CONFIG_SCHEMA

# Flatten nested schema dict into a dict of section -> {key: value}
def build(schema):
    out = {}
    for section, fields in schema.items():
        if not isinstance(fields, dict):
            continue
        sec = out.setdefault(section, {})
        for k, f in fields.items():
            if hasattr(f, 'default'):
                d = f.default
            elif isinstance(f, dict):
                d = None
            else:
                d = None
            if d is not None:
                sec[k] = d
    return out

data = build(SCHEMA)

# Write as simple TOML manually
def toml_val(v):
    if isinstance(v, bool):
        return 'true' if v else 'false'
    if isinstance(v, (int, float)):
        return str(v)
    if isinstance(v, list):
        return '[' + ', '.join(toml_val(x) for x in v) + ']'
    s = str(v).replace('\\', '\\\\').replace('"', '\\"').replace('\n', '\\n')
    return '"' + s + '"'

lines = []
# top-level sections
flat_sections = {}
for section, fields in data.items():
    if '.' in section:
        continue
    flat_sections[section] = fields
for section, fields in flat_sections.items():
    lines.append('[%s]' % section)
    for k, v in fields.items():
        lines.append('%s = %s' % (k, toml_val(v)))
    lines.append('')

out_path = '/tmp/test_plugins/selfie_painter/config.toml'
open(out_path, 'w', encoding='utf-8').write('\n'.join(lines))
print('written', out_path, 'sections:', list(flat_sections.keys())[:10])
