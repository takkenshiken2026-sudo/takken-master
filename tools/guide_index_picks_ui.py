#!/usr/bin/env python3
"""試験ガイド・用語・過去問一覧に共通のおすすめ講座・教材カード HTML。"""

from __future__ import annotations

import html
from pathlib import Path

from tools.site_config import brand_name, exam_name, guide_index_picks


def apply_vars(value: str) -> str:
    text = (value or "").strip()
    return (
        text.replace("Sampleマスター", brand_name())
        .replace("◯◯試験（プレースホルダー）", exam_name())
        .replace("◯◯試験", exam_name())
    )


def guide_index_pick_href(href: str, rel_path: Path) -> str:
    raw = (href or "").strip()
    if not raw:
        return ""
    if raw.startswith(("http://", "https://", "/")):
        return raw
    if raw.startswith("../"):
        return raw
    hub = rel_path.parent.name if rel_path.parent != Path(".") else ""
    if hub == "articles":
        return raw.lstrip("/")
    article_href = raw.lstrip("/")
    if not article_href.startswith("articles/"):
        article_href = f"articles/{article_href}"
    return f"../{article_href}"


def guide_index_pick_image_src(image: str, rel_path: Path) -> str:
    raw = (image or "").strip()
    if not raw:
        return ""
    if raw.startswith(("http://", "https://", "/")):
        return raw
    if raw.startswith("../"):
        return raw
    depth = len(rel_path.parent.parts)
    prefix = "/".join([".."] * depth) + "/" if depth else ""
    return f"{prefix}{raw.lstrip('/')}"


def build_guide_index_pick_image_html(
    item: dict[str, str],
    *,
    title: str,
    rel_path: Path,
) -> str:
    image = (item.get("image") or "").strip()
    if not image:
        return ""
    src = guide_index_pick_image_src(image, rel_path)
    alt = (item.get("imageAlt") or title or "おすすめ教材").strip()
    kind = (item.get("kind") or "textbook").strip()
    media_kind = "course" if kind == "course" else "book"
    if media_kind == "course":
        size_attrs = 'width="320" height="180"'
    else:
        size_attrs = 'width="160" height="220"'
    return (
        f'<div class="article-index-pick-media article-index-pick-media--{media_kind}">'
        f'<img src="{html.escape(src, quote=True)}" alt="{html.escape(alt)}" '
        f'{size_attrs} loading="lazy" decoding="async">'
        f"</div>"
    )


def build_guide_index_picks_html(rel_path: Path) -> str:
    picks = guide_index_picks()
    if not picks:
        return ""
    cards: list[str] = []
    for item in picks["items"]:
        href = guide_index_pick_href(apply_vars(item["href"]), rel_path)
        title = apply_vars(item["title"])
        description = apply_vars(item.get("description") or "")
        kind = html.escape(item.get("kind") or "textbook", quote=True)
        kind_label = html.escape(apply_vars(item.get("kindLabel") or "教材"))
        cta = html.escape(apply_vars(item.get("cta") or "記事を読む"))
        external = href.startswith("http://") or href.startswith("https://")
        rel_attr = ' rel="noopener noreferrer"' if external else ""
        target_attr = ' target="_blank"' if external else ""
        image_html = build_guide_index_pick_image_html(item, title=title, rel_path=rel_path)
        cards.append(
            f'<article class="article-index-pick" data-pick-kind="{kind}">'
            f'<a class="article-index-pick-link" href="{html.escape(href, quote=True)}"{target_attr}{rel_attr}>'
            + image_html
            + f"<h3>{html.escape(title)}</h3>"
            + (f"<p>{html.escape(description)}</p>" if description else "")
            + '<div class="article-index-pick-foot">'
            + f'<span class="article-index-pick-cta">{cta}</span>'
            + f'<span class="article-index-pick-kind">{kind_label}</span>'
            + "</div>"
            + "</a></article>"
        )
    lead = apply_vars(picks.get("lead") or "")
    lead_html = f"<p>{html.escape(lead)}</p>" if lead else ""
    return (
        '<section class="article-index-picks" aria-labelledby="article-index-picks-heading">'
        '<div class="article-index-picks-head">'
        f'<h2 id="article-index-picks-heading">{html.escape(apply_vars(picks["title"]))}</h2>'
        f"{lead_html}"
        "</div>"
        f'<div class="article-index-picks-grid">{"".join(cards)}</div>'
        "</section>"
    )
