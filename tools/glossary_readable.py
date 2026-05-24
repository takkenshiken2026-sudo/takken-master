#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""用語記事をわかりやすい文体に整え、要点・覚え方・FAQを拡充する。"""

from __future__ import annotations

import re

from tools.glossary_enrich import norm, split_points

_FAQ_COUNT = 4


def split_points_semicolon(value: str) -> list[str]:
    return [p.strip() for p in re.split(r"[;；]", value or "") if p.strip()]


def to_plain_style(text: str) -> str:
    """専門文を読みやすいです・ます調に整える（内容は変えない）。"""
    t = norm(text)
    if not t:
        return ""
    t = t.replace("である。", "です。")
    t = t.replace("である、", "です。")
    t = t.replace("となる。", "になります。")
    t = t.replace("となる、", "になります。")
    t = t.replace("とされる。", "とされています。")
    t = t.replace("とされる、", "とされています。")
    t = t.replace("が問われる。", "が問われます。")
    t = t.replace("が問われる、", "が問われます。")
    t = t.replace("が必要。", "が必要です。")
    t = t.replace("できない。", "できません。")
    t = t.replace("できる。", "できます。")
    t = re.sub(r"\s+", " ", t)
    return t.strip()


def _first_sentence(text: str, *, max_len: int = 100) -> str:
    t = to_plain_style(text)
    if not t:
        return ""
    for sep in ("。", "．"):
        if sep in t:
            t = t.split(sep, 1)[0].strip() + "。"
            break
    if len(t) > max_len:
        t = t[: max_len - 1] + "…"
    return t


def _related_list(related_terms: str) -> list[str]:
    raw = (related_terms or "").replace("・", ";")
    return [p.strip() for p in re.split(r"[;；]", raw) if p.strip()]


def build_concrete_example(item: dict[str, str]) -> str:
    """まず押さえる要点用の具体例（1段落）。"""
    term = norm(item.get("term"))
    cat = norm(item.get("category"))
    pts = split_points_semicolon(norm(item.get("exam_points")))
    detail = norm(item.get("detail_body") or item.get("term_detail_body") or "")
    mistakes = norm(item.get("common_mistakes"))

    for sent in re.split(r"(?<=[。．])", detail):
        sent = sent.strip()
        if any(k in sent for k in ("たとえば", "例えば", "例として", "具体例")):
            return to_plain_style(sent)

    if pts:
        lead = pts[0].rstrip("。")
        if cat == "宅建業法":
            return (
                f"例として、{term}の場面では「{lead}」かどうかが問題になります。"
                "書面の交付や宅建士の関与があるかを、取引の段階ごとに分けて考えると整理しやすいです。"
            )
        if cat == "権利関係":
            return (
                f"例として、{term}が問われるときは「{lead}」という点が"
                "正しいかどうかを、条文番号とセットで確認する問題が多いです。"
            )
        if cat == "法令上の制限":
            return (
                f"例として、{term}では「{lead}」の数値や要件が"
                "区域・用途と組み合わさって出題されます。図や表でイメージすると覚えやすいです。"
            )
        if cat == "税・その他":
            return (
                f"例として、{term}では「{lead}」が誰に・いつ・いくらかかるかを"
                "計算問題や正誤問題の両方で問われることがあります。"
            )
        return (
            f"例として、試験では「{lead}」を軸に、"
            f"{term}の説明が正しいかどうかを選ぶ問題が出やすいです。"
        )

    if mistakes:
        return f"例として、次のような説明が誤りになりやすいです。{to_plain_style(mistakes[:120])}"

    return (
        f"例として、{term}は教科書の定義をそのまま暗記するより、"
        "関連する過去問で「どの選択肢が正しい説明か」を確認しながら覚えると定着しやすいです。"
    )


