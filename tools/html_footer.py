# -*- coding: utf-8 -*-
"""静的 HTML 用ヘッダー・フッター（相対パス付き）と GA4 共通タグ。"""

from __future__ import annotations

import html
from pathlib import Path

from tools.site_config import (
    brand_mark,
    brand_name,
    contact_url,
    copyright_text,
    exam_name,
    footer_disclaimer,
    ga4_measurement_id,
    navigation_items,
)

FORM_URL = contact_url()
ROBOTS_INDEX_FOLLOW = '<meta name="robots" content="index, follow">'
GA4_MEASUREMENT_ID = ga4_measurement_id()
FOOTER_DISCLAIMER = footer_disclaimer()
SITE_COPYRIGHT = copyright_text()

SITE_HEADER_NAV: list[tuple[str, str, str]] = navigation_items("header")
SITE_FOOTER_NAV: list[tuple[str, str, str]] = navigation_items("footer")

# フッターはサイト直下の絶対パス（どの階層からも同じ遷移先にする）
FOOTER_ROOT_HREFS: frozenset[str] = frozenset(
    {
        "index.html",
        "about.html",
        "q/index.html",
        "terms/index.html",
        "articles/index.html",
        "related-sites.html",
        "privacy.html",
        "privacy-terms.html",
    }
)

SHELL_COLUMN_PAGE_CLASS = "site-shell-column-page"


def shell_body_class(*parts: str) -> str:
    merged: list[str] = []
    for part in parts:
        for token in part.split():
            if token and token not in merged:
                merged.append(token)
    if SHELL_COLUMN_PAGE_CLASS not in merged:
        merged.append(SHELL_COLUMN_PAGE_CLASS)
    return " ".join(merged)


def footer_href(rel_path: Path, site_rel: str) -> str:
    site_rel = site_rel.lstrip("/")
    parent = rel_path.parent
    parts = parent.parts

    # terms/index.html（用語索引）
    if site_rel == "terms/index.html" and parts and parts[0] == "terms":
        if parts == ("terms",):
            return "index.html"
        return "/".join([".."] * (len(parts) - 1)) + "/index.html"

    # terms/ 直下の g-*.html から field-* ハブへ
    if parts == ("terms",) and site_rel.startswith("field-"):
        return site_rel

    # q/index.html（q 配下はカレントが q の index）
    if site_rel == "q/index.html":
        if not parts:
            return "q/index.html"
        if parts[0] == "q":
            depth_under_q = len(parts) - 1
            if depth_under_q <= 0:
                return "index.html"
            return "/".join([".."] * depth_under_q) + "/index.html"
        up = len(parts)
        prefix = "/".join([".."] * up)
        return f"{prefix}/q/index.html" if prefix else "q/index.html"

    # q/past/y20xx/... から年度ハブ（past/y2023/index.html）
    if (
        len(parts) >= 4
        and parts[0] == "q"
        and parts[1] == "past"
        and site_rel.startswith("past/y")
        and site_rel.endswith("/index.html")
    ):
        up = len(parts) - 3
        return ("/".join([".."] * up) + "/index.html") if up else "index.html"

    # q/past/... からの相対（賃管マスター踏襲）
    up = len(parts)
    if (
        len(parts) >= 3
        and parts[0] == "q"
        and parts[1] == "past"
        and site_rel.startswith("q/")
        and site_rel.count("/") == 1
    ):
        up = len(parts) - 1
    prefix = "/".join([".."] * up)
    if not prefix:
        return site_rel
    return prefix + "/" + site_rel


def analytics_snippet(rel_path: Path) -> str:
    """全静的ページ共通: フッター直後（</body> 直前想定）に置く GA4 タグ。"""
    src = html.escape(footer_href(rel_path, "site-analytics.js"))
    mid = html.escape(GA4_MEASUREMENT_ID)
    return (
        "<!-- GA4: tools/html_footer.analytics_snippet（測定IDは GA4_MEASUREMENT_ID） -->\n"
        f'<script>window.__GA4_MEASUREMENT_ID__="{mid}";</script>\n'
        f'<script defer src="{src}"></script>'
    )


def static_q_site_header(*, root_href: str, breadcrumb_items: list[tuple[str, str | None]]) -> str:
    """過去問一覧・個別問題ページ用の q-static ヘッダー。"""
    lis: list[str] = []
    for text, href in breadcrumb_items:
        if href:
            lis.append(f'<li><a href="{html.escape(href)}">{html.escape(text)}</a></li>')
        else:
            lis.append(f'<li aria-current="page">{html.escape(text)}</li>')
    crumbs = "\n      ".join(lis)
    return f"""<header class="q-static-header">
  <p class="q-static-brand"><a href="{html.escape(root_href)}">{html.escape(brand_name())}</a>（{html.escape(exam_name())}）</p>
  <nav aria-label="パンくず">
    <ol class="q-breadcrumb">
      {crumbs}
    </ol>
  </nav>
</header>"""


