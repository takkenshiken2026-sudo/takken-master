#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""模試セットの静的ページ q/mock/ を生成する。"""

from __future__ import annotations

import csv
import html
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from tools.mock_exam_config import MOCK_PATTERNS  # noqa: E402
from tools.past_question_seo import _collection_json_ld, _hub_meta_tags  # noqa: E402
from tools.site_config import brand_name, clean_origin, exam_name  # noqa: E402

DATA_CSV = ROOT / "data" / "mock_sets.csv"
MOCK_ROOT = ROOT / "q" / "mock"
BASE_DEFAULT = clean_origin()

FIELD_LABELS = {
    "rights": "権利関係",
    "law": "宅建業法",
    "limit": "法令上の制限",
    "tax": "税・その他",
}


def load_mock_rows() -> list[dict]:
    if not DATA_CSV.is_file():
        return []
    text = DATA_CSV.read_text(encoding="utf-8-sig")
    return list(csv.DictReader(text.splitlines()))


def main() -> int:
    import argparse

    ap = argparse.ArgumentParser(description="模試静的ページを q/mock/ に生成")
    ap.add_argument("--base-url", default=BASE_DEFAULT)
    args = ap.parse_args()
    base = args.base_url.rstrip("/")
    rows = load_mock_rows()
    if not rows:
        print(f"no data: {DATA_CSV} (run tools/generate_mock_sets.py first)", file=sys.stderr)
        return 1

    if MOCK_ROOT.exists():
        shutil.rmtree(MOCK_ROOT)
    MOCK_ROOT.mkdir(parents=True)

    by_pat: dict[str, list[dict]] = {}
    for row in rows:
        by_pat.setdefault(row["pattern_id"], []).append(row)
    for pid in by_pat:
        by_pat[pid].sort(key=lambda r: int(r["seq"]))

    brand = brand_name()
    exam = exam_name()

    # 模試トップ
    cards = []
    for pat in MOCK_PATTERNS:
        pid = str(pat["id"])
        n = len(by_pat.get(pid, []))
        cards.append(
            f'<article class="mock-static-card">'
            f'<h2><a href="{pid}/index.html">{html.escape(pat["title"])}</a></h2>'
            f'<p class="mock-static-meta">{html.escape(pat["subtitle"])} · {n}問</p>'
            f'<p>{html.escape(pat["desc"])}</p>'
            f'<p><a href="{pid}/index.html">出題一覧</a> · '
            f'<a href="../../index.html#mock-play-{pid}">アプリで受験</a></p>'
            f"</article>"
        )
    root_canonical = f"{base}/q/mock/index.html"
    root_title = f"オリジナル模試一覧｜{brand}（{exam}）"
    root_desc = "本番形式50問・120分の模擬試験。過去問から分野別に抽出した5パターン。"
    root_ld = _collection_json_ld(
        canonical=root_canonical,
        title=root_title,
        desc=root_desc,
        items=[(p["title"], f"{base}/q/mock/{p['id']}/index.html") for p in MOCK_PATTERNS],
        site_url=base,
    )
    (MOCK_ROOT / "index.html").write_text(
        f"""<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{html.escape(root_title)}</title>
<meta name="description" content="{html.escape(root_desc)}">
{_hub_meta_tags(root_title, root_desc, root_canonical)}
<link rel="stylesheet" href="../../site-pages.css">
{root_ld}
</head>
<body class="q-static-body">
<header class="q-static-header">
  <p class="q-static-brand"><a href="../../index.html">{html.escape(brand)}</a></p>
  <nav aria-label="パンくず"><ol class="q-breadcrumb">
    <li><a href="../../index.html">トップ</a></li>
    <li><a href="../index.html">問題一覧</a></li>
    <li aria-current="page">オリジナル模試</li>
  </ol></nav>
</header>
<main class="q-static-main">
  <h1 class="q-h1">オリジナル模試</h1>
  <p class="glos-static-intro">各回50問・本試験と同じ配分（権利14・業法20・制限8・税8）。一覧から個別の解説ページへ進むか、アプリで120分の模試形式に挑戦できます。</p>
  <div class="mock-static-grid">{''.join(cards)}</div>
</main>
</body>
</html>""",
        encoding="utf-8",
    )

    for pat in MOCK_PATTERNS:
        pid = str(pat["id"])
        items = by_pat.get(pid, [])
        if not items:
            continue
        lis = []
        for row in items:
            seq = row["seq"]
            href = row["static_href"]
            # q/mock/{id}/index.html → q/past/... は ../../past/...
            rel = href[2:] if href.startswith("q/") else href
            label = f"問{seq} · {row['category']}"
            if row.get("exam_year") and row.get("question_no"):
                label += f"（{row['exam_year']}年第{row['question_no']}問）"
            preview = html.escape((row.get("stem_preview") or "")[:48])
            lis.append(
                f'<li><span class="mock-q-seq">{seq}</span> '
                f'<a href="../../{html.escape(rel)}">{html.escape(label)}</a>'
                f'<span class="mock-q-prev">{preview}</span> '
                f'<a class="mock-q-app" href="../../../index.html#past-play-{html.escape(row["question_id"])}">演習</a>'
                f"</li>"
            )
        pat_dir = MOCK_ROOT / pid
        pat_dir.mkdir(parents=True)
        canonical = f"{base}/q/mock/{pid}/index.html"
        title = f"{pat['title']}｜出題一覧｜{brand}"
        desc = pat["desc"]
        pat_ld = _collection_json_ld(
            canonical=canonical,
            title=title,
            desc=desc,
            items=[
                (f"問{r['seq']}", f"{base}/{r['static_href']}") for r in items[:50]
            ],
            site_url=base,
        )
        (pat_dir / "index.html").write_text(
            f"""<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(desc)}">
{_hub_meta_tags(title, desc, canonical)}
<link rel="stylesheet" href="../../../site-pages.css">
{pat_ld}
</head>
<body class="q-static-body">
<header class="q-static-header">
  <p class="q-static-brand"><a href="../../../index.html">{html.escape(brand)}</a></p>
  <nav aria-label="パンくず"><ol class="q-breadcrumb">
    <li><a href="../../../index.html">トップ</a></li>
    <li><a href="../../index.html">問題一覧</a></li>
    <li><a href="../index.html">模試一覧</a></li>
    <li aria-current="page">{html.escape(pat["title"])}</li>
  </ol></nav>
</header>
<main class="q-static-main">
  <h1 class="q-h1">{html.escape(pat["title"])}</h1>
  <p class="q-meta">{html.escape(pat["subtitle"])} · {len(items)}問</p>
  <p>{html.escape(pat["desc"])}</p>
  <p class="q-app-link"><a href="../../../index.html#mock-play-{pid}">アプリでこの模試を受ける（120分）</a></p>
  <ol class="mock-set-list">{''.join(lis)}</ol>
</main>
</body>
</html>""",
            encoding="utf-8",
        )

    # quiz/mock リダイレクトを静的一覧へ
    quiz_mock = ROOT / "quiz" / "mock" / "index.html"
    quiz_mock.parent.mkdir(parents=True, exist_ok=True)
    quiz_mock.write_text(
        """<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="UTF-8">
<meta http-equiv="refresh" content="0;url=/q/mock/index.html">
<script>location.replace('/q/mock/index.html');</script>
<title>模試一覧へ移動中...</title>
</head>
<body><p><a href="/q/mock/index.html">模試一覧へ</a></p></body>
</html>""",
        encoding="utf-8",
    )

    print(f"wrote q/mock/ ({len(MOCK_PATTERNS)} patterns, {len(rows)} question slots)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
