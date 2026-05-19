#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""過去問ページの SEO 拡張（年度ハブ・分野ハブ・相互リンク）。"""

from __future__ import annotations

import html
import json
import re
from pathlib import Path

from tools.seo_common import (
    AUTHOR_LABEL,
    FIELD_HUB_META,
    UPDATED_LABEL,
    build_term_match_index,
    extract_theme_label,
    field_id_for_category,
    load_glossary_items_from_js,
    match_terms_in_text,
    primary_source_links_html,
    trust_table_html,
)


def enrich_pages(pages: list[dict]) -> None:
    """page dict に theme, field_id, related_terms, prev, next を付与。"""
    term_index = build_term_match_index(load_glossary_items_from_js())
    by_year: dict[int, list[dict]] = {}
    for p in pages:
        by_year.setdefault(p["year"], []).append(p)
    for y in by_year:
        by_year[y].sort(key=lambda x: x["qno"])
        for i, p in enumerate(by_year[y]):
            p["prev"] = by_year[y][i - 1] if i > 0 else None
            p["next"] = by_year[y][i + 1] if i < len(by_year[y]) - 1 else None
    for p in pages:
        theme = extract_theme_label(p.get("stem_plain") or "")
        p["theme"] = theme
        p["field_id"] = field_id_for_category(p.get("category") or "")
        hay = (p.get("stem_plain") or "") + " " + (p.get("exp") or "")
        p["related_terms"] = match_terms_in_text(hay, term_index, max_hits=4)


def page_title_mid(page: dict) -> str:
    theme = page.get("theme") or ""
    base = f"{page['wareki']} 第{page['qno']}問・{page['category']}"
    if theme:
        return f"{base}（{theme}）"
    return base


def page_meta_description(page: dict, limit: int = 155) -> str:
    theme = page.get("theme") or ""
    stem = (page.get("stem_plain") or "").strip()
    prefix = f"{page['wareki']}第{page['qno']}問"
    if theme:
        prefix += f"「{theme}」"
    body = stem or page.get("category") or ""
    one = re.sub(r"\s+", " ", f"{prefix}。{body} 正答・解説・関連用語リンク付き。宅建マスターで無料演習。").strip()
    if len(one) <= limit:
        return one
    return one[: limit - 1] + "…"


def related_terms_html(page: dict, rel_path: Path) -> str:
    slugs = page.get("related_terms") or []
    if not slugs:
        return ""
    root_up = "/".join([".."] * len(rel_path.parent.parts))
    items = load_glossary_items_from_js()
    by_slug = {
        (i.get("articleSlug") or str(i.get("id", "")).replace("_", "-")).strip(): i for i in items
    }
    links = []
    for slug in slugs:
        item = by_slug.get(slug)
        label = str(item.get("term") if item else slug)
        links.append(
            f'<li><a href="{html.escape(root_up)}/terms/{html.escape(slug)}/">{html.escape(label)}</a></li>'
        )
    return (
        '<section class="q-block q-related" aria-labelledby="q-terms-h">'
        '<h2 id="q-terms-h" class="q-h2">関連する用語解説</h2>'
        f'<ul class="q-related-list">{"".join(links)}</ul></section>'
    )


def nav_adjacent_html(page: dict, rel_path: Path) -> str:
    parts = []
    root_up = "/".join([".."] * len(rel_path.parent.parts))
    prev_p, next_p = page.get("prev"), page.get("next")
    if prev_p:
        parts.append(
            f'<a class="q-nav-prev" href="../q{prev_p["qno"]:02d}/index.html">← 第{prev_p["qno"]}問</a>'
        )
    parts.append(f'<a class="q-nav-year" href="../index.html">{html.escape(page["wareki"])}一覧</a>')
    if next_p:
        parts.append(
            f'<a class="q-nav-next" href="../q{next_p["qno"]:02d}/index.html">第{next_p["qno"]}問 →</a>'
        )
    fid = page.get("field_id")
    if fid:
        parts.append(
            f'<a class="q-nav-field" href="{html.escape(root_up)}/q/field/{html.escape(fid)}/index.html">'
            f'{html.escape(page["category"])}の過去問</a>'
        )
    return '<nav class="q-adj-nav" aria-label="前後の問題">' + " · ".join(parts) + "</nav>"


def hub_links_html(page: dict, rel_path: Path) -> str:
    root_up = "/".join([".."] * len(rel_path.parent.parts))
    fid = page.get("field_id")
    links = [
        f'<a href="{html.escape(root_up)}/q/index.html">過去問一覧</a>',
        f'<a href="../index.html">{html.escape(page["wareki"])}まとめ</a>',
    ]
    if fid:
        links.append(
            f'<a href="{html.escape(root_up)}/q/field/{html.escape(fid)}/index.html">'
            f'{html.escape(page["category"])}ハブ</a>'
        )
    links.append(f'<a href="{html.escape(root_up)}/terms/index.html">用語解説</a>')
    links.append(f'<a href="{html.escape(root_up)}/articles/index.html">試験ガイド</a>')
    return '<p class="q-hub-links">' + " · ".join(links) + "</p>"


