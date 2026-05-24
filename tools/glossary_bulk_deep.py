#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""手書き深掘り以外の用語向けに、過去問・既存定義から記事データを生成。"""

from __future__ import annotations

from tools.glossary_article_quality import (
    build_detail_from_insights,
    derive_common_mistakes,
    merge_exam_points,
    strip_generic_padding,
)
from tools.glossary_enrich import (
    clean_exam_points,
    derive_exam_points,
    norm,
    sanitize_legacy_text,
    split_points,
)
from tools.glossary_past_insights import build_past_insights


def build_bulk_overrides(row: dict[str, str]) -> dict[str, str]:
    """手書き深掘りに無い用語向けの上書きフィールド（定型パディングなし）。"""
    term = norm(row.get("term"))
    definition = strip_generic_padding(sanitize_legacy_text(row.get("definition")))
    short_def = strip_generic_padding(norm(row.get("short_def")))

    base = dict(row)
    base["definition"] = definition or short_def
    insights = build_past_insights(base)

    exam = merge_exam_points(base, insights)
    if len(split_points(exam)) < 2:
        exam = clean_exam_points(
            derive_exam_points(
                {
                    "term": term,
                    "definition": base["definition"],
                    "explanation": "",
                    "exam_points": exam,
                }
            )
        )

    detail = build_detail_from_insights(base, insights)
    mistakes = derive_common_mistakes(base, insights)

    memory = norm(row.get("memory_tip"))
    if not memory or ("を起点に、" in memory and len(memory) < 48):
        mis = mistakes
        pts = split_points(exam)
        if mis:
            memory = mis[:80]
        elif pts:
            memory = f"{pts[0][:32]}を軸に整理する。"
        else:
            memory = ""

    return {
        "detail_body": detail,
        "exam_points": exam,
        "common_mistakes": mistakes,
        "memory_tip": memory,
    }
