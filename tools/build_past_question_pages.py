#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
静的問題ページ q/past/... と q/index.html を生成する。

優先順位:
1. data/past_questions.csv（賃管マスターと同一ヘッダー）
2. CSV が空なら takken-master-data.js の BASE_QUESTIONS を自動利用（--no-js-fallback で無効化）

データがどちらも無いときは q/index.html にプレースホルダーのみ出力する。
"""

from __future__ import annotations

import csv
import html
import json
import re
import shutil
import sys
from pathlib import Path
from xml.sax.saxutils import escape as xml_escape

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from tools.html_footer import (  # noqa: E402
    ROBOTS_INDEX_FOLLOW,
    breadcrumb_html,
    site_page_footer,
    site_page_header,
    site_page_wrap_close,
    site_page_wrap_open,
    static_q_footer_block,
    static_q_site_header,
)
from tools.past_question_seo import (  # noqa: E402
    build_field_hub_html,
    build_year_hub_html,
    enrich_pages,
    hub_links_html,
    nav_adjacent_html,
    page_meta_description,
    page_title_mid,
    q_list_table_html,
    q_year_index_summary_html,
    question_json_ld,
    related_terms_html,
)
from tools.site_config import brand_name, clean_origin, exam_name  # noqa: E402
from tools.seo_common import trust_table_html  # noqa: E402

DATA_CSV_DEFAULT = ROOT / "data" / "past_questions.csv"
MASTER_JS_DEFAULT = ROOT / "takken-master-data.js"
Q_ROOT = ROOT / "q"
BASE_DEFAULT = clean_origin()

FIELD_LABELS_JS = {
    "rights": "権利関係",
    "law": "宅建業法",
    "limit": "法令上の制限",
    "tax": "税・その他",
}

LABELS = [("ア", "statement_a"), ("イ", "statement_b"), ("ウ", "statement_c"), ("エ", "statement_d")]

HEAD_FONTS = """<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@400;500;600;700&display=swap" rel="stylesheet">"""

Q_INDEX_CSS_VER = "20260521-index-layout"
GLOSSARY_CSV = ROOT / "data" / "glossary_terms.csv"


def norm(s: str | None) -> str:
    return (s or "").strip()


def parse_correct(raw: str) -> int | None:
    raw = norm(raw)
    if not raw:
        return None
    try:
        n = int(raw)
    except ValueError:
        return None
    if 1 <= n <= 4:
        return n
    return None


def build_stem_html(row: dict) -> str:
    parts: list[str] = []
    stem = norm(row.get("stem"))
    preamble = norm(row.get("preamble"))
    br = "<br>\n"
    if stem:
        parts.append(f"<p>{html.escape(stem).replace(chr(10), br)}</p>")
    if preamble:
        parts.append(f"<p>{html.escape(preamble).replace(chr(10), br)}</p>")
    stmts: list[tuple[str, str]] = []
    for lab, key in LABELS:
        t = norm(row.get(key))
        if t:
            stmts.append((lab, t))
    if stmts:
        lis = "".join(
            f"<li><strong>{html.escape(lab)}</strong> {html.escape(t).replace(chr(10), br)}</li>"
            for lab, t in stmts
        )
        parts.append(f'<ol class="q-stmt-list" style="list-style:none;padding-left:0;">{lis}</ol>')
    return "\n".join(parts) if parts else "<p>（問題文なし）</p>"


def meta_description(text: str, limit: int = 155) -> str:
    one = re.sub(r"\s+", " ", text).strip()
    if len(one) <= limit:
        return one
    return one[: limit - 1] + "…"


def stem_preview(text: str, limit: int = 52) -> str:
    one = re.sub(r"\s+", " ", text).strip()
    if not one:
        return ""
    if len(one) <= limit:
        return one
    return one[: limit - 1] + "…"


def q_index_filter_chip_btn(
    class_name: str,
    data_attr: str,
    data_value: str,
    label: str,
    *,
    count: int | None = None,
    on: bool = False,
) -> str:
    on_cls = " on" if on else ""
    count_html = ""
    if count is not None:
        count_html = f'<span class="q-index-filter-count">（{count}）</span>'
    return (
        f'<button type="button" class="q-index-filter-opt {class_name}{on_cls}" '
        f'{data_attr}="{html.escape(data_value, quote=True)}">'
        f"{html.escape(label)}{count_html}</button>"
    )


