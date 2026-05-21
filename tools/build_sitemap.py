#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build sitemap.xml with lastmod for all indexable public HTML pages."""

from __future__ import annotations

import csv
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from tools.site_config import clean_origin  # noqa: E402
from tools.sitemap_utils import SitemapEntry, iso_date, iso_from_mtime, write_sitemap  # noqa: E402

GUIDE_CSV = ROOT / "data" / "guide_articles.csv"
CANONICAL_RE = re.compile(r'<link\s+[^>]*rel=["\']canonical["\'][^>]*>', re.IGNORECASE)
HREF_RE = re.compile(r'href=["\']([^"\']+)["\']', re.IGNORECASE)
ROBOTS_RE = re.compile(
    r'<meta\s+[^>]*name=["\']robots["\'][^>]*content=["\']([^"\']+)["\']',
    re.IGNORECASE,
)


def guide_lastmod_by_slug() -> dict[str, str]:
    out: dict[str, str] = {}
    if not GUIDE_CSV.is_file():
        return out
    text = GUIDE_CSV.read_text(encoding="utf-8-sig")
    for row in csv.DictReader(text.splitlines()):
        slug = (row.get("slug") or "").strip()
        if not slug:
            continue
        for col in ("fact_checked_at", "last_reviewed_at", "source_checked_at"):
            d = iso_date(row.get(col))
            if d:
                out[slug] = d
                break
    return out


def file_url(base: str, path: Path) -> str:
    rel = path.relative_to(ROOT).as_posix()
    if rel == "index.html":
        return f"{base}/"
    return f"{base}/{rel}"


def normalized_url(url: str) -> str:
    text = url.strip()
    if text.endswith("/index.html"):
        text = text[: -len("index.html")]
    return text.rstrip("/")


def canonical_href(html: str, base: str) -> str | None:
    match = CANONICAL_RE.search(html)
    if not match:
        return None
    href_match = HREF_RE.search(match.group(0))
    if not href_match:
        return None
    href = href_match.group(1).strip()
    if href.startswith("/"):
        return f"{base}{href}"
    if href.startswith("http://") or href.startswith("https://"):
        return href
    return None


def is_noindex(html: str) -> bool:
    match = ROBOTS_RE.search(html)
    if not match:
        return False
    directives = {part.strip().lower() for part in match.group(1).split(",")}
    return "noindex" in directives


def article_lastmod(path: Path, guide_dates: dict[str, str]) -> str | None:
    try:
        rel = path.relative_to(ROOT).as_posix()
    except ValueError:
        return None
    parts = rel.split("/")
    if len(parts) == 3 and parts[0] == "articles" and parts[2] == "index.html":
        return guide_dates.get(parts[1])
    return None


def add_indexable_html(
    entries: list[SitemapEntry],
    base: str,
    path: Path,
    guide_dates: dict[str, str],
) -> None:
    html = path.read_text(encoding="utf-8", errors="ignore")
    if is_noindex(html):
        return

    own_url = file_url(base, path)
    canonical = canonical_href(html, base)
    if canonical:
        if not canonical.startswith(f"{base}/") and canonical != base:
            return
        if normalized_url(canonical) != normalized_url(own_url):
            return
        loc = canonical
    else:
        loc = own_url

    entries.append(
        SitemapEntry(
            loc=loc,
            lastmod=article_lastmod(path, guide_dates) or iso_from_mtime(path),
        )
    )


def public_html_paths() -> list[Path]:
    paths: list[Path] = []
    for path in sorted(ROOT.glob("*.html")):
        paths.append(path)
    for dirname in ("articles", "q", "terms"):
        root = ROOT / dirname
        if root.is_dir():
            paths.extend(sorted(root.rglob("*.html")))
    return paths


def collect_entries(base: str) -> list[SitemapEntry]:
    entries: list[SitemapEntry] = []
    guide_dates = guide_lastmod_by_slug()

    for path in public_html_paths():
        add_indexable_html(entries, base, path, guide_dates)

    return entries


def main() -> int:
    import argparse

    ap = argparse.ArgumentParser()
    ap.add_argument("--base-url", default=clean_origin())
    args = ap.parse_args()
    base = args.base_url.rstrip("/")
    entries = collect_entries(base)
    out = ROOT / "sitemap.xml"
    write_sitemap(entries, out)
    with_lastmod = sum(1 for e in entries if e.lastmod)
    print(f"Wrote {out} ({len(entries)} URLs, {with_lastmod} with lastmod)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
