#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""guide_articles.csv の example.com プレースホルダを site-config の公式リンクに置換。"""

from __future__ import annotations

import csv
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from tools.scaffold_guide_article import default_primary_sources  # noqa: E402

CSV_PATH = ROOT / "data" / "guide_articles.csv"


def main() -> int:
    if not CSV_PATH.is_file():
        print(f"Missing {CSV_PATH}", file=sys.stderr)
        return 1
    replacement = default_primary_sources()
    text = CSV_PATH.read_text(encoding="utf-8-sig")
    rows = list(csv.DictReader(text.splitlines()))
    fieldnames = rows[0].keys() if rows else []
    updated = 0
    for row in rows:
        src = (row.get("primary_sources") or "").strip()
        if "example.com" in src or src == "試験実施団体（公式）|https://example.com/":
            row["primary_sources"] = replacement
            updated += 1
    with CSV_PATH.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames, lineterminator="\n")
        w.writeheader()
        w.writerows(rows)
    print(f"Updated primary_sources on {updated} row(s) in {CSV_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
