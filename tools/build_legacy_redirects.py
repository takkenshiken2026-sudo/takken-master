#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""旧 URL 向けリダイレクト HTML を生成（data/legacy_url_redirects.csv + articles/）。"""

from __future__ import annotations

import csv
import html
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

LEGACY_CSV = ROOT / "data" / "legacy_url_redirects.csv"

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


def load_legacy_rows() -> list[dict[str, str]]:
    if not LEGACY_CSV.is_file():
        print(f"Missing {LEGACY_CSV}", file=sys.stderr)
        return []
    with LEGACY_CSV.open(encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def redirect_from_csv(rows: list[dict[str, str]]) -> tuple[int, int, int]:
    n_readable = n_hash = n_glossary = 0
    for row in rows:
        kind = (row.get("legacy_kind") or "").strip()
        slug = (row.get("legacy_slug") or "").strip()
        target = (row.get("target_url") or "").strip()
        if not slug or not target:
            continue
        if kind == "terms_readable":
            write_redirect(ROOT / "terms" / slug / "index.html", target)
            n_readable += 1
        elif kind == "terms_hash":
            write_redirect(ROOT / "terms" / slug / "index.html", target)
            n_hash += 1
        elif kind == "glossary":
            write_redirect(ROOT / "glossary" / slug / "index.html", target)
            n_glossary += 1
    return n_readable, n_hash, n_glossary


def redirect_takken_articles() -> int:
    articles_dir = ROOT / "articles"
    if not articles_dir.is_dir():
        return 0
    count = 0
    for slug_dir in sorted(articles_dir.iterdir()):
        if not slug_dir.is_dir() or slug_dir.name.startswith("."):
            continue
        slug = slug_dir.name
        # 旧 takken/ 配下にあった slug のみ（takken- 接頭辞の移行記事）
        if not slug.startswith("takken-"):
            continue
        if not (slug_dir / "index.html").is_file():
            continue
        write_redirect(ROOT / "takken" / slug / "index.html", f"/articles/{slug}/")
        count += 1
    return count


def redirect_privacy() -> None:
    write_redirect(ROOT / "privacy-terms.html", "/privacy.html")


def redirect_practice_to_orig() -> int:
    """旧 q/practice/ を q/orig/ へリダイレクト（リンク切れ防止）。"""
    practice = ROOT / "q" / "practice"
    if not practice.is_dir():
        return 0
    write_redirect(practice / "index.html", "/q/orig/")
    count = 1
    for path in sorted(practice.glob("p*/index.html")):
        num = path.parent.name[1:]
        if not num.isdigit():
            continue
        write_redirect(path, f"/q/orig/id{num}/")
        count += 1
    return count


def redirect_ichimon_hub() -> None:
    """一問一答静的ハブが無い場合は SPA へ誘導。"""
    write_redirect(ROOT / "q" / "ichimon" / "index.html", "/#ichimondou")


def main() -> int:
    rows = load_legacy_rows()
    n_readable, n_hash, n_glossary = redirect_from_csv(rows)
    n_takken = redirect_takken_articles()
    redirect_privacy()
    n_practice = redirect_practice_to_orig()
    redirect_ichimon_hub()
    print(
        f"legacy redirects: terms-readable/{n_readable}, terms-hash/{n_hash}, "
        f"glossary/{n_glossary}, takken/{n_takken}, practice/{n_practice}, "
        f"privacy-terms.html, ichimon-hub"
    )
    if not rows:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
