#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
glossary_terms.csv の importance S/A から terms/priority/index.html を生成する。

得点源（S）・頻出（A）の用語だけを一覧し、重要度と分野で絞り込める。
"""

from __future__ import annotations

import html
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from tools.build_glossary_pages import (  # noqa: E402
    HEAD_FONTS,
    TERMS_INDEX_CSS_VER,
    ordered_term_categories,
    public_url,
    terms_index_href,
    terms_index_item_dict,
    terms_index_snippet,
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
from tools.knowledge_hub_tabs import (  # noqa: E402
    IMPORTANCE_LABELS,
    PRIORITY_IMPORTANCE_LEVELS,
    knowledge_hub_tab_hrefs,
    knowledge_hub_tabs_html,
)
from tools.seo_utils import SITEMAP_EXCLUDED_BASENAMES  # noqa: E402
from tools.site_config import brand_name, clean_origin, exam_name  # noqa: E402

PRIORITY_DIR = ROOT / "terms" / "priority"
PRIORITY_INDEX_JS_VER = "20260527-priority-index"
BASE_DEFAULT = clean_origin()

IMPORTANCE_SORT = {"S": 0, "A": 1}


def is_priority_entry(entry: dict) -> bool:
    importance = (entry.get("importance") or "").strip().upper()
    if importance not in PRIORITY_IMPORTANCE_LEVELS:
        return False
    slug_file = entry.get("slug_file") or ""
    if slug_file in SITEMAP_EXCLUDED_BASENAMES:
        return False
    term = (entry.get("term") or "").strip()
    if term.startswith("【"):
        return False
    return True


def filter_priority_entries(entries: list[dict]) -> list[dict]:
    out = [e for e in entries if is_priority_entry(e)]
    return sorted(
        out,
        key=lambda e: (
            IMPORTANCE_SORT.get((e.get("importance") or "").upper(), 9),
            e.get("category") or "",
            e.get("term") or "",
        ),
    )


def importance_label(importance: str) -> str:
    key = (importance or "").strip().upper()
    return IMPORTANCE_LABELS.get(key, key)


def importance_badge_html(importance: str) -> str:
    key = (importance or "").strip().upper()
    label = html.escape(importance_label(key))
    return (
        f'<span class="term-importance-badge term-importance-{html.escape(key.lower())}">'
        f"{label}</span>"
    )


def priority_index_item_dict(entry: dict) -> dict:
    base = terms_index_item_dict(entry)
    imp = (entry.get("importance") or "").strip().upper()
    label = importance_label(imp)
    base["importance"] = imp
    base["importanceLabel"] = label
    base["search"] = f"{base.get('search', '')} {label} {imp}".strip()
    return base


def render_priority_index_tbody(entries: list[dict]) -> str:
    rows: list[str] = []
    for item in entries:
        href = html.escape(terms_index_href(item["slug_file"]))
        href_attr = f' data-entry-href="{href}"'
        snippet = html.escape(terms_index_snippet(item))
        badge = importance_badge_html(item.get("importance") or "")
        rows.append(
            "<tr class=\"terms-idx-table-row priority-idx-table-row\">"
            f'<td class="terms-idx-td-term" data-label="用語"{href_attr} tabindex="0">'
            f'<div class="terms-idx-term-cell"><a href="{href}">{html.escape(item["term"])}</a>'
            f"</div></td>"
            f'<td class="terms-idx-td-importance" data-label="重要度"{href_attr}>{badge}</td>'
            f'<td class="terms-idx-td-cat" data-label="分野"{href_attr}>'
            f'{html.escape(item.get("category") or "")}</td>'
            f'<td class="terms-idx-td-snippet" data-label="定義（抜粋）"{href_attr}>'
            f"{snippet}</td>"
            "</tr>"
        )
    return "\n".join(rows)


def build_priority_index(entries: list[dict], base_url: str) -> str:
    priority_entries = filter_priority_entries(entries)
    by_cat: dict[str, list[dict]] = {}
    by_imp: dict[str, list[dict]] = {"S": [], "A": []}
    for e in priority_entries:
        by_cat.setdefault(e.get("category") or "その他", []).append(e)
        imp = (e.get("importance") or "").upper()
        if imp in by_imp:
            by_imp[imp].append(e)

    cat_keys = ordered_term_categories(by_cat)
    n_terms = len(priority_entries)
    n_cats = len(cat_keys)
    n_s = len(by_imp["S"])
    n_a = len(by_imp["A"])

    imp_chip_lines = [
        '    <button type="button" class="terms-idx-chip on" data-imp="all">すべて<b>'
        f"{n_terms}</b></button>",
        '    <button type="button" class="terms-idx-chip" data-imp="S">得点源<b>'
        f"{n_s}</b></button>",
        '    <button type="button" class="terms-idx-chip" data-imp="A">頻出<b>'
        f"{n_a}</b></button>",
    ]
    imp_chips_html = "\n".join(imp_chip_lines)

    cat_chip_lines = [
        '    <button type="button" class="terms-idx-chip on" data-cat="all">すべて<b>'
        f"{n_terms}</b></button>"
    ]
    for cat in cat_keys:
        count = len(by_cat[cat])
        cat_chip_lines.append(
            "    "
            f'<button type="button" class="terms-idx-chip" data-cat="{html.escape(cat, quote=True)}">'
            f"{html.escape(cat)}<b>{count}</b></button>"
        )
    cat_chips_html = "\n".join(cat_chip_lines)

    seo_links = [
        f'<li><a href="{html.escape(terms_index_href(e["slug_file"]))}">'
        f'{html.escape(e["term"])}（{html.escape(importance_label(e.get("importance") or ""))}）'
        f"</a></li>"
        for e in priority_entries
    ]
    seo_html = (
        '<ul class="terms-idx-seo-list">\n    '
        + "\n    ".join(seo_links)
        + "\n  </ul>"
    )

    list_items_ld: list[dict] = []
    for pos, e in enumerate(priority_entries, start=1):
        list_items_ld.append(
            {
                "@type": "ListItem",
                "position": pos,
                "name": e["term"],
                "item": public_url(base_url, f"terms/{e['slug_file']}"),
            }
        )
    ld = {
        "@context": "https://schema.org",
        "@type": "ItemList",
        "name": f"{exam_name()} 頻出・得点源用語一覧",
        "description": "試験で特に重要な得点源（S）・頻出（A）用語への索引です。",
        "numberOfItems": n_terms,
        "itemListElement": list_items_ld,
    }

    json_data = json.dumps(
        [priority_index_item_dict(e) for e in priority_entries], ensure_ascii=False
    )
    tbody_html = render_priority_index_tbody(priority_entries)

    idx_path = Path("terms/priority/index.html")
    page_header = site_page_header(idx_path, current="terms", wide=True)
    page_footer = site_page_footer(idx_path, current="terms", wide=True)
    page_breadcrumb = breadcrumb_html(
        idx_path,
        [("トップ", "index.html"), ("用語解説", "../index.html"), ("頻出・得点源", None)],
    )
    tabs_html = knowledge_hub_tabs_html(current="priority", **knowledge_hub_tab_hrefs(here="priority"))

    canonical = public_url(base_url, "terms/priority/index.html")
    title = f"頻出・得点源｜{brand_name()}（{exam_name()}）"
    desc = (
        f"{exam_name()}の得点源（S）・頻出（A）用語を一覧し、各解説記事へリンクします。"
        "重要度と分野で絞り込み、試験対策の優先順位づけに使えます。"
    )
    lead = (
        f"{exam_name()}で特に優先して押さえたい用語を、重要度 S（得点源）・A（頻出）に絞って一覧しています。"
        "検索と重要度・分野の絞り込みで、まず読むべき用語から効率よく確認できます。"
    )

    return f"""<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(desc)}">
{ROBOTS_INDEX_FOLLOW}
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
<body class="{shell_body_class('priority-index-page')}" data-priority-total="{n_terms}">
{site_page_wrap_open()}
{page_header}
<main class="site-page-main">
  {page_breadcrumb}
  <h1>頻出・得点源</h1>
  <p class="site-page-lead">{html.escape(lead)}</p>
  {tabs_html}
  <section class="terms-index-panel priority-index-panel" aria-labelledby="priority-index-heading">
    <div class="terms-index-head">
      <div>
        <h2 id="priority-index-heading">重要用語一覧</h2>
        <p>得点源 {n_s} 語・頻出 {n_a} 語（計 {n_terms} 語・{n_cats} 分野）。重要度と分野で絞り込めます。</p>
      </div>
    </div>
    <div class="terms-index-tools">
      <div class="terms-index-tools-primary">
      <label class="terms-index-search" for="priority-idx-q">
        <span class="u-visually-hidden">用語検索</span>
        <input type="search" id="priority-idx-q" class="terms-idx-q" placeholder="例：重要事項説明、建ぺい率、37条書面…" autocomplete="off" enterkeyhint="search">
        <button type="button" class="terms-idx-clear hide" id="priority-idx-clear" aria-label="検索をクリア">×</button>
      </label>
      <p class="terms-idx-hit" id="priority-idx-hit" aria-live="polite">{n_terms} / {n_terms} 語</p>
      </div>
      <div class="terms-idx-chips terms-idx-chips--importance" aria-label="重要度フィルタ">
{imp_chips_html}
      </div>
      <div class="terms-idx-chips" aria-label="分野フィルタ">
{cat_chips_html}
      </div>
      <button type="button" class="terms-idx-reset hide" id="priority-idx-reset">条件をクリア</button>
      <div class="terms-idx-active-filters hide" id="priority-idx-active-filters" aria-live="polite"></div>
    </div>
    <div class="terms-idx-empty-panel hide" id="priority-idx-empty" role="status" hidden>
      <p class="terms-idx-empty-title">条件に一致する用語がありません</p>
      <p class="terms-idx-empty-hint">検索語を短くするか、重要度・分野を「すべて」に戻してお試しください。</p>
      <button type="button" class="terms-idx-reset" id="priority-idx-empty-reset">条件をクリア</button>
    </div>
    <div class="terms-idx-layout" aria-label="頻出・得点源一覧">
      <div class="terms-idx-table-wrap">
        <table class="terms-idx-table priority-idx-table">
          <thead><tr>
            <th scope="col" class="terms-idx-th-term">用語</th>
            <th scope="col" class="terms-idx-th-importance">重要度</th>
            <th scope="col" class="terms-idx-th-cat">分野</th>
            <th scope="col" class="terms-idx-th-def">定義（抜粋）</th>
          </tr></thead>
          <tbody id="priority-idx-flat-body">
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
<button type="button" class="terms-idx-top priority-idx-top" id="priority-idx-top" aria-label="ページ上部へ">↑</button>
<script type="application/json" id="priority-index-data">{json_data}</script>
<script defer src="../../site-priority-index.js?v={PRIORITY_INDEX_JS_VER}"></script>
</body>
</html>
"""


def build_all(*, entries: list[dict], base_url: str = BASE_DEFAULT) -> int:
    PRIORITY_DIR.mkdir(parents=True, exist_ok=True)
    (PRIORITY_DIR / "index.html").write_text(
        build_priority_index(entries, base_url),
        encoding="utf-8",
    )
    n = len(filter_priority_entries(entries))
    print(f"Wrote {PRIORITY_DIR / 'index.html'} ({n} priority terms)")
    return n


def main() -> int:
    from tools.build_glossary_pages import field_hub_slug, load_glossary_rows, norm, term_slug

    rows = load_glossary_rows()
    used: dict[str, str] = {}
    entries: list[dict] = []
    for row in rows:
        term = norm(row.get("term"))
        if not term:
            continue
        legacy_slug = norm(row.get("slug")) or norm(row.get("url_slug"))
        if legacy_slug:
            slug_file = f"{legacy_slug}.html"
        else:
            slug_file = term_slug(term, used) + ".html"
        entries.append(
            {
                "term": term,
                "category": norm(row.get("category")),
                "tags": norm(row.get("tags")),
                "short_def": norm(row.get("short_def")),
                "definition": norm(row.get("definition")),
                "importance": norm(row.get("importance")),
                "slug_file": slug_file,
                "field_hub": field_hub_slug(norm(row.get("category"))),
            }
        )
    build_all(entries=entries)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