def parse_tags(raw: str) -> list[str]:
    return [t.strip() for t in re.split(r"[,、/|]", raw) if t.strip()]


def load_glossary_lookup() -> dict[str, str]:
    from tools.build_glossary_pages import make_term_lookup, term_slug

    if not GLOSSARY_CSV.is_file():
        return {}
    rows = list(csv.DictReader(GLOSSARY_CSV.read_text(encoding="utf-8-sig").splitlines()))
    used: dict[str, str] = {}
    entries = []
    for row in rows:
        term = norm(row.get("term"))
        if not term:
            continue
        reading = norm(row.get("reading"))
        slug = term_slug(term, reading, used)
        entries.append({"term": term, "reading": reading, "slug_file": f"{slug}.html"})
    lookup = make_term_lookup(entries)
    return {k: f"../terms/{v}" for k, v in lookup.items()}


def glossary_links_for_tags(tags: list[str], lookup: dict[str, str]) -> list[dict]:
    from tools.build_glossary_pages import lookup_key

    out: list[dict] = []
    seen: set[str] = set()
    for tag in tags:
        for key in (lookup_key(tag), tag):
            href = lookup.get(key)
            if not href or href in seen:
                continue
            seen.add(href)
            out.append({"label": tag, "href": href})
            break
        if len(out) >= 3:
            break
    return out


def index_item_dict(page: dict) -> dict:
    preview = stem_preview(page.get("stem_plain") or "")
    tags = page.get("tags") or []
    search_bits = [
        f"第{page['qno']}問",
        page["category"],
        str(page["year"]),
        page.get("wareki", ""),
        preview,
        *tags,
    ]
    return {
        "appId": page["app_id"],
        "year": page["year"],
        "qno": page["qno"],
        "category": page["category"],
        "wareki": page.get("wareki", ""),
        "href": page["href_rel"],
        "preview": preview,
        "tags": tags,
        "exempt": bool(page.get("is_exempt")),
        "invalidated": bool(page.get("is_invalidated")),
        "correct": page.get("correct"),
        "search": " ".join(x for x in search_bits if x),
        "glossary": page.get("glossary_links") or [],
    }


def build_index_table_row(page: dict) -> str:
    href = html.escape(page["href_rel"])
    label = f"第{page['qno']}問"
    preview = stem_preview(page.get("stem_plain") or "")
    preview_cell = (
        html.escape(preview)
        if preview
        else '<span class="q-year-table-desc--empty">問題文は各ページで確認できます</span>'
    )
    tag_html = "".join(
        f'<span class="q-tag-badge">{html.escape(t)}</span>' for t in (page.get("tags") or [])
    )
    gloss = page.get("glossary_links") or []
    gloss_html = (
        " ".join(
            f'<a class="q-glossary-link" href="{html.escape(g["href"])}" onclick="event.stopPropagation()">'
            f"{html.escape(g['label'])}</a>"
            for g in gloss
        )
        if gloss
        else "—"
    )
    badges = []
    if page.get("is_exempt"):
        badges.append('<span class="q-year-table-badge">免除</span>')
    if page.get("is_invalidated"):
        badges.append('<span class="q-year-table-badge q-year-table-badge-warn">無効</span>')
    note_cell = "".join(badges) if badges else "—"
    app_href = html.escape(f"../index.html#past-play-{page['app_id']}")
    return (
        '<tr class="q-year-table-row" tabindex="0"'
        f' data-app-id="{page["app_id"]}"'
        f' data-href="{html.escape(page["href_rel"], quote=True)}"'
        f' data-category="{html.escape(page["category"], quote=True)}">'
        f'<td class="q-year-table-no" data-label="問"><a href="{href}">{html.escape(label)}</a></td>'
        f'<td class="q-year-table-cat" data-label="分野">{html.escape(page["category"])}</td>'
        f'<td class="q-year-table-tags" data-label="タグ">{tag_html or "—"}</td>'
        f'<td class="q-year-table-desc" data-label="問題文">{preview_cell}</td>'
        f'<td class="q-year-table-gloss" data-label="用語">{gloss_html}</td>'
        f'<td class="q-year-table-note" data-label="備考">{note_cell}</td>'
        f'<td class="q-year-table-action" data-label="操作">'
        f'<a class="q-row-link" href="{href}">解説</a> '
        f'<a class="q-row-link q-row-link-app" href="{app_href}">演習</a>'
        "</td></tr>"
    )


