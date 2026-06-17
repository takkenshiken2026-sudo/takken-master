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


def is_redirect_stub(path: Path) -> bool:
    """既存の実ページ（一覧・各問）を上書きしない。"""
    if not path.is_file():
        return True
    head = path.read_text(encoding="utf-8", errors="replace")[:800].lower()
    return "refresh" in head and "0;url=" in head


def target_exists(target: str) -> bool:
    rel = target.lstrip("/")
    return (ROOT / rel).is_file()


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
        if not target_exists(target):
            print(f"skip legacy redirect (missing target): {kind}/{slug} -> {target}", file=sys.stderr)
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


def redirect_takken_legacy_slugs() -> int:
    """旧 takken/ 配下の非 takken-* slug（通信講座おすすめ等）を現行記事へ。"""
    legacy_map = {
        "takken-tsushin-osusume": "/articles/affiliate-correspondence-course/",
    }
    count = 0
    for slug, target in legacy_map.items():
        write_redirect(ROOT / "takken" / slug / "index.html", target)
        count += 1
    return count


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
    """旧 q/practice/ を q/orig/ へリダイレクト（既存の実ページは維持）。"""
    practice = ROOT / "q" / "practice"
    practice.mkdir(parents=True, exist_ok=True)
    count = 0
    index_path = practice / "index.html"
    if is_redirect_stub(index_path):
        write_redirect(index_path, "/q/orig/")
        count += 1
    seen: set[str] = set()
    for path in sorted(practice.glob("p*/index.html")):
        num = path.parent.name[1:]
        if not num.isdigit() or num in seen:
            continue
        if not is_redirect_stub(path):
            continue
        seen.add(num)
        write_redirect(path, f"/q/orig/id{num}/")
        count += 1
    csv_path = ROOT / "data" / "practice_questions.csv"
    if csv_path.is_file():
        with csv_path.open(encoding="utf-8-sig", newline="") as f:
            for row in csv.DictReader(f):
                qno = (row.get("question_no") or "").strip()
                if not qno.isdigit() or qno in seen:
                    continue
                stub = practice / f"p{qno}" / "index.html"
                if not is_redirect_stub(stub):
                    continue
                seen.add(qno)
                write_redirect(stub, f"/q/orig/id{qno}/")
                count += 1
    return count


def redirect_ichimon_hub() -> None:
    """一問一答静的ハブが無い場合のみ SPA へ誘導（既存の一覧ページは上書きしない）。"""
    path = ROOT / "q" / "ichimon" / "index.html"
    if not path.is_file():
        write_redirect(path, "/#ichimondou")
        return
    head = path.read_text(encoding="utf-8", errors="replace")[:800]
    if "refresh" in head.lower() and "0;url=" in head.lower():
        write_redirect(path, "/#ichimondou")


def main() -> int:
    rows = load_legacy_rows()
    n_readable, n_hash, n_glossary = redirect_from_csv(rows)
    n_takken_legacy = redirect_takken_legacy_slugs()
    n_takken = redirect_takken_articles()
    redirect_privacy()
    n_practice = redirect_practice_to_orig()
    redirect_ichimon_hub()
    print(
        f"legacy redirects: terms-readable/{n_readable}, terms-hash/{n_hash}, "
        f"glossary/{n_glossary}, takken-legacy/{n_takken_legacy}, takken/{n_takken}, practice/{n_practice}, "
        f"privacy-terms.html, ichimon-hub"
    )
    if not rows:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
