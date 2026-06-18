#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""過去問ページの SEO 拡張（年度ハブ・分野ハブ・相互リンク）。"""

from __future__ import annotations

import html
import json
import re
from pathlib import Path

from tools.html_footer import (
    breadcrumb_html,
    footer_href,
    shell_body_class,
    site_page_header,
    site_page_wrap_close,
    site_page_wrap_open,
)
from tools.seo_common import (
    AUTHOR_LABEL,
    FIELD_HUB_META,
    UPDATED_LABEL,
    build_term_match_index,
    extract_theme_label,
    field_id_for_category,
    glossary_term_file_by_legacy_slug,
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
    items = load_glossary_items_from_js()
    by_slug = {
        (i.get("articleSlug") or str(i.get("id", "")).replace("_", "-")).strip(): i for i in items
    }
    href_by_slug = glossary_term_file_by_legacy_slug()
    links = []
    for slug in slugs:
        item = by_slug.get(slug)
        label = str(item.get("term") if item else slug)
        term_file = href_by_slug.get(slug) or f"{slug}/index.html"
        href = footer_href(rel_path, f"terms/{term_file}")
        links.append(
            f'<a class="related-link" href="{html.escape(href)}">{html.escape(label)}</a>'
        )
    return (
        '<section class="q-block q-related" aria-labelledby="q-terms-h">'
        '<h2 id="q-terms-h" class="q-h2">関連する用語解説</h2>'
        '<div class="related-box">'
        '<div class="related-links q-related-links">'
        f'{"".join(links)}'
        "</div></div></section>"
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
                    "item": canonical.rsplit(f"/q{page['qno']:02d}/", 1)[0] + "/index.html",
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


EXAM_QUESTIONS_PER_YEAR = 50

FIELD_HUB_ORDER = ("rights", "law", "limit", "tax")


def _hub_meta_tags(title: str, desc: str, canonical: str) -> str:
    return f"""<meta name="robots" content="index, follow">
<link rel="canonical" href="{html.escape(canonical)}">
<meta property="og:type" content="website">
<meta property="og:title" content="{html.escape(title)}">
<meta property="og:description" content="{html.escape(desc)}">
<meta property="og:url" content="{html.escape(canonical)}">
<meta name="twitter:card" content="summary">
<meta name="twitter:title" content="{html.escape(title)}">
<meta name="twitter:description" content="{html.escape(desc)}">"""


def _collection_json_ld(
    *,
    canonical: str,
    title: str,
    desc: str,
    items: list[tuple[str, str]],
    site_url: str,
) -> str:
    """CollectionPage + ItemList（一覧ページ向け）。"""
    elements = [
        {
            "@type": "ListItem",
            "position": i,
            "name": name,
            "url": url,
        }
        for i, (name, url) in enumerate(items[:50], start=1)
    ]
    site_root = site_url.rstrip("/") + "/"
    graph = [
        {
            "@type": "CollectionPage",
            "@id": canonical + "#webpage",
            "url": canonical,
            "name": title,
            "description": desc,
            "inLanguage": "ja",
            "isPartOf": {"@type": "WebSite", "name": "宅建マスター", "url": site_root},
        },
        {
            "@type": "ItemList",
            "@id": canonical + "#itemlist",
            "numberOfItems": len(items),
            "itemListElement": elements,
        },
    ]
    payload = json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False)
    return f'<script type="application/ld+json">{payload}</script>'


def _field_count_summary(by_field: dict[str, list[dict]]) -> str:
    parts = []
    for cat in sorted(by_field.keys()):
        parts.append(f"{html.escape(cat)}<strong>{len(by_field[cat])}問</strong>")
    return "・".join(parts)


def _year_nav_html(year: int, years: list[int], base_url: str) -> str:
    base = base_url.rstrip("/")
    links = []
    if year - 1 in years:
        yp = year - 1
        links.append(f'<a href="{base}/q/past/y{yp}/index.html">前の年度（{yp}年）</a>')
    links.append(f'<a href="{base}/q/past/index.html">年度別一覧</a>')
    if year + 1 in years:
        yn = year + 1
        links.append(f'<a href="{base}/q/past/y{yn}/index.html">次の年度（{yn}年）</a>')
    if not links:
        return ""
    return '<nav class="q-hub-nav" aria-label="年度ナビ">' + " · ".join(links) + "</nav>"


def _field_hub_links_html(base_url: str) -> str:
    base = base_url.rstrip("/")
    lis = []
    for fid in FIELD_HUB_ORDER:
        meta = FIELD_HUB_META[fid]
        lis.append(
            f'<li><a href="{base}/q/field/{fid}/index.html">'
            f'{html.escape(meta["name"])}の過去問一覧</a></li>'
        )
    return (
        '<section class="q-hub-fields" aria-labelledby="q-field-links">'
        '<h2 class="q-h2" id="q-field-links">分野別の過去問一覧</h2>'
        f'<ul class="q-hub-field-list">{"".join(lis)}</ul></section>'
    )


def coverage_note_html(published: int, total: int = EXAM_QUESTIONS_PER_YEAR) -> str:
    if published >= total:
        return ""
    missing = total - published
    return (
        f'<p class="q-coverage-note">'
        f"本試験は全<strong>{total}問</strong>です。"
        f"当ページでは<strong>{published}問</strong>を掲載しています"
        f"（未掲載 <strong>{missing}問</strong> は順次追加予定）。"
        f"表の「未掲載」はデータ準備中の問番です。"
        f"</p>"
    )


def q_list_table_html(
    items: list[dict],
    href_for,
    *,
    qno_min: int = 1,
    qno_max: int | None = EXAM_QUESTIONS_PER_YEAR,
    show_missing: bool = False,
    show_category: bool = False,
) -> str:
    """問一覧の表。show_missing 時は第1問〜qno_max まで欠番行を表示。"""
    by_qno = {int(p["qno"]): p for p in items}
    if not by_qno:
        return ""

    qnos = sorted(by_qno.keys()) if qno_max is None else list(range(qno_min, qno_max + 1))
    head = '<th scope="col">問</th>'
    if show_category:
        head += '<th scope="col">分野</th>'
    head += '<th scope="col">テーマ</th>'

    rows: list[str] = []
    for qno in qnos:
        p = by_qno.get(qno)
        if p:
            theme = (p.get("theme") or p.get("category") or "").strip()
            href = html.escape(href_for(p))
            num_cell = f'<a href="{href}">第{qno}問</a>'
            theme_cell = (
                f'<a href="{href}">{html.escape(theme)}</a>'
                if theme
                else f'<a href="{href}">解説を見る</a>'
            )
            row = f'<tr><td class="q-year-table-num">{num_cell}</td>'
            if show_category:
                row += f'<td class="q-year-table-cat">{html.escape((p.get("category") or "").strip())}</td>'
            row += f'<td class="q-year-table-theme">{theme_cell}</td></tr>'
            rows.append(row)
        elif show_missing and qno_max is not None:
            row = f'<tr class="q-year-table-missing"><td class="q-year-table-num">第{qno}問</td>'
            if show_category:
                row += '<td class="q-year-table-cat">—</td>'
            row += '<td class="q-year-table-theme">未掲載</td></tr>'
            rows.append(row)

    if not rows:
        return ""
    return (
        '<div class="q-year-table-wrap">'
        '<table class="q-year-table">'
        f"<thead><tr>{head}</tr></thead>"
        f"<tbody>{''.join(rows)}</tbody>"
        "</table></div>"
    )


def q_year_index_summary_html(by_year: dict[int, list[dict]]) -> str:
    rows: list[str] = []
    for y in sorted(by_year.keys(), reverse=True):
        ys = by_year[y]
        n = len(ys)
        wareki = ys[0]["wareki"]
        total = EXAM_QUESTIONS_PER_YEAR
        count_label = f"全{total}問" if n >= total else f"{n}/{total}問"
        row_class = "q-year-index-complete" if n >= total else "q-year-index-partial"
        rows.append(
            f'<tr class="{row_class}">'
            f'<td class="q-year-index-year">'
            f'<a href="past/y{y}/index.html">{html.escape(str(y))}年（{html.escape(wareki)}）</a></td>'
            f'<td class="q-year-index-count">{html.escape(count_label)}</td>'
            f'<td class="q-year-index-link"><a href="past/y{y}/index.html">一覧を見る</a></td>'
            "</tr>"
        )
    if not rows:
        return ""
    return (
        '<section class="q-year-index-section" aria-labelledby="q-year-index">'
        '<h2 class="q-h2" id="q-year-index">年度別一覧</h2>'
        '<p class="q-year-index-lead">各年度ページで第1問から順に確認できます。掲載数が50問未満の年度は追加準備中です。</p>'
        '<div class="q-year-table-wrap"><table class="q-year-table q-year-index-table">'
        '<thead><tr><th scope="col">試験年度</th><th scope="col">掲載</th><th scope="col"></th></tr></thead>'
        f"<tbody>{''.join(rows)}</tbody></table></div>"
        "</section>"
    )


def build_past_root_hub_html(
    years: list[int], pages: list[dict], base_url: str, brand: str, exam: str
) -> str:
    """q/past/index.html — 年度別静的ハブのトップ。"""
    base = base_url.rstrip("/")
    rel_path = "q/past/index.html"
    canonical = f"{base}/{rel_path}"
    y_min, y_max = min(years), max(years)
    title = f"宅建 過去問 年度別一覧｜{y_max}年〜{y_min}年｜{brand}（{exam}）"
    desc = (
        f"{exam}の過去問を年度別に一覧。{len(years)}年度・全{len(pages)}問を掲載し、"
        "各問の解説・正答・関連用語リンク付きで無料演習できます。"
    )

    by_year: dict[int, list[dict]] = {}
    for p in pages:
        by_year.setdefault(p["year"], []).append(p)

    year_rows = []
    list_items: list[tuple[str, str]] = []
    for y in sorted(years, reverse=True):
        ys = sorted(by_year[y], key=lambda p: p["qno"])
        wareki = ys[0]["wareki"]
        n = len(ys)
        first_href = ys[0]["rel_path"].removeprefix("q/past/")
        url = f"{base}/q/past/{first_href}"
        year_rows.append(
            f'<li><a href="{html.escape(first_href)}"><strong>{html.escape(wareki)}</strong>'
            f"（{y}年）— {n}問掲載</a></li>"
        )
        list_items.append((f"{wareki}（{y}年）", url))

    json_ld = _collection_json_ld(
        canonical=canonical, title=title, desc=desc, items=list_items, site_url=base
    )
    trust = trust_table_html(anchor_id="trust", compact=True)
    field_links = _field_hub_links_html(base)
    rel = Path("q/past/index.html")
    page_header = site_page_header(rel, current="q")
    page_breadcrumb = breadcrumb_html(
        rel,
        [
            ("トップ", "index.html"),
            ("過去問一覧", "q/index.html"),
            ("年度別一覧", None),
        ],
    )

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
<body class="{shell_body_class('q-past-hub-page')}">
{site_page_wrap_open()}
{page_header}
<main class="q-static-main">
  {page_breadcrumb}
  <h1 class="q-h1">宅建 過去問 年度別一覧</h1>
  <p class="q-meta">全 {len(pages)} 問 · {len(years)} 年度</p>
  <p class="glos-static-intro">
    {html.escape(exam)}の過去問を、試験年度ごとに整理した静的ページです。
    各年度ページから第1問以降の<strong>解説付き問題</strong>へ進めます。
    絞り込み検索は<a href="../index.html">過去問一覧（検索付き）</a>をご利用ください。
  </p>
  {trust}
  <section class="glos-cat-section" aria-labelledby="q-past-years">
    <h2 class="glos-cat-heading" id="q-past-years">試験年度を選ぶ</h2>
    <ol class="q-year-list q-past-year-overview">{"".join(year_rows)}</ol>
  </section>
  {field_links}
  <p class="q-hub-links"><a href="../../terms/index.html">用語解説一覧</a> · <a href="../../articles/index.html">試験ガイド</a></p>
  <p class="q-app-link"><a href="../../index.html#past">アプリで過去問を演習</a></p>
</main>
{site_page_wrap_close()}
</body>
</html>"""


def build_year_hub_html(year: int, pages: list[dict], base_url: str, brand: str, exam: str) -> str:
    year_pages = sorted([p for p in pages if p["year"] == year], key=lambda x: x["qno"])
    if not year_pages:
        return ""
    wareki = year_pages[0]["wareki"]
    years = sorted({p["year"] for p in pages})
    rel_path = f"q/past/y{year}/index.html"
    base = base_url.rstrip("/")
    canonical = f"{base}/{rel_path}"
    title = f"{wareki} 宅建過去問まとめ（全{len(year_pages)}問）｜{brand}（{exam}）"
    desc = (
        f"{wareki}（{year}年）の{exam}過去問{len(year_pages)}問を掲載。"
        "正答・解説・関連用語リンク付き。権利関係・宅建業法・法令制限・税の分野別に確認できます。"
    )

    by_field: dict[str, list[dict]] = {}
    for p in year_pages:
        by_field.setdefault(p["category"], []).append(p)

    list_items = [
        (
            f"第{p['qno']}問",
            f"{base}/q/past/y{year}/q{p['qno']:02d}/index.html",
        )
        for p in year_pages
    ]
    json_ld = _collection_json_ld(
        canonical=canonical, title=title, desc=desc, items=list_items, site_url=base
    )
    trust = trust_table_html(anchor_id="trust", compact=True)
    coverage = coverage_note_html(len(year_pages))
    year_nav = _year_nav_html(year, years, base)
    field_summary = _field_count_summary(by_field)

    field_sections = []
    for cat in sorted(by_field.keys()):
        cat_pages = sorted(by_field[cat], key=lambda x: x["qno"])
        table = q_list_table_html(
            cat_pages,
            lambda p: f"q{p['qno']:02d}/index.html",
            show_category=False,
        )
        field_sections.append(
            f'<section class="glos-cat-section"><h2 class="glos-cat-heading">{html.escape(cat)}'
            f"（{len(cat_pages)}問）</h2>{table}</section>"
        )

    rel = Path(f"q/past/y{year}/index.html")
    page_header = site_page_header(rel, current="q")
    page_breadcrumb = breadcrumb_html(
        rel,
        [
            ("トップ", "index.html"),
            ("過去問一覧", "q/index.html"),
            ("年度別一覧", "q/past/index.html"),
            (wareki, None),
        ],
    )

    body = f"""<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(desc)}">
{_hub_meta_tags(title, desc, canonical)}
<link rel="stylesheet" href="../../../site-pages.css">
{json_ld}
</head>
<body class="{shell_body_class('q-past-year-hub-page')}">
{site_page_wrap_open()}
{page_header}
<main class="q-static-main">
  {page_breadcrumb}
  <h1 class="q-h1">{html.escape(wareki)} 過去問まとめ</h1>
  <p class="q-meta">全 {len(year_pages)} 問 · 解説・関連用語リンク付き</p>
  <p class="glos-static-intro">
    {html.escape(wareki)}（{year}年）の{html.escape(exam)}過去問を掲載しています。
    内訳は{field_summary}です。各問ページでは<strong>正答・解説</strong>のほか、
    問題文に関連する<a href="../../../terms/index.html">用語解説</a>へリンクしています。
  </p>
  {year_nav}
  {coverage}
  {trust}
  {"".join(field_sections)}
  <p class="q-hub-links"><a href="../index.html">ほかの年度を見る</a> · <a href="../../index.html">過去問一覧（検索）</a></p>
  <p class="q-app-link"><a href="../../../index.html#past">アプリで{html.escape(wareki)}を演習</a></p>