def rel_to_root(rel_file: Path) -> str:
    depth = len(rel_file.parent.parts)
    return "/".join([".."] * depth) + "/index.html"


def rel_to_q_index(rel_file: Path) -> str:
    depth = len(rel_file.parent.parts)
    up = max(depth - 1, 1)
    return "/".join([".."] * up) + "/index.html"


def rel_css(rel_file: Path) -> str:
    depth = len(rel_file.parent.parts)
    return "/".join([".."] * depth) + f"/site-pages.css?v={Q_INDEX_CSS_VER}"


def public_url(base: str, rel_path: str) -> str:
    return f"{base.rstrip('/')}/{rel_path.lstrip('/')}"


def load_rows(csv_path: Path) -> list[dict]:
    if not csv_path.is_file():
        return []
    text = csv_path.read_text(encoding="utf-8-sig")
    rows = list(csv.DictReader(text.splitlines()))
    return [r for r in rows if any(norm(v) for v in r.values())]


def wareki_label(year: int) -> str:
    """試験年度の西暦から一覧見出し用の元号表記。"""
    if year <= 2018:
        return f"平成{year - 1988}年度"
    return f"令和{year - 2018}年度"


def parse_base_questions(js_path: Path) -> list[dict]:
    text = js_path.read_text(encoding="utf-8")
    m = re.search(r"let\s+BASE_QUESTIONS\s*=\s*", text)
    if not m:
        raise ValueError("BASE_QUESTIONS が見つかりません: " + str(js_path))
    idx = m.end()
    while idx < len(text) and text[idx] in " \t\n":
        idx += 1
    decoder = json.JSONDecoder()
    data, _end = decoder.raw_decode(text, idx)
    if not isinstance(data, list):
        raise ValueError("BASE_QUESTIONS は配列である必要があります")
    return data


def infer_correct_from_exp_prefix(exp: str) -> int | None:
    """exp 先頭の「正解は選択肢Nです／正解はN。」形式から正答を取る（テンプレ文言が信頼できるため ans より優先）。"""
    s = (exp or "").lstrip()
    m = re.match(r"正解は選択肢([1-4])です", s)
    if m:
        return int(m.group(1))
    m = re.match(r"正解は選択肢([1-4])[。．]", s)
    if m:
        return int(m.group(1))
    m = re.match(r"正解は([1-4])[。．]", s)
    if m:
        return int(m.group(1))
    return None


def infer_correct_from_exp_last_sentence(exp: str) -> int | None:
    """本文末などにだけ現れる「正解は4。」形式を拾う（誤答検討や「3は誤り」の後に続く結論向け）。"""
    if not exp:
        return None
    ms = list(re.finditer(r"正解は(?:選択肢)?([1-4])[。．]", exp))
    if ms:
        return int(ms[-1].group(1))
    return None


def infer_correct_from_kaisetsu_summary(q: dict) -> int | None:
    ks = q.get("kaisetsu")
    if not isinstance(ks, dict):
        return None
    summary = ks.get("summary")
    if not isinstance(summary, dict):
        return None
    rows = summary.get("rows")
    if not isinstance(rows, list):
        return None
    for row in rows:
        if not isinstance(row, (list, tuple)) or len(row) < 2:
            continue
        if norm(str(row[0])) != "正解":
            continue
        cell = str(row[1])
        m = re.search(r"選択肢([1-4])", cell)
        if m:
            return int(m.group(1))
        if re.match(r"^[1-4]$", cell.strip()):
            return int(cell.strip())
    return None


def master_question_correct(q: dict) -> int | None:
    """JS の ans と矛盾しやすいため、解説テキスト・kaisetsu を優先して 1〜4 を決める。"""
    exp = q.get("exp") or ""
    ci = infer_correct_from_exp_prefix(exp)
    if ci is not None:
        return ci
    ci = infer_correct_from_kaisetsu_summary(q)
    if ci is not None:
        return ci
    ci = infer_correct_from_exp_last_sentence(exp)
    if ci is not None:
        return ci
    cor = q.get("ans")
    try:
        n = int(cor)
    except (TypeError, ValueError):
        return None
    if 1 <= n <= 4:
        return n
    return None


