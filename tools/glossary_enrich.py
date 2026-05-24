#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""用語CSV行の本文分離・FAQ補完・例題用テキスト生成。"""

from __future__ import annotations

import re
from typing import Any


def norm(s: str | None) -> str:
    return (s or "").strip()


_LIMB_PHRASE = re.compile(
    r"肢では[「\"][^」\"]*[」\"]のいずれかが正誤の分かれ目になりやすいです。?"
)
_MISTAKE_BOILER = re.compile(
    r"特に類似制度（期間・要件・効力）の取り違え。数字と条文番号をセットで暗記する。"
)
_LIMB_TAIL = re.compile(r"[」\"]のいずれ(?:かが正誤の分かれ目になりやすいです。?)?$")


def sanitize_legacy_text(text: str) -> str:
    """一括強化で重複した「肢では…」などを除去。"""
    t = norm(text)
    if not t:
        return ""
    while "肢では「肢では「" in t:
        t = t.replace("肢では「肢では「", "肢では「")
    for _ in range(8):
        prev = t
        t = _LIMB_PHRASE.sub("", t)
        t = _MISTAKE_BOILER.sub("", t)
        t = _LIMB_TAIL.sub("", t)
        t = re.sub(r"^(?:肢では[「\"])+", "", t)
        if t == prev:
            break
    return re.sub(r"\s+", " ", t).strip()


def clean_exam_points(value: str) -> str:
    """exam_points 列の汚染（肢では…・汎用ミス）を除去。"""
    parts: list[str] = []
    for p in split_points(sanitize_legacy_text(value)):
        p = re.sub(r"^肢では[「\"]?", "", p).strip("」\"")
        if len(p) < 4:
            continue
        if "のいずれかが正誤" in p or "類似制度（期間・要件・効力）" in p:
            continue
        if p.startswith("特に類似制度"):
            continue
        parts.append(p)
    return ";".join(parts[:6])


def split_points(value: str) -> list[str]:
    return [p.strip() for p in re.split(r"[;；]", value or "") if p.strip()]


def derive_exam_points(item: dict[str, str]) -> str:
    """既存の exam_points が定義文のコピーなら、試験向けに箇条書きへ分解。"""
    existing = split_points(norm(item.get("exam_points")))
    definition = norm(item.get("definition"))
    if len(existing) >= 2 and not all(e == definition or e in definition for e in existing[:2]):
        return ";".join(existing)

    sources = [
        sanitize_legacy_text(item.get("explanation")),
        sanitize_legacy_text(item.get("definition")),
        sanitize_legacy_text(item.get("exam_points")),
    ]
    text = next((s for s in sources if s), "")
    if not text:
        return ""

    clauses: list[str] = []
    for chunk in re.split(r"[。．\n]", text):
        chunk = chunk.strip()
        if len(chunk) < 8:
            continue
        if any(
            mark in chunk
            for mark in (
                "条",
                "原則",
                "場合",
                "必要",
                "不可",
                "効力",
                "期間",
                "要件",
                "頻出",
                "肢",
                "問わ",
                "％",
                "年",
                "㎡",
                "％",
            )
        ):
            clauses.append(chunk)
    if len(clauses) >= 2:
        return ";".join(clauses[:6])
    if len(clauses) == 1:
        return clauses[0]
    return ";".join(existing) if existing else text[:120]


def polish_short_def(term: str, short_def: str, definition: str) -> str:
    sd = norm(short_def)
    if sd and not sd.endswith("の概要") and not sd.endswith("概要"):
        return sd
    if definition:
        first = definition.split("。", 1)[0].strip()
        if first:
            return first + "。"
    return sd or f"{term}の要点"


def related_phrase(related: str) -> str:
    items = split_points(related.replace("・", ";"))
    if not items:
        return ""
    if len(items) == 1:
        return items[0]
    return "、".join(items[:-1]) + "および" + items[-1]


def build_detail_body(item: dict[str, str]) -> str:
    """定義とは別の「制度の位置づけ・学習のつなぎ」段落。"""
    term = norm(item.get("term"))
    category = norm(item.get("category"))
    legal = norm(item.get("legal_basis"))
    related = related_phrase(norm(item.get("related_terms")))
    custom = norm(item.get("detail_body"))

    if custom and len(custom) >= 72:
        parts = [custom]
        if legal and legal not in custom:
            parts.append(f"{term}の根拠は主に{legal}にあります。")
        if related and related not in custom:
            parts.append(
                f"理解を深めるには、{related}との関係を条文・要件表で並べて整理するのが有効です。"
            )
        return "\n\n".join(parts)

    parts: list[str] = []
    if custom:
        parts.append(custom)
    if legal:
        parts.append(f"{term}の根拠は主に{legal}にあります。")
    return "\n\n".join(parts)


def build_exam_explanation(item: dict[str, str]) -> str:
    """選択肢で問われやすい点（定義の繰り返しを避ける）。"""
    from tools.glossary_article_quality import build_natural_explanation

    return build_natural_explanation(item)


