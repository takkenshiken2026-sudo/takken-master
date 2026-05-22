#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""tools/glossary_additions_batch50.py の50用語を data/glossary_terms.csv に追記する。"""

from __future__ import annotations

import csv
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from tools.export_legacy_data_to_csv import GLOSSARY_HEADER  # noqa: E402
from tools.glossary_additions_batch50 import GLOSSARY_ADDITIONS  # noqa: E402
from tools.glossary_enrich import enrich_glossary_item  # noqa: E402

GLOSSARY_CSV = ROOT / "data" / "glossary_terms.csv"


def norm(s: str | None) -> str:
    return (s or "").strip()


def build_row(item: dict[str, str]) -> dict[str, str]:
    term = norm(item["term"])
    reading = norm(item["reading"])
    category = norm(item["category"])
    short_def = norm(item["short_def"])
    definition = norm(item["definition"])
    explanation = norm(item.get("explanation") or "")
    term_detail_body = norm(item.get("term_detail_body") or definition)
    exam_points = norm(item.get("exam_points") or "")
    common_mistakes = norm(item.get("common_mistakes") or "")
    memory_tip = norm(item.get("memory_tip") or "")

    row = {k: "" for k in GLOSSARY_HEADER}
    row.update(
        {
            "term": term,
            "reading": reading,
            "category": category,
            "tags": category,
            "short_def": short_def,
            "definition": definition,
            "related_terms": norm(item.get("related_terms") or ""),
            "legal_basis": norm(item.get("legal_basis") or ""),
            "importance": "A",
            "explanation": explanation,
            "article_title": f"{term}とは",
            "article_lead": short_def,
            "term_detail_body": term_detail_body,
            "exam_points": exam_points,
            "common_mistakes": common_mistakes,
            "memory_tip": memory_tip,
            "example_question": norm(item.get("example_question") or ""),
            "example_answer": norm(item.get("example_answer") or ""),
            "faq_1_question": norm(item.get("faq_1_question") or ""),
            "faq_1_answer": norm(item.get("faq_1_answer") or ""),
            "faq_2_question": norm(item.get("faq_2_question") or ""),
            "faq_2_answer": norm(item.get("faq_2_answer") or ""),
        }
    )
    return row


def main() -> int:
    if len(GLOSSARY_ADDITIONS) != 50:
        print(f"Expected 50 additions, got {len(GLOSSARY_ADDITIONS)}", file=sys.stderr)
        return 1

    text = GLOSSARY_CSV.read_text(encoding="utf-8-sig")
    rows = list(csv.DictReader(text.splitlines()))
    existing = {norm(r.get("term")) for r in rows if norm(r.get("term"))}

    dupes = [item["term"] for item in GLOSSARY_ADDITIONS if item["term"] in existing]
    if dupes:
        print("Already in CSV:", ", ".join(dupes), file=sys.stderr)
        return 1

    new_rows = [build_row(enrich_glossary_item(item)) for item in GLOSSARY_ADDITIONS]
    rows.extend(new_rows)

    with GLOSSARY_CSV.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=GLOSSARY_HEADER, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)

    print(f"Appended {len(new_rows)} terms → {GLOSSARY_CSV} (total {len(rows)})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
