#!/usr/bin/env python3
"""Regenerate every data-derived table, macro and figure of the article and compare it with the article.

    python3 tools/reproduce.py

Runs the four generators into outputs/, then checks each output against the copy the article
compiles, kept in paper/:
  * tables (.tex without macro definitions): every non-comment line identical;
  * macro files: every definition the article uses present with the same value (a generator may
    define a few more, which the article does not use);
  * figures: the values each figure draws (fig_*_data.csv) identical to those of the article's figure;
    the rendered pages are also compared at 100 dpi when pdftoppm and Pillow are available, for
    information only, because text and line rendering change between matplotlib versions (with
    matplotlib 3.3 the pages are identical to the article's).
Files in paper/generated/ that no generator writes are recorded outputs and are listed as such; the
speaker columns of the partition table among them are checked against the protocol logs (check_splits.py).
Exit status 0 only when every regenerated output matches.
"""
from __future__ import annotations

import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TOOLS = ROOT / "tools"
OUT = ROOT / "outputs"
PAPER = ROOT / "paper"
GENERATORS = ["build_paper_sota.py", "build_cost_macros.py", "build_protocol_macros.py", "build_sensitivity_macros.py"]
FIGURES = ["fig_blocks.pdf", "fig_rank_curve.pdf"]


def body(path: Path) -> list[str]:
    return [l for l in path.read_text(encoding="utf-8").splitlines() if not l.startswith("%")]


def compare_tex(new: Path, ref: Path) -> str | None:
    a, b = body(new), body(ref)
    if any(l.startswith("\\newcommand") for l in b):
        missing = sorted(set(b) - set(a))
        return None if not missing else f"{len(missing)} definition(s) differ, e.g. {missing[0]}"
    return None if a == b else "content differs"


def render(pdf: Path, stem: Path):
    subprocess.run(["pdftoppm", "-r", "100", "-png", "-singlefile", str(pdf), str(stem)], check=True)
    from PIL import Image
    return Image.open(str(stem) + ".png").convert("L")


def compare_fig(new: Path, ref: Path) -> str | None:
    if shutil.which("pdftoppm") is None:
        return "skipped (pdftoppm not found)"
    try:
        from PIL import ImageChops
    except ImportError:
        return "skipped (Pillow not installed)"
    with tempfile.TemporaryDirectory() as tmp:
        a, b = render(new, Path(tmp) / "a"), render(ref, Path(tmp) / "b")
    if a.size != b.size:
        return f"size differs {a.size} vs {b.size}"
    hist = ImageChops.difference(a, b).histogram()
    bad = sum(hist[16:])
    return None if bad == 0 else f"{bad} pixels differ"


def main() -> int:
    for g in GENERATORS:
        print(f"--- {g}")
        r = subprocess.run([sys.executable, str(TOOLS / g)], cwd=ROOT, capture_output=True, text=True)
        if r.returncode != 0:
            sys.stderr.write(r.stdout + r.stderr)
            print(f"FAILED: {g}")
            return 1
        last = [l for l in r.stdout.splitlines() if l.strip()]
        print(last[-1][:160] if last else "ok")
    print("\n--- comparison with the article")
    failures, recorded = 0, []
    for ref in sorted((PAPER / "generated").glob("*.tex")):
        new = OUT / "generated" / ref.name
        if not new.exists():
            recorded.append(ref.name)
            continue
        msg = compare_tex(new, ref)
        print(f"{'ok  ' if msg is None else 'FAIL'} {ref.name}{'' if msg is None else ': ' + msg}")
        failures += msg is not None
    for name in FIGURES:
        data = name.replace(".pdf", "_data.csv")
        same = (OUT / "figs" / data).read_bytes() == (PAPER / "figs" / data).read_bytes()
        print(f"{'ok  ' if same else 'FAIL'} {data}{'' if same else ': plotted values differ'}")
        failures += not same
        msg = compare_fig(OUT / "figs" / name, PAPER / "figs" / name)
        note = "identical rendering" if msg is None else msg + " (rendering only; informational)"
        print(f"info {name}: {note}")
    print("\nrecorded, not regenerated from the released data (see paper/README.md): " + ", ".join(recorded))
    print("\n--- speaker columns of the partition table against the protocol logs")
    r = subprocess.run([sys.executable, str(TOOLS / "check_splits.py")], cwd=ROOT, capture_output=True, text=True)
    print(r.stdout.rstrip())
    failures += r.returncode != 0
    print("\nALL REGENERATED OUTPUTS MATCH THE ARTICLE" if failures == 0 else f"\n{failures} MISMATCH(ES)")
    return 0 if failures == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
