#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""宅建 知識ハブ S30 ヘルパー（誤答追加分など）."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"

HEADER_MISTAKES = [
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


def _faq(qa: list[tuple[str, str]]) -> dict[str, str]:
    out: dict[str, str] = {}
    for i, (q, a) in enumerate(qa, start=1):
        out[f"faq_{i}_question"] = q
        out[f"faq_{i}_answer"] = a
    return out


def _rows(*items: dict) -> str:
    return json.dumps(list(items), ensure_ascii=False)


_OFFICIAL = (
    "数値・手続の最新は公益財団法人 全日本不動産協会・"
    "公益財団法人 不動産流通推進センターの試験要項・法令改正情報で必ずご確認ください。"
)


def mis(
    slug: str,
    title: str,
    cat: str,
    tags: str,
    summary: str,
    confusion: str,
    patterns: list[tuple[str, str, str, str]],
    article_title: str,
    lead: str,
    points: str,
    mistakes: str,
    tip: str,
    related: str,
    qa: list[tuple[str, str]],
) -> dict:
    return {
        "slug": slug,
        "title": title,
        "category": cat,
        "tags": tags,
        "summary": summary,
        "confusion_point": confusion,
        "pattern_rows": _rows(
            *[{"topic": t, "wrong": w, "correct": c, "trap": p} for t, w, c, p in patterns]
        ),
        "article_title": article_title,
        "article_lead": lead,
        "exam_points": points,
        "common_mistakes": mistakes,
        "memory_tip": tip,
        "related_terms": related,
        "fact_checked_at": "2026-05-27",
        **_faq(qa),
    }
