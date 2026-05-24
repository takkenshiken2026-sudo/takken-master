#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""全試験ガイド記事に専門家・プロライター品質パスを適用。"""

from __future__ import annotations

import csv
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from tools.guide_expert_writer import upgrade_guide_expert  # noqa: E402
from tools.guide_pro_pass import norm  # noqa: E402

GUIDE_CSV = ROOT / "data" / "guide_articles.csv"


def main() -> int:
    text = GUIDE_CSV.read_text(encoding="utf-8-sig")
    rows = list(csv.DictReader(text.splitlines()))
    if not rows:
        print("No guide rows", file=sys.stderr)
        return 1
    fieldnames = list(rows[0].keys())

    updated = 0
    for i, row in enumerate(rows):
        slug = norm(row.get("slug"))
        if not slug:
            continue
        rows[i] = upgrade_guide_expert(row)
        updated += 1

    with GUIDE_CSV.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, lineterminator="\n", extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)

    print(f"Applied guide expert writer to {updated} articles")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
