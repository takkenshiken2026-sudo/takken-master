#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""SEO 共通: 信頼性ブロック・用語マッチ・設定読込。"""

from __future__ import annotations

import html
import json
import re
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SEO_CONFIG_PATH = ROOT / "data" / "seo_config.json"

UPDATED_LABEL = "2026年5月19日"
AUTHOR_LABEL = "宅建マスター編集部"

CATEGORY_TO_FIELD: dict[str, str] = {
    "権利関係": "rights",
    "宅建業法": "law",
    "法令上の制限": "limit",
    "税・その他": "tax",
}

FIELD_HUB_META: dict[str, dict[str, str]] = {
    "rights": {
        "name": "権利関係",
        "title": "宅建 権利関係の過去問一覧｜解説付き",
        "description": "宅地建物取引士試験の権利関係（民法等）の過去問を年度別に一覧。意思表示・物権・担保・相続など頻出テーマの解説付き問題へリンクします。",
    },
    "law": {
        "name": "宅建業法",
        "title": "宅建 宅建業法の過去問一覧｜解説付き",
        "description": "宅建業法・宅地建物取引業法の過去問を年度別に一覧。35条書面・37条・媒介契約・広告規制などの解説付き問題へリンクします。",
    },
    "limit": {
        "name": "法令上の制限",
        "title": "宅建 法令上の制限の過去問一覧｜解説付き",
        "description": "都市計画法・建築基準法など法令上の制限の過去問を年度別に一覧。用途地域・建ぺい率・開発許可の解説付き問題へリンクします。",
    },
    "tax": {
        "name": "税・その他",
        "title": "宅建 税・その他の過去問一覧｜解説付き",
        "description": "税金・統計・土地建物など税その他分野の過去問を年度別に一覧。解説付きで無料演習できます。",
    },
}


def load_seo_config() -> dict:
    if not SEO_CONFIG_PATH.is_file():
        return {}
    try:
        return json.loads(SEO_CONFIG_PATH.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}


def primary_source_links_html(max_links: int = 2) -> str:
    from tools.site_config import external_links

    items = external_links()[:max_links]
    if not items:
        return "公式情報・関連法令"
    return "、".join(
        f'<a href="{html.escape(i["url"], quote=True)}" target="_blank" rel="noopener noreferrer">'
        f'{html.escape(i["label"])}</a>'
        for i in items
    )


def trust_table_html(*, anchor_id: str = "trust", compact: bool = False) -> str:
    sources = primary_source_links_html()
    if compact:
        h2 = f'<h2 class="q-h2" id="{html.escape(anchor_id)}">この記事の信頼性について</h2>'
    else:
        h2 = (
            f'<h2 class="term-h2" id="{html.escape(anchor_id)}">'
            '<svg class="term-h2-icon" viewBox="0 0 16 16">'
            '<path d="M8 1l2 4h4l-3 3 1 5-4-2-4 2 1-5-3-3h4z"/></svg>'
            "この記事の信頼性について</h2>"
        )
    return f"""<section class="term-trust-section" aria-labelledby="{html.escape(anchor_id)}">
{h2}
<div class="article-table-wrap"><table class="article-table trust-table"><tbody>
<tr><th scope="row">執筆者</th><td>{html.escape(AUTHOR_LABEL)}</td></tr>
<tr><th scope="row">更新日</th><td>{html.escape(UPDATED_LABEL)}</td></tr>
<tr><th scope="row">主な参照元</th><td>{sources}</td></tr>
</tbody></table></div>
<p class="term-trust-note"><small>試験の日程・合格基準・法令改正は必ず公式情報でご確認ください。</small></p>
</section>"""


def file_lastmod_iso(path: Path) -> str:
    if path.is_file():
        ts = path.stat().st_mtime
        return datetime.fromtimestamp(ts, tz=timezone.utc).strftime("%Y-%m-%d")
    return UPDATED_LABEL.replace("年", "-").replace("月", "-").replace("日", "")[:10]


def normalize_match_text(text: str) -> str:
    return re.sub(r"\s+", "", text or "")


