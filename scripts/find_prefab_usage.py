#!/usr/bin/env python3
"""
Scan Unity project Assets for .prefab files and determine whether each prefab's GUID
(from its .meta file) is referenced anywhere in the Assets folder.

Outputs:
  - reports/used_prefabs.txt
  - reports/unused_prefabs.txt
  - reports/summary.txt

Run from repository root (where Assets/ is located):
  python scripts/find_prefab_usage.py

This script ignores the Library/, Logs/, .git/ folders and only scans Assets/.
"""
import os
import sys
from pathlib import Path


def find_all_prefabs(assets_root: Path):
    for root, dirs, files in os.walk(assets_root):
        # skip Library folders inside Assets (shouldn't be there) but just in case
        if ".git" in root or "Library" in root or "Logs" in root:
            continue
        for f in files:
            if f.lower().endswith('.prefab'):
                yield Path(root) / f


def read_guid_from_meta(prefab_path: Path):
    meta_path = prefab_path.with_suffix(prefab_path.suffix + '.meta')
    if not meta_path.exists():
        # Unity sometimes stores meta with .prefab.meta; handle generic
        meta_path = prefab_path.with_name(prefab_path.name + '.meta')
        if not meta_path.exists():
            return None
    try:
        with meta_path.open('r', encoding='utf-8', errors='ignore') as fh:
            for line in fh:
                line = line.strip()
                if line.startswith('guid:'):
                    parts = line.split()
                    if len(parts) >= 2:
                        return parts[1].strip()
    except Exception as e:
        print(f"Warning: couldn't read meta for {prefab_path}: {e}")
    return None


def search_guid_in_assets(guid: str, assets_root: Path, exclude_paths=None):
    """
    Search for GUID string within all text files under assets_root. Exclude files in exclude_paths.
    Returns True if found (excluding the prefab's own meta), False otherwise.
    """
    if exclude_paths is None:
        exclude_paths = set()
    target = guid
    # We'll search for the guid string anywhere in files
    for root, dirs, files in os.walk(assets_root):
        # skip common large folders
        if any(x in root for x in ('.git', 'Library', 'Logs')):
            continue
        for fname in files:
            fpath = Path(root) / fname
            # skip the excluded paths
            if str(fpath) in exclude_paths:
                continue
            # limit to text-like asset files (scenes, prefabs, materials, assets, animator, controller, mat)
            if not fname.lower().endswith(('.prefab', '.unity', '.mat', '.asset', '.controller', '.anim', '.overridecontroller', '.playable', '.mask', '.meta', '.txt')):
                # still try some script/text files
                if not fname.lower().endswith(('.cs', '.js', '.shader', '.uxml', '.uss', '.asmdef', '.json', '.xml', '.yaml', '.yml')):
                    continue
            try:
                with fpath.open('r', encoding='utf-8', errors='ignore') as fh:
                    data = fh.read()
                    if target in data:
                        return True
            except Exception:
                # skip binary/unreadable files
                continue
    return False


def main():
    repo_root = Path(__file__).resolve().parents[1]
    assets_root = repo_root / 'Assets'
    if not assets_root.exists():
        print('Error: Assets/ folder not found in repository root:', repo_root)
        sys.exit(1)

    reports_dir = repo_root / 'reports'
    reports_dir.mkdir(exist_ok=True)

    used = []
    unused = []
    total = 0

    prefab_list = list(find_all_prefabs(assets_root))
    total = len(prefab_list)
    print(f'Found {total} prefab files under {assets_root}')

    for i, prefab in enumerate(prefab_list, 1):
        rel = prefab.relative_to(repo_root)
        print(f'[{i}/{total}] Checking {rel}')
        guid = read_guid_from_meta(prefab)
        if not guid:
            # if no guid found, treat as used to be safe
            print(
                f'  - No meta guid found for {rel}; marking as USED (no meta)')
            used.append(str(rel))
            continue
        # exclude own meta file path
        own_meta = str((prefab.parent / (prefab.name + '.meta')).resolve())
        found = search_guid_in_assets(
            guid, assets_root, exclude_paths={own_meta})
        if found:
            used.append(str(rel))
        else:
            unused.append(str(rel))

    # write reports
    (reports_dir / 'used_prefabs.txt').write_text('\n'.join(used), encoding='utf-8')
    (reports_dir / 'unused_prefabs.txt').write_text('\n'.join(unused), encoding='utf-8')
    summary = (
        f'Total prefabs scanned: {total}\n'
        f'Used prefabs: {len(used)}\n'
        f'Unused prefabs: {len(unused)}\n'
        f'Reports written to: {reports_dir}\n'
    )
    (reports_dir / 'summary.txt').write_text(summary, encoding='utf-8')
    print('\n' + summary)


if __name__ == '__main__':
    main()
