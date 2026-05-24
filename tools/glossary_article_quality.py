#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""用語詳細記事の読者価値・SEO（独自性重視。定型パディングは使わない）。"""

from __future__ import annotations

import re

from tools.glossary_enrich import (
    clean_exam_points,
    norm,
    sanitize_legacy_text,
    split_points,
)
from tools.glossary_past_insights import build_past_insights
from tools.site_config import exam_name

_GENERIC_SNIPPETS = (
    "宅建業法上の義務・書面・監督処分との関係で頻出します",
    "宅建業法では書面交付の時期、記載事項、監督処分の段階など",
    "手続の順序と義務者（業者・宅建士）の区別が問われやすいです",
    "権利関係では「誰に・どのような効果が及ぶか」",
    "効力の発生・消滅のタイミングまでセットで押さえてください",
    "権利の得喪・効力・第三者対抗要件が問われやすい用語です",
    "区域・用途・数値基準とセットで出題されることが多い用語です",
    "課税主体・期限・税率・計算手順と合わせて確認してください",
    "最新の試験要綱・公式情報と照らして暗記する用語です",
    "学習では",
    "との要件・効力の違いを表にまとめると",
    "を選択肢で使い分けやすくなります",
    "関連する",
    "との比較も有効です",
    "理解を深めるには、",
    "との関係を条文・要件表で並べて整理するのが有効です",
    "条文・要件・よくある誤りを整理し、過去問で問われ方に慣れるための解説です",
    "定義・法令の根拠・過去問で問われやすいポイントを整理します",
)

_CATEGORY_MISTAKE_MARKERS = (
    "類似制度（期間・要件・効力）",
    "35条・37条・8条・14条の交付時期",
    "35条・37条・8条・14条の表で整理",
    "35条・37条・8条・14条を表で整理",
    "区域・用途・数値（面積・率・幅員）",
    "課税主体・申告期限・税率",
    "出題比率・合格点など暗記数字",
    "出題比率や学習時間の目安",
    "成立要件・効力・期間の取り違え。",
    "の適用場面と数値・期限の混同。",
    "の有無や表現の違いを誤って判断する。",
)

_LIMB_MARKERS = (
    "のいずれかが正誤の分かれ目",
    "肢では「肢では",
    "正誤の分かれ目になりやすいのは",
)


def strip_generic_padding(text: str) -> str:
    """分野共通のテンプレ文を除去。"""
    t = sanitize_legacy_text(text)
    if not t:
        return ""
    for snippet in _GENERIC_SNIPPETS:
        t = t.replace(snippet, "")
    t = re.sub(r"\s+", " ", t).strip()
    t = re.sub(r"[。．]{2,}", "。", t)
    t = re.sub(r"\n{3,}", "\n\n", t)
    return t.strip()


def is_boilerplate_mistakes(text: str) -> bool:
    t = norm(text)
    if not t:
        return True
    return any(m in t for m in _CATEGORY_MISTAKE_MARKERS)


def is_boilerplate_explanation(text: str) -> bool:
    t = sanitize_legacy_text(text)
    if not t:
        return True
    if any(m in t for m in _LIMB_MARKERS):
        return True
    if any(g in t for g in _GENERIC_SNIPPETS[:6]):
        return True
    return False


def is_substantive_field(text: str, *, min_len: int = 36) -> bool:
    t = strip_generic_padding(text)
    return len(t) >= min_len and not is_boilerplate_explanation(t)


def example_needs_refresh(row: dict[str, str]) -> bool:
    q = norm(row.get("example_question"))
    a = norm(row.get("example_answer"))
    if not q or not a:
        return True
    if "【学習確認】" in q:
        return True
    if "押さえるべき説明として最も適切" in q or (
        "に関する説明として適切" in q and "年 第" not in q
    ):
        return True
    if any(m in a for m in _LIMB_MARKERS):
        return True
    if a.startswith("要点は「") and "過去問" not in a:
        return True
    return False


def build_article_title(term: str, category: str) -> str:
    term = norm(term)
    cat = norm(category)
    if cat and cat not in ("その他", "試験対策"):
        return f"{term}とは？意味・根拠・{cat}の試験ポイント"
    return f"{term}とは？意味・根拠・宅建試験のポイント"


def _core_definition(item: dict[str, str]) -> str:
    for key in ("definition", "short_def"):
        t = strip_generic_padding(item.get(key) or "")
        if t:
            return t.split("\n\n")[0].strip()
    return ""


