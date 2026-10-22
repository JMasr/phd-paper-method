"""Shared access to the released data: locate a stage folder, verify it, read its CSVs.

Every reader goes through `stage()`, which checks the SHA-256 of every file listed in the
folder's MANIFEST.json before anything is read, so a script cannot run on altered data.
"""
from __future__ import annotations

import csv
import hashlib
import io
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
STAGES = {1: "screening_stage", 2: "extension_stage"}


def die(msg: str):
    sys.stderr.write("ERROR: " + msg + "\n")
    sys.exit(1)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


_verified: set[Path] = set()


def stage(n: int) -> Path:
    """Folder of stage n (1 screening, 2 extension), after verifying every file's hash."""
    d = ROOT / STAGES[n]
    if d not in _verified:
        man = json.loads((d / "MANIFEST.json").read_text())
        for name, meta in man["files"].items():
            if sha256(d / name) != meta["sha256"]:
                die(f"{d.name}/{name} does not match its MANIFEST.json sha256")
        _verified.add(d)
    return d


def manifest(n: int) -> dict:
    return json.loads((stage(n) / "MANIFEST.json").read_text())


def rows(n: int, name: str) -> list[dict]:
    with (stage(n) / name).open(newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def both_stages(name: str) -> list[dict]:
    """Rows of a per-stage extract from both stages, screening first (the order of the original extract)."""
    return rows(1, name) + rows(2, name)