def rows_from_master_js(js_path: Path) -> list[dict]:
    """takken-master-data.js の過去問を CSV 行形式に変換する。"""
    items = parse_base_questions(js_path)
    rows: list[dict] = []
    for q in items:
        try:
            year = int(q["year"])
            num = int(q["num"])
            opts = q.get("opts") or []
            if len(opts) != 4:
                continue
            ci = master_question_correct(q)
            if ci is None:
                continue
            field = norm(q.get("field"))
            rows.append(
                {
                    "exam_year": str(year),
                    "exam_wareki": wareki_label(year),
                    "question_no": str(num),
                    "type": "single",
                    "category": FIELD_LABELS_JS.get(field, field or "その他"),
                    "tags": "",
                    "stem": q.get("text") or "",
                    "preamble": "",
                    "statement_a": "",
                    "statement_b": "",
                    "statement_c": "",
                    "statement_d": "",
                    "choice_1": str(opts[0]),
                    "choice_2": str(opts[1]),
                    "choice_3": str(opts[2]),
                    "choice_4": str(opts[3]),
                    "correct": str(ci),
                    "is_exempt": "FALSE",
                    "is_invalidated": "FALSE",
                    "note": "",
                    "explanation": q.get("exp") or "",
                }
            )
        except (KeyError, TypeError, ValueError):
            continue
    return rows


def page_dict(row: dict, line_no: int) -> dict:
    year = int(row["exam_year"])
    qno = int(row["question_no"])
    opts = [norm(row.get(f"choice_{i}")) for i in range(1, 5)]
    if not all(opts):
        raise ValueError(f"line {line_no}: 選択肢欠け {year}-{qno}")
    inv = norm(row.get("is_invalidated", "")).upper() == "TRUE"
    cor = parse_correct(row.get("correct"))
    if cor is None and not inv:
        raise ValueError(f"line {line_no}: 正答なし {year}-{qno}")
    wareki = norm(row.get("exam_wareki")) or wareki_label(year)
    cat = norm(row.get("category"))
    typ = norm(row.get("type")) or "single"
    stem_plain = norm(row.get("stem"))
    exp = norm(row.get("explanation")) or "（解説は未入力です。）"
    return {
        "year": year,
        "qno": qno,
        "wareki": wareki,
        "category": cat,
        "type": typ,
        "stem_html": build_stem_html(row),
        "stem_plain": stem_plain,
        "opts": opts,
        "correct": cor,
        "is_exempt": norm(row.get("is_exempt", "")).upper() == "TRUE",
        "is_invalidated": inv,
        "note": norm(row.get("note")),
        "exp": exp,
        "id": f"past-{year}-{qno:02d}",
        "app_id": year * 100 + qno,
        "tags": parse_tags(norm(row.get("tags"))),
        "rel_path": f"q/past/y{year}/q{qno:02d}/index.html",
    }


