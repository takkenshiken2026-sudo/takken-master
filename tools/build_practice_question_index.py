#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""実践演習一覧 q/orig/index.html（過去問 q/index.html 相当）。"""

from __future__ import annotations

import html
import json
import re
from pathlib import Path

from tools.build_past_question_pages import (  # noqa: E402
    HEAD_FONTS,
    Q_INDEX_CSS_VER,
    ROBOTS_INDEX_FOLLOW,
    glossary_links_for_tags,
    load_glossary_lookup,
    public_url,
    q_index_filter_chip_btn,
    site_page_footer,
    site_page_header,
    site_page_wrap_close,
    site_page_wrap_open,
    stem_preview,
)
from tools.html_footer import breadcrumb_html  # noqa: E402
from tools.orig_units import FIELD_LABELS  # noqa: E402
from tools.past_question_seo import _collection_json_ld  # noqa: E402
from tools.seo_common import trust_table_html  # noqa: E402
from tools.site_config import brand_name, exam_name  # noqa: E402

ORIG_INDEX_TABLE_HEAD = (
    "<thead><tr>"
    '<th scope="col">ID</th><th scope="col">分野</th><th scope="col">レベル</th>'
    '<th scope="col">問題文（抜粋）</th><th scope="col">操作</th>'
    "</tr></thead>"
)


def orig_index_item_dict(page: dict) -> dict:
    preview = stem_preview(page.get("stem_plain") or "")
    tags = page.get("tags") or []
    search_bits = [
        str(page["question_id"]),
        page["category"],
        page["unit_label"],
        f"レベル{page['level']}",
        preview,
        *tags,
    ]
    return {
        "appId": page["question_id"],
        "category": page["category"],
        "level": page["level"],
        "unit": page["unit"],
        "unitLabel": page["unit_label"],
        "field": page.get("field") or "",
        "href": page["href_rel"],
        "preview": preview,
        "tags": tags,
        "correct": page.get("correct"),
        "search": " ".join(x for x in search_bits if x),
        "glossary": page.get("glossary_links") or [],
    }


def build_orig_index_table_row(page: dict) -> str:
    href = html.escape(page["href_rel"])
    qid = page["question_id"]
    preview = stem_preview(page.get("stem_plain") or "")
    preview_cell = (
        html.escape(preview)
        if preview
        else '<span class="q-year-table-desc--empty">問題文は各ページで確認できます</span>'
    )
    app_href = html.escape(f"../../index.html#orig-play-{qid}")
    return (
        '<tr class="q-year-table-row" tabindex="0"'
        f' data-app-id="{qid}"'
        f' data-href="{html.escape(page["href_rel"], quote=True)}"'
        f' data-category="{html.escape(page["category"], quote=True)}"'
        f' data-level="{page["level"]}"'
        f' data-unit="{html.escape(page["unit"], quote=True)}"'
        f' data-field="{html.escape(page.get("field") or "", quote=True)}">'
        f'<td class="q-year-table-no" data-label="ID">'
        f'<a href="{href}">{qid}</a></td>'
        f'<td class="q-year-table-cat" data-label="分野">{html.escape(page["category"])}</td>'
        f'<td class="q-year-table-level" data-label="レベル">L{page["level"]}</td>'
        f'<td class="q-year-table-desc" data-label="問題文">{preview_cell}</td>'
        f'<td class="q-year-table-action" data-label="操作">'
        f'<a class="q-row-link" href="{href}">解説</a> '
        f'<a class="q-row-link q-row-link-app" href="{app_href}">演習</a>'
        "</td></tr>"
    )


