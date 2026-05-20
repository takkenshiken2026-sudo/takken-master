#!/usr/bin/env python3
"""Audit public HTML for missing CSS/JS assets and key layout hooks."""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CSS = (ROOT / "site-pages.css").read_text(encoding="utf-8", errors="replace")
SKIP_PREFIX = ("glossary/", "takken/", "terms/")


def is_redirect(text: str) -> bool:
    head = text[:500]
    return "refresh" in head and "0;url=" in head


def main() -> int:
    issues: list[str] = []
    css_classes = set(re.findall(r"\.([a-zA-Z][\w-]*)", CSS))

    for html_path in sorted(ROOT.rglob("*.html")):
        rel = html_path.relative_to(ROOT)
        if any(str(rel).startswith(p) for p in SKIP_PREFIX) and rel.name != "index.html":
            if "field-" in str(rel) or rel.match("terms/g-*.html"):
                continue
        text = html_path.read_text(encoding="utf-8", errors="replace")
        if is_redirect(text):
            continue

        for m in re.finditer(r'<link[^>]+href="([^"]+\.css[^"]*)"', text):
            href = m.group(1).split("?")[0]
            if href.startswith("http"):
                continue
            target = (html_path.parent / href).resolve()
            if not target.is_file():
                issues.append(f"{rel}: missing CSS {href}")

        for m in re.finditer(r'<script[^>]+src="([^"]+\.js[^"]*)"', text):
            href = m.group(1).split("?")[0]
            if href.startswith("http"):
                continue
            target = (html_path.parent / href).resolve()
            if not target.is_file():
                issues.append(f"{rel}: missing JS {href}")

        if "terms-index-panel" in text and "terms-index-panel" not in css_classes:
            issues.append(f"{rel}: HTML uses terms-index-panel but CSS has no rule")
        if "article-index-panel" in text and "article-index-panel" not in css_classes:
            issues.append(f"{rel}: HTML uses article-index-panel but CSS has no rule")
        if "seo-article-main" in text and "seo-article-main" not in css_classes:
            issues.append(f"{rel}: HTML uses seo-article-main but CSS has no rule")

    print(f"Scanned under {ROOT}")
    if not issues:
        print("OK: no UI asset/layout hook issues found.")
        return 0
    print(f"Issues ({len(issues)}):")
    for line in issues[:50]:
        print(" ", line)
    if len(issues) > 50:
        print(f"  ... and {len(issues) - 50} more")
    return 1


if __name__ == "__main__":
    sys.exit(main())
