#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""手書き深掘り以外の用語向けに、CSV内容から記事品質データを生成。"""

from __future__ import annotations

import re

from tools.glossary_enrich import (
    clean_exam_points,
    derive_exam_points,
    norm,
    sanitize_legacy_text,
    split_points,
)

CATEGORY_MISTAKES = {
    "権利関係": "類似制度（期間・要件・効力）の取り違え。条文番号と数字をセットで暗記する。",
    "宅建業法": "35条・37条・8条・14条の交付時期・記載事項の混同。",
    "法令上の制限": "区域・用途・数値（面積・率・幅員）の組み合わせ誤り。",
    "税・その他": "課税主体・期限・税率・控除要件の混同。計算の順序ミスに注意。",
    "試験対策": "出題比率・合格点など暗記数字を最新情報と混同しない。",
}

CATEGORY_DETAIL = {
    "権利関係": (
        "権利関係では誰にどの効果が及ぶか、期間・要件の有無が問われやすいです。"
        "関連用語と条文番号を比較表にまとめてください。"
    ),
    "宅建業法": (
        "宅建業法では書面交付の順序、記載事項、業者・宅建士の責任区分が頻出です。"
        "35条・37条・8条・14条を表で整理すると得点が安定します。"
    ),
    "法令上の制限": (
        "法令上の制限では「どの法令の・どの区域で・何が必要か」を三段で覚えるとよいです。"
        "数値と例外規定の区別が問われます。"
    ),
    "税・その他": (
        "税・その他は課税主体・申告期限・税率・控除要件と計算手順がセットで出題されます。"
    ),
    "試験対策": (
        "試験対策は数値・手続の最新情報を公式要綱で確認し、過去問演習と併用してください。"
    ),
}


def _first_sentence(text: str, *, max_len: int = 200) -> str:
    t = sanitize_legacy_text(text)
    if not t:
        return ""
    for sep in ("。", "．", "\n"):
        if sep in t:
            t = t.split(sep, 1)[0].strip() + "。"
            break
    if len(t) > max_len:
        t = t[: max_len - 1] + "…"
    return t


def build_bulk_overrides(row: dict[str, str]) -> dict[str, str]:
    """手書き深掘りに無い用語向けの上書きフィールド。"""
    term = norm(row.get("term"))
    cat = norm(row.get("category")) or "権利関係"
    short_def = norm(row.get("short_def"))
    definition = sanitize_legacy_text(row.get("definition"))
    legal = norm(row.get("legal_basis"))
    related = norm(row.get("related_terms"))

    lead = _first_sentence(definition) or (
        short_def if short_def.endswith("。") else f"{short_def}。" if short_def else ""
    )
    parts: list[str] = []
    if lead:
        parts.append(lead)
    if legal:
        parts.append(f"{term}の根拠は主に{legal}にあります。")
    if related:
        parts.append(f"関連する{related.replace(';', '・')}との比較も有効です。")
    parts.append(CATEGORY_DETAIL.get(cat, CATEGORY_DETAIL["権利関係"]))

    exam = clean_exam_points(norm(row.get("exam_points")))
    if len(split_points(exam)) < 2:
        exam = clean_exam_points(
            derive_exam_points(
                {
                    "term": term,
                    "definition": lead or definition,
                    "explanation": "",
                    "exam_points": exam,
                }
            )
        )
    if len(split_points(exam)) < 2 and lead:
        exam = lead.rstrip("。")

    mistakes = sanitize_legacy_text(row.get("common_mistakes"))
    if not mistakes or "類似制度（期間・要件・効力）" in mistakes:
        mistakes = CATEGORY_MISTAKES.get(cat, CATEGORY_MISTAKES["権利関係"])

    memory = norm(row.get("memory_tip"))
    if not memory or "を起点に、" in memory and len(memory) < 40:
        pts = split_points(exam)
        if pts:
            memory = f"「{pts[0][:28]}」を軸に{term}の比較表を作る。"
        else:
            memory = f"{term}は定義→要件→効果の3段で整理。"

    return {
        "detail_body": "".join(parts),
        "exam_points": exam,
        "common_mistakes": mistakes,
        "memory_tip": memory,
    }