def build_term_match_index(items: list[dict]) -> list[tuple[str, str, str, int]]:
    """(slug, term, reading, priority) のリスト。長い語を先にマッチ。"""
    index: list[tuple[str, str, str, int]] = []
    cfg = load_seo_config()
    priority = set(cfg.get("priorityTerms") or [])
    for item in items:
        slug = (item.get("articleSlug") or str(item.get("id", "")).replace("_", "-")).strip()
        term = str(item.get("term") or "").strip()
        reading = str(item.get("reading") or "").strip()
        if not slug or not term:
            continue
        pri = 10 if slug in priority else len(term)
        index.append((slug, term, reading, pri))
    index.sort(key=lambda x: (-x[3], -len(x[1])))
    return index


def match_terms_in_text(
    text: str,
    term_index: list[tuple[str, str, str, int]],
    *,
    max_hits: int = 4,
) -> list[str]:
    hay = normalize_match_text(text)
    if not hay:
        return []
    found: list[str] = []
    seen: set[str] = set()
    for slug, term, reading, _pri in term_index:
        if slug in seen:
            continue
        if term and term in hay:
            found.append(slug)
            seen.add(slug)
            if len(found) >= max_hits:
                break
            continue
        if reading and reading in hay:
            found.append(slug)
            seen.add(slug)
            if len(found) >= max_hits:
                break
    return found


def extract_theme_label(stem: str, limit: int = 18) -> str:
    s = re.sub(r"\s+", " ", (stem or "").strip())
    if not s:
        return ""
    for sep in ("、", "。", "，", "．", "について", "に関する"):
        if sep in s:
            s = s.split(sep)[0]
            break
    if len(s) > limit:
        return s[:limit].rstrip("、。 ") + "…"
    return s


def field_id_for_category(category: str) -> str | None:
    return CATEGORY_TO_FIELD.get((category or "").strip())


_LEGACY_HEX_SLUG = re.compile(r"^[0-9a-f]{16}$")


def normalize_extracted_term(term: str | None) -> str | None:
    if not term:
        return None
    t = term.strip()
    if t.endswith("とは"):
        t = t[:-2].strip()
    return t or None


def _term_match_key(s: str) -> str:
    return (
        s.replace(" ", "")
        .replace("　", "")
        .replace("・", "")
        .replace("と", "")
        .replace("の", "")
    )


# 旧静的ページの用語名 → 現行 glossary_terms.csv の用語名
# 旧ディレクトリ名 → 用語名（build_readable_term_slug_targets 用）
LEGACY_READABLE_DIR_TERMS: dict[str, str] = {
    "baikai": "媒介契約の種類",
    "baikai-compare": "媒介契約の種類",
    "reins": "レインズ",
}

LEGACY_TERM_ALIASES: dict[str, str] = {
    "報酬限度額": "報酬の計算（売買）",
    "自己所有に属しない物件の制限": "自己所有外物件の制限",
    "手付金・保全措置": "手付金等の保全措置",
    "営業保証金・弁済業務保証金": "営業保証金と弁済業務保証金",
    "宅建 直前対策": "宅建の直前対策",
}


def lookup_term_file(term: str | None, term_to_file: dict[str, str]) -> str | None:
    """用語名から terms/g-*.html を解決（旧ページ表記のゆれを許容）。"""
    t = normalize_extracted_term(term)
    if not t:
        return None
    t = LEGACY_TERM_ALIASES.get(t, t)
    if t in term_to_file:
        return term_to_file[t]
    compact = _term_match_key(t)
    best_key = ""
    best_file: str | None = None
    for key, file in term_to_file.items():
        key_compact = _term_match_key(key)
        if key_compact == compact:
            return file
        if key in t or t in key:
            if len(key) > len(best_key):
                best_key = key
                best_file = file
    if best_file:
        return best_file
    # 旧タイトル略称（例: 宅建 直前対策 → 宅建の直前対策）
    for key, file in term_to_file.items():
        if _term_match_key(key) in compact or compact in _term_match_key(key):
            if len(key) > len(best_key):
                best_key = key
                best_file = file
    return best_file


def extract_term_name_from_legacy_term_html(html: str) -> str | None:
    """旧 terms/{readable-slug}/ の HTML から用語名を抽出。"""
    m = re.search(
        r'"@type"\s*:\s*"DefinedTerm"[^}]*?"name"\s*:\s*"((?:\\.|[^"\\])*)"',
        html,
        re.S,
    )
    if m:
        return normalize_extracted_term(m.group(1).replace("\\/", "/"))
    m = re.search(r'<h1 class="term-h1">([^<]+)', html)
    if m:
        title = m.group(1).strip()
        if "とは" in title:
            title = title.split("とは", 1)[0].strip()
        return normalize_extracted_term(title)
    return None


