#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""既存 mistakes.csv に追加分3件をマージ（同一 slug は置換）."""

from __future__ import annotations

import csv
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from tools.write_takken_hub_s30 import DATA, HEADER_MISTAKES  # noqa: E402
from tools.write_takken_hub_s30_mistakes_add3 import MISTAKES_ADD3  # noqa: E402


def main() -> None:
    path = DATA / "mistakes.csv"
    with path.open(encoding="utf-8", newline="") as f:
        rows = list(csv.DictReader(f))
    by_slug = {r["slug"]: i for i, r in enumerate(rows)}
    for row in MISTAKES_ADD3:
        if row["slug"] in by_slug:
            rows[by_slug[row["slug"]]] = row
        else:
            by_slug[row["slug"]] = len(rows)
            rows.append(row)
    with path.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=HEADER_MISTAKES, lineterminator="\n")
        w.writeheader()
        w.writerows(rows)
    print(f"mistakes.csv: {len(rows)} rows (+{len(MISTAKES_ADD3)} new/updated)")


if __name__ == "__main__":
    main()
