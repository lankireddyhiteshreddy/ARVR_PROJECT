#!/usr/bin/env python3
"""
Copy all prefabs listed in reports/used_prefabs.txt into Assets/prefabs,
preserving their relative paths. Also copy associated .meta files.

Produces: reports/copy_to_prefabs_log.txt

Run from repository root (where Assets/ is located):
  python scripts/copy_used_to_prefabs.py
"""
from pathlib import Path
import shutil

repo_root = Path(__file__).resolve().parents[1]
assets_root = repo_root / 'Assets'
reports_dir = repo_root / 'reports'
used_list = reports_dir / 'used_prefabs.txt'

if not used_list.exists():
    print('Error: used_prefabs.txt not found in reports/. Run find_prefab_usage.py first.')
    raise SystemExit(1)

# target folder per your request
target_root = assets_root / 'prefabs'
# create the folder if it doesn't exist
target_root.mkdir(parents=True, exist_ok=True)

log_lines = []

with used_list.open('r', encoding='utf-8') as fh:
    prefabs = [line.strip() for line in fh if line.strip()]

for p in prefabs:
    src = repo_root / p
    if not src.exists():
        log_lines.append(f'MISSING: {p} (source not found)')
        continue
    # compute relative path under Assets and then replicate under Assets/prefabs
    try:
        rel_under_assets = src.relative_to(assets_root)
    except Exception:
        rel_under_assets = src.name
    dest = target_root / rel_under_assets
    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dest)
    # copy meta if exists (prefab.meta or name.prefab.meta)
    meta_candidates = [src.with_name(
        src.name + '.meta'), src.with_suffix(src.suffix + '.meta')]
    meta_copied = False
    for m in meta_candidates:
        if m.exists():
            shutil.copy2(m, dest.with_name(dest.name + '.meta'))
            meta_copied = True
            break
    log_lines.append(f'COPIED: {p} -> {dest} (meta_copied={meta_copied})')

# write log
log_file = reports_dir / 'copy_to_prefabs_log.txt'
log_file.write_text('\n'.join(log_lines), encoding='utf-8')
print('Done. Log written to', log_file)
