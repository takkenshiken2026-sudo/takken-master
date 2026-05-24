#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""全用語の記事品質フィールドを一括更新（CSV正本）。"""

from __future__ import annotations

import csv
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from tools.append_glossary_batch50 import build_row  # noqa: E402
from tools.export_legacy_data_to_csv import GLOSSARY_HEADER  # noqa: E402
from tools.glossary_article_quality import upgrade_glossary_fields  # noqa: E402
from tools.glossary_enrich import enrich_glossary_item, norm  # noqa: E402
from tools.glossary_priority_deep import PRIORITY_DEEP  # noqa: E402

GLOSSARY_CSV = ROOT / "data" / "glossary_terms.csv"
DEEP_TERMS = {norm(t) for t in PRIORITY_DEEP}


def main() -> int:
    rows = list(csv.DictReader(GLOSSARY_CSV.read_text(encoding="utf-8-sig").splitlines()))
    updated = 0
    for i, row in enumerate(rows):
        term = norm(row.get("term"))
        if not term:
            continue
        preserve = term in DEEP_TERMS
        base = upgrade_glossary_fields(row, preserve_deep=preserve)
        rows[i] = build_row(enrich_glossary_item(base))
        updated += 1

    with GLOSSARY_CSV.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=GLOSSARY_HEADER, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)

    print(f"Upgraded article fields for {updated}/{len(rows)} terms")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