def build_question_html(page: dict, rel_path: Path, base_url: str) -> str:
    title_mid = page_title_mid(page)
    title = f"{title_mid}｜解説付き｜{brand_name()}（{exam_name()}）"
    desc = page_meta_description(page)
    canonical = public_url(base_url, page["rel_path"])
    root_idx = rel_to_root(rel_path)
    css_href = rel_css(rel_path)

    opts_html = "".join(
        f'<li class="q-opt"><span class="q-opt-num">（{i}）</span> {html.escape(o)}</li>'
        for i, o in enumerate(page["opts"], start=1)
    )

    if page["is_invalidated"] or page["correct"] is None:
        ans_block = (
            "<p>本問は試験上「出題無効」となった年度があります（"
            + html.escape(page["note"] or "公式の扱いを確認してください")
            + "）。学習用に選択肢のみ掲載します。</p>"
        )
    else:
        ans_block = f'<p>正答は <strong>（{page["correct"]}）</strong> です。</p>'

    badges: list[str] = []
    if page["is_exempt"]:
        badges.append('<span class="q-badge">試験免除出題</span>')
    if page["is_invalidated"]:
        badges.append('<span class="q-badge q-badge-warn">出題無効</span>')
    badge_html = ('<p class="q-badges">' + " ".join(badges) + "</p>") if badges else ""

    exp_html = html.escape(page["exp"]).replace("\n", "<br>\n")
    json_ld = question_json_ld(page, canonical, title, desc)
    trust = trust_table_html(anchor_id="trust", compact=True)
    related = related_terms_html(page, rel_path)
    adj = nav_adjacent_html(page, rel_path)
    hubs = hub_links_html(page, rel_path)
    year_crumb_href = "/".join([".."] * (len(rel_path.parent.parts) - 1)) + "/index.html"

    header = static_q_site_header(
        root_href=root_idx,
        breadcrumb_items=[
            ("トップ", root_idx),
            ("過去問一覧", rel_to_q_index(rel_path)),
            (page["wareki"], year_crumb_href),
            (title_mid, None),
        ],
    )

    app_href = html.escape(root_idx + "#past")

    return f"""<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(desc)}">
{ROBOTS_INDEX_FOLLOW}
<link rel="canonical" href="{html.escape(canonical)}">
<meta property="og:type" content="article">
<meta property="og:title" content="{html.escape(title)}">
<meta property="og:description" content="{html.escape(desc)}">
<meta property="og:url" content="{html.escape(canonical)}">
<meta name="twitter:card" content="summary">
<link rel="stylesheet" href="{html.escape(css_href)}">
<script type="application/ld+json">
{json.dumps(json_ld, ensure_ascii=False, indent=2)}
</script>
</head>
<body class="q-static-body">
{header}
<main class="q-static-main">
  <p class="q-meta"><span class="q-id">ID: <code>{html.escape(page["id"])}</code></span> · <span>{html.escape(page["category"])}</span> · <span>{html.escape(page["type"])}</span></p>
  {badge_html}
  <h1 class="q-h1">{html.escape(title_mid)}</h1>
  {hubs}
  {trust}
  <section class="q-block" aria-labelledby="q-stem-h">
    <h2 id="q-stem-h" class="q-h2">問題</h2>
    <div class="q-stem">{page["stem_html"]}</div>
  </section>
  <section class="q-block" aria-labelledby="q-opts-h">
    <h2 id="q-opts-h" class="q-h2">選択肢</h2>
    <ol class="q-opts">
      {opts_html}
    </ol>
  </section>
  <section class="q-block q-answer" aria-labelledby="q-ans-h">
    <h2 id="q-ans-h" class="q-h2">正答</h2>
    {ans_block}
  </section>
  <section class="q-block" aria-labelledby="q-exp-h">
    <h2 id="q-exp-h" class="q-h2">解説</h2>
    <div class="q-exp">{exp_html}</div>
  </section>
  {related}
  {adj}
  <p class="q-app-link"><a href="{app_href}">アプリで過去問を開く</a></p>
</main>
{static_q_footer_block(rel_path)}
</body>
</html>
"""


