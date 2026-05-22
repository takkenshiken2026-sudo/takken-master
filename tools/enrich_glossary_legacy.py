#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""既存用語（batch50以外）の記事品質を一括改善。"""

from __future__ import annotations

import csv
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from tools.export_legacy_data_to_csv import GLOSSARY_HEADER  # noqa: E402
from tools.glossary_additions_batch50 import GLOSSARY_ADDITIONS  # noqa: E402
from tools.glossary_enrich import enrich_csv_row, norm, split_points  # noqa: E402
from tools.glossary_priority_deep import PRIORITY_DEEP  # noqa: E402

GLOSSARY_CSV = ROOT / "data" / "glossary_terms.csv"
SKIP_TERMS = {norm(x["term"]) for x in GLOSSARY_ADDITIONS} | {norm(t) for t in PRIORITY_DEEP}

MISTAKE_TEMPLATES = {
    "権利関係": "類似制度（期間・要件・効力）の取り違え。数字と条文番号をセットで暗記する。",
    "宅建業法": "書面の交付時期・記載事項・監督処分の段階の混同。35条・37条・8条・14条の表で整理する。",
    "法令上の制限": "区域・用途・数値（面積・率・幅員）の組み合わせ誤り。例外規定との区別が問われる。",
    "税・その他": "課税主体・申告期限・税率・控除の要件の混同。計算問題では算式の順序を誤りやすい。",
    "試験対策": "出題比率や学習時間の目安を暗記数字と混同する。最新の試験要綱・公式情報で確認する。",
}


def default_memory_tip(term: str, exam_points: str) -> str:
    points = split_points(exam_points)
    if points:
        return f"「{points[0][:24]}」を起点に、{term}の表を作って関連用語と並べる。"
    return f"{term}は定義→要件→効果の3段で短いメモにまとめる。"


def main() -> int:
    rows = list(csv.DictReader(GLOSSARY_CSV.read_text(encoding="utf-8-sig").splitlines()))
    updated = 0
    for i, row in enumerate(rows):
        term = norm(row.get("term"))
        if not term or term in SKIP_TERMS:
            continue
        cat = norm(row.get("category")) or "その他"
        if not norm(row.get("common_mistakes")):
            row["common_mistakes"] = MISTAKE_TEMPLATES.get(cat, MISTAKE_TEMPLATES["権利関係"])
        if not norm(row.get("memory_tip")):
            row["memory_tip"] = default_memory_tip(term, norm(row.get("exam_points")))
        before_body = norm(row.get("term_detail_body"))
        before_expl = norm(row.get("explanation"))
        before_faq = norm(row.get("faq_1_question"))
        rows[i] = enrich_csv_row(row)
        if (
            rows[i].get("term_detail_body") != before_body
            or rows[i].get("explanation") != before_expl
            or (rows[i].get("faq_1_question") and not before_faq)
        ):
            updated += 1

    with GLOSSARY_CSV.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=GLOSSARY_HEADER, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)

    print(f"Enriched {updated} legacy terms in {GLOSSARY_CSV}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
