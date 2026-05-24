#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""試験ガイド記事を専門家・プロライター水準へ引き上げる（全件）。"""

from __future__ import annotations

import re

from tools.glossary_readable import to_plain_style
from tools.guide_pro_pass import norm, split_semicolon
from tools.site_config import exam_name

_BOILER = (
    "理解が固まったら、",
    "正解理由を声に出して説明できるかまでチェックしましょう。",
    "インプットのあとはアウトプットが重要です。",
    "まずは実力を確認してみましょう。",
    "登録不要・すぐに体験できます。",
    "試験本番でも同じパターンのケアレスミスが点を落とす原因になるため、模試の振り返りに組み込んでください。",
    "当日は新しい知識より、練習済みの手順どおりに進めることが安定につながります。",
)

_GENRE_OPENING: dict[str, str] = {
    "学習計画": "宅建合格は総時間より、宅建業法と過去問演習に割く週の時間が成果を分けます。",
    "合格・難易度": "合格点は毎年変動しますが、学習中は「落とせない基本点」を先に固める設計が有効です。",
    "分野別対策": "分野攻略では満点狙いより、出題数に見合った「取れる点数」を先に確保します。",
    "過去問活用": "過去問は回数より、正解理由と誤り肢の理由を説明できるかが伸びの指標です。",
    "独学対策": "独学では教材の数より、同じ過去問を間違いノート付きで何周するかが成果を分けます。",
    "直前・当日": "直前期は新規インプットより、時間配分とケアレスミスの潰し込みが得点に直結します。",
    "受験・申込": "申込・当日手続きのミスは学力と無関係に失格につながるため、公式案内の一次確認が最優先です。",
    "試験概要": "宅建は範囲が広い国家資格ですが、出題の型は一定なので全体像→分野別→過去問の順で迷いが減ります。",
    "用語整理": "用語は単語帯の量より、似た用語の対比表と過去問での出題文脈で覚えると定着します。",
    "出題・形式": "出題形式に慣れることで、本番は読みの速度と判断の精度が上がります。",
    "注意点・更新": "法改正・統計は年度で変わるため、直前期は公式・直前資料で差分だけ更新するのが効率的です。",
    "復習・苦手克服": "苦手克服は難問の追い込みより、基本問題の取りこぼしをゼロにすることから始めます。",
}

_FIELD_FROM_SLUG: list[tuple[str, str]] = [
    ("hooreijou-seigen", "法令上の制限"),
    ("zei-sonota", "税・その他"),
    ("gyoho", "宅建業法"),
    ("kenri", "権利関係"),
    ("minpo", "権利関係"),
    ("35jou", "宅建業法"),
    ("baisho", "宅建業法"),
    ("yoto-chiiki", "法令上の制限"),
    ("kenpei", "法令上の制限"),
    ("toukei", "税・その他"),
]

_HEADING_HINTS: list[tuple[str, str]] = [
    ("優先", "得点効率の高い論点から手を付け、後回しにしがちな分野は週次で最低限の演習時間を確保します。"),
    ("注意", "試験本番でも同じパターンのミスが点を落とすため、模試の振り返りに「なぜ誤ったか」を一行で残します。"),
    ("失敗", "失敗の多くは知識不足ではなく、復習設計と時間配分の崩れから起きます。計画を細かく立て直しましょう。"),
    ("直前", "直前期は暗記の追加より、本番と同じ2時間・50問のペースで解く演習が効果的です。"),
    ("当日", "当日は新しい論点に手を出さず、練習済みの見直し手順と持ち物確認に集中します。"),
    ("申込", "申込情報はRETIOの案内を基準にし、締切・受験地・記載内容を早めに確定させます。"),
    ("過去問", "過去問は解いたあと、誤り肢が「どの要件をずらしたか」を言語化できるまで読み返します。"),
    ("模試", "模試の点数は一喜一憂せず、分野別の内訳から次の2週間の修正課題を決めます。"),
    ("時間", "学習時間は「確保できた時間」より「演習に使えた時間」で評価すると計画が現実的になります。"),
    ("合格", "合格ラインは年度で上下しますが、38点前後を安定して狙える実力を目標にすると安心です。"),
    ("独学", "独学では解説を読む時間と、自分の言葉で説明する時間の比率を意識すると伸びます。"),
    ("用語", "用語は定義の丸暗記より、類似語との違いを表にしたうえで過去問の文脈で確認します。"),
]


def strip_repeat_genre_frames(text: str, genre: str, section_idx: int) -> str:
    """他セクションに混入したジャンル共通の冒頭・締めを除去。"""
    t = text
    base = _GENRE_OPENING.get(genre, "")
    if base and section_idx > 1:
        t = t.replace(base, "")
    for phrase in (
        "学習の次の一手は、用語解説で用語を確認したうえで過去問・一問一答に進むと効率的です。",
        "学習の次の一手は、用語解説で用語を確認したうえで過去問・一問一答に進むと効率的です",
    ):
        if section_idx < 5:
            t = t.replace(phrase, "")
    return re.sub(r"\s+", " ", t).strip()


