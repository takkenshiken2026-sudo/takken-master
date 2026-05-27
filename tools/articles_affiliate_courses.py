# -*- coding: utf-8 -*-
"""A8 宅建講座アフィリエイト記事で共通利用する講座データ・画像・UI部品."""

from __future__ import annotations

import html
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COURSE_IMAGE_DIR = ROOT / "images" / "courses"
COURSE_IMAGE_REL = "../../images/courses/"

COURSE_IMAGE_SIZES: dict[str, tuple[int, int]] = {
    "shikakutaisaku": (700, 329),
    "onsuku": (545, 307),
    "square": (800, 418),
    "yotsuya": (960, 402),
}

COURSE_PRODUCTS: list[dict[str, str]] = [
    {
        "id": "shikakutaisaku",
        "rank": "第一候補",
        "name": "資格対策ドットコム",
        "tag": "低価格オンライン",
        "style": "オンライン完結・費用を抑えたい人向け",
        "href": (
            "https://px.a8.net/svt/ejp?a8mat=4B3TF0+DRY3OY+3L4C+BW0YB"
            "&a8ejpredirect=https%3A%2F%2Fwww.shikakutaisaku.com%2Fpersonal%2Ftakken.html"
        ),
        "cta": "資格対策ドットコムの宅建講座を確認する",
        "audience_short": "独学の補助として安く始めたい人",
    },
    {
        "id": "onsuku",
        "rank": "月額制",
        "name": "オンスク.JP",
        "tag": "まず安く試す",
        "style": "月額制・スキマ時間に講義",
        "href": (
            "https://px.a8.net/svt/ejp?a8mat=4B3TF0+DUX9PU+408S+BW0YB"
            "&a8ejpredirect=https%3A%2F%2Fonsuku.jp%2Ftraining%2Ftakkenshi"
        ),
        "cta": "オンスク.JPの宅建講座を確認する",
        "audience_short": "月額制で試したい人",
    },
    {
        "id": "square",
        "rank": "通信講座",
        "name": "資格スクエア",
        "tag": "しっかり比較",
        "style": "通信講座型・カリキュラム重視",
        "href": (
            "https://px.a8.net/svt/ejp?a8mat=4B3TF0+DXB04Y+373C+BW0YB"
            "&a8ejpredirect=https%3A%2F%2Fwww.shikaku-square.com%2Ftakken"
        ),
        "cta": "資格スクエアの宅建講座を確認する",
        "audience_short": "講座として比較したい人",
    },
    {
        "id": "yotsuya",
        "rank": "サポート",
        "name": "四谷学院",
        "tag": "安心感重視",
        "style": "サポート充実・質問しやすい",
        "href": (
            "https://px.a8.net/svt/ejp?a8mat=4B3TF0+DRCO36+5IEI+BW0YB"
            "&a8ejpredirect=https%3A%2F%2Fyotsuyagakuin-tsushin.com%2Ftakken%2F"
        ),
        "cta": "四谷学院の宅建講座を確認する",
        "audience_short": "サポートを重視したい人",
    },
]

TSUSHIN_RANK_LABELS = ("1位", "2位", "3位", "4位")


def course_products_ranked() -> list[dict[str, str]]:
    return [{**product, "rank": TSUSHIN_RANK_LABELS[index]} for index, product in enumerate(COURSE_PRODUCTS)]


def affiliate_attrs() -> str:
    return 'target="_blank" rel="nofollow sponsored noopener noreferrer"'


def resolve_course_image_src(product_id: str) -> str | None:
    for ext in (".webp", ".jpg", ".jpeg", ".png"):
        path = COURSE_IMAGE_DIR / f"course-{product_id}{ext}"
        if path.is_file():
            return f"{COURSE_IMAGE_REL}{path.name}"
    return None


def course_image_html(
    product: dict[str, str],
    *,
    hero: bool = False,
    section: bool = False,
    thumb: bool = False,
    eager: bool = False,
) -> str:
    name = product["name"]
    alt = html.escape(f"{name}の宅建講座")
    src = resolve_course_image_src(product["id"])
    width, height = COURSE_IMAGE_SIZES.get(product["id"], (640, 360))
    if src:
        if hero:
            css = "affiliate-course-hero-image"
            sizes = "(max-width: 760px) 42vw, 220px"
        elif thumb:
            css = "affiliate-course-table-thumb"
            sizes = "72px"
        else:
            css = "affiliate-course-section-image"
            sizes = "(max-width: 760px) 100vw, 720px"
        loading = "eager" if eager else "lazy"
        priority = ' fetchpriority="high"' if eager else ""
        return (
            f'<img class="{css}" src="{html.escape(src)}" alt="{alt}" '
            f'width="{width}" height="{height}" sizes="{sizes}" '
            f'loading="{loading}" decoding="async"{priority}>'
        )
    if hero:
        size = "affiliate-course-placeholder--hero"
    elif thumb:
        size = "affiliate-course-placeholder--thumb"
    else:
        size = "affiliate-course-placeholder--section"
    return (
        f'<div class="affiliate-course-placeholder affiliate-course-placeholder--{product["id"]} {size}" '
        f'role="img" aria-label="{alt}">'
        f'<span class="affiliate-course-placeholder-name">{html.escape(name)}</span>'
        f'<span class="affiliate-course-placeholder-tag">{html.escape(product["tag"])}</span>'
        f"</div>"
    )


