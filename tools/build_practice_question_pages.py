#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
実践演習の静的ページ q/orig/id{id}/index.html を生成する。

データ: data/practice_questions.csv（export_orig_to_practice_csv.py で生成）
"""

from __future__ import annotations

import html
import json
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from tools.build_past_question_pages import (  # noqa: E402
    HEAD_FONTS,
    Q_ROOT,
    build_stem_html,
    load_rows,
    norm,
    parse_correct,
    parse_tags,
    public_url,
    rel_css,
    rel_href,
    rel_theme_css,
)
from tools.html_footer import (  # noqa: E402
    ROBOTS_INDEX_FOLLOW,
    breadcrumb_html,
    site_page_footer,
    site_page_header,
    site_page_wrap_close,
    site_page_wrap_open,
)
from tools.orig_units import FIELD_LABELS, unit_label  # noqa: E402
from tools.build_practice_question_index import build_orig_q_index  # noqa: E402
from tools.practice_question_seo import (  # noqa: E402
    build_field_hub_html,
    build_level_hub_html,
    build_unit_hub_html,
    enrich_practice_pages,
    nav_adjacent_html,
    page_meta_description,
    page_title_mid,
    practice_hub_links_html,
    question_json_ld,
    related_terms_html,
)
from tools.site_config import brand_name, clean_origin, exam_name  # noqa: E402
from tools.seo_common import trust_table_html  # noqa: E402

DATA_CSV_DEFAULT = ROOT / "data" / "practice_questions.csv"
ORIG_ROOT = Q_ROOT / "orig"
BASE_DEFAULT = clean_origin()


def practice_page_dict(row: dict, line_no: int) -> dict:
    qid = int(row["question_no"])
    opts = [norm(row.get(f"choice_{i}")) for i in range(1, 5)]
    if not all(opts):
        raise ValueError(f"line {line_no}: 選択肢欠け id={qid}")
    cor = parse_correct(row.get("correct"))
    if cor is None:
        raise ValueError(f"line {line_no}: 正答なし id={qid}")
    field = norm(row.get("field"))
    if not field:
        from tools.orig_units import FIELD_LABELS as FL

        inv = {v: k for k, v in FL.items()}
        field = inv.get(norm(row.get("category")), "")
    unit = norm(row.get("unit"))
    ulabel = norm(row.get("unit_label")) or unit_label(unit)
    level = int(norm(row.get("level")) or "1")
    cat = norm(row.get("category"))
    stem_plain = norm(row.get("stem"))
    exp = norm(row.get("explanation")) or "（解説は未入力です。）"
    return {
        "question_id": qid,
        "level": level,
        "unit": unit,
        "unit_label": ulabel,
        "field": field,
        "category": cat,
        "type": norm(row.get("type")) or "single",
        "stem_html": build_stem_html(row),
        "stem_plain": stem_plain,
        "opts": opts,
        "correct": cor,
        "is_exempt": False,
        "is_invalidated": False,
        "note": "",
        "exp": exp,
        "tags": parse_tags(norm(row.get("tags"))),
        "rel_path": f"q/orig/id{qid}/index.html",
    }


def build_question_html(page: dict, rel_path: Path, base_url: str) -> str:
    title_mid = page_title_mid(page)
    title = f"{title_mid}｜解説付き｜{brand_name()}（{exam_name()}）"
    desc = page_meta_description(page)
    canonical = public_url(base_url, page["rel_path"])
    css_href = rel_css(rel_path)
    theme_href = rel_theme_css(rel_path)
    context_line = f"実践演習 · レベル{page['level']} · {page['category']}"
    lead = norm(page.get("stem_plain"))
    lead_html = f'<p class="q-page-lead">{html.escape(lead)}</p>' if lead else ""
    opts_html = "".join(
        f'<li class="q-opt"><span class="q-opt-num">（{i}）</span> {html.escape(o)}</li>'
        for i, o in enumerate(page["opts"], start=1)
    )
    ans_block = f'<p>正答は <strong>（{page["correct"]}）</strong> です。</p>'
    exp_html = html.escape(page["exp"]).replace("\n", "<br>\n")
    json_ld = question_json_ld(page, canonical, title, desc)
    trust = trust_table_html(anchor_id="trust", compact=True)
    related = related_terms_html(page, rel_path)
    adj = nav_adjacent_html(page, rel_path)
    hubs = practice_hub_links_html(page, rel_path)
    site_header = site_page_header(rel_path, current="q")
    site_breadcrumb = breadcrumb_html(
        rel_path,
        [
            ("トップ", "index.html"),
            ("問題一覧", "q/index.html"),
            ("実践演習", "q/orig/index.html"),
            (page["unit_label"], f"q/orig/unit/{page['unit']}/index.html"),
            (title_mid, None),
        ],
    )
    site_footer = site_page_footer(rel_path, current="q")
    app_href = html.escape(rel_href(rel_path, f"index.html#orig-play-{page['question_id']}"))

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
{HEAD_FONTS}
<link rel="stylesheet" href="{html.escape(css_href)}">
<link rel="stylesheet" href="{html.escape(theme_href)}">
<script type="application/ld+json">
{json.dumps(json_ld, ensure_ascii=False, indent=2)}
</script>
</head>
<body class="q-question-page">
{site_page_wrap_open()}
{site_header}
<main class="q-static-main">
  {site_breadcrumb}
  <p class="q-meta-line">{html.escape(context_line)}</p>
  <h1 class="q-h1">{html.escape(title_mid)}</h1>
  {lead_html}
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
    <p class="q-rich-note">図解つきの詳しい解説は<a href="{app_href}">アプリの実践演習</a>で表示できます。</p>
  </section>
  {related}
  {adj}
  <p class="q-app-link"><a href="{app_href}">アプリでこの問題を演習する</a></p>
</main>
{site_footer}
{site_page_wrap_close()}
</body>
</html>
"""


