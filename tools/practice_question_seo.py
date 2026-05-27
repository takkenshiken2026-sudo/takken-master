#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""実践演習ページの SEO 拡張。"""

from __future__ import annotations

import html
import json
import re
from pathlib import Path

from tools.html_footer import analytics_snippet, footer_href
from tools.orig_units import FIELD_LABELS
from tools.past_question_seo import (
    _collection_json_ld,
    _hub_meta_tags,
    related_terms_html,
)
from tools.seo_common import (
    UPDATED_LABEL,
    build_term_match_index,
    extract_theme_label,
    field_id_for_category,
    load_glossary_items_from_js,
    match_terms_in_text,
    trust_table_html,
)


def enrich_practice_pages(pages: list[dict]) -> None:
    term_index = build_term_match_index(load_glossary_items_from_js())
    by_unit: dict[str, list[dict]] = {}
    by_level: dict[int, list[dict]] = {}
    for p in pages:
        by_unit.setdefault(p["unit"], []).append(p)
        by_level.setdefault(p["level"], []).append(p)
    for unit_pages in by_unit.values():
        unit_pages.sort(key=lambda x: x["question_id"])
        for i, p in enumerate(unit_pages):
            p["prev"] = unit_pages[i - 1] if i > 0 else None
            p["next"] = unit_pages[i + 1] if i < len(unit_pages) - 1 else None
    for level_pages in by_level.values():
        level_pages.sort(key=lambda x: x["question_id"])
    for p in pages:
        theme = extract_theme_label(p.get("stem_plain") or "")
        p["theme"] = theme
        p["field_id"] = p.get("field") or field_id_for_category(p.get("category") or "")
        hay = (p.get("stem_plain") or "") + " " + (p.get("exp") or "")
        p["related_terms"] = match_terms_in_text(hay, term_index, max_hits=4)


def page_title_mid(page: dict) -> str:
    theme = page.get("theme") or ""
    base = f"実践演習・{page['category']}（{page['unit_label']}）"
    if theme:
        return f"{base}｜{theme}"
    return base


def page_meta_description(page: dict, limit: int = 155) -> str:
    theme = page.get("theme") or ""
    stem = (page.get("stem_plain") or "").strip()
    prefix = f"実践演習・レベル{page['level']}・{page['unit_label']}"
    if theme:
        prefix += f"「{theme}」"
    body = stem or page.get("category") or ""
    one = re.sub(
        r"\s+",
        " ",
        f"{prefix}。{body} 正答・解説・関連用語リンク付き。宅建マスターで無料演習。",
    ).strip()
    if len(one) <= limit:
        return one
    return one[: limit - 1] + "…"


def practice_hub_links_html(page: dict, rel_path: Path) -> str:
    root_up = "/".join([".."] * len(rel_path.parent.parts))
    fid = page.get("field_id")
    links = [
        f'<a href="{html.escape(root_up)}/q/index.html">問題一覧</a>',
        f'<a href="{html.escape(root_up)}/q/orig/index.html">実践演習一覧</a>',
        f'<a href="../index.html">{html.escape(page["unit_label"])}まとめ</a>',
    ]
    if fid:
        links.append(
            f'<a href="{html.escape(root_up)}/q/orig/field/{html.escape(fid)}/index.html">'
            f'{html.escape(page["category"])}</a>'
        )
    links.append(f'<a href="{html.escape(root_up)}/terms/index.html">用語解説</a>')
    return '<p class="q-hub-links">' + " · ".join(links) + "</p>"


def nav_adjacent_html(page: dict, rel_path: Path) -> str:
    parts = []
    prev_p, next_p = page.get("prev"), page.get("next")
    if prev_p:
        parts.append(
            f'<a class="q-nav-prev" href="../id{prev_p["question_id"]}/index.html">← 前の問題</a>'
        )
    parts.append(
        f'<a class="q-nav-year" href="../unit/{html.escape(page["unit"])}/index.html">'
        f'{html.escape(page["unit_label"])}一覧</a>'
    )
    if next_p:
        parts.append(
            f'<a class="q-nav-next" href="../id{next_p["question_id"]}/index.html">次の問題 →</a>'
        )
    fid = page.get("field_id")
    if fid:
        root_up = "/".join([".."] * len(rel_path.parent.parts))
        parts.append(
            f'<a class="q-nav-field" href="{html.escape(root_up)}/q/orig/field/{html.escape(fid)}/index.html">'
            f'{html.escape(page["category"])}</a>'
        )
    return '<nav class="q-adj-nav" aria-label="前後の問題">' + " · ".join(parts) + "</nav>"


