#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""試験ガイド記事を専門家・プロライター水準へ引き上げる。"""

from __future__ import annotations

import re

from tools.glossary_readable import to_plain_style
from tools.site_config import exam_name

_FAQ_GENERIC_Q1 = "最初に何を確認すればよいですか"
_FAQ_GENERIC_Q2 = "独学でも活用できますか"

_BOILER_PHRASES = (
    "インプットのあとはアウトプットが重要です。過去問を解いて知識を定着させましょう。",
    "インプットのあとはアウトプットが大切です。",
    "この分野の過去問を解いて知識を定着させましょう。",
    "まずは実力を確認してみましょう。",
    "登録不要・すぐに体験できます。",
)

_GENRE_EXPERT_HOOK: dict[str, str] = {
    "学習計画": "合格までの時間配分は、総時間より「宅建業法と過去問演習に何時間割くか」で決まります。",
    "合格・難易度": "合格点は年度で上下しますが、学習中は「落とせない基本点」を先に固める設計が有効です。",
    "分野別対策": "分野攻略の鍵は、頻出論点を表にまとめ、過去問で条件の読み取りを反復することです。",
    "過去問活用": "過去問は回数より、正解理由と誤り肢の理由を説明できるかが伸びの指標になります。",
    "独学対策": "独学では教材の数より、同じ過去問を間違いノート付きで何周するかが成果を分けます。",
    "直前・当日": "直前期は新規インプットより、時間配分とケアレスミスの潰し込みが得点に直結します。",
    "受験・申込": "申込・当日手続きのミスは学力と無関係に失格につながるため、公式案内の一次確認が最優先です。",
    "試験概要": "宅建は範囲が広い国家資格ですが、出題の型は一定なので、全体像→分野別→過去問の順で迷いが減ります。",
    "用語整理": "用語は単語帳の量より、似た用語の対比表と過去問での出題文脈で覚えると定着します。",
    "出題・形式": "出題形式に慣れることで、本番は読みの速度と判断の精度が上がります。",
    "注意点・更新": "法改正・統計は年度で変わるため、直前期は公式・直前資料で差分だけ更新するのが効率的です。",
    "復習・苦手克服": "苦手克服は難問の追い込みより、基本問題の取りこぼしをゼロにすることから始めます。",
}


def norm(value: str | None) -> str:
    return (value or "").strip()


def split_semicolon(value: str) -> list[str]:
    return [x.strip() for x in (value or "").split(";") if x.strip()]


def _dedupe_sentences(text: str) -> str:
    t = to_plain_style(text)
    if not t:
        return ""
    sentences = re.split(r"(?<=[。．])", t)
    seen: set[str] = set()
    out: list[str] = []
    for s in sentences:
        s = s.strip()
        if not s:
            continue
        key = re.sub(r"\s+", "", s)
        if any(b in s for b in _BOILER_PHRASES):
            continue
        if key in seen:
            continue
        seen.add(key)
        out.append(s if s.endswith("。") else s + "。")
    return "".join(out)


def _first_section_summary(article: dict[str, str]) -> str:
    body = norm(article.get("section_1_body"))
    if not body:
        return norm(article.get("lead"))
    return _dedupe_sentences(body.split("\n")[0] if "\n" in body else body[:200])


def build_pro_lead(article: dict[str, str]) -> str:
    lead = _dedupe_sentences(norm(article.get("lead")))
    genre = norm(article.get("genre"))
    hook = _GENRE_EXPERT_HOOK.get(genre, "")
    if not lead:
        return hook
    if hook and hook[:20] not in lead:
        return f"{lead} {hook}"
    return lead


def enrich_section_body(article: dict[str, str], idx: int) -> str:
    body = norm(article.get(f"section_{idx}_body"))
    if not body:
        return ""
    body = _dedupe_sentences(body)
    genre = norm(article.get("genre"))
    heading = norm(article.get(f"section_{idx}_heading"))

    note = norm(article.get("revision_note"))
    if "expert_writer" in note or "guide_expert_writer" in note:
        return body

    return body


