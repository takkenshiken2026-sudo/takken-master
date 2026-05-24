#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""過去問解説から用語ごとの固有の学習インサイトを抽出。"""

from __future__ import annotations

import csv
import re
from functools import lru_cache
from pathlib import Path

from tools.glossary_enrich import norm, split_points
from tools.glossary_past_questions import find_past_questions_for_term
from tools.glossary_term_search import term_search_keys

ROOT = Path(__file__).resolve().parents[1]
PAST_CSV = ROOT / "data" / "past_questions.csv"

_SKIP_IN_SENTENCE = (
    "確認ポイントは",
    "正解は選択肢",
    "正解は",
    "本問は無効",
)


def _strip_html(text: str) -> str:
    return re.sub(r"<[^>]+>", "", text or "").strip()


def _split_sentences(text: str) -> list[str]:
    text = _strip_html(text).replace("\n", " ")
    parts = re.split(r"(?<=[。．])", text)
    return [p.strip() for p in parts if len(p.strip()) >= 10]


@lru_cache(maxsize=1)
def _past_rows_by_key() -> dict[tuple[int, int], dict[str, str]]:
    if not PAST_CSV.is_file():
        return {}
    out: dict[tuple[int, int], dict[str, str]] = {}
    for row in csv.DictReader(PAST_CSV.read_text(encoding="utf-8-sig").splitlines()):
        try:
            key = (int(row["exam_year"]), int(row["question_no"]))
        except (ValueError, KeyError):
            continue
        out[key] = row
    return out


def _sentence_matches(sentence: str, keys: list[str]) -> bool:
    return any(k and k in sentence for k in keys)


def _is_boiler_sentence(sentence: str) -> bool:
    return any(skip in sentence for skip in _SKIP_IN_SENTENCE)


def extract_wrong_choice_mistakes(explanation: str, *, limit: int = 3) -> list[str]:
    """解説中の「Nは誤り」付き記述から、肢選びの注意点を抽出。"""
    mistakes: list[str] = []
    seen: set[str] = set()
    for sent in _split_sentences(explanation):
        if not re.search(r"（?\d+は誤り）?", sent):
            continue
        stmt = re.sub(r"（\d+は誤り）.*$", "", sent)
        stmt = re.sub(r"\d+は誤り.*$", "", stmt).strip("（( ）) ")
        if len(stmt) < 12 or stmt in seen:
            continue
        seen.add(stmt)
        tip = stmt if stmt.endswith("。") else stmt + "。"
        mistakes.append(f"過去問では「{tip.rstrip('。')}」のような説明が誤り肢になりやすいです。")
        if len(mistakes) >= limit:
            break
    return mistakes


def extract_exam_clauses(
    explanation: str, keys: list[str], *, limit: int = 4
) -> list[str]:
    """用語・関連キーワードに触れる解説文から試験の論点を抽出。"""
    clauses: list[str] = []
    seen: set[str] = set()
    for sent in _split_sentences(explanation):
        if _is_boiler_sentence(sent) or re.search(r"（?\d+は誤り）?", sent):
            continue
        if not _sentence_matches(sent, keys):
            continue
        core = sent.strip()
        if core in seen or len(core) < 14:
            continue
        seen.add(core)
        clauses.append(core if core.endswith("。") else core + "。")
        if len(clauses) >= limit:
            break
    return clauses


def gather_past_hits(
    term: str,
    related_terms: str = "",
    legal_basis: str = "",
    *,
    limit: int = 3,
) -> list[dict]:
    hits = find_past_questions_for_term(
        term, limit=limit, related_terms=related_terms, legal_basis=legal_basis
    )
    if hits:
        return hits
    for rel in split_points((related_terms or "").replace("・", ";")):
        if len(rel) < 2:
            continue
        extra = find_past_questions_for_term(rel, limit=1)
        for h in extra:
            if h not in hits:
                hits.append(h)
        if len(hits) >= limit:
            break
    return hits[:limit]


def build_past_insights(item: dict[str, str], *, limit_hits: int = 3) -> dict[str, object]:
    """過去問ベースの用語固有データ。見つからない場合は空に近い dict。"""
    term = norm(item.get("term"))
    related = norm(item.get("related_terms"))
    legal = norm(item.get("legal_basis"))
    keys = term_search_keys(term, related, legal)

    exam_points: list[str] = []
    mistakes: list[str] = []
    contexts: list[str] = []
    past_refs: list[tuple[int, int]] = []
    seen_pts: set[str] = set()
    seen_mis: set[str] = set()

    by_key = _past_rows_by_key()
    for hit in gather_past_hits(term, related, legal, limit=limit_hits):
        row = by_key.get((hit["year"], hit["qno"]))
        if not row:
            continue
        past_refs.append((hit["year"], hit["qno"]))
        exp = row.get("explanation") or ""
        stem = _strip_html(row.get("stem") or "")

        for clause in extract_exam_clauses(exp, keys, limit=4):
            if clause not in seen_pts:
                seen_pts.add(clause)
                exam_points.append(clause.rstrip("。"))
        for m in extract_wrong_choice_mistakes(exp, limit=2):
            if m not in seen_mis:
                seen_mis.add(m)
                mistakes.append(m)

        if stem and _sentence_matches(stem, keys) and len(contexts) < 2:
            preview = stem if len(stem) <= 100 else stem[:99] + "…"
            contexts.append(preview)

    return {
        "exam_points": exam_points[:6],
        "mistakes": mistakes[:3],
        "contexts": contexts[:2],
        "past_refs": past_refs[:2],
        "has_past": bool(past_refs),
    }
