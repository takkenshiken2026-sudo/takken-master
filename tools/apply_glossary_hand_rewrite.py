#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""全354用語に手作りリライトを適用（CSV正本）。"""

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

GLOSSARY_CSV = ROOT / "data" / "glossary_terms.csv"


def apply_hand(row: dict[str, str], overrides: dict[str, str]) -> dict[str, str]:
    from tools.glossary_article_quality import _first_sentence

    base = {**row, **overrides}
    if norm(overrides.get("definition")):
        base["short_def"] = _first_sentence(overrides["definition"])
    if norm(overrides.get("detail_body")) and "explanation" not in overrides:
        base["explanation"] = norm(overrides["detail_body"])
    # 手書き適用後は FAQ を手書き内容から再生成
    for key in (
        "faq_1_question",
        "faq_1_answer",
        "faq_2_question",
        "faq_2_answer",
        "faq_3_question",
        "faq_3_answer",
        "faq_4_question",
        "faq_4_answer",
        "summary_points",
    ):
        base[key] = ""
    enriched = enrich_glossary_item(base)
    return build_row(enriched)


def main() -> int:
    rows = list(csv.DictReader(GLOSSARY_CSV.read_text(encoding="utf-8-sig").splitlines()))
    by_term = {norm(r["term"]): i for i, r in enumerate(rows) if norm(r.get("term"))}

    applied = 0
    missing_hand: list[str] = []
    for term, overrides in HAND_REWRITE.items():
        idx = by_term.get(norm(term))
        if idx is None:
            print(f"skip (not in CSV): {term}", file=sys.stderr)
            continue
        rows[idx] = apply_hand(rows[idx], overrides)
        applied += 1

    for r in rows:
        if norm(r.get("term")) and norm(r["term"]) not in {norm(k) for k in HAND_REWRITE}:
            missing_hand.append(norm(r["term"]))

    with GLOSSARY_CSV.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=GLOSSARY_HEADER, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)

    print(f"Applied hand rewrite to {applied} terms")
    if missing_hand:
        print(f"WARNING: {len(missing_hand)} terms lack hand rewrite:", file=sys.stderr)
        for t in missing_hand[:20]:
            print(f"  - {t}", file=sys.stderr)
        if len(missing_hand) > 20:
            print(f"  ... and {len(missing_hand) - 20} more", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