def question_json_ld(page: dict, canonical: str, title: str, desc: str) -> dict:
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
                {"@type": "ListItem", "position": 1, "name": "トップ", "item": canonical.rsplit("/q/", 1)[0] + "/"},
                {"@type": "ListItem", "position": 2, "name": "過去問一覧", "item": canonical.rsplit("/q/past/", 1)[0] + "/q/index.html"},
                {
                    "@type": "ListItem",
                    "position": 3,
                    "name": page["wareki"],
                    "item": canonical.rsplit(f"/q{page['qno']:02d}/", 1)[0] + "/",
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
    if page.get("correct") and not page.get("is_invalidated"):
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


def build_year_hub_html(year: int, pages: list[dict], base_url: str, brand: str, exam: str) -> str:
    year_pages = sorted([p for p in pages if p["year"] == year], key=lambda x: x["qno"])
    if not year_pages:
        return ""
    wareki = year_pages[0]["wareki"]
    rel_path = f"q/past/y{year}/index.html"
    canonical = f"{base_url.rstrip('/')}/{rel_path}"
    title = f"{wareki} 宅建過去問まとめ（全{len(year_pages)}問）｜{brand}（{exam}）"
    desc = f"{wareki}（{year}年）の宅建試験過去問を第1問から掲載。分野別のリンク・解説・関連用語付きで無料演習できます。"

    by_field: dict[str, list[dict]] = {}
    for p in year_pages:
        by_field.setdefault(p["category"], []).append(p)

    field_sections = []
    for cat in sorted(by_field.keys()):
        lis = []
        for p in by_field[cat]:
            theme = p.get("theme") or ""
            label = f"第{p['qno']}問"
            if theme:
                label += f"（{theme}）"
            lis.append(f'<li><a href="q{p["qno"]:02d}/index.html">{html.escape(label)}</a></li>')
        field_sections.append(
            f'<section class="glos-cat-section"><h2 class="glos-cat-heading">{html.escape(cat)}</h2>'
            f'<ol class="q-year-list">{"".join(lis)}</ol></section>'
        )

    trust = trust_table_html(anchor_id="trust", compact=True)
    body = f"""<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(desc)}">
<meta name="robots" content="index, follow">
<link rel="canonical" href="{html.escape(canonical)}">
<link rel="stylesheet" href="../../../site-pages.css">
</head>
<body class="q-static-body">
<header class="q-static-header">
  <p class="q-static-brand"><a href="../../../index.html">{html.escape(brand)}</a>（{html.escape(exam)}）</p>
  <nav aria-label="パンくず"><ol class="q-breadcrumb">
    <li><a href="../../../index.html">トップ</a></li>
    <li><a href="../../index.html">過去問一覧</a></li>
    <li aria-current="page">{html.escape(wareki)}</li>
  </ol></nav>
</header>
<main class="q-static-main">
  <h1 class="q-h1">{html.escape(wareki)} 過去問まとめ</h1>
  <p class="q-meta">全 {len(year_pages)} 問 · 解説・関連用語リンク付き</p>
  <p class="glos-static-intro">各問のページでは正答・解説のほか、問題文に関連する<strong><a href="../../../terms/index.html">用語解説</a></strong>へリンクしています。</p>
  {trust}
  {"".join(field_sections)}
  <p class="q-app-link"><a href="../../../index.html#past">アプリで{html.escape(wareki)}を演習</a></p>
</main>
</body>
</html>"""
    return body


def build_field_hub_html(field_id: str, pages: list[dict], base_url: str, brand: str, exam: str) -> str:
    meta = FIELD_HUB_META[field_id]
    field_pages = [p for p in pages if p.get("field_id") == field_id]
    if not field_pages:
        return ""
    rel_path = f"q/field/{field_id}/index.html"
    canonical = f"{base_url.rstrip('/')}/{rel_path}"
    title = f"{meta['title']}｜{brand}（{exam}）"
    desc = meta["description"]

    by_year: dict[int, list[dict]] = {}
    for p in field_pages:
        by_year.setdefault(p["year"], []).append(p)

    year_sections = []
    for y in sorted(by_year.keys(), reverse=True):
        ys = sorted(by_year[y], key=lambda x: x["qno"])
        wareki = ys[0]["wareki"]
        lis = []
        for p in ys:
            lis.append(
                f'<li><a href="../../past/y{y}/q{p["qno"]:02d}/index.html">'
                f'{html.escape(wareki)} 第{p["qno"]}問</a></li>'
            )
        year_sections.append(
            f'<section class="glos-cat-section"><h2 class="glos-cat-heading">{y}年（{html.escape(wareki)}）</h2>'
            f'<ol class="q-year-list">{"".join(lis)}</ol></section>'
        )

    trust = trust_table_html(anchor_id="trust", compact=True)
    return f"""<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(desc)}">
<meta name="robots" content="index, follow">
<link rel="canonical" href="{html.escape(canonical)}">
<link rel="stylesheet" href="../../site-pages.css">
</head>
<body class="q-static-body">
<header class="q-static-header">
  <p class="q-static-brand"><a href="../../index.html">{html.escape(brand)}</a>（{html.escape(exam)}）</p>
  <nav aria-label="パンくず"><ol class="q-breadcrumb">
    <li><a href="../../index.html">トップ</a></li>
    <li><a href="../index.html">過去問一覧</a></li>
    <li aria-current="page">{html.escape(meta["name"])}</li>
  </ol></nav>
</header>
<main class="q-static-main">
  <h1 class="q-h1">{html.escape(meta["name"])}の過去問</h1>
  <p class="q-meta">掲載 {len(field_pages)} 問</p>
  {trust}
  {"".join(year_sections)}
  <p class="q-hub-links"><a href="../../terms/index.html">用語解説一覧</a> · <a href="../../articles/index.html">試験ガイド</a></p>
</main>
</body>
</html>"""