def build_orig_q_index(pages: list[dict], base_url: str) -> str:
    glossary_lookup = load_glossary_lookup()
    index_pages: list[dict] = []
    for page in pages:
        pg = dict(page)
        rel = page["rel_path"]
        if rel.startswith("q/orig/"):
            pg["href_rel"] = rel[len("q/orig/") :]
        elif rel.startswith("q/"):
            pg["href_rel"] = rel[2:]
        else:
            pg["href_rel"] = rel
        pg["glossary_links"] = glossary_links_for_tags(pg.get("tags") or [], glossary_lookup)
        index_pages.append(pg)

    by_field: dict[str, list[dict]] = {}
    by_category: dict[str, int] = {}
    by_level: dict[int, int] = {}
    for pg in index_pages:
        fid = pg.get("field") or ""
        by_field.setdefault(fid, []).append(pg)
        by_category[pg["category"]] = by_category.get(pg["category"], 0) + 1
        by_level[pg["level"]] = by_level.get(pg["level"], 0) + 1
    for fid in by_field:
        by_field[fid].sort(key=lambda x: (x["unit"], x["question_id"]))

    field_blocks: list[str] = []
    field_jump_links: list[str] = []
    open_fields = set(list(FIELD_LABELS.keys())[:2])

    for fid in ("rights", "law", "limit", "tax"):
        field_pages = by_field.get(fid, [])
        if not field_pages:
            continue
        label = FIELD_LABELS[fid]
        field_jump_links.append(
            f'<a class="q-index-filter-opt q-index-field-link" href="#field-{fid}" data-field="{fid}">'
            f'{html.escape(label)}<span class="q-index-filter-count">（{len(field_pages)}）</span></a>'
        )
        by_unit: dict[str, list[dict]] = {}
        for pg in field_pages:
            by_unit.setdefault(pg["unit"], []).append(pg)

        unit_sections: list[str] = []
        for uid in sorted(by_unit.keys(), key=lambda u: by_unit[u][0]["unit_label"]):
            unit_pages = by_unit[uid]
            ulabel = unit_pages[0]["unit_label"]
            rows_html = "".join(build_orig_index_table_row(pg) for pg in unit_pages)
            unit_sections.append(
                f'<section class="q-index-unit-block" id="unit-{html.escape(uid, quote=True)}"'
                f' data-field="{html.escape(fid, quote=True)}">'
                f'<h3 class="q-index-unit-heading">'
                f'<a href="unit/{html.escape(uid)}/index.html">{html.escape(ulabel)}</a>'
                f' <span class="q-index-unit-count">{len(unit_pages)}問</span></h3>'
                f'<div class="q-year-table-wrap">'
                f'<table class="q-year-table" aria-labelledby="unit-{html.escape(uid, quote=True)}-h">'
                f"{ORIG_INDEX_TABLE_HEAD}<tbody>{rows_html}</tbody></table></div></section>"
            )

        expanded = "true" if fid in open_fields else "false"
        collapsed = "" if fid in open_fields else " is-collapsed"
        field_blocks.append(
            f'<section class="q-index-field-block{collapsed}" id="field-{fid}">'
            f'<div class="q-index-year-head">'
            f'<div class="q-index-year-head-main">'
            f'<button type="button" class="q-index-year-toggle" aria-expanded="{expanded}" '
            f'aria-controls="field-body-{fid}">'
            f'<span class="q-index-year-chevron" aria-hidden="true"></span></button>'
            f'<h2 id="field-{fid}-heading">{html.escape(label)}</h2>'
            f"</div>"
            f'<span class="q-index-year-count" data-total="{len(field_pages)}">'
            f"{len(field_pages)}問</span></div>"
            f'<div class="q-index-field-body" id="field-body-{fid}">{"".join(unit_sections)}</div>'
            f"</section>"
        )

    json_data = json.dumps([orig_index_item_dict(pg) for pg in index_pages], ensure_ascii=False)
    category_chips = [
        q_index_filter_chip_btn("q-orig-chip-btn", "data-cat", "all", "すべて", on=True)
    ]
    for cat, count in sorted(by_category.items()):
        category_chips.append(
            q_index_filter_chip_btn("q-orig-chip-btn", "data-cat", cat, cat, count=count)
        )
    level_chips = [q_index_filter_chip_btn("q-orig-level-btn", "data-level", "all", "すべて", on=True)]
    for lv in sorted(by_level.keys()):
        level_chips.append(
            q_index_filter_chip_btn(
                "q-orig-level-btn", "data-level", str(lv), f"レベル{lv}", count=by_level[lv]
            )
        )
    status_chips = [
        q_index_filter_chip_btn("q-orig-status-btn", "data-status", "all", "すべて", on=True),
        q_index_filter_chip_btn("q-orig-status-btn", "data-status", "wrong", "不正解"),
        q_index_filter_chip_btn("q-orig-status-btn", "data-status", "bookmark", "ブックマーク"),
    ]

    rel_path = Path("q/orig/index.html")
    header = site_page_header(rel_path, current="practice")
    crumb = breadcrumb_html(
        rel_path,
        [("トップ", "index.html"), ("問題一覧", "q/index.html"), ("実践演習", None)],
    )
    footer = site_page_footer(rel_path, current="practice")
    trust = trust_table_html(anchor_id="trust", compact=True)

    page_title = f"実践演習一覧｜{brand_name()}（{exam_name()}）"
    page_desc = (
        f"{exam_name()}の実践演習{len(pages)}問を単元別・分野別・レベル別に掲載。"
        "検索と絞り込みのあと、各問題の解説ページへ進めます。"
    )
    canonical = public_url(base_url, "q/orig/index.html")
    list_items = [
        (f"{p['unit_label']} #{p['question_id']}", f"{base_url.rstrip('/')}/{p['rel_path']}")
        for p in sorted(index_pages, key=lambda x: x["question_id"])[:100]
    ]
    json_ld = _collection_json_ld(
        canonical=canonical, title=page_title, desc=page_desc, items=list_items, site_url=base_url
    )

    page_lead = (
        f"{html.escape(exam_name())}の実践演習全{len(pages)}問を掲載しています。"
        "キーワード検索と分野・レベルで絞り込み、解説ページで正誤と解説を確認できます。"
        ' <a href="../index.html">過去問一覧</a>・'
        '<a href="../mock/index.html">オリジナル模試</a>も利用できます。'
    )

    return f"""<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{html.escape(page_title)}</title>
<meta name="description" content="{html.escape(page_desc)}">
<meta property="og:title" content="{html.escape(page_title)}">
<meta property="og:description" content="{html.escape(page_desc)}">
{ROBOTS_INDEX_FOLLOW}
<link rel="canonical" href="{html.escape(canonical)}">
{HEAD_FONTS}
<link rel="stylesheet" href="../../site-pages.css?v={Q_INDEX_CSS_VER}">
<link rel="stylesheet" href="../../site-theme.css">
{json_ld}
</head>
<body class="q-index-page q-orig-index-page">
{site_page_wrap_open()}
{header}
<main class="site-page-main">
  {crumb}
  <h1>実践演習</h1>
  <p class="site-page-lead">{page_lead}</p>
  {trust}
  <section class="past-index-panel" aria-labelledby="orig-index-heading">
    <div class="past-index-head">
      <div>
        <h2 id="orig-index-heading">実践演習一覧</h2>
        <p>全{len(pages)}問・{len(by_category)}分野・{len({pg["unit"] for pg in index_pages})}単元。キーワード検索と絞り込みで探せます。</p>
      </div>
      <span id="q-orig-hit" class="past-index-hit" aria-live="polite">{len(pages)} / {len(pages)} 問</span>
    </div>
    <div class="past-index-tools" aria-label="絞り込み">
      <label class="past-index-search" for="q-orig-q">
        <span>実践演習を検索</span>
        <input id="q-orig-q" type="search" inputmode="search" autocomplete="off" placeholder="例：ID、単元名、問題文…">
      </label>
      <div class="past-index-tools-actions">
        <button type="button" class="q-index-reset hide" id="q-orig-reset">条件をクリア</button>
      </div>
      <div class="q-index-active-filters hide" id="q-orig-active-filters" aria-live="polite"></div>
      <div class="q-index-chips-row q-index-year-row" id="q-orig-field-row">
        <span class="q-index-chips-label">分野</span>
        <nav class="q-index-chips q-index-field-jump" aria-label="分野で移動">{"".join(field_jump_links)}</nav>
      </div>
      <div class="q-index-chips-row">
        <span class="q-index-chips-label">分野絞り込み</span>
        <div class="q-index-chips">{"".join(category_chips)}</div>
      </div>
      <div class="q-index-chips-row">
        <span class="q-index-chips-label">レベル</span>
        <div class="q-index-chips">{"".join(level_chips)}</div>
      </div>
      <div class="q-index-chips-row">
        <span class="q-index-chips-label">学習状況</span>
        <div class="q-index-chips q-index-status-chips">{"".join(status_chips)}</div>
      </div>
    </div>
    <div class="q-index-empty-panel hide" id="q-orig-empty" role="status">
      <p class="q-index-empty-title">条件に一致する問題がありません</p>
      <p class="q-index-empty-hint">検索語を短くするか、分野・レベルを「すべて」に戻してお試しください。</p>
      <button type="button" class="q-index-reset" id="q-orig-empty-reset">条件をクリア</button>
    </div>
    <div class="q-index-layout">
      <div class="q-index-content">
        <section class="q-index-fields q-index-view-panel" id="q-orig-view-unit" aria-label="単元別実践演習">{"".join(field_blocks)}</section>
        <section class="q-index-view-panel hide" id="q-orig-view-flat" aria-label="実践演習フラット一覧">
          <div class="q-year-table-wrap">
            <table class="q-year-table">
              {ORIG_INDEX_TABLE_HEAD}
              <tbody id="q-orig-flat-body"></tbody>
            </table>
          </div>
        </section>
        <nav class="q-index-pagination hide" id="q-orig-pagination" aria-label="ページ送り"></nav>
      </div>
    </div>
  </section>
</main>
{footer}
{site_page_wrap_close()}
<button type="button" class="q-index-top" id="q-orig-top" aria-label="ページ上部へ">↑</button>
<script type="application/json" id="q-orig-index-data">{json_data}</script>
<script defer src="../../site-q-orig-index.js"></script>
</body>
</html>"""