</main>
{site_page_wrap_close()}
</body>
</html>"""
    return body


def build_field_hub_html(field_id: str, pages: list[dict], base_url: str, brand: str, exam: str) -> str:
    meta = FIELD_HUB_META[field_id]
    field_pages = [p for p in pages if p.get("field_id") == field_id]
    if not field_pages:
        return ""
    rel_path = f"q/field/{field_id}/index.html"
    base = base_url.rstrip("/")
    canonical = f"{base}/{rel_path}"
    title = f"{meta['title']}｜{brand}（{exam}）"
    desc = meta["description"]
    years = sorted({p["year"] for p in field_pages}, reverse=True)

    by_year: dict[int, list[dict]] = {}
    for p in field_pages:
        by_year.setdefault(p["year"], []).append(p)

    list_items = [
        (
            f"{p['wareki']} 第{p['qno']}問",
            f"{base}/q/past/y{p['year']}/q{p['qno']:02d}/index.html",
        )
        for p in sorted(field_pages, key=lambda x: (-x["year"], x["qno"]))
    ]
    json_ld = _collection_json_ld(
        canonical=canonical, title=title, desc=desc, items=list_items, site_url=base
    )

    year_sections = []
    for y in years:
        ys = sorted(by_year[y], key=lambda x: x["qno"])
        wareki = ys[0]["wareki"]
        table = q_list_table_html(
            ys,
            lambda p: f"../../past/y{y}/q{p['qno']:02d}/index.html",
            show_category=False,
        )
        year_sections.append(
            f'<section class="glos-cat-section"><h2 class="glos-cat-heading">'
            f'<a href="{base}/q/past/y{y}/index.html">{y}年（{html.escape(wareki)}）</a>'
            f"（{len(ys)}問）</h2>{table}</section>"
        )

    trust = trust_table_html(anchor_id="trust", compact=True)
    depth = len(Path(rel_path).parent.parts)
    to_root = "/".join([".."] * depth)
    to_q = "/".join([".."] * (depth - 1))
    year_links = " · ".join(
        f'<a href="{base}/q/past/y{y}/index.html">{y}年</a>' for y in years[:6]
    )
    if len(years) > 6:
        year_links += f' … <a href="{base}/q/past/index.html">全年度</a>'

    rel = Path(rel_path)
    page_header = site_page_header(rel, current="q")
    page_breadcrumb = breadcrumb_html(
        rel,
        [
            ("トップ", "index.html"),
            ("過去問一覧", "q/index.html"),
            (meta["name"], None),
        ],
    )

    return f"""<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(desc)}">
{_hub_meta_tags(title, desc, canonical)}
<link rel="stylesheet" href="{to_root}/site-pages.css">
{json_ld}
</head>
<body class="{shell_body_class('q-field-hub-page')}">
{site_page_wrap_open()}
{page_header}
<main class="q-static-main">
  {page_breadcrumb}
  <h1 class="q-h1">{html.escape(meta["name"])}の過去問</h1>
  <p class="q-meta">掲載 {len(field_pages)} 問 · {len(years)} 年度</p>
  <p class="glos-static-intro">
    {html.escape(exam)}の<strong>{html.escape(meta["name"])}</strong>分野の過去問を年度別にまとめています。
    各問ページでは正答・解説・<a href="{to_root}/terms/index.html">用語解説</a>へのリンクがあります。
    年度ページ例：{year_links}
  </p>
  {trust}
  {"".join(year_sections)}
  <p class="q-hub-links"><a href="{base}/q/past/index.html">年度別一覧</a> · <a href="{to_q}/index.html">過去問一覧（検索）</a></p>
  <p class="q-hub-links"><a href="{to_root}/terms/index.html">用語解説一覧</a> · <a href="{to_root}/articles/index.html">試験ガイド</a></p>