def _faq_answer_is_stale(answer: str) -> bool:
    a = norm(answer)
    return bool(
        a
        and (
            "のいずれかが正誤の分かれ目" in a
            or "肢では「" in a
            or "。 詳しくは、" in a
        )
    )


def _faq1_is_stale(answer: str, short_def: str, definition: str) -> bool:
    if _faq_answer_is_stale(answer):
        return True
    a = norm(answer)
    sd = short_def.rstrip("。")
    if sd and sd in a and a.count("。") >= 3:
        return True
    body = (definition or "").split("\n\n")[0].rstrip("。")
    if body and body in a and len(a) > len(body) + 40:
        return True
    return False


def ensure_faq(item: dict[str, str]) -> dict[str, str]:
    """FAQ1・2を未設定なら補完。定型の古い回答は上書きする。"""
    out = dict(item)
    term = norm(out.get("term"))
    reading = norm(out.get("reading"))
    short_def = norm(out.get("short_def"))
    definition = norm(out.get("definition"))
    points = split_points(clean_exam_points(norm(out.get("exam_points"))))

    if norm(out.get("faq_3_question")):
        return out

    if not norm(out.get("faq_1_question")) or _faq1_is_stale(
        out.get("faq_1_answer") or "", short_def, definition
    ):
        out["faq_1_question"] = f"{term}とは何ですか？"
        label = f"{term}（{reading}）" if reading else term
        body = definition.split("\n\n")[0] if definition else short_def
        out["faq_1_answer"] = f"{label}とは、{body.rstrip('。')}。"

    if not norm(out.get("faq_2_question")) or _faq_answer_is_stale(
        out.get("faq_2_answer") or ""
    ):
        out["faq_2_question"] = f"{term}は試験でどう押さえればよいですか？"
        if points:
            tail = f"次に{points[1]}。" if len(points) >= 2 else ""
            out["faq_2_answer"] = (
                f"まず{points[0]}。{tail}"
                "関連用語と条文番号を表にまとめ、過去問で出題形式に慣れるのが効率的です。"
            )
        else:
            mistakes = norm(out.get("common_mistakes"))
            out["faq_2_answer"] = (
                mistakes
                if mistakes
                else f"{term}は定義の確認に加え、関連制度との比較で押さえるとよいです。"
            )

    return out


def enrich_glossary_item(item: dict[str, str]) -> dict[str, str]:
    """1用語分のフィールドを記事向けに分離・補完。"""
    from tools.glossary_article_quality import (
        build_article_lead,
        build_article_title,
        expand_definition,
    )

    out = ensure_faq(dict(item))
    out["exam_points"] = clean_exam_points(derive_exam_points(out))
    out["definition"] = expand_definition(out)
    definition = norm(out.get("definition"))
    short_def = polish_short_def(norm(out.get("term")), norm(out.get("short_def")), definition)
    detail_extra = build_detail_body(out)
    exam_expl = build_exam_explanation(out)
    term = norm(out.get("term"))

    out["short_def"] = short_def
    out["term_detail_body"] = detail_extra if detail_extra else definition
    out["article_title"] = norm(out.get("article_title")) or build_article_title(
        term, norm(out.get("category"))
    )
    out["article_lead"] = norm(out.get("article_lead")) or build_article_lead(out)
    if detail_extra and detail_extra != definition:
        out["term_detail_body"] = f"{definition}\n\n{detail_extra}"
    else:
        out["term_detail_body"] = definition
    out["explanation"] = exam_expl
    return out


def enrich_csv_row(row: dict[str, str], *, source_item: dict[str, str] | None = None) -> dict[str, str]:
    """CSV行を enrich_glossary_item 相当に更新。"""
    base = source_item or {
        "term": row.get("term"),
        "reading": row.get("reading"),
        "category": row.get("category"),
        "short_def": row.get("short_def"),
        "definition": row.get("definition"),
        "related_terms": row.get("related_terms"),
        "legal_basis": row.get("legal_basis"),
        "explanation": row.get("explanation"),
        "exam_points": row.get("exam_points"),
        "common_mistakes": row.get("common_mistakes"),
        "memory_tip": row.get("memory_tip"),
        "detail_body": "",
        "faq_1_question": row.get("faq_1_question"),
        "faq_1_answer": row.get("faq_1_answer"),
        "faq_2_question": row.get("faq_2_question"),
        "faq_2_answer": row.get("faq_2_answer"),
        "example_question": row.get("example_question"),
        "example_answer": row.get("example_answer"),
    }
    enriched = enrich_glossary_item(base)
    out = dict(row)
    out["definition"] = enriched["definition"]
    out["short_def"] = enriched["short_def"]
    out["term_detail_body"] = enriched["term_detail_body"]
    out["explanation"] = enriched["explanation"]
    out["exam_points"] = clean_exam_points(enriched.get("exam_points") or out.get("exam_points", ""))
    out["article_lead"] = enriched["short_def"]
    out["exam_points"] = enriched.get("exam_points") or out.get("exam_points", "")
    for key in ("faq_1_question", "faq_1_answer", "faq_2_question", "faq_2_answer"):
        if enriched.get(key):
            out[key] = enriched[key]
    return out
