#!/usr/bin/env python3
"""
Map used prefabs to their top-level asset folders to help identify where they came from
(eg. 'Brick Project Studio', 'POLYGON city pack', 'Fire_Extinguisher', etc.).

Reads: reports/used_prefabs.txt
Writes: reports/prefab_sources.csv and reports/prefab_sources.md
"""
from collections import defaultdict
from pathlib import Path
import csv

repo_root = Path(__file__).resolve().parents[1]
assets_root = repo_root / 'Assets'
reports_dir = repo_root / 'reports'
reports_dir.mkdir(exist_ok=True)
used_file = reports_dir / 'used_prefabs.txt'
if not used_file.exists():
    print('Error: reports/used_prefabs.txt not found. Run find_prefab_usage.py first.')
    raise SystemExit(1)

prefabs = [line.strip() for line in used_file.read_text(
    encoding='utf-8').splitlines() if line.strip()]

# Group by top-level folder under Assets (the first path segment after Assets/)
groups = defaultdict(list)
for p in prefabs:
    try:
        rel = Path(p)
        parts = rel.parts
        # parts like ('Assets', 'Brick Project Studio', '...') or ('Assets','Fire_Extinguisher','Prefab','...')
        if len(parts) >= 2 and parts[0] == 'Assets':
            top = parts[1]
        else:
            top = parts[0] if parts else 'Unknown'
    except Exception:
        top = 'Unknown'
    groups[top].append(p)

# For each top-level group, attempt to find README/LICENSE or package indicators


def find_evidence(folder_name):
    folder = assets_root / folder_name
    evidence = []
    if not folder.exists():
        return evidence
    for fname in ('README.md', 'readme.md', 'LICENSE', 'license.txt', 'package.json'):
        f = folder / fname
        if f.exists():
            evidence.append(str(f.relative_to(repo_root)))
    # also search for meta files with same folder name
    meta_files = list(folder.rglob('*.meta'))[:10]
    if meta_files:
        evidence.append('found .meta files')
    return evidence


csv_file = reports_dir / 'prefab_sources.csv'
md_file = reports_dir / 'prefab_sources.md'

with csv_file.open('w', newline='', encoding='utf-8') as cf:
    writer = csv.writer(cf)
    writer.writerow(['top_folder', 'evidence',
                    'prefab_count', 'sample_prefab'])
    for top, items in sorted(groups.items()):
        evidence = '; '.join(find_evidence(top)) or ''
        sample = items[0] if items else ''
        writer.writerow([top, evidence, len(items), sample])

with md_file.open('w', encoding='utf-8') as mf:
    mf.write('# Prefab sources summary\n\n')
    mf.write('This report groups used prefabs by the top-level folder under `Assets/` where they live.\n\n')
    for top, items in sorted(groups.items()):
        mf.write(f'## {top} — {len(items)} prefabs\n\n')
        evidence = find_evidence(top)
        if evidence:
            mf.write('Evidence files found:\n')
            for e in evidence:
                mf.write(f'- {e}\n')
            mf.write('\n')
        mf.write('Sample prefabs:\n')
        for s in items[:10]:
            mf.write(f'- {s}\n')
        mf.write('\n')

print('Wrote', csv_file, 'and', md_file)
