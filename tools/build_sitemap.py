#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generate sitemap.xml from indexable local HTML files."""

from __future__ import annotations

import html
import re
import sys
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
BASE_URL = "https://takken-master.jp"
SITEMAP = ROOT / "sitemap.xml"

EXCLUDED_DIRS = {
    ".git",
    "glossary",  # legacy redirect pages to /terms/
    "tools",  # build scripts and snippets, not public pages
}

CANONICAL_RE = re.compile(
    r'<link[^>]+rel=["\']canonical["\'][^>]+href=["\']([^"\']+)["\']',
    re.IGNORECASE,
)
ROBOTS_RE = re.compile(
    r'<meta[^>]+name=["\']robots["\'][^>]+content=["\']([^"\']+)["\']',
    re.IGNORECASE,
)
REFRESH_RE = re.compile(r'<meta[^>]+http-equiv=["\']refresh["\']', re.IGNORECASE)


def is_excluded(path: Path) -> bool:
    parts = set(path.relative_to(ROOT).parts)
    return bool(parts & EXCLUDED_DIRS)


def local_url_for(path: Path) -> str:
    rel = path.relative_to(ROOT).as_posix()
    if rel == "index.html":
        return f"{BASE_URL}/"
    if rel.endswith("/index.html"):
        return f"{BASE_URL}/{rel[:-10]}/"
    return f"{BASE_URL}/{rel}"


def canonical_to_local_path(url: str) -> Path | None:
    parsed = urlparse(url)
    if f"{parsed.scheme}://{parsed.netloc}" != BASE_URL:
        return None
    request_path = parsed.path
    if request_path == "/":
        candidate = ROOT / "index.html"
    elif request_path.endswith("/"):
        candidate = ROOT / request_path.lstrip("/") / "index.html"
    else:
        candidate = ROOT / request_path.lstrip("/")
    return candidate if candidate.exists() else None


def sitemap_priority(url: str) -> tuple[int, str]:
    path = urlparse(url).path
    if path == "/":
        return (0, path)
    if path.startswith("/articles/"):
        return (1, path)
    if path.startswith("/takken/"):
        return (2, path)
    if path.startswith("/terms/"):
        return (3, path)
    if path.startswith("/q/"):
        return (4, path)
    return (5, path)


def collect_urls() -> list[str]:
    urls: set[str] = set()
    errors: list[str] = []

    for path in sorted(ROOT.rglob("*.html")):
        if is_excluded(path):
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        if REFRESH_RE.search(text):
            continue
        robots_match = ROBOTS_RE.search(text)
        if robots_match and "noindex" in robots_match.group(1).lower():
            continue

        local_url = local_url_for(path)
        canonical_match = CANONICAL_RE.search(text)
        if canonical_match:
            canonical = canonical_match.group(1)
            canonical_path = canonical_to_local_path(canonical)
            if canonical_path is None:
                errors.append(f"Canonical does not map to a local file: {path.relative_to(ROOT)} -> {canonical}")
            else:
                urls.add(canonical)
        else:
            urls.add(local_url)

    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        raise SystemExit("Sitemap generation aborted because canonical URLs are invalid.")

    return sorted(urls, key=sitemap_priority)


def render(urls: list[str]) -> str:
    lines = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for url in urls:
        lines.append("  <url>")
        lines.append(f"    <loc>{html.escape(url, quote=False)}</loc>")
        lines.append("  </url>")
    lines.append("</urlset>")
    lines.append("")
    return "\n".join(lines)


def main() -> None:
    urls = collect_urls()
    SITEMAP.write_text(render(urls), encoding="utf-8")
    print(f"Wrote {SITEMAP.relative_to(ROOT)} with {len(urls)} URLs.")


if __name__ == "__main__":
    main()