def build_article_lead(item: dict[str, str], insights: dict[str, object] | None = None) -> str:
    term = norm(item.get("term"))
    core = _core_definition(item)
    if not core:
        core = norm(item.get("term"))
    core = core.rstrip("。")
    ins = insights or build_past_insights(item)

    contexts = ins.get("contexts") or []
    refs = ins.get("past_refs") or []
    if contexts:
        ctx = str(contexts[0]).rstrip("。")
        return f"「{term}」は{core}。過去問では「{ctx}」のように出題文脈と結びつけて問われます。"
    if refs:
        y, n = refs[0]
        return (
            f"「{term}」は{core}。"
            f"{exam_name()}の過去問（{y}年 第{n}問など）で論点にされる用語として整理しています。"
        )
    return f"「{term}」は{core}。定義と、試験で実際に問われる条件の区別を中心に解説します。"


def expand_definition(item: dict[str, str]) -> str:
    """定義は事実ベースのみ補足。分野テンプレは付けない。"""
    term = norm(item.get("term"))
    core = strip_generic_padding(
        sanitize_legacy_text(item.get("definition"))
        or norm(item.get("short_def"))
    )
    if not core:
        return ""
    if not core.endswith("。"):
        core = core + "。"
    legal = norm(item.get("legal_basis"))
    if legal and legal not in core and len(core) < 90:
        return f"{core}\n\n主な根拠は{legal}です。"
    return core


def derive_common_mistakes(
    item: dict[str, str], insights: dict[str, object] | None = None
) -> str:
    existing = strip_generic_padding(item.get("common_mistakes") or "")
    if existing and not is_boilerplate_mistakes(existing):
        return existing

    ins = insights or build_past_insights(item)
    from_past = ins.get("mistakes") or []
    if from_past:
        return " ".join(str(m) for m in from_past[:2])

    points = split_points(clean_exam_points(norm(item.get("exam_points"))))
    if len(points) >= 2:
        return f"「{points[0]}」と「{points[1]}」の関係・要件を取り違えないこと。"

    term = norm(item.get("term"))
    related = split_points(norm(item.get("related_terms")).replace("・", ";"))
    if related:
        return f"「{related[0]}」など近い制度と{term}の要件・効力を取り違えないこと。"

    return ""


def build_natural_explanation(
    item: dict[str, str], insights: dict[str, object] | None = None
) -> str:
    custom = strip_generic_padding(item.get("explanation") or "")
    definition = _core_definition(item)
    ins = insights or build_past_insights(item)
    term = norm(item.get("term"))

    chunks: list[str] = []
    if is_substantive_field(custom) and custom != definition:
        chunks.append(custom)

    for clause in ins.get("exam_points") or []:
        c = str(clause).strip()
        if c and c not in " ".join(chunks) and c.rstrip("。") != definition.rstrip("。"):
            chunks.append(c if c.endswith("。") else c + "。")
        if len(chunks) >= 3:
            break

    if chunks:
        return "\n\n".join(chunks[:3])

    points = split_points(clean_exam_points(norm(item.get("exam_points"))))
    if points:
        return "。".join(points[:3]) + ("。" if not points[-1].endswith("。") else "")

    return f"{term}は定義の暗記だけでなく、関連制度との比較で理解すると得点しやすくなります。"


def build_learning_example(
    item: dict[str, str], insights: dict[str, object] | None = None
) -> tuple[str, str]:
    from tools.glossary_past_insights import gather_past_hits
    from tools.glossary_past_questions import example_from_past_hit

    term = norm(item.get("term"))
    ins = insights or build_past_insights(item)
    hits = gather_past_hits(
        term,
        norm(item.get("related_terms")),
        norm(item.get("legal_basis")),
        limit=1,
    )
    if hits:
        return example_from_past_hit(hits[0], term)

    points = split_points(clean_exam_points(norm(item.get("exam_points"))))
    if not points and ins.get("exam_points"):
        points = [str(p) for p in ins["exam_points"][:2]]
    lead = points[0] if points else _core_definition(item)
    q = f"次のうち、{term}に関する説明として適切なものはどれか。（{norm(item.get('category'))}）"
    a = (
        f"本ページの定義・試験ポイントを確認し、"
        f"特に「{lead.rstrip('。')}」を軸に関連条文・用語と照合してください。"
    )
    return q, a


