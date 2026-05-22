#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""過去問マッチから example_question / example_answer を CSV に付与。"""

from __future__ import annotations

import csv
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from tools.export_legacy_data_to_csv import GLOSSARY_HEADER  # noqa: E402
from tools.glossary_enrich import split_points  # noqa: E402
from tools.glossary_past_questions import example_from_past_hit, find_past_questions_for_term  # noqa: E402

GLOSSARY_CSV = ROOT / "data" / "glossary_terms.csv"


def main() -> int:
    rows = list(csv.DictReader(GLOSSARY_CSV.read_text(encoding="utf-8-sig").splitlines()))
    attached = 0
    for row in rows:
        term = (row.get("term") or "").strip()
        if not term:
            continue
        hits = find_past_questions_for_term(
            term,
            limit=1,
            related_terms=row.get("related_terms") or "",
            legal_basis=row.get("legal_basis") or "",
        )
        if hits:
            q, a = example_from_past_hit(hits[0], term)
        else:
            points = split_points(row.get("exam_points") or "")
            if not points:
                continue
            cat = (row.get("category") or "").strip()
            q = f"【学習確認】{term}について、次のうち試験で押さえるべき説明として適切なものはどれか。"
            lead = points[0]
            a = (
                f"要点は「{lead}」です。"
                f"{cat}分野の関連用語・過去問演習ページで、条文番号と数値をセットで復習してください。"
            )
        if not (row.get("example_question") or "").strip():
            row["example_question"] = q
            attached += 1
        if not (row.get("example_answer") or "").strip():
            row["example_answer"] = a

    with GLOSSARY_CSV.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=GLOSSARY_HEADER, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)

    print(f"Attached examples to {attached} terms in {GLOSSARY_CSV}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
