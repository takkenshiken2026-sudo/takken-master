#!/usr/bin/env python3
"""Post-merge corrections for numbers rows (official verify fixes)."""
from __future__ import annotations

import json
from typing import Any

PASS_ITEMS = [
    {"item": "総出題数", "value": "50問", "note": "四肢択一式。登録講習修了者は5問免除で45問出題。"},
    {"item": "試験時間", "value": "120分", "note": "5問免除者も同じ120分で45問を解答。"},
    {"item": "合格判定", "value": "相対評価（総合点）", "note": "科目別足切りなし。基準点は試験後に国交省が発表。"},
    {"item": "合格基準点", "value": "試験後に発表", "note": "例年35〜38点程度だが年度変動。固定36点ルールではない。"},
    {"item": "5問免除（登録講習）", "value": "45問出題", "note": "登録講習修了で最終5問免除（正解扱い）。"},
    {"item": "権利関係", "value": "14問", "note": "民法・借地借家法等。"},
    {"item": "宅建業法", "value": "20問", "note": "出題最多。"},
    {"item": "法令上の制限", "value": "8問", "note": "都計法・建基法等。"},
    {"item": "税・その他", "value": "8問", "note": "税法・統計等。"},
    {"item": "受験料", "value": "8,200円", "note": "RETIO要項（年度で改定の可能性）。"},
    {"item": "試験実施日", "value": "10月第3日曜日", "note": "例年10月第3日曜日。"},
]

BAIKAI_ITEMS = [
    {"item": "専任媒介 契約期間", "value": "3か月以内", "note": "更新は原則1回まで。"},
    {"item": "専任媒介 報告", "value": "2週に1回以上", "note": "書面または電磁的方法。"},
    {"item": "専任媒介 レインズ", "value": "7日以内", "note": "契約後7日以内に登録。"},
    {"item": "専属専任 報告", "value": "1週に1回以上", "note": "専任より頻度が高い。"},
    {"item": "専属専任 レインズ", "value": "5日以内", "note": "契約後5日以内。"},
    {"item": "一般媒介", "value": "法定報告義務なし", "note": "7日報告義務はない。"},
]

PASS_PATCH: dict[str, Any] = {
    "highlight": "50問・120分・相対評価。科目別足切りなし。基準点は試験後発表。",
    "item_rows": PASS_ITEMS,
    "exam_points": "相対評価の総合点;科目別足切りなし;基準点は試験後発表;50問120分;旧36+7点は現行と不一致",
    "common_mistakes": "各科目7点足切りがあると誤解;固定36点と暗記;旧制度の合格基準をそのまま使う",
    "memory_tip": "「50問120分・相対評価・足切りなし」",
}

BAIKAI_PATCH: dict[str, Any] = {
    "highlight": "一般媒介に法定7日報告義務なし。専任2週・レインズ7日、専属1週・レインズ5日。",
    "item_rows": BAIKAI_ITEMS,
    "exam_points": "一般媒介に法定7日報告なし;専任2週1回以上;専属1週1回以上;レインズ7日/5日",
    "common_mistakes": "一般媒介にも7日報告があると誤解;専任と専属の頻度を逆に覚える",
    "memory_tip": "「一般=報告なし／専任2週7日／専属1週5日」",
}

CORRECTIONS: dict[str, dict[str, Any]] = {
    "takken-shiken-goukaku-shutsudai": PASS_PATCH,
    "s32-takken-shiken-2025": {**PASS_PATCH, "title": "宅建試験2025の出題数・合格判定"},
    "s33-takken-36ten": {
        **PASS_PATCH,
        "title": "宅建合格判定（相対評価）",
        "article_title": "宅建合格点｜相対評価と旧36点表記の整理",
    },
    "baikai-hokoku-7days": {
        **BAIKAI_PATCH,
        "title": "媒介契約の報告義務（一般・専任・専属）",
    },
    "s34-baikai-7days": {
        **BAIKAI_PATCH,
        "title": "一般媒介の報告義務（法定7日なし）",
    },
}


def apply_numbers_corrections(rows: list[dict[str, str]]) -> None:
    for row in rows:
        patch = CORRECTIONS.get(row.get("slug", ""))
        if not patch:
            continue
        for key, val in patch.items():
            if key == "item_rows":
                row["item_rows"] = json.dumps(val, ensure_ascii=False)
            else:
                row[key] = val