def _summary_core_sentence(item: dict[str, str]) -> str:
    """要点の核となる文（短い暗記用語句より定義文を優先）。"""
    definition = norm(item.get("definition") or "")
    short = norm(item.get("short_def") or "")
    if definition and len(definition) >= 28:
        return _first_sentence(definition, max_len=140)
    if short and len(short) >= 28 and "：" not in short[:20]:
        return _first_sentence(short, max_len=140)
    if definition:
        return _first_sentence(definition, max_len=140)
    return _first_sentence(short, max_len=140)


def build_summary_points(item: dict[str, str]) -> str:
    """まず押さえる要点（定義＋具体例）。"""
    core = _summary_core_sentence(item)
    if not core:
        core = f"{norm(item.get('term'))}の基本的な意味と、試験で問われるポイントを整理します。"
    example = build_concrete_example(item)
    return f"{core}\n\n【具体例】\n{example}"


def build_memory_guide(item: dict[str, str]) -> str:
    """覚え方・整理のコツ（やや詳しめ）。"""
    term = norm(item.get("term"))
    raw_tip = norm(item.get("memory_tip"))
    tip = raw_tip
    if "◆" in raw_tip:
        m = re.search(r"ひとことで覚える\s*(.+?)(?=\n*◆|\Z)", raw_tip, re.DOTALL)
        tip = m.group(1).strip() if m else raw_tip.split("◆")[0].strip()
    tip = re.sub(r"^(◆\s*ひとことで覚える\s*)+", "", tip).strip()
    tip = re.sub(r"ひとことで覚える\s*ひとことで覚える", "ひとことで覚える", tip)
    if tip:
        tip = to_plain_style(tip)
    pts = split_points_semicolon(norm(item.get("exam_points")))
    mistakes = to_plain_style(norm(item.get("common_mistakes")))
    related = _related_list(norm(item.get("related_terms")))
    legal = norm(item.get("legal_basis"))

    parts: list[str] = []
    if tip:
        parts.append(f"◆ ひとことで覚える\n{tip}")
    else:
        parts.append(f"◆ ひとことで覚える\n{term}は「定義→要件→試験で問われる違い」の順で整理します。")

    steps: list[str] = [
        f"「{term}」を一言で説明できるようにする（定義の最初の文を口に出す）。",
    ]
    if pts:
        steps.append(
            f"試験ポイント「{pts[0][:40]}」"
            + (f"と「{pts[1][:40]}」" if len(pts) > 1 else "")
            + "をメモに書き、○×で確認する。"
        )
    if related:
        steps.append(
            f"「{related[0]}」"
            + (f"・「{related[1]}」" if len(related) > 1 else "")
            + "との違いを2列の表にまとめる。"
        )
    if legal:
        steps.append(f"根拠（{legal}）を条文番号まで確認し、数字・期限があればセットで暗記する。")
    if mistakes:
        steps.append(f"よくある誤り（{mistakes[:60]}…）を赤ペンで1行メモする。")
    steps.append("関連する過去問を1問だけ解き、解説と条文の対応を読み返す。")

    parts.append(
        "◆ 整理の手順\n\n"
        + "\n\n".join(f"{i + 1}. {to_plain_style(s)}" for i, s in enumerate(steps[:5]))
    )
    return "\n\n".join(parts)