def affiliate_pr_notice_html() -> str:
    return (
        '<p class="affiliate-pr-notice" role="note">'
        "この記事には広告・PR（アフィリエイト）を含みます。"
        "</p>"
    )


def affiliate_cta(href: str, label: str) -> str:
    return (
        f'<p class="affiliate-cta-wrap">'
        f'<a class="affiliate-cta-btn" href="{html.escape(href)}" {affiliate_attrs()}>'
        f"{html.escape(label)}</a></p>"
    )


def course_section_visual(product: dict[str, str]) -> str:
    image = course_image_html(product, section=True)
    return (
        f'<div class="affiliate-course-section-visual">'
        f'<a class="affiliate-course-section-link" href="{product["href"]}" {affiliate_attrs()}>{image}</a>'
        f"</div>"
    )


def course_section(product: dict[str, str], section_num: int, heading: str, body_html: str) -> str:
    anchor = f"pick-{product['id']}"
    return f"""
<section class="seo-article-section" aria-labelledby="{anchor}">
<h2 id="{anchor}"><span class="section-heading-num">{section_num}</span>{html.escape(heading)}</h2>
{course_section_visual(product)}
{body_html}
{affiliate_cta(product['href'], product['cta'])}
</section>"""


def course_hero_html(
    *,
    section_id: str,
    heading: str,
    note_html: str,
    products: list[dict[str, str]],
    foot_href: str,
    foot_label: str,
    primary_id: str = "shikakutaisaku",
) -> str:
    attrs = affiliate_attrs()
    items: list[str] = []
    for index, product in enumerate(products):
        primary = " affiliate-course-hero-item--primary" if product["id"] == primary_id else ""
        image = course_image_html(product, hero=True, eager=index == 0)
        items.append(
            f"""<a class="affiliate-course-hero-item affiliate-course-hero-item--{product['id']}{primary}" href="{product['href']}" {attrs}>
<span class="affiliate-course-hero-rank">{html.escape(product['rank'])}</span>
<div class="affiliate-course-hero-media">{image}</div>
<span class="affiliate-course-hero-name">{html.escape(product['name'])}</span>
<span class="affiliate-course-hero-tag">{html.escape(product['tag'])}</span>
</a>"""
        )
    return f"""
<section class="affiliate-course-hero" id="{section_id}" aria-labelledby="{section_id}-title">
<h2 id="{section_id}-title" class="affiliate-course-hero-heading">{html.escape(heading)}</h2>
<p class="affiliate-course-hero-note">{note_html}</p>
<div class="affiliate-course-hero-grid" role="list">{"".join(items)}</div>
<p class="affiliate-course-hero-foot"><a href="{html.escape(foot_href)}">{html.escape(foot_label)}</a></p>
</section>""".strip()


def course_compare_table_rows(products: list[dict[str, str]]) -> str:
    attrs = affiliate_attrs()
    rows: list[str] = []
    for product in products:
        thumb = course_image_html(product, thumb=True)
        link = f'<a href="{product["href"]}" class="affiliate-table-cell-link" {attrs}>'
        rows.append(
            f"""<tr class="affiliate-course-table-row">
<td class="affiliate-course-table-rank">{html.escape(product['rank'])}</td>
<td class="affiliate-course-table-thumb">{link}{thumb}</a></td>
<td>{link}<span class="affiliate-course-table-name">{html.escape(product['name'])}</span></a></td>
<td>{link}{html.escape(product['style'])}</a></td>
<td>{link}<strong>{html.escape(product['audience_short'])}</strong></a></td>
<td class="affiliate-course-table-action">{link}<span class="affiliate-table-btn">詳細を見る</span></a></td>
</tr>"""
        )
    return "".join(rows)


def course_compare_cards(products: list[dict[str, str]]) -> str:
    attrs = affiliate_attrs()
    cards: list[str] = []
    for product in products:
        image = course_image_html(product, section=True)
        cards.append(
            f"""<a class="affiliate-course-card" href="{product['href']}" {attrs}>
<span class="affiliate-course-card-rank">{html.escape(product['rank'])}</span>
<div class="affiliate-course-card-media">{image}</div>
<div class="affiliate-course-card-body">
<span class="affiliate-course-card-name">{html.escape(product['name'])}</span>
<span class="affiliate-course-card-style">{html.escape(product['style'])}</span>
<span class="affiliate-course-card-audience">{html.escape(product['audience_short'])}</span>
<span class="affiliate-course-card-cta">講座を確認する</span>
</div>
</a>"""
        )
    return f'<div class="affiliate-course-card-grid" role="list">{"".join(cards)}</div>'