def build_q_index(pages: list[dict], base_url: str) -> str:
    glossary_lookup = load_glossary_lookup()
    index_pages: list[dict] = []
    for page in pages:
        pg = dict(page)
        pg["href_rel"] = (
            page["rel_path"][2:] if page["rel_path"].startswith("q/") else page["rel_path"]
        )
        pg["glossary_links"] = glossary_links_for_tags(pg.get("tags") or [], glossary_lookup)
        index_pages.append(pg)

    by_year: dict[int, list[dict]] = {}
    by_category: dict[str, int] = {}
    for pg in index_pages:
        by_year.setdefault(pg["year"], []).append(pg)
        by_category[pg["category"]] = by_category.get(pg["category"], 0) + 1
    for y in by_year:
        by_year[y].sort(key=lambda x: x["qno"])

    sorted_years = sorted(by_year.keys(), reverse=True)
    open_years = set(sorted_years[:2])

    year_blocks = []
    year_jump_links = []
    for y in sorted_years:
        rows_html = "".join(build_index_table_row(pg) for pg in by_year[y])
        heading = (
            by_year[y][0]["wareki"]
            if y > 9999
            else f"{y}年（{by_year[y][0]['wareki']}）"
        )
        expanded = "true" if y in open_years else "false"
        collapsed = "" if y in open_years else " is-collapsed"
        year_jump_links.append(
            f'<a class="q-index-filter-opt q-index-year-link" href="#year-{y}" data-year="{y}">'
            f'{html.escape(f"{y}年")}<span class="q-index-filter-count">（{len(by_year[y])}）</span></a>'
        )
        year_blocks.append(
            f'<section class="q-index-year-block{collapsed}" id="year-{y}">'
            f'<div class="q-index-year-head">'
            f'<div class="q-index-year-head-main">'
            f'<button type="button" class="q-index-year-toggle" aria-expanded="{expanded}" '
            f'aria-controls="year-body-{y}"><span class="q-index-year-chevron" aria-hidden="true"></span></button>'
            f'<h2 id="year-{y}-heading">{html.escape(heading)}</h2>'
            f"</div>"
            f'<span class="q-index-year-count" data-total="{len(by_year[y])}">{len(by_year[y])}問</span>'
            f"</div>"
            f'<div class="q-year-table-wrap" id="year-body-{y}">'
            f'<table class="q-year-table" aria-labelledby="year-{y}-heading">'
            "<thead><tr>"
            '<th scope="col">問</th><th scope="col">分野</th><th scope="col">タグ</th>'
            '<th scope="col">問題文（抜粋）</th><th scope="col">用語</th><th scope="col">備考</th><th scope="col">操作</th>'
            "</tr></thead>"
            f"<tbody>{rows_html}</tbody>"
            "</table></div></section>"
        )
    year_blocks_html = "".join(year_blocks)

    status_chips = [
        q_index_filter_chip_btn("q-index-status-btn", "data-status", "all", "すべて", on=True),
        q_index_filter_chip_btn("q-index-status-btn", "data-status", "wrong", "不正解"),
        q_index_filter_chip_btn("q-index-status-btn", "data-status", "bookmark", "ブックマーク"),
        q_index_filter_chip_btn("q-index-status-btn", "data-status", "exempt", "免除"),
        q_index_filter_chip_btn("q-index-status-btn", "data-status", "invalid", "無効"),
    ]
    json_data = json.dumps([index_item_dict(pg) for pg in index_pages], ensure_ascii=False)
    status_chips_html = "".join(status_chips)
    category_chips = [
        q_index_filter_chip_btn("q-index-chip-btn", "data-cat", "all", "すべて", on=True)
    ]
    for cat, count in sorted(by_category.items()):
        category_chips.append(
            q_index_filter_chip_btn("q-index-chip-btn", "data-cat", cat, cat, count=count)
        )
    category_chips_html = "".join(category_chips)
    year_jump_html = "".join(year_jump_links)
    year_count = len(by_year)

    rel_path = Path("q/index.html")
    q_index_header = site_page_header(rel_path, current="q")
    q_index_breadcrumb = breadcrumb_html(rel_path, [("トップ", "index.html"), ("過去問一覧", None)])
    q_index_footer = site_page_footer(rel_path, current="q")

    page_title = f"過去問｜{brand_name()}（{exam_name()}）"
    page_desc = (
        f"{exam_name()}の過去問{len(pages)}問を年度・分野別に掲載。"
        "検索と絞り込みのあと、各問題の解説ページへ進めます。"
    )
    page_lead = (
        f"{exam_name()}の過去問を年度別・分野別にまとめています。"
        "検索と絞り込みで目的の問題を探し、解説ページで正誤と解説を確認できます。"
    )

    return f"""<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{html.escape(page_title)}</title>
<meta name="description" content="{html.escape(page_desc)}">
<meta property="og:title" content="{html.escape(page_title)}">
<meta property="og:description" content="{html.escape(page_desc)}">
{ROBOTS_INDEX_FOLLOW}
<link rel="canonical" href="{html.escape(public_url(base_url, "q/index.html"))}">
{HEAD_FONTS}
<link rel="stylesheet" href="../site-pages.css?v={Q_INDEX_CSS_VER}">
<link rel="stylesheet" href="../site-theme.css">
</head>
<body class="q-index-page">
{site_page_wrap_open()}
{q_index_header}
<main class="site-page-main">
  {q_index_breadcrumb}
  <h1>過去問</h1>
  <p class="site-page-lead">{html.escape(page_lead)}</p>
  <section class="past-index-panel" aria-labelledby="past-index-heading">
    <div class="past-index-head">
      <div>
        <h2 id="past-index-heading">過去問一覧</h2>
        <p>全{len(pages)}問・{year_count}年度・{len(by_category)}分野。キーワード検索と絞り込みで探せます。</p>
      </div>
      <span id="q-index-hit" class="past-index-hit" aria-live="polite">{len(pages)} / {len(pages)} 問</span>
    </div>
    <div class="past-index-tools" aria-label="絞り込み">
      <label class="past-index-search" for="q-index-q">
        <span>過去問検索</span>
        <input id="q-index-q" type="search" inputmode="search" autocomplete="off" placeholder="例：第1問、分野名、問題文…">
      </label>
      <div class="past-index-tools-actions">
        <button type="button" class="q-index-reset hide" id="q-index-reset">条件をクリア</button>
      </div>
      <div class="q-index-active-filters hide" id="q-index-active-filters" aria-live="polite"></div>
    <div class="q-index-chips-row q-index-year-row" id="q-index-year-row">
      <span class="q-index-chips-label">年度</span>
      <nav class="q-index-chips q-index-year-jump" aria-label="年度で移動">{year_jump_html}</nav>
    </div>
    <div class="q-index-chips-row">
      <span class="q-index-chips-label" id="q-index-chips-label">分野</span>
      <div class="q-index-chips" aria-labelledby="q-index-chips-label">{category_chips_html}</div>
    </div>
    <div class="q-index-chips-row">
      <span class="q-index-chips-label">学習状況</span>
      <div class="q-index-chips q-index-status-chips" role="group" aria-label="学習状況（アプリ連携）">{status_chips_html}</div>
    </div>
    </div>
    <div class="q-index-empty-panel hide" id="q-index-empty" role="status">
      <p class="q-index-empty-title">条件に一致する過去問がありません</p>
      <p class="q-index-empty-hint">検索語を短くするか、分野・学習状況を「すべて」に戻してお試しください。</p>
      <button type="button" class="q-index-reset" id="q-index-empty-reset">条件をクリア</button>
    </div>
    <div class="q-index-layout">
      <div class="q-index-content">
        <section class="q-index-years q-index-view-panel" id="q-index-view-year" aria-label="年度別過去問">{year_blocks_html}</section>
        <section class="q-index-view-panel hide" id="q-index-view-cat" aria-label="分野別過去問"><div id="q-index-cat-mount"></div></section>
        <section class="q-index-view-panel hide" id="q-index-view-flat" aria-label="過去問一覧">
          <div class="q-year-table-wrap">
            <table class="q-year-table">
              <thead><tr>
                <th scope="col">問</th><th scope="col">分野</th><th scope="col">タグ</th>
                <th scope="col">問題文（抜粋）</th><th scope="col">用語</th><th scope="col">備考</th><th scope="col">操作</th>
              </tr></thead>
              <tbody id="q-index-flat-body"></tbody>
            </table>
          </div>
        </section>
        <nav class="q-index-pagination hide" id="q-index-pagination" aria-label="ページ送り"></nav>
      </div>
    </div>
  </section>
</main>
{q_index_footer}
{site_page_wrap_close()}
<button type="button" class="q-index-top" id="q-index-top" aria-label="ページ上部へ">↑</button>
<script type="application/json" id="q-index-data">{json_data}</script>
<script defer src="../site-q-index.js"></script>
</body>
</html>
"""