def question_json_ld(page: dict, canonical: str, title: str, desc: str) -> dict:
    site_root = canonical.rsplit("/q/", 1)[0] + "/"
    graph: list[dict] = [
        {
            "@type": "WebPage",
            "@id": canonical + "#webpage",
            "url": canonical,
            "name": title,
            "description": desc,
            "inLanguage": "ja-JP",
            "dateModified": UPDATED_LABEL,
        },
        {
            "@type": "BreadcrumbList",
            "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": "トップ", "item": site_root},
                {
                    "@type": "ListItem",
                    "position": 2,
                    "name": "実践演習一覧",
                    "item": site_root + "q/orig/index.html",
                },
                {
                    "@type": "ListItem",
                    "position": 3,
                    "name": page["unit_label"],
                    "item": site_root
                    + f"q/orig/unit/{page['unit']}/index.html",
                },
                {"@type": "ListItem", "position": 4, "name": page_title_mid(page), "item": canonical},
            ],
        },
        {
            "@type": "Quiz",
            "name": page_title_mid(page),
            "about": {"@type": "Thing", "name": page.get("category")},
            "educationalLevel": "Professional",
            "inLanguage": "ja-JP",
        },
    ]
    if page.get("correct"):
        graph.append(
            {
                "@type": "Question",
                "name": page.get("stem_plain") or page_title_mid(page),
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": f"正答は選択肢（{page['correct']}）です。",
                },
            }
        )
    return {"@context": "https://schema.org", "@graph": graph}


def build_orig_root_hub_html(pages: list[dict], base_url: str, brand: str, exam: str) -> str:
    base = base_url.rstrip("/")
    rel_path = "q/orig/index.html"
    canonical = f"{base}/{rel_path}"
    title = f"実践演習一覧｜{brand}（{exam}）"
    desc = (
        f"{exam}の実践演習{len(pages)}問を単元別・分野別・レベル別に掲載。"
        "解説付きで模試対策の演習ができます。"
    )
    field_links = []
    for fid, label in FIELD_LABELS.items():
        n = sum(1 for p in pages if p.get("field") == fid)
        if not n:
            continue
        field_links.append(
            f'<li><a href="field/{fid}/index.html">{html.escape(label)}</a>（{n}問）</li>'
        )
    level_links = []
    for lv in sorted({p["level"] for p in pages}):
        n = sum(1 for p in pages if p["level"] == lv)
        level_links.append(f'<li><a href="level/{lv}/index.html">レベル{lv}</a>（{n}問）</li>')
    json_ld = _collection_json_ld(
        canonical=canonical,
        title=title,
        desc=desc,
        items=[(page_title_mid(p), f"{base}/{p['rel_path']}") for p in pages[:50]],
        site_url=base,
    )
    trust = trust_table_html(anchor_id="trust", compact=True)
    return f"""<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(desc)}">
{_hub_meta_tags(title, desc, canonical)}
<link rel="stylesheet" href="../../site-pages.css">
{json_ld}
</head>
<body class="q-static-body">
<header class="q-static-header">
  <p class="q-static-brand"><a href="../../index.html">{html.escape(brand)}</a>（{html.escape(exam)}）</p>
  <nav aria-label="パンくず"><ol class="q-breadcrumb">
    <li><a href="../../index.html">トップ</a></li>
    <li><a href="../index.html">問題一覧</a></li>
    <li aria-current="page">実践演習</li>
  </ol></nav>
</header>
<main class="q-static-main">
  <h1 class="q-h1">実践演習一覧</h1>
  <p class="q-meta">全 {len(pages)} 問 · 解説付き</p>
  <p class="glos-static-intro">単元別・分野別に問題と解説へ進めます。<a href="../../index.html#orig">アプリで演習</a>も利用できます。</p>
  {trust}
  <h2 class="q-h2">分野別</h2>
  <ul>{''.join(field_links)}</ul>
  <h2 class="q-h2">レベル別</h2>
  <ul>{''.join(level_links)}</ul>
  <p class="q-hub-links"><a href="../index.html">過去問一覧</a> · <a href="../mock/index.html">オリジナル模試</a></p>
</main>
{analytics_snippet(Path(rel_path))}
</body>
</html>"""


