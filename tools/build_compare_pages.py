#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
data/comparisons.csv から terms/compare/index.html と terms/compare/c-*.html を生成する。

用語一覧（terms/index.html）とは別 URL。タブで横断（tools/knowledge_hub_tabs.py）。
"""

from __future__ import annotations

import csv
import hashlib
import html
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from tools.build_glossary_pages import (  # noqa: E402
    HEAD_FONTS,
    GLOSSARY_CSV,
    TERMS_INDEX_CSS_VER,
    custom_faq_items,
    faq_items_for_term,
    faq_section_html,
    load_glossary_rows,
    make_term_lookup,
    meta_description,
    norm,
    ordered_term_categories,
    parse_term_tags,
    public_url,
    rel_css,
    rel_theme_css,
    semicolon_field_html,
    semicolon_list_html,
    split_semicolon,
    term_slug,
)
from tools.html_footer import (  # noqa: E402
    ROBOTS_INDEX_FOLLOW,
    breadcrumb_html,
    shell_body_class,
    site_page_footer,
    site_page_header,
    site_page_wrap_close,
    site_page_wrap_open,
)
from tools.knowledge_hub_tabs import knowledge_hub_tab_hrefs, knowledge_hub_tabs_html  # noqa: E402
from tools.seo_utils import content_date_from_row, json_ld_date_modified, meta_updated_html  # noqa: E402
from tools.site_config import brand_name, exam_name, clean_origin  # noqa: E402

COMPARE_CSV = ROOT / "data" / "comparisons.csv"
COMPARE_DIR = ROOT / "terms" / "compare"
BASE_DEFAULT = clean_origin()

COMPARE_INDEX_JS_VER = "20260527-compare-index"
COMPARE_INDEX_SEARCH_PLACEHOLDER = "例：過去問、模擬試験、公式情報…"
PRESERVED_COMPARE_GLOB = "c-*.html"


def compare_slug(title: str, used: dict[str, str]) -> str:
    base = title.strip()
    h = hashlib.sha256(base.encode("utf-8")).hexdigest()[:16]
    s = f"c-{h}"
    if s not in used:
        used[s] = base
        return s
    n = 2
    while True:
        cand = f"c-{h}-{n}"
        if cand not in used:
            used[cand] = base
            return cand
        n += 1


def compare_index_href(slug_file: str) -> str:
    return f"/terms/compare/{slug_file.lstrip('/')}"


def parse_compare_rows(raw: str, *, line: int) -> list[dict]:
    text = norm(raw)
    if not text:
        raise ValueError(f"line {line}: compare_rows が空です")
    try:
        rows = json.loads(text)
    except json.JSONDecodeError as exc:
        raise ValueError(f"line {line}: compare_rows の JSON が不正です: {exc}") from exc
    if not isinstance(rows, list) or not rows:
        raise ValueError(f"line {line}: compare_rows は空でない配列にしてください")
    out: list[dict] = []
    for i, row in enumerate(rows, start=1):
        if not isinstance(row, dict):
            raise ValueError(f"line {line}: compare_rows[{i - 1}] はオブジェクトにしてください")
        axis = norm(row.get("axis"))
        cols = row.get("cols")
        if not axis:
            raise ValueError(f"line {line}: compare_rows[{i - 1}].axis が空です")
        if not isinstance(cols, list) or len(cols) < 2:
            raise ValueError(f"line {line}: compare_rows[{i - 1}].cols は2件以上必要です")
        out.append({"axis": axis, "cols": [norm(c) for c in cols]})
    return out


def load_compare_rows() -> list[dict]:
    if not COMPARE_CSV.is_file():
        raise FileNotFoundError(str(COMPARE_CSV))
    text = COMPARE_CSV.read_text(encoding="utf-8-sig")
    used: dict[str, str] = {}
    entries: list[dict] = []
    for i, row in enumerate(csv.DictReader(text.splitlines()), start=2):
        title = norm(row.get("title"))
        if not title:
            raise ValueError(f"line {i}: title が空です")
        legacy_slug = norm(row.get("slug"))
        if legacy_slug:
            if not re.fullmatch(r"[a-z0-9][a-z0-9-]*", legacy_slug):
                raise ValueError(f"line {i}: slug は半角英数字とハイフンのみ: {legacy_slug!r}")
            slug_file = f"{legacy_slug}.html"
            if slug_file in used:
                raise ValueError(f"line {i}: slug が重複しています: {legacy_slug}")
            used[slug_file] = title
        else:
            slug_file = compare_slug(title, used) + ".html"
        col_labels = split_semicolon(norm(row.get("col_labels")))
        if len(col_labels) < 2:
            raise ValueError(f"line {i}: col_labels は2件以上必要です")
        compare_rows = parse_compare_rows(row.get("compare_rows") or "", line=i)
        for cr in compare_rows:
            if len(cr["cols"]) != len(col_labels):
                raise ValueError(
                    f"line {i}: compare_rows の列数が col_labels と一致しません "
                    f"({len(cr['cols'])} vs {len(col_labels)})"
                )
        entries.append(
            {
                "title": title,
                "category": norm(row.get("category")),
                "tags": norm(row.get("tags")),
                "summary": norm(row.get("summary")),
                "col_labels": col_labels,
                "compare_rows": compare_rows,
                "article_title": norm(row.get("article_title")),
                "article_lead": norm(row.get("article_lead")),
                "exam_points": norm(row.get("exam_points")),
                "common_mistakes": norm(row.get("common_mistakes")),
                "memory_tip": norm(row.get("memory_tip")),
                "related_terms": norm(row.get("related_terms")),
                "faq_1_question": norm(row.get("faq_1_question")),
                "faq_1_answer": norm(row.get("faq_1_answer")),
                "faq_2_question": norm(row.get("faq_2_question")),
                "faq_2_answer": norm(row.get("faq_2_answer")),
                "faq_3_question": norm(row.get("faq_3_question")),
                "faq_3_answer": norm(row.get("faq_3_answer")),
                "faq_4_question": norm(row.get("faq_4_question")),
                "faq_4_answer": norm(row.get("faq_4_answer")),
                "slug_file": slug_file,
                "fact_checked_at": norm(row.get("fact_checked_at")),
                "last_reviewed_at": norm(row.get("last_reviewed_at")),
                "source_checked_at": norm(row.get("source_checked_at")),
            }
        )
    return entries


def compare_index_item_dict(entry: dict) -> dict:
    tags = parse_term_tags(entry.get("tags") or "")
    subjects = " / ".join(entry.get("col_labels") or [])
    search_bits = [
        entry["title"],
        entry.get("category") or "",
        entry.get("summary") or "",
        subjects,
        *tags,
    ]
    return {
        "title": entry["title"],
        "category": entry.get("category") or "",
        "tags": tags,
        "summary": entry.get("summary") or "",
        "subjects": subjects,
        "href": compare_index_href(entry["slug_file"]),
        "search": " ".join(x for x in search_bits if x),
    }


def render_compare_index_tbody(entries: list[dict]) -> str:
    items = sorted(entries, key=lambda e: (e.get("category") or "", e.get("title") or ""))
    rows: list[str] = []
    for item in items:
        href = html.escape(compare_index_href(item["slug_file"]))
        href_attr = f' data-entry-href="{href}"'
        summary = html.escape(item.get("summary") or "")
        subjects = html.escape(" / ".join(item.get("col_labels") or []))
        rows.append(
            "<tr class=\"terms-idx-table-row compare-idx-table-row\">"
            f'<td class="terms-idx-td-term compare-idx-td-title" data-label="比較"{href_attr} tabindex="0">'
            f'<div class="terms-idx-term-cell"><a href="{href}">{html.escape(item["title"])}</a>'
            f"</div></td>"
            f'<td class="terms-idx-td-cat" data-label="分野"{href_attr}>'
            f'{html.escape(item.get("category") or "")}</td>'
            f'<td class="terms-idx-td-snippet compare-idx-td-subjects" data-label="比較対象"{href_attr}>'
            f"{subjects}</td>"
            "</tr>"
        )
    return "\n".join(rows)


def compare_matrix_table_html(col_labels: list[str], compare_rows: list[dict]) -> str:
    head = "<th scope=\"col\">比較軸</th>" + "".join(
        f'<th scope="col">{html.escape(label)}</th>' for label in col_labels
    )
    body_rows: list[str] = []
    for row in compare_rows:
        cells = "".join(f"<td>{html.escape(c)}</td>" for c in row["cols"])
        body_rows.append(
            f'<tr><th scope="row">{html.escape(row["axis"])}</th>{cells}</tr>'
        )
    return (
        '<table class="seo-info-table compare-matrix-table">'
        f"<thead><tr>{head}</tr></thead>"
        f"<tbody>{''.join(body_rows)}</tbody></table>"
        '<p class="term-compare-note">数値・手続の正誤は演習と公式テキストで必ず確認してください。</p>'
    )


def related_terms_links_html(related: str, term_lookup: dict[str, str]) -> str:
    items: list[str] = []
    seen: set[str] = set()
    for label in split_semicolon(related):
        href = term_lookup.get(label)
        if href and href not in seen:
            seen.add(href)
            items.append(
                f'<a class="related-link" href="../{html.escape(href)}">{html.escape(label)}</a>'
            )
    if not items:
        return ""
    return (
        '<div class="related-box" aria-labelledby="compare-related-title">'
        '<div id="compare-related-title" class="related-box-title">関連用語</div>'
        f'<div class="related-links term-related-links">{"".join(items)}</div></div>'
    )


def build_compare_detail_html(
    entry: dict,
    rel_path: Path,
    base_url: str,
    term_lookup: dict[str, str],
) -> str:
    title_text = entry["title"]
    category = entry.get("category") or ""
    summary = entry.get("summary") or ""
    col_labels = entry["col_labels"]
    compare_rows = entry["compare_rows"]
    article_title = entry.get("article_title") or f"{title_text}｜{exam_name()}"
    article_lead = entry.get("article_lead") or summary
    exam_points = entry.get("exam_points") or ""
    common_mistakes = entry.get("common_mistakes") or ""
    memory_tip = entry.get("memory_tip") or ""
    related = entry.get("related_terms") or ""

    page_title = f"{article_title}｜{brand_name()}"
    desc = meta_description(
        f"{title_text}を表で整理。{exam_name()}向けに{summary or '似た概念の使い分けを解説します。'}"
    )
    canonical = public_url(base_url, f"terms/compare/{entry['slug_file']}")
    updated = content_date_from_row(entry)
    css_href = rel_css(rel_path)
    theme_href = rel_theme_css(rel_path)

    matrix_html = compare_matrix_table_html(col_labels, compare_rows)
    points_html = semicolon_list_html(exam_points)
    mistakes_html = semicolon_field_html(common_mistakes) or (
        f"<p>{html.escape(common_mistakes)}</p>" if common_mistakes else ""
    )
    memory_html = (
        f"<blockquote><p>{html.escape(memory_tip)}</p></blockquote>" if memory_tip else ""
    )

    fallback_faq = faq_items_for_term(
        title_text,
        summary,
        summary,
        exam_points or summary,
    )
    faq_items = custom_faq_items(entry, fallback_faq)
    faq_html = faq_section_html(faq_items)

    rel_path_breadcrumb = rel_path
    page_header = site_page_header(rel_path_breadcrumb, current="terms")
    page_footer = site_page_footer(rel_path_breadcrumb, current="terms")
    page_breadcrumb = (
        '<nav class="site-page-header-crumb" aria-label="パンくず">'
        '<ol class="q-breadcrumb">'
        '<li><a href="../../index.html">トップ</a></li>'
        '<li><a href="index.html">比較・整理表</a></li>'
        f'<li aria-current="page">{html.escape(title_text)}</li>'
        "</ol></nav>"
    )
    tabs_html = knowledge_hub_tabs_html(current="compare", **knowledge_hub_tab_hrefs(here="compare"))
    rel_section = related_terms_links_html(related, term_lookup)
    subjects_line = " / ".join(col_labels)

    info_rows = [
        ("対象試験", exam_name()),
        ("分野", category),
        ("比較対象", subjects_line),
    ]
    info_table = (
        '<section class="seo-article-section" aria-labelledby="compare-info-title">'
        '<h2 id="compare-info-title">記事の基本情報</h2>'
        '<table class="seo-info-table"><tbody>'
        + "".join(
            f"<tr><th>{html.escape(k)}</th><td>{html.escape(v)}</td></tr>"
            for k, v in info_rows
            if v
        )
        + "</tbody></table></section>"
    )

    graph: list[dict] = [
        {
            "@type": "Article",
            "@id": canonical + "#article",
            "headline": article_title,
            "description": desc,
            "url": canonical,
            **json_ld_date_modified(updated),
            "inLanguage": "ja-JP",
            "author": {"@type": "Organization", "name": brand_name() + "編集部"},
        },
        {
            "@type": "BreadcrumbList",
            "itemListElement": [
                {
                    "@type": "ListItem",
                    "position": 1,
                    "name": "トップ",
                    "item": public_url(base_url, "index.html"),
                },
                {
                    "@type": "ListItem",
                    "position": 2,
                    "name": "比較・整理表",
                    "item": public_url(base_url, "terms/compare/index.html"),
                },
                {
                    "@type": "ListItem",
                    "position": 3,
                    "name": title_text,
                    "item": canonical,
                },
            ],
        },
    ]
    if faq_items:
        graph.append(
            {
                "@type": "FAQPage",
                "@id": canonical + "#faq",
                "mainEntity": [
                    {
                        "@type": "Question",
                        "name": item["question"],
                        "acceptedAnswer": {"@type": "Answer", "text": item["answer"]},
                    }
                    for item in faq_items
                ],
            }
        )

    next_links = (
        '<div class="related-box" aria-labelledby="compare-next-title">'
        '<div id="compare-next-title" class="related-box-title">次に確認するページ</div>'
        '<div class="related-links">'
        '<a class="related-link" href="index.html">比較・整理表一覧へ戻る</a>'
        '<a class="related-link" href="../index.html">用語解説一覧</a>'
        '<a class="related-link" href="../../q/index.html">過去問演習で確認する</a>'
        "</div></div>"
    )

    points_section = ""
    if points_html:
        points_section = (
            '<section class="seo-article-section" aria-labelledby="compare-sec-points">'
            '<h2 id="compare-sec-points"><span class="section-heading-num">2</span>試験で押さえるポイント</h2>'
            f"{points_html}</section>"
        )
    mistakes_section = ""
    if mistakes_html:
        mistakes_section = (
            '<section class="seo-article-section" aria-labelledby="compare-sec-mistakes">'
            '<h2 id="compare-sec-mistakes"><span class="section-heading-num">3</span>よくある誤解・注意点</h2>'
            f"{mistakes_html}</section>"
        )
    memory_section = ""
    if memory_html:
        memory_section = (
            '<section class="seo-article-section" aria-labelledby="compare-sec-memory">'
            '<h2 id="compare-sec-memory"><span class="section-heading-num">4</span>覚え方・整理のコツ</h2>'
            f"{memory_html}</section>"
        )
    faq_section = ""
    if faq_html:
        faq_section = (
            '<section class="seo-article-section" aria-labelledby="compare-sec-faq">'
            f'<h2 id="compare-sec-faq">よくある質問</h2>{faq_html}</section>'
        )

    return f"""<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{html.escape(page_title)}</title>