def merge_exam_points(item: dict[str, str], insights: dict[str, object]) -> str:
    existing = split_points(clean_exam_points(norm(item.get("exam_points"))))
    merged: list[str] = []
    seen: set[str] = set()
    for p in existing + [str(x) for x in (insights.get("exam_points") or [])]:
        p = strip_generic_padding(p).rstrip("。")
        if len(p) < 6 or p in seen:
            continue
        seen.add(p)
        merged.append(p)
    return ";".join(merged[:6])


def build_detail_from_insights(
    item: dict[str, str], insights: dict[str, object]
) -> str:
    """定義と重複しない、過去問・手書きに基づく補足段落。"""
    term = norm(item.get("term"))
    custom = strip_generic_padding(item.get("detail_body") or "")
    parts: list[str] = []
    if custom and len(custom) >= 72:
        parts.append(custom)

    contexts = insights.get("contexts") or []
    refs = insights.get("past_refs") or []
    if contexts and not parts:
        parts.append(f"出題例では、{contexts[0]}")
    elif refs and not parts:
        y, n = refs[0]
        parts.append(f"{y}年問{n}を含む過去問で、{term}に関する論点が問われています。")

    legal = norm(item.get("legal_basis"))
    if legal and legal not in " ".join(parts):
        parts.append(f"根拠法令は{legal}です。")

    return "\n\n".join(parts)


def upgrade_glossary_fields(item: dict[str, str], *, preserve_deep: bool = False) -> dict[str, str]:
    out = dict(item)
    term = norm(out.get("term"))
    if not term:
        return out

    for key in (
        "definition",
        "short_def",
        "explanation",
        "term_detail_body",
        "detail_body",
        "common_mistakes",
        "article_lead",
    ):
        if out.get(key):
            out[key] = strip_generic_padding(out[key])

    insights = build_past_insights(out)

    out["definition"] = expand_definition(out)
    out["short_def"] = _first_sentence(out["definition"]) or norm(out.get("short_def"))

    out["exam_points"] = merge_exam_points(out, insights)
    if not split_points(out["exam_points"]):
        from tools.glossary_enrich import derive_exam_points

        out["exam_points"] = clean_exam_points(derive_exam_points(out))

    mistakes = derive_common_mistakes(out, insights)
    if mistakes:
        out["common_mistakes"] = mistakes

    if not is_substantive_field(out.get("explanation") or ""):
        out["explanation"] = build_natural_explanation(out, insights)

    out["article_title"] = build_article_title(term, norm(out.get("category")))
    out["article_lead"] = build_article_lead(out, insights)

    if preserve_deep and len(norm(out.get("detail_body"))) >= 80:
        detail_extra = strip_generic_padding(out["detail_body"])
    else:
        detail_extra = build_detail_from_insights(out, insights)
        if not detail_extra:
            from tools.glossary_enrich import build_detail_body

            detail_extra = strip_generic_padding(build_detail_body(out))

    definition = norm(out["definition"])
    detail_extra = strip_generic_padding(detail_extra)
    if detail_extra and detail_extra != definition:
        out["term_detail_body"] = f"{definition}\n\n{detail_extra}"
    else:
        out["term_detail_body"] = definition

    memory = norm(out.get("memory_tip"))
    if not memory or ("を起点に、" in memory and len(memory) < 48):
        pts = split_points(out["exam_points"])
        mis = derive_common_mistakes(out, insights)
        if mis:
            out["memory_tip"] = mis[:80] + ("…" if len(mis) > 80 else "")
        elif pts:
            out["memory_tip"] = f"{pts[0][:32]}と{related_display(out)}を並べて整理する。"
        else:
            out["memory_tip"] = ""

    return out


def related_display(item: dict[str, str]) -> str:
    rel = split_points(norm(item.get("related_terms")).replace("・", ";"))
    return rel[0] if rel else "関連用語"


def _first_sentence(text: str, *, max_len: int = 120) -> str:
    t = strip_generic_padding(text)
    if not t:
        return ""
    for sep in ("。", "．", "\n"):
        if sep in t:
            t = t.split(sep, 1)[0].strip() + "。"
            break
    if len(t) > max_len:
        t = t[: max_len - 1] + "…"
    return t


def derive_exam_points_fallback(item: dict[str, str]) -> str:
    from tools.glossary_enrich import derive_exam_points

    return derive_exam_points(item)
