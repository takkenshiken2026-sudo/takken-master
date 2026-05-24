#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""全用語に読みやすさ・要点具体例・覚え方詳細・FAQ4件を適用。"""

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
from tools.glossary_hand_rewrite import HAND_REWRITE  # noqa: E402
from tools.glossary_readable import apply_readable_fields  # noqa: E402

GLOSSARY_CSV = ROOT / "data" / "glossary_terms.csv"

READABILITY_COLUMNS = (
    "summary_points",
    "faq_3_question",
    "faq_3_answer",
    "faq_4_question",
    "faq_4_answer",
)


def ensure_header(fieldnames: list[str]) -> list[str]:
    out = list(fieldnames)
    for col in READABILITY_COLUMNS:
        if col not in out:
            out.append(col)
    return out


def main() -> int:
    text = GLOSSARY_CSV.read_text(encoding="utf-8-sig")
    rows = list(csv.DictReader(text.splitlines()))
    header = ensure_header(list(GLOSSARY_HEADER))

    updated = 0
    for i, row in enumerate(rows):
        if not norm(row.get("term")):
            continue
        term = norm(row.get("term"))
        base = dict(row)
        hand = HAND_REWRITE.get(term, {})
        if hand.get("memory_tip"):
            base["memory_tip"] = hand["memory_tip"]
        readable = apply_readable_fields(base)
        rows[i] = build_row(enrich_glossary_item(readable))
        updated += 1

    with GLOSSARY_CSV.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=header, lineterminator="\n", extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)

    print(f"Applied readability pass to {updated} terms")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