def static_q_footer_block(rel_path: Path) -> str:
    """過去問静的ページ用フッター + GA4。"""

    def h(dest: str) -> str:
        return html.escape(footer_href(rel_path, dest))

    return f"""<footer class="q-static-footer">
  <nav class="q-static-footer-nav" aria-label="サイトの他ページ">
    <a href="{h("index.html")}">トップ</a>
    <a href="{h("about.html")}">このサイトについて</a>
    <a href="{h("q/index.html")}">過去問一覧</a>
    <a href="{h("terms/index.html")}">用語集</a>
    <a href="{h("articles/index.html")}">試験ガイド</a>
    <a href="{h("related-sites.html")}">関連リンク</a>
    <a href="{h("privacy.html")}">プライバシー</a>
    <a href="{html.escape(FORM_URL)}" target="_blank" rel="noopener noreferrer">お問い合わせ</a>
  </nav>
  <p><small>{html.escape(FOOTER_DISCLAIMER)}</small></p>
  <p><small>{html.escape(SITE_COPYRIGHT)}</small></p>
</footer>
{analytics_snippet(rel_path)}"""


def _breadcrumb_ol(rel_path: Path, items: list[tuple[str, str | None]]) -> str:
    lis: list[str] = []
    for text, href in items:
        if href:
            h = footer_href(rel_path, href) if not href.startswith("http") else href
            lis.append(f'<li><a href="{html.escape(h)}">{html.escape(text)}</a></li>')
        else:
            lis.append(f'<li aria-current="page">{html.escape(text)}</li>')
    crumbs = "\n        ".join(lis)
    return f"""<nav class="site-page-header-crumb" aria-label="パンくず">
      <ol class="q-breadcrumb">
        {crumbs}
      </ol>
    </nav>"""


def site_page_header(
    rel_path: Path,
    *,
    current: str | None = None,
    breadcrumb_items: list[tuple[str, str | None]] | None = None,
    wide: bool = False,
) -> str:
    root = html.escape(footer_href(rel_path, "index.html"))
    nav_links: list[str] = []
    for label, dest, key in SITE_HEADER_NAV:
        if dest.startswith("http"):
            href = dest
            nav_links.append(
                f'<a href="{html.escape(href)}" target="_blank" rel="noopener noreferrer">{html.escape(label)}</a>'
            )
        else:
            href = footer_href(rel_path, dest)
            cur = ' aria-current="page"' if current == key else ""
            nav_links.append(f'<a href="{html.escape(href)}"{cur}>{html.escape(label)}</a>')
    nav_html = "\n          ".join(nav_links)
    crumb_block = ""
    if breadcrumb_items:
        crumb_block = "\n      " + _breadcrumb_ol(rel_path, breadcrumb_items)
    header_class = "site-page-header site-page-header--wide" if wide else "site-page-header"
    return f"""<header class="{header_class}">
      <div class="site-page-header-inner">
        <a class="site-page-brand" href="{root}">
          <span class="site-page-mark" title="サービス略称">{html.escape(brand_mark())}</span>
          <span class="site-page-brand-text">
            <span class="site-page-brand-name">{html.escape(brand_name())}</span>
            <span class="site-page-brand-sub">{html.escape(exam_name())}</span>
          </span>
        </a>
        <nav class="site-page-nav" aria-label="サイト内ナビゲーション">
          {nav_html}
        </nav>
      </div>{crumb_block}
    </header>"""


def _footer_nav_href(rel_path: Path, dest: str) -> str:
    dest = dest.lstrip("/")
    if dest in FOOTER_ROOT_HREFS:
        return "/" + dest
    return footer_href(rel_path, dest)


def site_shell_footer(
    rel_path: Path,
    *,
    include_analytics: bool = True,
) -> str:
    """index.html と同型のフッター（site-pages.css の .site-footer）。"""
    root = html.escape(_footer_nav_href(rel_path, "index.html"))
    mark = html.escape(brand_mark())
    name = html.escape(brand_name())
    title = html.escape(f"{brand_name()}（{exam_name()}対策）トップへ")
    links: list[str] = []
    for label, dest, _key in SITE_FOOTER_NAV:
        if dest.startswith("http"):
            links.append(
                f'<a href="{html.escape(dest)}" target="_blank" rel="noopener noreferrer">'
                f"{html.escape(label)}</a>"
            )
        else:
            href = html.escape(_footer_nav_href(rel_path, dest))
            links.append(f'<a href="{href}">{html.escape(label)}</a>')
    links_html = "\n          ".join(links)
    footer = f"""<footer class="site-footer" role="contentinfo">
    <div class="site-footer-scroll">
      <div class="site-footer-inner">
        <a class="site-footer-brand" href="{root}" title="{title}">
          <span class="site-footer-logo-mark" title="サービス略称">{mark}</span>
          <span class="site-footer-site-name">{name}</span>
        </a>
        <span class="site-footer-sep" aria-hidden="true"></span>
        <nav class="site-footer-legal" aria-label="サイト情報・ポリシー">
          {links_html}
        </nav>
        <span class="site-footer-sep" aria-hidden="true"></span>
        <span class="site-footer-copy">{html.escape(SITE_COPYRIGHT)}</span>
      </div>
    </div>
  </footer>"""
    if include_analytics:
        return footer + "\n" + analytics_snippet(rel_path)
    return footer