def main() -> int:
    import argparse

    ap = argparse.ArgumentParser(description="実践演習静的ページを q/orig/ に生成")
    ap.add_argument("--base-url", default=BASE_DEFAULT)
    ap.add_argument("--csv", type=Path, default=None)
    ap.add_argument("--limit", type=int, default=0, help="テスト用: 生成する問題数の上限")
    args = ap.parse_args()
    base = args.base_url.rstrip("/")
    csv_path = Path(args.csv).resolve() if args.csv else DATA_CSV_DEFAULT

    rows = load_rows(csv_path)
    if not rows:
        print(f"no data: {csv_path} (run tools/export_orig_to_practice_csv.py first)", file=sys.stderr)
        return 1

    pages = [practice_page_dict(r, i) for i, r in enumerate(rows, start=2)]
    if args.limit and args.limit > 0:
        pages = pages[: args.limit]
    enrich_practice_pages(pages)

    if ORIG_ROOT.exists():
        shutil.rmtree(ORIG_ROOT)

    for p in pages:
        rel = Path(p["rel_path"])
        out_file = ROOT / rel
        out_file.parent.mkdir(parents=True, exist_ok=True)
        html_out = build_question_html(p, out_file.relative_to(ROOT), base)
        out_file.write_text(html_out, encoding="utf-8")

    brand = brand_name()
    exam = exam_name()
    orig_index = ORIG_ROOT / "index.html"
    orig_index.parent.mkdir(parents=True, exist_ok=True)
    orig_index.write_text(build_orig_q_index(pages, base), encoding="utf-8")

    for fid in FIELD_LABELS:
        hub_html = build_field_hub_html(fid, pages, base, brand, exam)
        if hub_html:
            hub_path = ORIG_ROOT / "field" / fid / "index.html"
            hub_path.parent.mkdir(parents=True, exist_ok=True)
            hub_path.write_text(hub_html, encoding="utf-8")

    units = sorted({p["unit"] for p in pages})
    for uid in units:
        hub_html = build_unit_hub_html(uid, pages, base, brand, exam)
        if hub_html:
            hub_path = ORIG_ROOT / "unit" / uid / "index.html"
            hub_path.parent.mkdir(parents=True, exist_ok=True)
            hub_path.write_text(hub_html, encoding="utf-8")

    for lv in sorted({p["level"] for p in pages}):
        hub_html = build_level_hub_html(lv, pages, base, brand, exam)
        if hub_html:
            hub_path = ORIG_ROOT / "level" / str(lv) / "index.html"
            hub_path.parent.mkdir(parents=True, exist_ok=True)
            hub_path.write_text(hub_html, encoding="utf-8")

    print(
        f"wrote {len(pages)} practice pages + hubs under {ORIG_ROOT} (source: {csv_path.name})"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
