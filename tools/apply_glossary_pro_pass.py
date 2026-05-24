#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""全用語にプロ品質パス（過去問知見・専門段落）を適用し、読みやすさ拡充まで実行。"""

from __future__ import annotations

import csv
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from tools.append_glossary_batch50 import build_row  # noqa: E402
from tools.export_legacy_data_to_csv import GLOSSARY_HEADER  # noqa: E402
from tools.glossary_enrich import enrich_glossary_item, norm  # noqa: E402
from tools.glossary_pro_pass import upgrade_glossary_pro  # noqa: E402
from tools.glossary_readable import apply_readable_fields  # noqa: E402

GLOSSARY_CSV = ROOT / "data" / "glossary_terms.csv"


def main() -> int:
    rows = list(csv.DictReader(GLOSSARY_CSV.read_text(encoding="utf-8-sig").splitlines()))
    updated = 0
    for i, row in enumerate(rows):
        term = norm(row.get("term"))
        if not term:
            continue
        pro = upgrade_glossary_pro(row)
        readable = apply_readable_fields(pro)
        built = build_row(readable)
        if len(norm(readable.get("term_detail_body"))) > len(norm(built.get("term_detail_body"))):
            built["term_detail_body"] = norm(readable["term_detail_body"])
        rows[i] = built
        updated += 1

    with GLOSSARY_CSV.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=GLOSSARY_HEADER, lineterminator="\n", extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)

    print(f"Applied glossary pro pass to {updated} terms")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