def strip_boiler(text: str) -> str:
    t = to_plain_style(text)
    for phrase in _BOILER:
        while phrase in t:
            idx = t.find(phrase)
            end = t.find("。", idx)
            if end == -1:
                t = t[:idx] + t[idx + len(phrase) :]
            else:
                t = t[:idx] + t[end + 1 :]
    t = re.sub(r"\s+", " ", t).strip()
    t = re.sub(r"[。．]{2,}", "。", t)
    return t.strip()


def _word_count(text: str) -> int:
    return len(re.sub(r"\s+", "", text))


def _field_hint(slug: str) -> str:
    for key, label in _FIELD_FROM_SLUG:
        if key in slug:
            return label
    return ""


def _heading_hint(heading: str) -> str:
    for key, sentence in _HEADING_HINTS:
        if key in heading:
            return sentence
    return ""


def _format_table_like(text: str) -> str:
    """表形式が1行に潰れている本文を読みやすい段落・箇条書きに整える。"""
    t = text
    row_starts = (
        "法律初学者 ",
        "社会人初学者 ",
        "不動産業界経験者 ",
        "再受験者 ",
        "1年 ",
        "6ヶ月 ",
        "3ヶ月 ",
        "1ヶ月 ",
        "宅建業法：",
        "権利関係：",
        "法令上の制限：",
        "税・その他：",
        "模試・総復習：",
        "都市計画法 ",
        "建築基準法 ",
        "国土利用計画法 ",
        "農地法 ",
    )
    for start in row_starts:
        if start in t:
            t = t.replace(f" {start}", f"\n\n・{start}")
            t = t.replace(start, f"\n\n・{start}", 1)
    for label in (
        "社会人初学者 ",
        "不動産業界経験者 ",
        "再受験者 ",
        "権利関係：",
        "法令上の制限：",
        "税・その他：",
        "模試・総復習：",
    ):
        if label in t and f"\n\n・{label}" not in t:
            t = t.replace(label, f"\n\n・{label}")
    t = re.sub(r"([。．])\s*([①②③④⑤])", r"\1\n\n\2", t)
    t = re.sub(r"考え方：\s*", "\n\n【考え方】\n", t)
    t = re.sub(r"注意：\s*", "\n\n【注意】\n", t)
    t = re.sub(r"狙い：\s*", "\n\n【狙い】\n", t)
    return t


def _expert_opening(
    genre: str,
    heading: str,
    slug: str,
    title: str,
    *,
    section_idx: int,
) -> str:
    parts: list[str] = []
    if section_idx == 1:
        base = _GENRE_OPENING.get(genre, "")
        if base:
            parts.append(base)
        field = _field_hint(slug)
        if field and field not in title:
            parts.append(f"本記事は{field}を中心に、{exam_name()}の学習設計を整理します。")
    hint = _heading_hint(heading)
    if hint:
        parts.append(hint)
    return "\n\n".join(parts)


def _expert_closing(genre: str, heading: str) -> str:
    if any(k in heading for k in ("注意", "失敗", "落とし穴")):
        return "同じ誤りを繰り返さないよう、間違いノートに「条文・数字・主体」のどれを取り違えたかを記録しておきましょう。"
    if genre in ("過去問活用", "分野別対策", "独学対策"):
        return f"この段階が固まったら、{exam_name()}の過去問で条件文の読み取りまで確認しましょう。"
    if genre in ("直前・当日", "受験・申込"):
        return "本番は慣れた手順どおりに進めることが、得点よりも先に大切です。"
    return "学習の次の一手は、用語解説で用語を確認したうえで過去問・一問一答に進むと効率的です。"


def _section_from_title(title: str, heading: str) -> str:
    """見出しとタイトルから専門的な補足段落を生成。"""
    core = title.split("｜")[0].split("？")[0]
    if "？" in title:
        return (
            f"「{core}」という疑問は、受験者の多くが同じ段階でぶつかる論点です。"
            f"ここでは{heading}の観点から、試験対策に直結する形で整理します。"
        )
    return (
        f"{heading}では、{core}について実務と試験の両方で迷いやすい点を押さえます。"
        "暗記の前に「何を判断する問題か」を言語化してから条文や数字に入ると定着しやすくなります。"
    )


def enhance_section_body(
    article: dict[str, str],
    idx: int,
    *,
    used_openings: set[str],
) -> str:
    body = norm(article.get(f"section_{idx}_body"))
    heading = norm(article.get(f"section_{idx}_heading"))
    if not heading and not body:
        return ""
    genre = norm(article.get("genre"))
    slug = norm(article.get("slug"))
    title = norm(article.get("title"))

    if not body:
        body = _section_from_title(title, heading or f"セクション{idx}")

    body = strip_boiler(body)
    body = strip_repeat_genre_frames(body, genre, idx)
    body = _format_table_like(body)

    opening = _expert_opening(genre, heading, slug, title, section_idx=idx)
    if opening:
        key = opening[:40]
        if key not in used_openings:
            used_openings.add(key)
            if opening[:24] not in body:
                body = f"{opening}\n\n{body}" if body else opening

    if _word_count(body) < 160:
        extra = _section_from_title(title, heading)
        if extra not in body:
            body = f"{body}\n\n{extra}".strip()

    closing = _expert_closing(genre, heading)
    if idx >= 4 and closing not in body:
        body = f"{body}\n\n{closing}"

    return strip_boiler(body)