</main>
{site_page_wrap_close()}
</body>
</html>"""


def past_index_page_title(count: int, brand: str) -> str:
    return f"宅建 過去問（解説付き）{count}問 無料｜年度別・分野別｜{brand}"


def past_index_meta_description(*, count: int, year_count: int) -> str:
    text = (
        f"宅建 過去問{count}問を年度別・分野別に無料掲載。"
        f"{year_count}年度分・解説付き。宅建試験 過去問の検索・演習・解き直しに対応。"
        "実践演習・一問一答も同サイトで学習できます。"
    )
    if len(text) <= 155:
        return text
    return text[:154] + "…"


def past_index_collection_json_ld(
    *,
    canonical: str,
    title: str,
    desc: str,
    count: int,
    site_url: str,
) -> str:
    site_root = site_url.rstrip("/") + "/"
    graph = [
        {
            "@type": "CollectionPage",
            "@id": canonical + "#webpage",
            "url": canonical,
            "name": title,
            "description": desc,
            "inLanguage": "ja",
            "isPartOf": {"@type": "WebSite", "name": "宅建マスター", "url": site_root},
        },
        {
            "@type": "ItemList",
            "@id": canonical + "#itemlist",
            "name": "宅建 過去問一覧",
            "numberOfItems": count,
            "itemListElement": [
                {
                    "@type": "ListItem",
                    "position": 1,
                    "name": "年度別一覧",
                    "url": site_root + "q/past/index.html",
                },
                {
                    "@type": "ListItem",
                    "position": 2,
                    "name": "宅建業法の過去問",
                    "url": site_root + "q/field/law/index.html",
                },
            ],
        },
    ]
    payload = json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False)
    return f'<script type="application/ld+json">{payload}</script>'