def build_q_index_placeholder(base_url: str) -> str:
    """CSV が未配置のときの案内ページ。"""
    q_header = static_q_site_header(
        root_href="../index.html",
        breadcrumb_items=[("トップ", "../index.html"), ("過去問一覧", None)],
    )
    return f"""<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>宅建 過去問一覧（無料）｜年度別｜{html.escape(brand_name())}</title>
<meta name="description" content="宅建・宅建士試験の過去問を無料で年度別に一覧。解説・関連用語リンク付きで演習できます。">
{ROBOTS_INDEX_FOLLOW}
<link rel="canonical" href="{html.escape(public_url(base_url, "q/index.html"))}">
<link rel="stylesheet" href="../site-pages.css">
</head>
<body class="q-static-body">
{q_header}
<main class="q-static-main">
  <h1 class="q-h1">宅建の過去問一覧（無料・年度別）</h1>
  <p class="glos-static-intro q-index-intro">
    静的な問題ページは <code>data/past_questions.csv</code> を用意したうえで、リポジトリ直下で
    <code>python3 tools/build_past_question_pages.py</code> を実行すると生成されます。
    （CSV の列形式は賃管マスター製ツールと同一です。<code>data/README.md</code> を参照してください。）
  </p>
  <p class="q-app-link"><a href="../index.html#past">アプリで過去問を開く</a></p>
</main>
{static_q_footer_block(Path("q/index.html"))}
</body>
</html>
"""


