#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""宅建マスター向け 知識ハブ CSV（比較・数値・誤答）の一括リライト。"""

from __future__ import annotations

import csv
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from tools.knowledge_hub_content.comparisons import COMPARISONS  # noqa: E402
from tools.knowledge_hub_content.mistakes import MISTAKES  # noqa: E402
from tools.knowledge_hub_content.numbers import NUMBERS  # noqa: E402

DATE = "2026-05-27"

COMPARE_FIELDS = [
    "slug",
    "title",
    "category",
    "tags",
    "summary",
    "col_labels",
    "compare_rows",
    "article_title",
    "article_lead",
    "exam_points",
    "common_mistakes",
    "memory_tip",
    "related_terms",
    "faq_1_question",
    "faq_1_answer",
    "faq_2_question",
    "faq_2_answer",
    "faq_3_question",
    "faq_3_answer",
    "faq_4_question",
    "faq_4_answer",
    "fact_checked_at",
]

NUMBERS_FIELDS = [
    "slug",
    "title",
    "category",
    "tags",
    "summary",
    "highlight",
    "item_rows",
    "article_title",
    "article_lead",
    "exam_points",
    "common_mistakes",
    "memory_tip",
    "related_terms",
    "faq_1_question",
    "faq_1_answer",
    "faq_2_question",
    "faq_2_answer",
    "faq_3_question",
    "faq_3_answer",
    "faq_4_question",
    "faq_4_answer",
    "fact_checked_at",
]

MISTAKES_FIELDS = [
    "slug",
    "title",
    "category",
    "tags",
    "summary",
    "confusion_point",
    "pattern_rows",
    "article_title",
    "article_lead",
    "exam_points",
    "common_mistakes",
    "memory_tip",
    "related_terms",
    "faq_1_question",
    "faq_1_answer",
    "faq_2_question",
    "faq_2_answer",
    "faq_3_question",
    "faq_3_answer",
    "faq_4_question",
    "faq_4_answer",
    "fact_checked_at",
]

# 得点源（S）に設定する用語（部分一致）
S_TERM_KEYS = [
    "重要事項説明",
    "35条書面",
    "37条書面",
    "契約書の作成・交付",
    "媒介契約",
    "専任媒介",
    "専属専任",
    "一般媒介",
    "手付",
    "クーリングオフ",
    "宅建士",
    "報酬",
    "建ぺい率",
    "容積率",
    "用途地域",
    "抵当権",
    "借地借家",
    "定期借地",
    "自己契約",
    "双方代理",
    "固定資産税",
    "都市計画",
    "農地法",
    "都市計画法",
    "建築基準法",
    "登記",
    "意思表示",
    "先取特権",
    "質権",
    "根抵当",
    "35条",
    "37条",
    "業務規程",
    "重要事項の不告知",
]


def _json_field(rows: list) -> str:
    return json.dumps(rows, ensure_ascii=False)


def _normalize_list_text(value: str) -> str:
    """セミコロン区切りフィールドを ASCII ; に統一。"""
    return value.replace("；", ";")


def _serialize_value(key: str, value: object) -> str:
    if value is None:
        return ""
    if key == "col_labels" and isinstance(value, list):
        return ";".join(str(v).strip() for v in value if str(v).strip())
    if key in {"exam_points", "common_mistakes"} and isinstance(value, str):
        return _normalize_list_text(value)
    if key in {"compare_rows", "item_rows", "pattern_rows"}:
        if isinstance(value, str):
            return value
        return _json_field(value)
    if isinstance(value, (list, dict)):
        return _json_field(value) if isinstance(value, list) else json.dumps(value, ensure_ascii=False)
    return str(value)


def _row_base(d: dict) -> dict:
    d = dict(d)
    d["slug"] = ""
    d["fact_checked_at"] = DATE
    return d


def write_csv(path: Path, fields: list[str], rows: list[dict], json_keys: list[str]) -> None:
    out: list[dict] = []
    for raw in rows:
        row = _row_base(raw)
        for key in json_keys:
            if key in row and not isinstance(row[key], str):
                row[key] = _json_field(row[key])
        serialized = {f: _serialize_value(f, row.get(f, "")) for f in fields}
        out.append(serialized)
    with path.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields, lineterminator="\n")
        w.writeheader()
        w.writerows(out)


def update_glossary_importance() -> tuple[int, int]:
    path = ROOT / "data" / "glossary_terms.csv"
    text = path.read_text(encoding="utf-8-sig")
    rows = list(csv.DictReader(text.splitlines()))
    fieldnames = rows[0].keys() if rows else []
    if "importance" not in fieldnames:
        raise SystemExit("glossary_terms.csv に importance 列がありません")
    n_s = n_a = 0
    for row in rows:
        term = row.get("term") or ""
        if any(k in term for k in S_TERM_KEYS):
            row["importance"] = "S"
            n_s += 1
        else:
            row["importance"] = "A"
            n_a += 1
    with path.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames, lineterminator="\n")
        w.writeheader()
        w.writerows(rows)
    return n_s, n_a


def main() -> int:
    write_csv(ROOT / "data" / "comparisons.csv", COMPARE_FIELDS, COMPARISONS, ["compare_rows"])
    write_csv(ROOT / "data" / "numbers.csv", NUMBERS_FIELDS, NUMBERS, ["item_rows"])
    write_csv(ROOT / "data" / "mistakes.csv", MISTAKES_FIELDS, MISTAKES, ["pattern_rows"])
    n_s, n_a = update_glossary_importance()
    print(f"Wrote {len(COMPARISONS)} comparisons, {len(NUMBERS)} numbers, {len(MISTAKES)} mistakes")
    print(f"Glossary importance: S={n_s}, A={n_a}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
