#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""新規50用語のCSV行を品質改善版に差し替える。"""

from __future__ import annotations

import csv
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from tools.export_legacy_data_to_csv import GLOSSARY_HEADER  # noqa: E402
from tools.glossary_additions_batch50 import GLOSSARY_ADDITIONS  # noqa: E402
from tools.glossary_enrich import enrich_glossary_item, norm  # noqa: E402
from tools.append_glossary_batch50 import build_row  # noqa: E402

GLOSSARY_CSV = ROOT / "data" / "glossary_terms.csv"
BATCH_TERMS = {norm(x["term"]) for x in GLOSSARY_ADDITIONS}


def main() -> int:
    if len(GLOSSARY_ADDITIONS) != 50:
        print(f"Expected 50 additions, got {len(GLOSSARY_ADDITIONS)}", file=sys.stderr)
        return 1

    rows = list(csv.DictReader(GLOSSARY_CSV.read_text(encoding="utf-8-sig").splitlines()))
    by_term = {norm(r["term"]): i for i, r in enumerate(rows) if norm(r.get("term"))}

    missing = [t for t in BATCH_TERMS if t not in by_term]
    if missing:
        print("Not in CSV:", ", ".join(missing), file=sys.stderr)
        return 1

    for item in GLOSSARY_ADDITIONS:
        enriched = enrich_glossary_item(item)
        rows[by_term[norm(item["term"])]] = build_row(enriched)

    with GLOSSARY_CSV.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=GLOSSARY_HEADER, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)

    print(f"Refreshed {len(GLOSSARY_ADDITIONS)} terms in {GLOSSARY_CSV}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