<meta name="description" content="{html.escape(desc)}">
{ROBOTS_INDEX_FOLLOW}
<link rel="canonical" href="{html.escape(canonical)}">
<meta property="og:type" content="article">
<meta property="og:title" content="{html.escape(page_title)}">
<meta property="og:description" content="{html.escape(desc)}">
<meta property="og:url" content="{html.escape(canonical)}">
<meta name="twitter:card" content="summary">
<script type="application/ld+json">
{json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False, indent=2)}
</script>
{HEAD_FONTS}
<link rel="stylesheet" href="{html.escape(css_href)}">
<link rel="stylesheet" href="{html.escape(theme_href)}">
</head>
<body class="{shell_body_class('compare-article-page')}">
{site_page_wrap_open()}
{page_header}
<main class="seo-article-main">
  {page_breadcrumb}
  {tabs_html}
  <article class="seo-article-card article-body">
    <div class="article-meta">
      <span class="meta-category">比較・整理表</span>
      {meta_updated_html(updated)}
      <span class="meta-updated"><span class="q-id">比較</span> · <span>{html.escape(category)}</span> · <span>{html.escape(subjects_line)}</span></span>
    </div>
    <h1 class="article-title">{html.escape(article_title)}</h1>
    <p class="article-lead">{html.escape(article_lead)}</p>
    <section class="seo-article-section" aria-labelledby="compare-sec-matrix">
      <h2 id="compare-sec-matrix"><span class="section-heading-num">1</span>比較表</h2>
      {matrix_html}
    </section>
    {points_section}
    {mistakes_section}
    {memory_section}
    {faq_section}
    {info_table}
    {rel_section}
    {next_links}
  </article>
