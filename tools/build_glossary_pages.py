#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
glossary/*/index.html を賃管マスター型の site-pages デザインに差し替え、
glossary/index.html（用語索引）を再生成する。
"""

from __future__ import annotations

import html
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from tools.html_footer import (  # noqa: E402
    ROBOTS_INDEX_FOLLOW,
    site_page_footer,
    site_page_header,
    site_page_wrap_close,
    site_page_wrap_open,
)

GLOSSARY_DIR = ROOT / "glossary"
BASE_URL = "https://takken-master.jp"
HEAD_FONTS = """<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@400;500;600;700&display=swap" rel="stylesheet">"""

CAT_ORDER = (
    "権利関係",
    "宅建業法",
    "法令上の制限",
    "税・その他",
    "試験対策",
)

QUIZ_SCRIPT = """<script>
function answerQuiz(q,el,ok){
  var b=document.getElementById(q);
  if(!b)return;
  b.querySelectorAll(".quiz-choice").forEach(function(c){c.onclick=null});
  el.classList.add(ok?"correct":"wrong");
  var a=document.getElementById(q+"-answer");
  if(a)a.classList.add("show");
}
</script>"""


def public_url(base: str, path: str) -> str:
    return base.rstrip("/") + "/" + path.lstrip("/")


def scan_glossary_entries() -> list[dict]:
    entries: list[dict] = []
    for d in sorted(GLOSSARY_DIR.iterdir()):
        if not d.is_dir() or d.name.startswith("."):
            continue
        idx = d / "index.html"
        if not idx.is_file():
            continue
        raw = idx.read_text(encoding="utf-8")
        cat_m = re.search(r'class="term-category">([^<]+)<', raw)
        h1_m = re.search(r'class="term-h1">([^<]+)<', raw)
        read_m = re.search(r'class="term-reading">（([^）]+)）<', raw)
        title_m = re.search(r"<title>([^<]+)</title>", raw)
        term = (h1_m.group(1) if h1_m else title_m.group(1) if title_m else d.name).strip()
        term = re.sub(r"【宅建】.*", "", term).strip()
        entries.append(
            {
                "slug": d.name,
                "term": term,
                "reading": read_m.group(1) if read_m else "",
                "category": cat_m.group(1).strip() if cat_m else "その他",
                "href": f"{d.name}/index.html",
            }
        )
    return entries


def extract_head_bits(raw: str) -> dict[str, str]:
    def meta(name: str) -> str:
        m = re.search(
            rf'<meta\s+name="{re.escape(name)}"\s+content="([^"]*)"',
            raw,
            re.I,
        )
        return m.group(1) if m else ""

    title_m = re.search(r"<title>([^<]*)</title>", raw, re.I)
    canon_m = re.search(r'<link\s+rel="canonical"\s+href="([^"]*)"', raw, re.I)
    ld_m = re.search(
        r'<script\s+type="application/ld\+json">(.*?)</script>',
        raw,
        re.I | re.S,
    )
    return {
        "title": title_m.group(1).strip() if title_m else "",
        "description": meta("description"),
        "canonical": canon_m.group(1).strip() if canon_m else "",
        "json_ld": ld_m.group(1).strip() if ld_m else "",
    }


def fix_extract_rich_content(raw: str) -> str:
    """Extract main article body from legacy glossary page."""
    m = re.search(r'<div\s+class="page-wrap">(.*)', raw, re.I | re.S)
    if not m:
        return ""
    rest = m.group(1)
    for marker in (
        '<div class="term-footer-nav">',
        '<footer class="site-footer">',
        "</main>",
    ):
        pos = rest.find(marker)
        if pos >= 0:
            rest = rest[:pos]
            break
    content = rest.strip()
    if content.endswith("</div>"):
        content = content[:-6].strip()
    content = re.sub(r'href="/glossary/([^"/]+)/"', r'href="../\1/"', content)
    content = re.sub(r'href="/glossary/"', r'href="../index.html"', content)
    content = re.sub(r'href="/"', r'href="../../index.html"', content)
    content = re.sub(r'href="/quiz/', r'href="../../index.html"', content)
    content = re.sub(
        r'<nav\s+class="breadcrumb">.*?</nav>\s*',
        "",
        content,
        count=1,
        flags=re.S,
    )
    return content


def build_term_page(slug: str, raw: str) -> str:
    head = extract_head_bits(raw)
    content = fix_extract_rich_content(raw)
    if len(content.strip()) < 200:
        raise ValueError(f"{slug}: 本文の抽出に失敗しました（page-wrap が見つからないか中身が空です）")
    rel_path = Path("glossary") / slug / "index.html"
    term_label = head["title"].split("｜")[0].strip() if head["title"] else slug
    crumb = [
        ("トップ", "index.html"),
        ("用語解説一覧", "glossary/index.html"),
        (term_label, None),
    ]
    page_header = site_page_header(rel_path, current="glossary", breadcrumb_items=crumb)
    page_footer = site_page_footer(rel_path, current="glossary")
    css_site = "../../site-pages.css?v=20260515"
    css_term = "../../glossary-term.css?v=20260515"
    json_ld_block = ""
    if head["json_ld"]:
        json_ld_block = f'<script type="application/ld+json">\n{head["json_ld"]}\n</script>\n'
    canonical = head["canonical"] or public_url(BASE_URL, f"glossary/{slug}/")
    title = head["title"] or f"{term_label}｜宅建マスター"
    desc = head["description"] or f"{term_label}の意味と試験ポイントを宅建マスターで解説。"
    og_title = html.escape(title)
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
<meta property="og:title" content="{og_title}">
<meta property="og:description" content="{html.escape(desc)}">
<meta property="og:url" content="{html.escape(canonical)}">
<meta name="twitter:card" content="summary">
{HEAD_FONTS}
<link rel="stylesheet" href="{css_site}">
<link rel="stylesheet" href="{css_term}">
{json_ld_block}</head>
<body>
{site_page_wrap_open()}
{page_header}
<main class="site-page-main term-page-main">
<div class="term-rich-content">
{content}
</div>
<p class="q-app-link"><a href="../../index.html#glossary">アプリで用語解説を開く</a></p>
</main>
{page_footer}
{site_page_wrap_close()}
{QUIZ_SCRIPT}
</body>
</html>
"""


def ordered_categories(by_cat: dict[str, list]) -> list[str]:
    keys = [c for c in CAT_ORDER if c in by_cat]
    for c in sorted(by_cat):
        if c not in keys:
            keys.append(c)
    return keys


def build_glossary_index(entries: list[dict]) -> str:
    by_cat: dict[str, list[dict]] = {}
    for e in entries:
        by_cat.setdefault(e["category"], []).append(e)
    for c in by_cat:
        by_cat[c].sort(key=lambda x: x["term"])

    cat_keys = ordered_categories(by_cat)
    body_sections: list[str] = []
    for i, cat in enumerate(cat_keys):
        lis = [
            f'    <li><a href="{html.escape(e["href"])}">{html.escape(e["term"])}</a></li>'
            for e in by_cat[cat]
        ]
        hid = f"terms-idx-cat-{i}"
        body_sections.append(
            f'<section class="terms-idx-cat" aria-labelledby="{hid}">\n'
            f'  <h2 id="{hid}">{html.escape(cat)}</h2>\n'
            f'  <ul class="terms-idx-list">\n'
            + "\n".join(lis)
            + "\n  </ul>\n</section>"
        )
    body_html = "\n".join(body_sections)

    chips = ['    <button type="button" class="terms-idx-chip on" data-cat="all">すべて</button>']
    for cat in cat_keys:
        chips.append(
            f'    <button type="button" class="terms-idx-chip" data-cat="{html.escape(cat, quote=True)}">'
            f"{html.escape(cat)}</button>"
        )
    chips_html = "\n".join(chips)

    n_terms = len(entries)
    list_items_ld = []
    pos = 1
    for cat in cat_keys:
        for e in by_cat[cat]:
            list_items_ld.append(
                {
                    "@type": "ListItem",
                    "position": pos,
                    "name": e["term"],
                    "item": public_url(BASE_URL, f"glossary/{e['href']}"),
                }
            )
            pos += 1
    ld = {
        "@context": "https://schema.org",
        "@type": "ItemList",
        "name": "宅建試験 用語解説一覧",
        "description": "宅地建物取引士試験で出やすい用語ごとの解説記事への索引です。",
        "numberOfItems": n_terms,
        "itemListElement": list_items_ld,
    }
    ld_json = json.dumps(ld, ensure_ascii=False, indent=2)

    terms_idx_script = f"""<script>
(() => {{
  try {{ if ('scrollRestoration' in history) history.scrollRestoration = 'manual'; }} catch (_e) {{}}
  window.scrollTo(0, 0);
  const q = document.getElementById('terms-idx-q');
  const chips = Array.from(document.querySelectorAll('.terms-idx-chip[data-cat]'));
  const cats = Array.from(document.querySelectorAll('.terms-idx-cat'));
  const totalEl = document.getElementById('terms-idx-total');
  const hitEl = document.getElementById('terms-idx-hit');
  let activeCat = 'all';
  function norm(s) {{ return (s || '').toString().trim().toLowerCase(); }}
  function apply() {{
    const query = norm(q.value);
    let shown = 0;
    cats.forEach((sec) => {{
      const cat = sec.querySelector('h2')?.textContent || '';
      const catOk = activeCat === 'all' || cat === activeCat;
      const items = Array.from(sec.querySelectorAll('li'));
      let anyInCat = 0;
      items.forEach((li) => {{
        const a = li.querySelector('a');
        const t = norm(a?.textContent || '');
        const ok = catOk && (!query || t.includes(query));
        li.classList.toggle('hide', !ok);
        if (ok) {{ anyInCat++; shown++; }}
      }});
      sec.classList.toggle('hide', anyInCat === 0);
    }});
    if (totalEl) totalEl.textContent = String({n_terms});
    if (hitEl) hitEl.textContent = (query || activeCat !== 'all') ? '表示：' + shown + '件' : '';
  }}
  q.addEventListener('input', apply);
  chips.forEach((btn) => {{
    btn.addEventListener('click', () => {{
      chips.forEach((b) => b.classList.remove('on'));
      btn.classList.add('on');
      activeCat = btn.dataset.cat || 'all';
      apply();
    }});
  }});
  apply();
}})();
</script>"""

    idx_path = Path("glossary/index.html")
    terms_header = site_page_header(
        idx_path,
        current="glossary",
        breadcrumb_items=[("トップ", "index.html"), ("用語解説一覧", None)],
        wide=True,
    )
    terms_footer = site_page_footer(idx_path, current="glossary", wide=True)
    canonical = public_url(BASE_URL, "glossary/")
    title = "用語解説一覧（全記事索引）｜宅建マスター（宅地建物取引士）"
    desc = (
        "宅地建物取引士試験の重要用語を一覧し、各用語の解説記事へリンクします。"
        "権利関係・宅建業法・法令上の制限・税その他などの語句を整理しています。"
    )
    return f"""<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(desc)}">
{ROBOTS_INDEX_FOLLOW}
<link rel="canonical" href="{html.escape(canonical)}">
<meta property="og:type" content="website">
<meta property="og:url" content="{html.escape(canonical)}">
<meta property="og:title" content="{html.escape(title)}">
<meta property="og:description" content="{html.escape(desc)}">
<meta property="og:locale" content="ja_JP">
<script type="application/ld+json">
{ld_json}
</script>
{HEAD_FONTS}
<link rel="stylesheet" href="../site-pages.css?v=20260515">
</head>
<body>
{site_page_wrap_open()}
{terms_header}
<main class="site-page-main terms-idx-main">
  <h1 class="terms-idx-page-title">用語解説一覧（全記事索引）</h1>
  <p class="terms-idx-lead">宅地建物取引士試験で頻出の用語を分野別にまとめ、各用語の解説記事（静的HTML）へ直接リンクします。上の検索・分野フィルタで目的の用語に素早く到達できます。演習アプリ内の<strong><a href="../index.html#glossary">用語解説</a></strong>では検索や折りたたみカードも利用できます。</p>

  <div class="terms-idx-meta-row">
    <span class="terms-idx-pill">全 <span id="terms-idx-total">{n_terms}</span> 記事</span>
    <div class="terms-idx-search" role="search" aria-label="用語検索">
      <input id="terms-idx-q" type="search" inputmode="search" placeholder="例：抵当権、建ぺい率、重要事項説明…" autocomplete="off">
    </div>
  </div>

  <div class="terms-idx-chips" aria-label="分野フィルタ">
{chips_html}
  </div>

  <section class="terms-idx-panel" aria-label="用語一覧">
{body_html}
    <div class="terms-idx-panel-footer">
      <span id="terms-idx-hit"></span>
      <div class="terms-idx-panel-footer-app">学習アプリ本体は <a href="../index.html">トップ</a> から利用できます。</div>
    </div>
  </section>
</main>
{terms_footer}
{site_page_wrap_close()}
{terms_idx_script}
</body>
</html>
"""


def main() -> None:
    entries = scan_glossary_entries()
    if not entries:
        raise SystemExit("glossary entries not found")
    GLOSSARY_DIR.mkdir(exist_ok=True)
    for e in entries:
        slug = e["slug"]
        path = GLOSSARY_DIR / slug / "index.html"
        raw = path.read_text(encoding="utf-8")
        if 'class="site-page-wrap"' in raw and 'class="page-wrap"' not in raw:
            print(f"  skip (already new shell): {slug}")
            continue
        path.write_text(build_term_page(slug, raw), encoding="utf-8")
        print(f"  term: {slug}")
    index_path = GLOSSARY_DIR / "index.html"
    index_path.write_text(build_glossary_index(entries), encoding="utf-8")
    print(f"index: {len(entries)} terms -> {index_path}")


if __name__ == "__main__":
    main()
