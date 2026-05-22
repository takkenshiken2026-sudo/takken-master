#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""手書き深掘り以外の全用語に一括深掘りを適用。"""

from __future__ import annotations

import csv
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from tools.append_glossary_batch50 import build_row  # noqa: E402
from tools.export_legacy_data_to_csv import GLOSSARY_HEADER  # noqa: E402
from tools.glossary_additions_batch50 import GLOSSARY_ADDITIONS  # noqa: E402
from tools.glossary_bulk_deep import build_bulk_overrides  # noqa: E402
from tools.glossary_enrich import enrich_glossary_item, norm  # noqa: E402
from tools.glossary_priority_deep import PRIORITY_DEEP  # noqa: E402

GLOSSARY_CSV = ROOT / "data" / "glossary_terms.csv"
SKIP = {norm(x["term"]) for x in GLOSSARY_ADDITIONS} | {norm(t) for t in PRIORITY_DEEP}


def main() -> int:
    rows = list(csv.DictReader(GLOSSARY_CSV.read_text(encoding="utf-8-sig").splitlines()))
    updated = 0
    for i, row in enumerate(rows):
        term = norm(row.get("term"))
        if not term or term in SKIP:
            continue
        overrides = build_bulk_overrides(row)
        base = {**row, **overrides}
        if "explanation" not in overrides:
            base["explanation"] = norm(overrides.get("detail_body"))
        if "definition" not in overrides:
            sd = norm(base.get("short_def"))
            base["definition"] = sd if sd.endswith("。") else f"{sd}。" if sd else norm(base.get("definition"))
        rows[i] = build_row(enrich_glossary_item(base))
        updated += 1

    with GLOSSARY_CSV.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=GLOSSARY_HEADER, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)

    print(f"Applied bulk deep enrich to {updated} terms")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