def site_page_footer(rel_path: Path, *, current: str | None = None, wide: bool = False) -> str:
    _ = current
    _ = wide
    return site_shell_footer(rel_path, include_analytics=True)


def site_page_wrap_open() -> str:
    return '<div class="site-page-wrap">'


def site_page_wrap_close() -> str:
    return "</div>"


def q_index_tools_open_html(
    *,
    search_label: str,
    search_placeholder: str,
    hit_text: str,
) -> str:
    return (
        '<div class="past-index-tools" aria-label="絞り込み">'
        '<div class="past-index-tools-primary">'
        f'<label class="past-index-search" for="q-index-q">'
        f'<span class="u-visually-hidden">{html.escape(search_label)}</span>'
        f'<input id="q-index-q" type="search" inputmode="search" autocomplete="off" '
        f'placeholder="{html.escape(search_placeholder)}" '
        f'aria-label="{html.escape(search_label)}">'
        "</label>"
        f'<span id="q-index-hit" class="past-index-hit" aria-live="polite">'
        f"{html.escape(hit_text)}</span>"
        "</div>"
        '<div class="past-index-tools-actions">'
        '<button type="button" class="q-index-reset hide" id="q-index-reset">'
        "条件をクリア</button></div>"
        '<div class="q-index-active-filters hide" id="q-index-active-filters" '
        'aria-live="polite"></div>'
    )


def q_index_tools_close_html() -> str:
    return "</div>"


def q_index_stats_line(*, question_count: int, mode: str, year_count: int = 0, category_count: int = 0) -> str:
    n = question_count
    if mode == "practice":
        return f"全{n}問・{category_count}分野"
    if mode == "ichimon":
        return f"全{n}問・{year_count}年度・{category_count}分野"
    return f"全{n}問・{year_count}年度・{category_count}分野"


def q_index_filters_details_html(
    *,
    year_row_label: str,
    year_jump_html: str,
    category_chips_html: str,
    status_chips_html: str,
    show_year_row: bool = True,
    show_category_row: bool = True,
    filters_hint: str = "年度・分野・学習状況",
) -> str:
    year_row = ""
    if show_year_row and year_jump_html.strip():
        year_row = (
            f'<div class="q-index-chips-row q-index-year-row" id="q-index-year-row">'
            f'<span class="q-index-chips-label">{html.escape(year_row_label)}</span>'
            f'<nav class="q-index-chips q-index-year-jump" aria-label="{html.escape(year_row_label)}で移動">'
            f"{year_jump_html}</nav></div>"
        )
    category_row = ""
    if show_category_row:
        category_row = (
            '<div class="q-index-chips-row">'
            '<span class="q-index-chips-label" id="q-index-chips-label">分野</span>'
            f'<div class="q-index-chips" aria-labelledby="q-index-chips-label">'
            f"{category_chips_html}</div></div>"
        )
    return (
        '<details class="q-index-filters-more">'
        '<summary class="q-index-filters-more-summary">'
        '<span class="q-index-filters-more-title">絞り込み</span>'
        f'<span class="q-index-filters-more-hint">{html.escape(filters_hint)}</span>'
        "</summary>"
        '<div class="q-index-filters-more-body">'
        f"{year_row}{category_row}"
        '<div class="q-index-chips-row">'
        '<span class="q-index-chips-label">学習状況</span>'
        f'<div class="q-index-chips q-index-status-chips" role="group" aria-label="学習状況（アプリ連携）">'
        f"{status_chips_html}</div></div></div></details>"
    )


def q_hub_links_html(rel_path: Path, *, current: str) -> str:
    items: list[tuple[str, str, str]] = [
        ("past", "過去問", "q/index.html"),
        ("practice", "実践演習", "q/orig/index.html"),
        ("ichimon", "一問一答", "index.html#ichimondou"),
    ]
    lis: list[str] = []
    for key, label, target in items:
        if key == current:
            lis.append(
                f'<li class="q-hub-tab is-current">'
                f'<span class="q-hub-tab-label" aria-current="page">{html.escape(label)}</span>'
                f"</li>"
            )
        else:
            href = "/" + target.lstrip("/")
            lis.append(
                f'<li class="q-hub-tab">'
                f'<a class="q-hub-tab-label" href="{html.escape(href)}">{html.escape(label)}</a>'
                f"</li>"
            )
    return (
        '<nav class="q-hub-links q-hub-links--tabs" aria-label="問題タイプ">'
        f'<ul class="q-hub-tabs-list">{"".join(lis)}</ul></nav>'
    )


def breadcrumb_html(rel_path: Path, items: list[tuple[str, str | None]]) -> str:
    return _breadcrumb_ol(rel_path, items)
