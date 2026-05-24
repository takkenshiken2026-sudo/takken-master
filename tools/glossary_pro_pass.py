#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""用語詳細記事を専門家・プロライター水準へ引き上げる（手書きを活かしつつ過去問知見を統合）。"""

from __future__ import annotations

import re

from tools.glossary_article_quality import (
    strip_generic_padding,
    upgrade_glossary_fields,
)
from tools.glossary_enrich import norm, split_points
from tools.glossary_hand_rewrite import HAND_REWRITE
from tools.glossary_past_insights import build_past_insights

_HAND_TERMS = {norm(t) for t in HAND_REWRITE}

_EXPERT_BY_CATEGORY: dict[str, str] = {
    "宅建業法": (
        "宅建業法の論点は「誰が・いつ・何を交付・説明するか」の順で整理すると、"
        "肢の微妙な差（期間・記載事項・監督処分）を見落としにくくなります。"
        "実務でも書面の段階が取引の進行と一致しているかを確認する視点が、そのまま試験の正誤判断に直結します。"
    ),
    "権利関係": (
        "権利関係は条文の丸暗記より、要件表（誰が・何を・相手方に対して）で理解すると安定します。"
        "過去問では要件を一つだけ変えた選択肢が多いため、「効力がいつ・誰に及ぶか」まで口に出して確認する習慣が有効です。"
    ),
    "法令上の制限": (
        "法令上の制限は制度名と数値をセットで覚えるより、"
        "「その土地で何ができるか」という利用イメージから逆算すると記憶が定着しやすいです。"
        "用途地域と開発許可・建築制限を横並びの表にすると、比較問題に強くなります。"
    ),
    "税・その他": (
        "税・その他は細部の税率より、課税の場面（いつ・誰が・何に）を先に押さえると得点しやすくなります。"
        "統計・住宅金融は直前期の数字確認が効くため、本番2週間前に最新資料へ差し替える運用がおすすめです。"
    ),
}


def _dedupe_paragraphs(text: str) -> str:
    parts = [p.strip() for p in re.split(r"\n{2,}", text) if p.strip()]
    seen: set[str] = set()
    out: list[str] = []
    for p in parts:
        key = re.sub(r"\s+", "", p)[:80]
        if key in seen:
            continue
        seen.add(key)
        out.append(p)
    return "\n\n".join(out)


def build_expert_lens(item: dict[str, str], insights: dict[str, object]) -> str:
    """試験・実務の着眼点（用語ごとに差し替え可能な専門段落）。"""
    term = norm(item.get("term"))
    cat = norm(item.get("category"))
    refs = insights.get("past_refs") or []
    contexts = insights.get("contexts") or []
    pts = split_points(norm(item.get("exam_points")))
    detail = norm(item.get("detail_body") or item.get("term_detail_body") or "")

    if term in _HAND_TERMS and detail and len(detail) >= 60:
        first = detail.split("。", 1)[0].strip()
        cat_extra = _EXPERT_BY_CATEGORY.get(cat) or (
            "過去問では要件の一部を変えた肢が多いため、"
            "「いつ・誰に・どの効果があるか」までセットで確認してください。"
        )
        return (
            f"実務・試験の双方で、{term}は「{first}」という理解が土台になります。"
            f"{cat_extra}"
        )

    if contexts:
        ctx = str(contexts[0]).rstrip("。")
        return (
            f"試験では、{term}が単独の定義問題として出るだけでなく、"
            f"「{ctx}」のような文脈の中で正しい説明かどうかを問う形式が多いです。"
            "肢の数字・主体・期限のいずれかがずれていないかを、条文とセットで確認してください。"
        )

    if refs:
        y, n = refs[0]
        lead_pt = pts[0] if pts else "定義と要件の区別"
        return (
            f"{y}年問{n}をはじめ過去問で繰り返し問われる論点は「{lead_pt.rstrip('。')}」周辺です。"
            f"{term}は関連制度との比較表を1枚作り、○×演習で「違いが言語化できる」状態を目指すと本番で安定します。"
        )

    base = _EXPERT_BY_CATEGORY.get(cat) or (
        f"{term}は出題範囲が広い中でも、定義→要件→効果の順に説明できると復習効率が上がります。"
        "過去問で1問解いたあと、なぜ他の肢が誤りかを一言で言えるかまで確認してください。"
    )
    return base


def append_expert_section(item: dict[str, str]) -> str:
    """term_detail_body 末尾に専門家視点を付与（重複時はスキップ）。"""
    body = strip_generic_padding(
        norm(item.get("term_detail_body") or item.get("detail_body") or "")
    )
    insights = build_past_insights(item)
    lens = build_expert_lens(item, insights)
    if not body:
        return lens
    if "試験では、" in body and lens[:12] in body:
        return _dedupe_paragraphs(body)
    if "過去問で" in body and "過去問で" in lens:
        return _dedupe_paragraphs(f"{body}\n\n【試験・実務の着眼点】\n{lens}")
    marker = "【試験・実務の着眼点】"
    if marker in body:
        return _dedupe_paragraphs(body)
    return _dedupe_paragraphs(f"{body}\n\n{marker}\n{lens}")


def upgrade_glossary_pro(item: dict[str, str]) -> dict[str, str]:
    """手書きリライトを保持しつつ品質フィールドを引き上げる。"""
    term = norm(item.get("term"))
    preserve = term in _HAND_TERMS
    out = upgrade_glossary_fields(item, preserve_deep=preserve)
    out["term_detail_body"] = append_expert_section(out)
    if norm(out.get("detail_body")):
        out["detail_body"] = strip_generic_padding(
            out["term_detail_body"].split("\n\n【試験・実務の着眼点】", 1)[0]
        )
    return out
