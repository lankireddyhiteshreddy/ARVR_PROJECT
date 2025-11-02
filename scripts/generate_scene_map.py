#!/usr/bin/env python3
"""
Generate a per-scene map: for each .unity scene (text YAML), list GameObjects and the scripts (MonoBehaviours)
attached to them. Output is written to reports/scene_map.md.

Algorithm (best-effort):
- Read all .cs.meta files under Assets/ to build guid -> script .cs path map.
- For each scene (.unity) file under Assets/, parse Unity YAML by splitting on "\n--- " and collecting
  blocks. GameObjects are type 1 (`!u!1`), MonoBehaviours are type 114 (`!u!114`).
- For each GameObject block extract m_Name and m_Component references (component fileIDs).
- For each component reference (fileID) find the component block and if it's a MonoBehaviour, extract
  m_Script guid and map to script path; otherwise ignore.

This is a best-effort parser that works for text-based Unity scenes (YAML). Binary scenes or unusual
formats won't be parsed.
"""
from pathlib import Path
import re

repo_root = Path(__file__).resolve().parents[1]
assets_root = repo_root / 'Assets'
reports_dir = repo_root / 'reports'
reports_dir.mkdir(exist_ok=True)

# Build guid -> script path map from .cs.meta files
guid_to_script = {}
for meta in assets_root.rglob('*.cs.meta'):
    try:
        text = meta.read_text(encoding='utf-8', errors='ignore')
    except Exception:
        continue
    m = re.search(r'^guid:\s*([0-9a-fA-F]+)$', text, flags=re.MULTILINE)
    if m:
        guid = m.group(1)
        # corresponding script path
        script_path = meta.with_suffix('')  # removes .meta
        # script_path is like Assets/.../name.cs
        guid_to_script[guid] = str(
            script_path.relative_to(repo_root)).replace('\\', '/')

# Find scene files (.unity) under Assets
scene_files = list(assets_root.rglob('*.unity'))
scene_files.sort()

scene_maps = {}

for scene in scene_files:
    try:
        content = scene.read_text(encoding='utf-8', errors='ignore')
    except Exception:
        continue
    # split blocks; ensure blocks start with '--- '
    parts = re.split(r'(?m)^---\s', content)
    # map header id to block text
    id_to_block = {}
    for part in parts:
        if not part.strip():
            continue
        header_line = part.splitlines()[0]
        # header_line like '!u!1 &123456'
        m = re.match(r'!u!([0-9]+)\s*&([0-9]+)', header_line)
        if not m:
            continue
        utype = m.group(1)
        fid = m.group(2)
        id_to_block[fid] = {'type': utype, 'text': part}

    # collect gameobjects
    gameobjects = []
    for fid, blk in id_to_block.items():
        if blk['type'] == '1':  # GameObject
            text = blk['text']
            # find m_Name:
            name_match = re.search(r'm_Name:\s*(.+)', text)
            name = name_match.group(1).strip(
            ) if name_match else f'GameObject_{fid}'
            # find component entries
            comps = re.findall(r'component:\s*\{fileID:\s*([0-9]+)\}', text)
            gameobjects.append({'fid': fid, 'name': name, 'components': comps})

    # for each gameobject, map components
    scene_map = {}
    for go in gameobjects:
        scripts = []
        for compid in go['components']:
            comp_blk = id_to_block.get(compid)
            if not comp_blk:
                continue
            if comp_blk['type'] == '114':  # MonoBehaviour
                comp_text = comp_blk['text']
                # find m_Script guid
                m = re.search(
                    r'm_Script:\s*\{\s*fileID:\s*[0-9]+,\s*guid:\s*([0-9a-fA-F]+),', comp_text)
                if not m:
                    # try alternative pattern
                    m = re.search(r'guid:\s*([0-9a-fA-F]+)', comp_text)
                if m:
                    guid = m.group(1)
                    script = guid_to_script.get(
                        guid, f'<unknown script guid={guid}>')
                else:
                    script = '<unknown mono behaviour>'
                # attempt to extract the component's 'm_Name' or className
                name_match = re.search(r'm_Name:\s*(.+)', comp_text)
                comp_name = name_match.group(1).strip() if name_match else None
                if comp_name and comp_name != '':
                    scripts.append(
                        {'script': script, 'component_name': comp_name})
                else:
                    scripts.append({'script': script, 'component_name': None})
        if scripts:
            scene_map[go['name']] = scripts
    scene_maps[str(scene.relative_to(repo_root))] = scene_map

# Write markdown report
out = []
out.append('# Scene → GameObject → MonoBehaviour map')
out.append('')
for scene_path, smap in scene_maps.items():
    out.append(f'## {scene_path}')
    if not smap:
        out.append(
            '_No GameObjects with MonoBehaviour scripts detected or scene uses only prefabs._')
        out.append('')
        continue
    for go_name, scripts in sorted(smap.items()):
        out.append(f'- **{go_name}**')
        for s in scripts:
            comp_label = f" ({s['component_name']})" if s['component_name'] else ''
            out.append(f"  - {s['script']}{comp_label}")
    out.append('')

(report_file := reports_dir / 'scene_map.md').write_text('\n'.join(out), encoding='utf-8')
print('Wrote', report_file)
