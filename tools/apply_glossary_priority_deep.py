#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""glossary_priority_deep.py の個別深掘りを CSV に反映。"""

from __future__ import annotations

import csv
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from tools.export_legacy_data_to_csv import GLOSSARY_HEADER  # noqa: E402
from tools.glossary_enrich import enrich_glossary_item, norm  # noqa: E402
from tools.glossary_priority_deep import PRIORITY_DEEP  # noqa: E402
from tools.append_glossary_batch50 import build_row  # noqa: E402

GLOSSARY_CSV = ROOT / "data" / "glossary_terms.csv"


def main() -> int:
    rows = list(csv.DictReader(GLOSSARY_CSV.read_text(encoding="utf-8-sig").splitlines()))
    by_term = {norm(r["term"]): i for i, r in enumerate(rows) if norm(r.get("term"))}
    updated = 0
    for term, overrides in PRIORITY_DEEP.items():
        idx = by_term.get(norm(term))
        if idx is None:
            print(f"skip (not found): {term}", file=sys.stderr)
            continue
        base = {**rows[idx], **overrides}
        if "explanation" not in overrides:
            base["explanation"] = norm(overrides.get("detail_body"))
        if "definition" not in overrides and norm(overrides.get("detail_body")):
            sd = norm(base.get("short_def"))
            base["definition"] = sd if sd.endswith("。") else f"{sd}。" if sd else norm(base.get("definition"))
        if "common_mistakes" not in overrides:
            base["common_mistakes"] = ""
        rows[idx] = build_row(enrich_glossary_item(base))
        updated += 1

    with GLOSSARY_CSV.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=GLOSSARY_HEADER, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)

    print(f"Applied priority deep enrich to {updated} terms")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