def practice_q_list_table_html(items: list[dict], href_for) -> str:
    """実践演習用の問題一覧表。"""
    rows: list[str] = []
    for p in sorted(items, key=lambda x: (x.get("unit_label", ""), x["question_id"])):
        theme = (p.get("theme") or p.get("unit_label") or "").strip()
        href = html.escape(href_for(p))
        qid = p["question_id"]
        rows.append(
            "<tr>"
            f'<td><a href="{href}">{qid}</a></td>'
            f"<td>{html.escape(p.get('unit_label') or '')}</td>"
            f'<td>L{p["level"]}</td>'
            f'<td><a href="{href}">{html.escape(theme)}</a></td>'
            "</tr>"
        )
    if not rows:
        return ""
    return (
        '<div class="q-year-table-wrap"><table class="q-year-table">'
        "<thead><tr><th scope=\"col\">ID</th><th scope=\"col\">単元</th>"
        "<th scope=\"col\">Lv</th><th scope=\"col\">テーマ</th></tr></thead>"
        f"<tbody>{''.join(rows)}</tbody></table></div>"
    )


def build_field_hub_html(field_id: str, pages: list[dict], base_url: str, brand: str, exam: str) -> str:
    subset = [p for p in pages if p.get("field") == field_id]
    if not subset:
        return ""
    label = FIELD_LABELS.get(field_id, field_id)
    base = base_url.rstrip("/")
    rel_path = f"q/orig/field/{field_id}/index.html"
    canonical = f"{base}/{rel_path}"
    title = f"実践演習・{label}｜{brand}（{exam}）"
    desc = (
        f"実践演習の{label}（{len(subset)}問）。単元別に問題ID・解説・"
        "関連用語リンク付きページへ進めます。"
    )
    by_unit: dict[str, list[dict]] = {}
    for p in subset:
        by_unit.setdefault(p["unit"], []).append(p)

    unit_sections = []
    for unit_id in sorted(by_unit.keys(), key=lambda u: by_unit[u][0]["unit_label"]):
        unit_pages = sorted(by_unit[unit_id], key=lambda x: x["question_id"])
        ulabel = unit_pages[0]["unit_label"]
        table = practice_q_list_table_html(
            unit_pages,
            lambda p: f"../../id{p['question_id']}/index.html",
        )
        unit_sections.append(
            f'<section class="glos-cat-section"><h2 class="glos-cat-heading">'
            f'<a href="../../unit/{html.escape(unit_id)}/index.html">{html.escape(ulabel)}</a>'
            f"（{len(unit_pages)}問）</h2>{table}</section>"
        )

    list_items = [
        (f"#{p['question_id']} {p['unit_label']}", f"{base}/{p['rel_path']}")
        for p in sorted(subset, key=lambda x: x["question_id"])[:50]
    ]
    json_ld = _collection_json_ld(
        canonical=canonical, title=title, desc=desc, items=list_items, site_url=base
    )
    trust = trust_table_html(anchor_id="trust", compact=True)
    return f"""<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(desc)}">
{_hub_meta_tags(title, desc, canonical)}
<link rel="stylesheet" href="../../../../site-pages.css">
{json_ld}
</head>
<body class="q-static-body">
<header class="q-static-header">
  <p class="q-static-brand"><a href="../../../../index.html">{html.escape(brand)}</a>（{html.escape(exam)}）</p>
  <nav aria-label="パンくず"><ol class="q-breadcrumb">
    <li><a href="../../../../index.html">トップ</a></li>
    <li><a href="../../../index.html">問題一覧</a></li>
    <li><a href="../../index.html">実践演習一覧</a></li>
    <li aria-current="page">{html.escape(label)}</li>
  </ol></nav>
</header>
<main class="q-static-main">
  <h1 class="q-h1">実践演習・{html.escape(label)}</h1>
  <p class="q-meta">掲載 {len(subset)} 問 · {len(by_unit)} 単元</p>
  <p class="glos-static-intro">
    {html.escape(exam)}の<strong>{html.escape(label)}</strong>分野の実践演習を単元別にまとめています。
    各問ページでは正答・解説・<a href="../../../../terms/index.html">用語解説</a>へのリンクがあります。
  </p>
  {trust}
  {"".join(unit_sections)}
  <p class="q-hub-links"><a href="../../index.html">実践演習一覧（検索）</a> · <a href="../../../index.html">過去問一覧</a></p>
  <p class="q-app-link"><a href="../../../../index.html#orig">アプリで実践演習</a></p>
</main>
{analytics_snippet(Path(rel_path))}
</body>
</html>"""