</main>
{page_footer}
{site_page_wrap_close()}
</body>
</html>
"""


def build_compare_index(entries: list[dict], base_url: str) -> str:
    by_cat: dict[str, list[dict]] = {}
    for e in entries:
        by_cat.setdefault(e.get("category") or "その他", []).append(e)
    cat_keys = ordered_term_categories(by_cat)

    n_items = len(entries)
    n_cats = len(cat_keys)

    chip_lines = [
        '    <button type="button" class="terms-idx-chip on" data-cat="all">すべて<b>'
        f"{n_items}</b></button>"
    ]
    for cat in cat_keys:
        count = len(by_cat[cat])
        chip_lines.append(
            "    "
            f'<button type="button" class="terms-idx-chip" data-cat="{html.escape(cat, quote=True)}">'
            f"{html.escape(cat)}<b>{count}</b></button>"
        )
    chips_html = "\n".join(chip_lines)

    list_items_ld: list[dict] = []
    pos = 1
    for cat in cat_keys:
        for e in sorted(by_cat[cat], key=lambda x: x["title"]):
            list_items_ld.append(
                {
                    "@type": "ListItem",
                    "position": pos,
                    "name": e["title"],
                    "item": public_url(base_url, f"terms/compare/{e['slug_file']}"),
                }
            )
            pos += 1

    ld = {
        "@context": "https://schema.org",
        "@type": "ItemList",
        "name": f"{exam_name()} 比較・整理表一覧",
        "description": "似た制度・用語・演習形式の違いを表で整理した索引です。",
        "numberOfItems": n_items,
        "itemListElement": list_items_ld,
    }

    json_data = json.dumps([compare_index_item_dict(e) for e in entries], ensure_ascii=False)
    tbody_html = render_compare_index_tbody(entries)

    idx_path = Path("terms/compare/index.html")
    page_header = site_page_header(idx_path, current="terms", wide=True)
    page_footer = site_page_footer(idx_path, current="terms", wide=True)
    page_breadcrumb = breadcrumb_html(
        idx_path,
        [("トップ", "index.html"), ("比較・整理表", None)],
    )
    tabs_html = knowledge_hub_tabs_html(current="compare", **knowledge_hub_tab_hrefs(here="compare"))

    canonical = public_url(base_url, "terms/compare/index.html")
    title = f"比較・整理表｜{brand_name()}（{exam_name()}）"
    desc = (
        f"{exam_name()}で混同しやすい制度・用語・演習形式の違いを表で整理。"
        "分野別に検索・絞り込みして、目的の比較ページへ進めます。"
    )
    lead = (
        f"{exam_name()}で押さえたい「似ているが違う」項目を、比較表で横並びに整理しています。"
        "用語解説とあわせて読むと、定義と差分の両方を効率よく確認できます。"
    )

    seo_links = []
    for e in sorted(entries, key=lambda x: (x.get("category") or "", x["title"])):
        href = compare_index_href(e["slug_file"])
        seo_links.append(f'<li><a href="{html.escape(href)}">{html.escape(e["title"])}</a></li>')
    seo_html = '<ul class="terms-idx-seo-list">\n    ' + "\n    ".join(seo_links) + "\n  </ul>"

    return f"""<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(desc)}">