def glossary_term_file_by_term_name() -> dict[str, str]:
    """用語名 → terms/g-*.html（CSV と build_glossary_pages と同一）。"""
    from tools.build_glossary_pages import load_glossary_rows, norm, term_slug  # noqa: WPS433

    used: dict[str, str] = {}
    out: dict[str, str] = {}
    for row in load_glossary_rows():
        term = norm(row.get("term"))
        if not term:
            continue
        reading = norm(row.get("reading"))
        out[term] = term_slug(term, reading, used) + ".html"
    return out


def build_readable_term_slug_targets() -> dict[str, str]:
    """旧 terms/{readable-slug}/ のディレクトリ名 → /terms/g-*.html。"""
    term_to_file = glossary_term_file_by_term_name()
    targets: dict[str, str] = {}
    terms_dir = ROOT / "terms"
    if not terms_dir.is_dir():
        return targets
    for slug_dir in terms_dir.iterdir():
        if not slug_dir.is_dir():
            continue
        name = slug_dir.name
        if name.startswith("field-") or _LEGACY_HEX_SLUG.fullmatch(name):
            continue
        index = slug_dir / "index.html"
        if not index.is_file():
            continue
        text = index.read_text(encoding="utf-8", errors="replace")
        if name in LEGACY_READABLE_DIR_TERMS:
            term = LEGACY_READABLE_DIR_TERMS[name]
        else:
            refresh = re.search(r'content="0;url=([^"]+)"', text)
            if refresh:
                target = refresh.group(1)
                if "#" not in target.split("/")[-1]:
                    targets[name] = target
                    continue
            term = extract_term_name_from_legacy_term_html(text)
        term_file = lookup_term_file(term, term_to_file)
        if term_file:
            targets[name] = f"/terms/{term_file}"
    return targets


def glossary_term_file_by_legacy_slug() -> dict[str, str]:
    """旧 articleSlug → terms/g-*.html（CSV と同一ロジック）。"""
    from tools.build_glossary_pages import load_glossary_rows, norm, term_slug  # noqa: WPS433

    js_items = load_glossary_items_from_js()
    slug_to_term = {
        (i.get("articleSlug") or str(i.get("id", "")).replace("_", "-")).strip(): str(i.get("term") or "")
        for i in js_items
    }
    used: dict[str, str] = {}
    term_to_file: dict[str, str] = {}
    for row in load_glossary_rows():
        term = norm(row.get("term"))
        if not term:
            continue
        reading = norm(row.get("reading"))
        term_to_file[term] = term_slug(term, reading, used) + ".html"
    out: dict[str, str] = {}
    for leg, term in slug_to_term.items():
        if leg and term in term_to_file:
            out[leg] = term_to_file[term]
    return out


def load_glossary_items_from_js() -> list[dict]:
    js_path = ROOT / "takken-data-glossary.js"
    if not js_path.is_file():
        return []
    text = js_path.read_text(encoding="utf-8")
    m = re.search(r"const\s+GLOSSARY_DATA\s*=\s*(\[.*\])\s*;", text, re.S)
    if not m:
        return []
    try:
        data = json.loads(m.group(1))
    except json.JSONDecodeError:
        return []
    out: list[dict] = []
    seen: set[str] = set()
    for item in data:
        slug = (item.get("articleSlug") or str(item.get("id", "")).replace("_", "-")).strip()
        if not slug or slug in seen:
            continue
        seen.add(slug)
        out.append(item)
    return out


def article_title_for_slug(slug: str) -> str:
    path = ROOT / "takken" / slug / "index.html"
    if not path.is_file():
        return slug.replace("-", " ")
    raw = path.read_text(encoding="utf-8", errors="replace")
    m = re.search(r"<h1[^>]*class=\"article-h1\"[^>]*>([^<]+)", raw)
    if m:
        return re.sub(r"\s+", " ", m.group(1)).strip()
    m = re.search(r"<title>([^<|｜\-]+)", raw)
    return m.group(1).strip() if m else slug.replace("-", " ")
