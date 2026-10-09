from __future__ import annotations
import hashlib
from pathlib import Path

def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()

def scan(root: Path) -> dict[str, str]:
    root = root.resolve()
    return {
        str(p.relative_to(root)): sha256_file(p)
        for p in root.rglob("*")
        if p.is_file() and p.name != ".fim-baseline.json"
    }

def compare(old: dict[str, str], new: dict[str, str]) -> dict[str, list[str]]:
    old_keys, new_keys = set(old), set(new)
    return {
        "added": sorted(new_keys - old_keys),
        "removed": sorted(old_keys - new_keys),
        "changed": sorted(k for k in old_keys & new_keys if old[k] != new[k]),
    }
