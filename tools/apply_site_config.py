#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Apply site-config.json to generated support files and hand-written HTML."""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from tools.site_config import (  # noqa: E402
    brand_mark,
    brand_name,
    clean_origin,
    contact_url,
    exam_name,
    ga4_measurement_id,
    sync_config_files,
)

TEXT_TARGETS = [
    ROOT / "index.html",
    ROOT / "about.html",
    ROOT / "related-sites.html",
    ROOT / "privacy-terms.html",
    ROOT / "site-analytics.js",
]


def replace_common_text(text: str) -> str:
    origin = clean_origin()
    host = origin.replace("https://", "").replace("http://", "").strip("/")
    replacements = [
        ("宅建マスター", brand_name()),
        ("宅地建物取引士試験", exam_name()),
        ("takken-master.jp", host),
        ("https://takken-master.jp", origin),
        ("https://forms.gle/Rfovea3QJhVo24NYA", contact_url()),
        ("G-3F5HESVZ9C", ga4_measurement_id()),
    ]
    for src, dst in replacements:
        text = text.replace(src, dst)
    return text


def ensure_index_config_assets(text: str) -> str:
    """トップページにテンプレート共通の設定・テーマ・GA読み込みを追加する。"""
    text = re.sub(
        r"<!-- Google tag \(gtag\.js\) -->\s*<script async src=\"https://www\.googletagmanager\.com/gtag/js\?id=[^\"]+\"></script>\s*<script>.*?</script>\s*",
        "",
        text,
        count=1,
        flags=re.S,
    )
    if "site-theme.css" not in text:
        text = text.replace(
            "<link rel=\"preconnect\" href=\"https://fonts.googleapis.com\">",
            "<link rel=\"stylesheet\" href=\"site-theme.css\">\n<link rel=\"preconnect\" href=\"https://fonts.googleapis.com\">",
            1,
        )
    if "site-config.js" not in text:
        text = text.replace("</head>", '<script src="site-config.js"></script>\n</head>', 1)
    if "site-analytics.js" not in text:
        text = text.replace(
            "</body>",
            f'<script>window.__GA4_MEASUREMENT_ID__="{ga4_measurement_id()}";</script>\n'
            '<script defer src="site-analytics.js"></script>\n</body>',
            1,
        )
    return text


def update_index_brand_mark(text: str) -> str:
    mark = brand_mark()
    text = re.sub(
        r'(<div class="topnav-logo-mark"[^>]*>)(.*?)(</div>)',
        rf"\1{mark}\3",
        text,
        count=1,
        flags=re.S,
    )
    text = re.sub(
        r'(<span class="site-footer-logo-mark"[^>]*>)(.*?)(</span>)',
        rf"\1{mark}\3",
        text,
        count=1,
        flags=re.S,
    )
    return text


def main() -> int:
    sync_config_files()
    for path in TEXT_TARGETS:
        if not path.is_file():
            continue
        old = path.read_text(encoding="utf-8")
        new = replace_common_text(old)
        if path == ROOT / "index.html":
            new = update_index_brand_mark(ensure_index_config_assets(new))
        if new != old:
            path.write_text(new, encoding="utf-8")
            print(f"Updated {path.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