def _title_core_question(title: str) -> str:
    t = title
    for suffix in ("を解説", "を徹底解説", "完全版", "まとめ", "攻略", "の解説"):
        t = t.replace(suffix, "")
    if "？" in t:
        return t.split("？")[0] + "？"
    if "とは" in t:
        return t.split("とは")[0] + "とは何ですか？"
    return f"{t[:40]}…について教えてください。"


def build_pro_faqs(article: dict[str, str]) -> list[tuple[str, str]]:
    title = norm(article.get("title"))
    slug = norm(article.get("slug"))
    genre = norm(article.get("genre"))
    lead = norm(article.get("lead"))
    tags = split_semicolon(norm(article.get("tags")))
    sections: list[tuple[str, str]] = []
    for i in range(1, 8):
        h = norm(article.get(f"section_{i}_heading"))
        b = norm(article.get(f"section_{i}_body"))
        if h and b:
            sections.append((h, _dedupe_sentences(b)))

    faqs: list[tuple[str, str]] = []

    core_q = _title_core_question(title)
    if sections:
        ans = _dedupe_sentences(sections[0][1])[:280]
        if not ans.endswith("。"):
            ans += "。"
    else:
        ans = _dedupe_sentences(lead) or f"{title}の要点は本文の目次順に沿って確認できます。"
    faqs.append((core_q, ans))

    if len(sections) >= 2:
        h2, b2 = sections[1]
        faqs.append(
            (
                f"「{h2}」で押さえるべきポイントは何ですか？",
                b2[:300] + ("…" if len(b2) > 300 else ""),
            )
        )

    pitfall = ""
    for h, b in sections:
        if any(k in h for k in ("注意", "失敗", "よくある", "間違い", "落とし穴")):
            pitfall = b[:280]
            break
    if not pitfall and genre in ("分野別対策", "学習計画", "独学対策"):
        pitfall = (
            f"{genre}でつまずきやすいのは、範囲を広げすぎて過去問演習が後回しになることです。"
            "宅建業法と過去問を先に固定し、他分野は弱点補填に回すと効率が上がります。"
        )
    if pitfall:
        faqs.append(
            (
                f"{title.replace('｜', ' ').split('｜')[0]}で避けたい失敗パターンは？",
                pitfall,
            )
        )

    tag_hint = tags[0] if tags else genre
    faqs.append(
        (
            f"{tag_hint}の学習をこのサイトで進めるには？",
            f"用語解説で基礎を確認したあと、過去問・実践演習・一問一答で演習できます。"
            f"関連記事は /articles/{slug}/ 付近のリンクから、同じテーマのガイドも参照してください。",
        )
    )

    return faqs[:4]


def is_generic_faq(article: dict[str, str]) -> bool:
    q1 = norm(article.get("faq_1_question"))
    return _FAQ_GENERIC_Q1 in q1 or _FAQ_GENERIC_Q2 in q1


def upgrade_guide_row(article: dict[str, str]) -> dict[str, str]:
    out = dict(article)
    out["lead"] = build_pro_lead(out)
    intent = norm(out.get("user_intent"))
    if not intent or len(intent) < 24:
        out["user_intent"] = out["lead"][:200]

    for i in range(1, 8):
        enriched = enrich_section_body(out, i)
        if enriched:
            out[f"section_{i}_body"] = enriched

    if is_generic_faq(out) or not norm(out.get("faq_1_question")):
        faqs = build_pro_faqs(out)
        for n, (q, a) in enumerate(faqs, start=1):
            out[f"faq_{n}_question"] = q
            out[f"faq_{n}_answer"] = to_plain_style(a)
        for n in range(len(faqs) + 1, 5):
            out[f"faq_{n}_question"] = ""
            out[f"faq_{n}_answer"] = ""

    actions = split_semicolon(norm(out.get("action_items")))
    if len(actions) < 2:
        extra = [
            "用語解説で関連キーワードを確認する",
            "過去問一覧で該当分野を1セット演習する",
        ]
        for e in extra:
            if e not in actions:
                actions.append(e)
        out["action_items"] = ";".join(actions[:4])

    note = norm(out.get("revision_note"))
    if "pro_pass" not in note:
        out["revision_note"] = (note + " guide_pro_pass適用").strip()

    return out
