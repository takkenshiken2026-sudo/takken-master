#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""旧 URL（takken/*, terms/{slug}/, glossary/*）から新 URL へリダイレクト HTML を置く。"""

from __future__ import annotations

import html
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from tools.seo_common import (  # noqa: E402
    build_readable_term_slug_targets,
    glossary_term_file_by_legacy_slug,
)

REDIRECT_HTML = """<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="UTF-8">
<meta http-equiv="refresh" content="0;url={url}">
<link rel="canonical" href="{url}">
<meta name="robots" content="noindex, follow">
<title>移動中…</title>
<script>location.replace({url_js});</script>
</head>
<body>
<p>新しいページへ移動します。<a href="{url}">こちら</a></p>
</body>
</html>
"""


def write_redirect(path: Path, target: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    esc = html.escape(target, quote=True)
    path.write_text(
        REDIRECT_HTML.format(url=esc, url_js=repr(target)),
        encoding="utf-8",
    )


def redirect_terms_legacy() -> int:
    href_map = glossary_term_file_by_legacy_slug()
    count = 0
    for slug, term_file in href_map.items():
        old = ROOT / "terms" / slug / "index.html"
        target = f"/terms/{term_file}"
        write_redirect(old, target)
        count += 1
    return count


def redirect_terms_readable(readable_targets: dict[str, str]) -> int:
    """旧 terms/{読みやすいslug}/ → terms/g-*.html"""
    count = 0
    for slug, target in readable_targets.items():
        write_redirect(ROOT / "terms" / slug / "index.html", target)
        count += 1
    return count


def redirect_glossary_legacy(readable_targets: dict[str, str]) -> int:
    href_map = glossary_term_file_by_legacy_slug()
    count = 0
    glossary_dir = ROOT / "glossary"
    if not glossary_dir.is_dir():
        return 0
    for slug_dir in glossary_dir.iterdir():
        if not slug_dir.is_dir():
            continue
        slug = slug_dir.name
        if slug in readable_targets:
            target = readable_targets[slug]
        elif slug in href_map:
            target = f"/terms/{href_map[slug]}"
        else:
            continue
        write_redirect(slug_dir / "index.html", target)
        count += 1
    return count


def redirect_takken_articles() -> int:
    articles_dir = ROOT / "articles"
    if not articles_dir.is_dir():
        return 0
    count = 0
    takken_dir = ROOT / "takken"
    if not takken_dir.is_dir():
        return 0
    for slug_dir in takken_dir.iterdir():
        if not slug_dir.is_dir():
            continue
        slug = slug_dir.name
        new_path = articles_dir / slug / "index.html"
        if not new_path.is_file():
            continue
        write_redirect(slug_dir / "index.html", f"/articles/{slug}/")
        count += 1
    return count


def redirect_privacy() -> None:
    write_redirect(ROOT / "privacy-terms.html", "/privacy.html")


def main() -> int:
    readable_targets = build_readable_term_slug_targets()
    n_readable = redirect_terms_readable(readable_targets)
    n_terms = redirect_terms_legacy()
    n_glossary = redirect_glossary_legacy(readable_targets)
    n_takken = redirect_takken_articles()
    redirect_privacy()
    print(
        f"legacy redirects: terms-readable/{n_readable}, terms-hash/{n_terms}, "
        f"glossary/{n_glossary}, takken/{n_takken}, privacy-terms.html"
    )
    missing = sum(
        1
        for d in (ROOT / "terms").iterdir()
        if d.is_dir()
        and not d.name.startswith("field-")
        and not re.fullmatch(r"^[0-9a-f]{16}$", d.name)
        and d.name not in readable_targets
    )
    if missing:
        print(
            f"  (warn) readable term dirs without redirect target: {missing}",
            file=sys.stderr,
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
