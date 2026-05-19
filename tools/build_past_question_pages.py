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


def rel_to_root(rel_file: Path) -> str:
    depth = len(rel_file.parent.parts)
    return "/".join([".."] * depth) + "/index.html"


def rel_to_q_index(rel_file: Path) -> str:
    depth = len(rel_file.parent.parts)
    up = max(depth - 1, 1)
    return "/".join([".."] * up) + "/index.html"


def rel_css(rel_file: Path) -> str:
    depth = len(rel_file.parent.parts)
    return "/".join([".."] * depth) + "/site-pages.css"


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
    wareki = norm(row.get("exam_wareki"))
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
    by_year: dict[int, list[dict]] = {}
    for p in pages:
        by_year.setdefault(p["year"], []).append(p)
    for y in by_year:
        by_year[y].sort(key=lambda x: int(x["qno"]))

    field_chips = []
    for fid, meta in (
        ("rights", "権利関係"),
        ("law", "宅建業法"),
        ("limit", "法令上の制限"),
        ("tax", "税・その他"),
    ):
        field_chips.append(
            f'<a class="terms-idx-chip" href="field/{html.escape(fid)}/index.html">{html.escape(meta)}</a>'
        )
    field_nav = (
        '<nav class="q-field-nav" aria-label="分野別過去問">'
        + "".join(field_chips)
        + "</nav>"
    )

    year_blocks = []
    for y in sorted(by_year.keys(), reverse=True):
        ys = by_year[y]
        wareki = ys[0]["wareki"]
        count = len(ys)
        def href_for(p: dict, _y: int = y) -> str:
            rel = p["rel_path"]
            return rel[2:] if rel.startswith("q/") else rel

        table = q_list_table_html(ys, href_for)
        year_blocks.append(
            f'<section class="glos-cat-section q-year-section">'
            f'<h2 class="glos-cat-heading glos-cat-heading--ja">'
            f'<a href="past/y{y}/index.html">{html.escape(str(y))}年（{html.escape(wareki)}）</a>'
            f' <span class="q-meta">{count}問</span></h2>'
            f"{table}"
            "</section>"
        )

    q_header = static_q_site_header(
        root_href="../index.html",
        breadcrumb_items=[("トップ", "../index.html"), ("過去問一覧", None)],
    )

    total_line = f"<p class=\"q-meta\">全 {len(pages)} 問</p>" if pages else ""

    recent_years = sorted(by_year.keys(), reverse=True)[:5]
    quick_year_links = []
    for y in recent_years:
        ys = by_year[y]
        wareki = ys[0]["wareki"]
        n = len(ys)
        quick_year_links.append(
            f'<a class="terms-idx-chip" href="past/y{y}/index.html">'
            f"宅建 {html.escape(str(y))}年 過去問（{html.escape(wareki)}・{n}問）</a>"
        )
    quick_years_nav = ""
    if quick_year_links:
        quick_years_nav = (
            '<nav class="q-index-quick-years" aria-label="年度別過去問（人気）">'
            '<p class="q-index-quick-label">年度別に見る</p>'
            + "".join(quick_year_links)
            + "</nav>"
        )

    index_title = f"宅建 過去問一覧（無料）｜年度別・解説付き｜{brand_name()}"
    index_desc = (
        f"宅建・宅建士試験の過去問を無料で年度別に演習。全{len(pages)}問に正答・解説・関連用語リンク付き。"
        "2025年度・2024年度から各問へ。分野別の絞り込みもできます。"
    )

    return f"""<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{html.escape(index_title)}</title>
<meta name="description" content="{html.escape(index_desc)}">
{ROBOTS_INDEX_FOLLOW}
<link rel="canonical" href="{html.escape(public_url(base_url, "q/index.html"))}">
<link rel="stylesheet" href="../site-pages.css">
</head>
<body class="q-static-body">
{q_header}
<main class="q-static-main">
  <h1 class="q-h1">宅建の過去問一覧（無料・年度別）</h1>
  {total_line}
  <p class="glos-static-intro q-index-intro">宅建・宅建士試験の<strong>過去問</strong>を<strong>無料</strong>で<strong>年度別</strong>に解けます。各問ページには<strong>解説</strong>と<strong>関連用語</strong>へのリンクがあります。<strong><a href="../index.html#past">アプリで過去問</a></strong>では絞り込みや学習記録も使えます。</p>
  {trust_table_html(anchor_id="trust", compact=True)}
  {quick_years_nav}
  {field_nav}
  {"".join(year_blocks)}
  <p class="q-app-link"><a href="../index.html#past">アプリで過去問を開く</a></p>
</main>
{static_q_footer_block(Path("q/index.html"))}
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
