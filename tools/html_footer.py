# -*- coding: utf-8 -*-
"""宅建マスター静的 HTML 用ヘッダー・フッター（相対パス付き）。"""

from __future__ import annotations

import html
from pathlib import Path

FORM_URL = "https://forms.gle/Rfovea3QJhVo24NYA"
ROBOTS_INDEX_FOLLOW = '<meta name="robots" content="index, follow">'
FOOTER_DISCLAIMER = "学習用のコンテンツです。出題・法令の正確な内容は公式情報で必ず確認してください。"
SITE_COPYRIGHT = "© 2026 宅建マスター学習支援・takken-master.jp"

SITE_HEADER_NAV: list[tuple[str, str, str]] = [
    ("トップ", "index.html", "top"),
    ("このサイトについて", "about.html", "about"),
    ("過去問一覧", "q/index.html", "q"),
    ("用語集", "terms/index.html", "terms"),
    ("関連リンク", "related-sites.html", "related"),
    ("プライバシー", "privacy-terms.html", "privacy"),
]

SITE_FOOTER_NAV: list[tuple[str, str, str]] = [
    ("トップ", "index.html", "top"),
    ("このサイトについて", "about.html", "about"),
    ("過去問一覧", "q/index.html", "q"),
    ("用語集", "terms/index.html", "terms"),
    ("試験ガイド", "articles/index.html", "articles"),
    ("関連リンク", "related-sites.html", "related"),
    ("プライバシー", "privacy-terms.html", "privacy"),
    ("お問い合わせ", FORM_URL, "contact"),
]


def footer_href(rel_path: Path, site_rel: str) -> str:
    site_rel = site_rel.lstrip("/")
    parent = rel_path.parent
    parts = parent.parts

    # terms/<slug>/... → terms/index.html
    if site_rel == "terms/index.html" and parts and parts[0] == "terms":
        if parts == ("terms",):
            return "index.html"
        return "/".join([".."] * (len(parts) - 1)) + "/index.html"

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
  <p class="q-static-brand"><a href="{html.escape(root_href)}">宅建マスター</a>（宅地建物取引士）</p>
  <nav aria-label="パンくず">
    <ol class="q-breadcrumb">
      {crumbs}
    </ol>
  </nav>
</header>"""


def static_q_footer_block(rel_path: Path) -> str:
    """過去問静的ページ用フッター（GA は未設定のため省略）。"""

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
    <a href="{h("privacy-terms.html")}">プライバシー</a>
    <a href="{html.escape(FORM_URL)}" target="_blank" rel="noopener noreferrer">お問い合わせ</a>
  </nav>
  <p><small>{html.escape(FOOTER_DISCLAIMER)}</small></p>
  <p><small>{html.escape(SITE_COPYRIGHT)}</small></p>
</footer>"""


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
          <span class="site-page-mark" title="宅建マスターの略表記">宅建</span>
          <span class="site-page-brand-text">
            <span class="site-page-brand-name">宅建マスター</span>
            <span class="site-page-brand-sub">宅地建物取引士試験</span>
          </span>
        </a>
        <nav class="site-page-nav" aria-label="サイト内ナビゲーション">
          {nav_html}
        </nav>
      </div>{crumb_block}
    </header>"""


def site_page_footer(rel_path: Path, *, current: str | None = None, wide: bool = False) -> str:
    links: list[str] = []
    for label, dest, key in SITE_FOOTER_NAV:
        if dest.startswith("http"):
            href = dest
            links.append(
                f'<a href="{html.escape(href)}" target="_blank" rel="noopener noreferrer">{html.escape(label)}</a>'
            )
        else:
            href = footer_href(rel_path, dest)
            cur = ' aria-current="page"' if current == key else ""
            links.append(f'<a href="{html.escape(href)}"{cur}>{html.escape(label)}</a>')
    links_html = "\n          ".join(links)
    footer_class = "site-page-footer site-page-footer--wide" if wide else "site-page-footer"
    return f"""<footer class="{footer_class}">
      <div class="site-page-footer-inner">
        <div class="site-page-footer-links">
          {links_html}
        </div>
        <span class="site-page-footer-sep" aria-hidden="true"></span>
        <span class="site-page-footer-copy">{html.escape(SITE_COPYRIGHT)}</span>
      </div>
    </footer>"""


def site_page_wrap_open() -> str:
    return '<div class="site-page-wrap">'


def site_page_wrap_close() -> str:
    return "</div>"