def build_unit_hub_html(unit_id: str, pages: list[dict], base_url: str, brand: str, exam: str) -> str:
    subset = [p for p in pages if p["unit"] == unit_id]
    if not subset:
        return ""
    subset.sort(key=lambda x: x["question_id"])
    ulabel = subset[0]["unit_label"]
    cat = subset[0]["category"]
    fid = subset[0].get("field", "")
    base = base_url.rstrip("/")
    rel_path = f"q/orig/unit/{unit_id}/index.html"
    canonical = f"{base}/{rel_path}"
    title = f"実践演習・{ulabel}｜{brand}（{exam}）"
    desc = f"実践演習「{ulabel}」{len(subset)}問。正答・解説付き。"
    lis = "".join(
        f'<li><a href="../../id{p["question_id"]}/index.html">'
        f'問題 {p["question_id"]}（レベル{p["level"]}）</a></li>'
        for p in subset
    )
    json_ld = _collection_json_ld(
        canonical=canonical,
        title=title,
        desc=desc,
        items=[(page_title_mid(p), f"{base}/{p['rel_path']}") for p in subset[:50]],
        site_url=base,
    )
    return f"""<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(desc)}">
{_hub_meta_tags(title, desc, canonical)}
<link rel="stylesheet" href="../../../../site-pages.css">
{json_ld}
</head>
<body class="q-static-body">
<header class="q-static-header">
  <p class="q-static-brand"><a href="../../../../index.html">{html.escape(brand)}</a></p>
  <nav aria-label="パンくず"><ol class="q-breadcrumb">
    <li><a href="../../../../index.html">トップ</a></li>
    <li><a href="../../../index.html">問題一覧</a></li>
    <li><a href="../../index.html">実践演習一覧</a></li>
    <li aria-current="page">{html.escape(ulabel)}</li>
  </ol></nav>
</header>
<main class="q-static-main">
  <h1 class="q-h1">実践演習・{html.escape(ulabel)}</h1>
  <p class="q-meta">{html.escape(cat)} · {len(subset)} 問</p>
  <ol>{lis}</ol>
  <p class="q-hub-links"><a href="../../index.html">実践演習トップ</a> · <a href="../../field/{html.escape(fid)}/index.html">{html.escape(cat)}</a></p>
</main>
{analytics_snippet(Path(rel_path))}
</body>
</html>"""


def build_level_hub_html(level: int, pages: list[dict], base_url: str, brand: str, exam: str) -> str:
    subset = [p for p in pages if p["level"] == level]
    if not subset:
        return ""
    base = base_url.rstrip("/")
    rel_path = f"q/orig/level/{level}/index.html"
    canonical = f"{base}/{rel_path}"
    title = f"実践演習・レベル{level}｜{brand}（{exam}）"
    desc = f"実践演習レベル{level}（{len(subset)}問）。難易度別の問題一覧。"
    table = practice_q_list_table_html(
        subset,
        lambda p: f"../../id{p['question_id']}/index.html",
    )
    json_ld = _collection_json_ld(
        canonical=canonical,
        title=title,
        desc=desc,
        items=[(page_title_mid(p), f"{base}/{p['rel_path']}") for p in subset[:30]],
        site_url=base,
    )
    return f"""<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(desc)}">
{_hub_meta_tags(title, desc, canonical)}
<link rel="stylesheet" href="../../../../site-pages.css">
{json_ld}
</head>
<body class="q-static-body">
<header class="q-static-header">
  <p class="q-static-brand"><a href="../../../../index.html">{html.escape(brand)}</a></p>
  <nav aria-label="パンくず"><ol class="q-breadcrumb">
    <li><a href="../../../../index.html">トップ</a></li>
    <li><a href="../../../index.html">問題一覧</a></li>
    <li><a href="../../index.html">実践演習</a></li>
    <li aria-current="page">レベル{level}</li>
  </ol></nav>
</header>
<main class="q-static-main">
  <h1 class="q-h1">実践演習・レベル{level}</h1>
  <p class="q-meta">{len(subset)} 問</p>
  {table}
  <p class="q-hub-links"><a href="../../index.html">実践演習一覧（検索）</a></p>
</main>
{analytics_snippet(Path(rel_path))}
</body>
</html>"""