<meta name="robots" content="index, follow">
<link rel="canonical" href="{html.escape(canonical)}">
<meta property="og:type" content="website">
<meta property="og:url" content="{html.escape(canonical)}">
<meta property="og:title" content="{html.escape(title)}">
<meta property="og:description" content="{html.escape(desc)}">
<meta property="og:locale" content="ja_JP">
<script type="application/ld+json">
{json.dumps(ld, ensure_ascii=False, indent=2)}
</script>
{HEAD_FONTS}
<link rel="stylesheet" href="../../site-pages.css?v={TERMS_INDEX_CSS_VER}">
<link rel="stylesheet" href="../../site-theme.css">
<script>document.documentElement.classList.add("js");</script>
</head>
<body class="{shell_body_class('compare-index-page')}" data-compare-total="{n_items}">
{site_page_wrap_open()}
{page_header}
<main class="site-page-main">
  {page_breadcrumb}
  <h1>比較・整理表</h1>
  <p class="site-page-lead">{html.escape(lead)}</p>
  {tabs_html}
  <section class="terms-index-panel compare-index-panel" aria-labelledby="compare-index-heading">
    <div class="terms-index-head">
      <div>
        <h2 id="compare-index-heading">比較一覧</h2>
        <p>全{n_items}件・{n_cats}分野。キーワード検索と分野で絞り込めます。</p>
      </div>
    </div>
    <div class="terms-index-tools">
      <div class="terms-index-tools-primary">
      <label class="terms-index-search" for="compare-idx-q">
        <span class="u-visually-hidden">比較検索</span>
        <input id="compare-idx-q" type="search" inputmode="search" autocomplete="off" placeholder="{html.escape(COMPARE_INDEX_SEARCH_PLACEHOLDER, quote=True)}">
      </label>
      <span id="compare-idx-hit" class="terms-index-hit" aria-live="polite">{n_items} / {n_items} 件</span>
      </div>
      <div class="terms-idx-chips" aria-label="分野フィルタ">
{chips_html}
      </div>
      <button type="button" class="terms-idx-reset hide" id="compare-idx-reset">条件をクリア</button>
      <div class="terms-idx-active-filters hide" id="compare-idx-active-filters" aria-live="polite"></div>
    </div>
    <div class="terms-idx-empty-panel hide" id="compare-idx-empty" role="status" hidden>
      <p class="terms-idx-empty-title">条件に一致する比較がありません</p>
      <p class="terms-idx-empty-hint">検索語を短くするか、分野を「すべて」に戻してお試しください。</p>
      <button type="button" class="terms-idx-reset" id="compare-idx-empty-reset">条件をクリア</button>
    </div>
    <div class="terms-idx-layout" aria-label="比較一覧">
      <div class="terms-idx-table-wrap">
        <table class="terms-idx-table compare-idx-table">
          <thead><tr>
            <th scope="col" class="terms-idx-th-term">比較</th>
            <th scope="col" class="terms-idx-th-cat">分野</th>
            <th scope="col" class="terms-idx-th-def">比較対象</th>
          </tr></thead>
          <tbody id="compare-idx-flat-body">
{tbody_html}
          </tbody>
        </table>
      </div>
      <div class="terms-idx-seo-fallback" aria-hidden="true" hidden>
{seo_html}
      </div>
    </div>
  </section>