def build_faqs(item: dict[str, str]) -> list[tuple[str, str]]:
    """よくある質問 3〜4件（質問, 回答）。"""
    term = norm(item.get("term"))
    reading = norm(item.get("reading"))
    label = f"{term}（{reading}）" if reading else term
    core = _first_sentence(item.get("definition") or item.get("short_def") or "")
    detail = to_plain_style(
        (item.get("term_detail_body") or item.get("detail_body") or "").split("\n\n")[0]
    )
    pts = split_points_semicolon(norm(item.get("exam_points")))
    mistakes = to_plain_style(norm(item.get("common_mistakes")))
    related = _related_list(norm(item.get("related_terms")))
    legal = norm(item.get("legal_basis"))

    faqs: list[tuple[str, str]] = []

    ans1 = core.rstrip("。")
    if ans1.endswith("です") or ans1.endswith("ます"):
        lead_ans = f"{label}とは、{ans1}。"
    else:
        lead_ans = f"{label}とは、{ans1}です。"
    faqs.append(
        (
            f"{term}とは何ですか？",
            f"{lead_ans}くわしい内容はこのページの「定義と基本理解」で確認できます。",
        )
    )

    if pts:
        exam_ans = (
            f"主に次の点が問われます。"
            f"①{pts[0]}。"
            + (f"②{pts[1]}。" if len(pts) > 1 else "")
            + (f"③{pts[2]}。" if len(pts) > 2 else "")
            + " 過去問では、これらの説明が正しいかどうかを選ぶ形式が多いです。"
        )
    else:
        exam_ans = (
            f"{term}は定義の暗記だけでなく、関連制度との比較や条文の適用場面が問われます。"
            "本ページの「試験で押さえるポイント」と過去問演習で出題形式に慣れてください。"
        )
    faqs.append((f"{term}は宅建試験でどう出ますか？", exam_ans))

    if mistakes:
        faqs.append(
            (
                f"{term}で間違えやすい点はありますか？",
                f"{mistakes} 選択肢では、要件や効力を少し変えた説明が紛れ込むことがあるので、"
                "「いつ・誰に・どのような効果があるか」まで確認すると安全です。",
            )
        )
    else:
        faqs.append(
            (
                f"{term}を勉強するときの注意点は？",
                f"{term}は似た用語とセットで出ることがあります。"
                "定義を覚えたら、関連用語との違いを表に書いてから過去問に進むと理解が定着しやすいです。",
            )
        )

    if related:
        faqs.append(
            (
                f"「{related[0]}」との違いは何ですか？",
                f"{term}と「{related[0]}」は論点が近いため混同しやすいです。"
                f"{term}は{core.rstrip('。')}ことに対し、"
                f"関連用語は別の制度・要件として整理してください。"
                "比較表を作り、過去問で出題パターンを確認するのがおすすめです。",
            )
        )
    elif legal:
        faqs.append(
            (
                f"{term}の根拠法令はどこですか？",
                f"主な根拠は{legal}です。"
                f"条文番号と{term}の定義・要件をセットで確認し、数字や期限があれば一緒に暗記してください。",
            )
        )
    else:
        faqs.append(
            (
                f"{term}はいつ使う言葉ですか？",
                f"不動産取引や権利関係の問題文・解説で{term}が出たとき、"
                f"「{core.rstrip('。')}」という意味で使われているかを確認する場面で必要になります。",
            )
        )

    return faqs[:_FAQ_COUNT]


def polish_article_text(item: dict[str, str]) -> dict[str, str]:
    """本文フィールドをわかりやすい文体に整える。"""
    out = dict(item)
    for key in (
        "definition",
        "short_def",
        "article_lead",
        "explanation",
        "common_mistakes",
        "term_detail_body",
        "detail_body",
    ):
        if norm(out.get(key)):
            out[key] = to_plain_style(out[key])
    return out


def apply_readable_fields(row: dict[str, str]) -> dict[str, str]:
    """1用語分の読みやすさ・拡充フィールドを生成。"""
    item = polish_article_text(row)
    sp = norm(row.get("summary_points"))
    if sp and "【具体例】" in sp and "\n\n【具体例】" in sp:
        item["summary_points"] = sp
    else:
        item["summary_points"] = build_summary_points(item)
    item["memory_tip"] = build_memory_guide(item)

    faqs = build_faqs(item)
    for i, (q, a) in enumerate(faqs, start=1):
        item[f"faq_{i}_question"] = q
        item[f"faq_{i}_answer"] = to_plain_style(a)
    for i in range(len(faqs) + 1, _FAQ_COUNT + 1):
        item[f"faq_{i}_question"] = ""
        item[f"faq_{i}_answer"] = ""

    return item
