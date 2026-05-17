#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""One-command build for takken-master."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def run(cmd: list[str]) -> None:
    print("+", " ".join(cmd))
    subprocess.run(cmd, cwd=ROOT, check=True)


def main() -> int:
    py = sys.executable
    run([py, "tools/apply_site_config.py"])
    run([py, "tools/build_additional_takken_articles.py"])
    run([py, "tools/build_past_question_pages.py"])
    run([py, "tools/build_glossary_pages.py"])
    run([py, "tools/build_sitemap.py"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