</main>
{page_footer}
{site_page_wrap_close()}
<button type="button" class="terms-idx-top compare-idx-top" id="compare-idx-top" aria-label="ページ上部へ">↑</button>
<script type="application/json" id="compare-index-data">{json_data}</script>
<script defer src="../../site-compare-index.js?v={COMPARE_INDEX_JS_VER}"></script>
</body>
</html>
"""


def glossary_term_lookup() -> dict[str, str]:
    if not GLOSSARY_CSV.is_file():
        return {}
    rows = load_glossary_rows()
    used_slugs: dict[str, str] = {}
    entries: list[dict] = []
    for row in rows:
        term = norm(row.get("term"))
        if not term:
            continue
        legacy_slug = norm(row.get("slug")) or norm(row.get("url_slug"))
        if legacy_slug:
            slug_file = f"{legacy_slug}.html"
        else:
            slug_file = term_slug(term, used_slugs) + ".html"
        entries.append({"term": term, "slug_file": slug_file})
    return make_term_lookup(entries)


def build_all(*, base_url: str = BASE_DEFAULT) -> int:
    entries = load_compare_rows()
    term_lookup = glossary_term_lookup()

    COMPARE_DIR.mkdir(parents=True, exist_ok=True)
    for stale in COMPARE_DIR.glob(PRESERVED_COMPARE_GLOB):
        stale.unlink()

    for entry in entries:
        out_file = COMPARE_DIR / entry["slug_file"]
        rel_path = out_file.relative_to(ROOT)
        out_file.write_text(
            build_compare_detail_html(entry, rel_path, base_url, term_lookup),
            encoding="utf-8",
        )

    (COMPARE_DIR / "index.html").write_text(
        build_compare_index(entries, base_url),
        encoding="utf-8",
    )

    print(f"Wrote {len(entries)} compare pages under {COMPARE_DIR}")
    print(f"Wrote {COMPARE_DIR / 'index.html'}")
    return len(entries)


def main() -> int:
    import argparse

    ap = argparse.ArgumentParser()
    ap.add_argument("--base-url", default=BASE_DEFAULT)
    args = ap.parse_args()
    build_all(base_url=args.base_url.rstrip("/"))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (FileNotFoundError, ValueError) as exc:
        print(exc, file=sys.stderr)
        raise SystemExit(1)