def build_expert_lead(article: dict[str, str]) -> str:
    title = norm(article.get("title"))
    genre = norm(article.get("genre"))
    lead = strip_boiler(norm(article.get("lead")))
    hook = _GENRE_OPENING.get(genre, "")
    field = _field_hint(norm(article.get("slug")))

    parts: list[str] = []
    if lead and _word_count(lead) >= 40:
        parts.append(lead)
    else:
        parts.append(
            f"本記事では、{title.split('｜')[0]}について、"
            f"{exam_name()}の受験者が実践で使える形に整理します。"
        )
    if hook and hook not in "".join(parts):
        parts.append(hook)
    if field:
        parts.append(f"特に{field}の論点と、学習の優先順位を意識しながら読み進めてください。")
    return "\n\n".join(parts)


def build_expert_faqs(article: dict[str, str]) -> list[tuple[str, str]]:
    title = norm(article.get("title"))
    slug = norm(article.get("slug"))
    genre = norm(article.get("genre"))
    lead = build_expert_lead(article)
    sections: list[tuple[str, str]] = []
    for i in range(1, 8):
        h = norm(article.get(f"section_{i}_heading"))
        b = norm(article.get(f"section_{i}_body"))
        if h and b:
            sections.append((h, strip_boiler(b)))

    faqs: list[tuple[str, str]] = []
    core_q = title if "？" in title else f"{title.split('｜')[0]}について教えてください。"
    if sections:
        ans = strip_boiler(sections[0][1])
        if len(ans) > 320:
            ans = ans[:317] + "…"
    else:
        ans = lead
    faqs.append((core_q, ans))

    if len(sections) >= 2:
        h2, b2 = sections[1]
        faqs.append(
            (
                f"「{h2}」で押さえるべきポイントは何ですか？",
                b2[:320] + ("…" if len(b2) > 320 else ""),
            )
        )

    pitfall = ""
    for h, b in sections:
        if any(k in h for k in ("注意", "失敗", "よくある", "落とし穴", "ミス")):
            pitfall = b[:300]
            break
    if not pitfall:
        pitfall = (
            f"{genre}では、範囲を広げすぎて過去問演習が後回しになるのが典型的な失敗です。"
            "宅建業法と過去問の時間を先に確保し、他分野は弱点補填に回すと効率が上がります。"
        )
    faqs.append((f"{title.split('｜')[0]}で避けたい失敗パターンは？", pitfall))

    tags = split_semicolon(norm(article.get("tags")))
    tag = tags[0] if tags else genre
    faqs.append(
        (
            f"{tag}の学習をこのサイトで進めるには？",
            "用語解説でキーワードを確認したあと、過去問・実践演習・一問一答で演習できます。"
            f"関連テーマは /articles/{slug}/ 付近のリンクや、同じジャンルの試験ガイドもあわせて参照してください。",
        )
    )
    return faqs[:4]


def upgrade_guide_expert(article: dict[str, str]) -> dict[str, str]:
    out = dict(article)
    out["lead"] = build_expert_lead(out)
    intent = strip_boiler(norm(out.get("user_intent")))
    if not intent or _word_count(intent) < 30:
        out["user_intent"] = out["lead"][:220]

    used_openings: set[str] = set()
    for i in range(1, 8):
        heading = norm(out.get(f"section_{i}_heading"))
        if not heading:
            out[f"section_{i}_body"] = ""
            continue
        out[f"section_{i}_body"] = enhance_section_body(out, i, used_openings=used_openings)

    faqs = build_expert_faqs(out)
    for n, (q, a) in enumerate(faqs, start=1):
        out[f"faq_{n}_question"] = q
        out[f"faq_{n}_answer"] = to_plain_style(a)
    for n in range(len(faqs) + 1, 5):
        out[f"faq_{n}_question"] = ""
        out[f"faq_{n}_answer"] = ""

    actions = split_semicolon(norm(out.get("action_items")))
    for extra in (
        "用語解説で関連キーワードを確認する",
        "過去問一覧で該当分野を1セット演習する",
        "間違えた論点を一行メモして翌日に再確認する",
    ):
        if extra not in actions and len(actions) < 4:
            actions.append(extra)
    out["action_items"] = ";".join(actions[:4])

    note = norm(out.get("revision_note"))
    if "expert_writer" not in note:
        out["revision_note"] = (note + " guide_expert_writer適用").strip()

    return out