def write_sitemap(urls: list[str], out: Path) -> None:
    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
    ]
    for u in sorted(set(urls)):
        lines.append("  <url>")
        lines.append(f"    <loc>{xml_escape(u)}</loc>")
        lines.append("    <changefreq>monthly</changefreq>")
        lines.append("  </url>")
    lines.append("</urlset>")
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    import argparse

    ap = argparse.ArgumentParser(description="過去問静的ページを q/ に生成")
    ap.add_argument("--base-url", default=BASE_DEFAULT)
    ap.add_argument("--csv", type=Path, default=None, help="past_questions.csv のパス（既定: data/past_questions.csv）")
    ap.add_argument(
        "--no-js-fallback",
        action="store_true",
        help="CSV が空でも takken-master-data.js は読まない",
    )
    ap.add_argument(
        "--master-js",
        type=Path,
        default=None,
        help="BASE_QUESTIONS を含む JS（既定: takken-master-data.js）",
    )
    args = ap.parse_args()
    base = args.base_url.rstrip("/")
    csv_path = Path(args.csv).resolve() if args.csv else DATA_CSV_DEFAULT

    rows = load_rows(csv_path)
    data_source = "csv" if rows else ""
    if not rows and not args.no_js_fallback:
        mj = Path(args.master_js).resolve() if args.master_js else MASTER_JS_DEFAULT
        if mj.is_file():
            rows = rows_from_master_js(mj)
            data_source = "js"

    if not rows:
        Q_ROOT.mkdir(parents=True, exist_ok=True)
        q_placeholder = Q_ROOT / "index.html"
        q_placeholder.write_text(build_q_index_placeholder(base), encoding="utf-8")
        print(f"no data (CSV / JS) -> placeholder only: {q_placeholder}")
        return 0

    pages = [page_dict(r, i) for i, r in enumerate(rows, start=2)]
    enrich_pages(pages)

    if Q_ROOT.exists():
        shutil.rmtree(Q_ROOT)

    for p in pages:
        rel = Path(p["rel_path"])
        out_file = ROOT / rel
        out_file.parent.mkdir(parents=True, exist_ok=True)
        html_out = build_question_html(p, out_file.relative_to(ROOT), base)
        out_file.write_text(html_out, encoding="utf-8")

    q_index = Q_ROOT / "index.html"
    q_index.parent.mkdir(parents=True, exist_ok=True)
    q_index.write_text(build_q_index(pages, base), encoding="utf-8")

    brand = brand_name()
    exam = exam_name()
    years = sorted({p["year"] for p in pages})
    for y in years:
        hub_path = Q_ROOT / "past" / f"y{y}" / "index.html"
        hub_path.parent.mkdir(parents=True, exist_ok=True)
        hub_path.write_text(build_year_hub_html(y, pages, base, brand, exam), encoding="utf-8")

    for fid in ("rights", "law", "limit", "tax"):
        hub_path = Q_ROOT / "field" / fid / "index.html"
        hub_path.parent.mkdir(parents=True, exist_ok=True)
        hub_html = build_field_hub_html(fid, pages, base, brand, exam)
        if hub_html:
            hub_path.write_text(hub_html, encoding="utf-8")

    print(
        f"wrote {len(pages)} question pages + {len(years)} year hubs + field hubs + {q_index} "
        f"(source: {data_source})"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
