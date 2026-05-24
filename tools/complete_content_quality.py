#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""用語詳細・試験ガイドのプロ品質パスと静的ページ再生成を一括実行。"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PY = sys.executable


def run(script: str) -> None:
    print(f"+ {script}")
    subprocess.run([PY, f"tools/{script}"], cwd=ROOT, check=True)


def main() -> int:
    run("apply_glossary_hand_rewrite.py")
    run("apply_glossary_readability_pass.py")
    run("apply_glossary_pro_pass.py")
    run("attach_glossary_examples.py")
    run("apply_guide_expert_writer.py")
    run("build_glossary_pages.py")
    run("build_article_pages.py")
    run("csv_to_takken_glossary_js.py")
    print("Content quality pass complete (glossary + guides).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
