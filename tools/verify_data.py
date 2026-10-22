#!/usr/bin/env python3
"""Verify every released data file against the SHA-256 recorded in its stage's MANIFEST.json.

    python3 tools/verify_data.py
"""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def main() -> int:
    bad = 0
    for stage in ("screening_stage", "extension_stage"):
        man = json.loads((ROOT / stage / "MANIFEST.json").read_text())
        for name, meta in man["files"].items():
            ok = hashlib.sha256((ROOT / stage / name).read_bytes()).hexdigest() == meta["sha256"]
            print(f"{'ok ' if ok else 'BAD'} {stage}/{name}")
            bad += not ok
    print("ALL DATA FILES MATCH THEIR MANIFESTS" if bad == 0 else f"{bad} FILE(S) DO NOT MATCH")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
