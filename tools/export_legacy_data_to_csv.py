#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""既存の JS / HTML / Python バッチからテンプレ用 CSV を生成する（一回限りの移行用）。"""

from __future__ import annotations

import ast
import csv
import html
import json
import re
import sys
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from tools.build_past_question_pages import rows_from_master_js  # noqa: E402

GLOSSARY_JS = ROOT / "takken-data-glossary.js"
MASTER_JS = ROOT / "takken-master-data.js"
GLOSSARY_CSV = ROOT / "data" / "glossary_terms.csv"
PAST_CSV = ROOT / "data" / "past_questions.csv"
GUIDE_CSV = ROOT / "data" / "guide_articles.csv"
TAKKEN_DIR = ROOT / "takken"

CAT_TO_CATEGORY = {
    "rights": "権利関係",
    "law": "宅建業法",
    "limit": "法令上の制限",
    "tax": "税・その他",
    "guide": "試験対策",
}

EYEBROW_TO_GENRE = {
    "宅建 学習計画": "学習計画",
    "宅建 合格ライン": "合格・難易度",
    "宅建 勉強法": "過去問活用",
    "宅建 独学": "独学対策",
    "宅建 直前": "直前・当日",
    "宅建 概要": "試験概要",
    "宅建 申込": "受験・申込",
    "宅建 分野別": "分野別対策",
    "宅建 用語": "用語整理",
}

SLUG_GENRE_HINTS: list[tuple[str, str]] = [
    ("schedule", "受験・申込"),
    ("moshikomi", "受験・申込"),
    ("jukenhi", "受験・申込"),
    ("goukaku", "合格・難易度"),
    ("gokaku", "合格・難易度"),
    ("kakomon", "過去問活用"),
    ("benkyou", "学習計画"),
    ("plan", "学習計画"),
    ("dokugaku", "独学対策"),
    ("chokuzen", "直前・当日"),
    ("saishuken", "注意点・更新"),
    ("kenri", "分野別対策"),
    ("gyoho", "分野別対策"),
    ("hooreijou", "分野別対策"),
    ("zei", "分野別対策"),
    ("overview", "試験概要"),
    ("to-wa", "試験概要"),
]

GUIDE_HEADER = [
    "slug",
    "genre",
    "title",
    "meta_description",
    "lead",
    "priority",
    "tags",
    "author_name",
    "author_profile",
    "reviewer_name",
    "reviewer_profile",
    "fact_checked_at",
    "primary_sources",
    "original_note",
    "user_intent",
    "action_items",
    "update_policy",
    "last_reviewed_at",
    "next_review_at",
    "source_checked_at",
    "content_status",
    "revision_note",
    "section_1_heading",
    "section_1_body",
    "section_2_heading",
    "section_2_body",
    "section_3_heading",
    "section_3_body",
    "section_4_heading",
    "section_4_body",
    "section_5_heading",
    "section_5_body",
    "section_6_heading",
    "section_6_body",
    "section_7_heading",
    "section_7_body",
    "faq_1_question",
    "faq_1_answer",
    "faq_2_question",
    "faq_2_answer",
    "related_links",
]

GLOSSARY_HEADER = [
    "term",
    "reading",
    "category",
    "tags",
    "short_def",
    "definition",
    "related_terms",
    "legal_basis",
    "importance",
    "explanation",
    "article_title",
    "article_lead",
    "term_detail_body",
    "exam_points",
    "common_mistakes",
    "memory_tip",
    "example_question",
    "example_answer",
    "summary_points",
    "faq_1_question",
    "faq_1_answer",
    "faq_2_question",
    "faq_2_answer",
    "faq_3_question",
    "faq_3_answer",
    "faq_4_question",
    "faq_4_answer",
]

PAST_HEADER = [
    "exam_year",
    "exam_wareki",
    "question_no",
    "type",
    "category",
    "tags",
    "stem",
    "preamble",
    "statement_a",
    "statement_b",
    "statement_c",
    "statement_d",
    "choice_1",
    "choice_2",
    "choice_3",
    "choice_4",
    "correct",
    "is_exempt",
    "is_invalidated",
    "note",
    "explanation",
]

PRIMARY_SOURCES = (
    "不動産適正取引推進機構（RETIO）|https://www.retio.or.jp/;"
    "国土交通省|https://www.mlit.go.jp/"
)
FACT_DATE = "2026-05-19"
REVIEW_DATE = "2026-05-19"
NEXT_REVIEW = "2026-06-19"


def parse_glossary_js(path: Path) -> list[dict]:
    text = path.read_text(encoding="utf-8")
    m = re.search(r"const\s+GLOSSARY_DATA\s*=\s*(\[.*?\]);\s*", text, re.DOTALL)
    if not m:
        raise RuntimeError("GLOSSARY_DATA が見つかりません")
    return ast.literal_eval(m.group(1))


def strip_html(text: str) -> str:
    text = re.sub(r"<[^>]+>", " ", text)
    text = html.unescape(text)
    return re.sub(r"\s+", " ", text).strip()


class SectionExtractor(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.sections: list[tuple[str, list[str]]] = []
        self._in_h2 = False
        self._in_p = False
        self._current_heading = ""
        self._buf: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag == "h2":
            self._flush_section()
            self._in_h2 = True
            self._buf = []
        elif tag == "p" and not self._in_h2:
            self._in_p = True
            self._buf = []

    def handle_endtag(self, tag: str) -> None:
        if tag == "h2":
            self._in_h2 = False
            self._current_heading = strip_html("".join(self._buf))
            self._buf = []
        elif tag == "p":
            if self._in_h2:
                return
            text = strip_html("".join(self._buf))
            if text and self._current_heading:
                if not self.sections or self.sections[-1][0] != self._current_heading:
                    self.sections.append((self._current_heading, []))
                self.sections[-1][1].append(text)
            self._in_p = False
            self._buf = []

    def handle_data(self, data: str) -> None:
        if self._in_h2 or self._in_p:
            self._buf.append(data)

    def _flush_section(self) -> None:
        self._current_heading = ""
        self._buf = []

    def close(self) -> None:
        super().close()
        self._flush_section()


def extract_faq_from_html(raw: str) -> list[tuple[str, str]]:
    out: list[tuple[str, str]] = []
    for block in re.findall(
        r'<script[^>]*type="application/ld\+json"[^>]*>(.*?)</script>',
        raw,
        re.I | re.DOTALL,
    ):
        try:
            data = json.loads(block.strip())
        except json.JSONDecodeError:
            continue
        nodes = data if isinstance(data, list) else [data]
        for node in nodes:
            if not isinstance(node, dict) or node.get("@type") != "FAQPage":
                continue
            for entity in node.get("mainEntity") or []:
                if not isinstance(entity, dict):
                    continue
                q = strip_html(str(entity.get("name") or ""))
                ans = entity.get("acceptedAnswer") or {}
                a = strip_html(str(ans.get("text") if isinstance(ans, dict) else ""))
                if q and a:
                    out.append((q, a))
    return out[:2]


def default_faqs(title: str) -> tuple[str, str, str, str]:
    short = title.split("｜")[0].split(" - ")[0][:60]
    return (
        f"{short}について、最初に何を確認すればよいですか？",
        "試験実施団体の公式サイトで最新の受験案内・出題範囲を確認してください。",
        f"{short}は独学でも活用できますか？",
        "はい。本文の手順に沿って、過去問演習と用語解説を組み合わせて進められます。",
    )


def apply_faqs(row: dict[str, str], faqs: list[tuple[str, str]]) -> None:
    if len(faqs) >= 2:
        row["faq_1_question"], row["faq_1_answer"] = faqs[0]
        row["faq_2_question"], row["faq_2_answer"] = faqs[1]
        return
    if len(faqs) == 1:
        row["faq_1_question"], row["faq_1_answer"] = faqs[0]
        q2, a2, _, _ = default_faqs(row["title"])
        row["faq_2_question"], row["faq_2_answer"] = q2, a2
        return
    q1, a1, q2, a2 = default_faqs(row["title"])
    row["faq_1_question"], row["faq_1_answer"] = q1, a1
    row["faq_2_question"], row["faq_2_answer"] = q2, a2


def genre_for_slug(slug: str, eyebrow: str = "") -> str:
    if eyebrow in EYEBROW_TO_GENRE:
        return EYEBROW_TO_GENRE[eyebrow]
    for hint, genre in SLUG_GENRE_HINTS:
        if hint in slug:
            return genre
    return "試験概要"


def batch_articles() -> list[dict]:
    """旧バッチ生成は廃止。再エクスポート時は takken/ または articles/ の HTML を利用。"""
    return []


def guide_row_from_batch(article: dict, priority: int) -> dict[str, str]:
    slug = article["slug"]
    sections: list[tuple[str, str]] = []
    for sec_id, heading in article.get("toc", []):
        m = re.search(
            rf'<h2[^>]*id="{re.escape(sec_id)}"[^>]*>.*?</h2>(.*?)(?=<h2|$)',
            article.get("body", ""),
            re.DOTALL | re.IGNORECASE,
        )
        body_html = m.group(1) if m else article.get("body", "")
        parser = SectionExtractor()
        parser.feed(body_html)
        parser.close()
        if parser.sections:
            for h, paras in parser.sections:
                sections.append((h, "\n\n".join(paras)))
        else:
            plain = strip_html(body_html)
            if plain:
                sections.append((heading, plain))

    if not sections:
        plain = strip_html(article.get("body", ""))
        if plain:
            sections.append((article.get("toc", [("main", "本文")])[0][1], plain))

    row: dict[str, str] = {
        "slug": slug,
        "genre": genre_for_slug(slug, article.get("eyebrow", "")),
        "title": article["title"],
        "meta_description": article["description"],
        "lead": article["lead"],
        "priority": str(priority),
        "tags": article.get("eyebrow", "").replace("宅建 ", ""),
        "author_name": "宅建マスター編集部",
        "author_profile": "宅建試験対策サイトの編集チーム",
        "reviewer_name": "公式情報確認担当",
        "reviewer_profile": "公開前に一次情報との照合を行う担当者",
        "fact_checked_at": FACT_DATE,
        "primary_sources": PRIMARY_SOURCES,
        "original_note": f"legacy batch から移行（{slug}）",
        "user_intent": article["lead"][:120],
        "action_items": "公式サイトで最新年度を確認する;過去問一覧で演習する",
        "update_policy": "試験要項や公式ページが更新されたタイミングで本文と参照元を見直します。",
        "last_reviewed_at": REVIEW_DATE,
        "next_review_at": NEXT_REVIEW,
        "source_checked_at": REVIEW_DATE,
        "content_status": "published",
        "revision_note": "export_legacy_data_to_csv.py による移行",
        "faq_1_question": "",
        "faq_1_answer": "",
        "faq_2_question": "",
        "faq_2_answer": "",
        "related_links": "",
    }
    apply_faqs(row, [])
    for i in range(1, 8):
        if i - 1 < len(sections):
            row[f"section_{i}_heading"] = sections[i - 1][0]
            row[f"section_{i}_body"] = sections[i - 1][1]
        else:
            row[f"section_{i}_heading"] = ""
            row[f"section_{i}_body"] = ""
    return row


def guide_row_from_html(slug: str, html_path: Path, priority: int) -> dict[str, str] | None:
    raw = html_path.read_text(encoding="utf-8", errors="replace")
    title_m = re.search(r"<title>([^<]+)</title>", raw, re.I)
    desc_m = re.search(r'<meta\s+name="description"\s+content="([^"]*)"', raw, re.I)
    lead_m = re.search(r'class="article-lead"[^>]*>(.*?)</p>', raw, re.I | re.DOTALL)
    eyebrow_m = re.search(r'class="article-eyebrow"[^>]*>([^<]+)<', raw, re.I)
    if not title_m:
        return None
    title = strip_html(title_m.group(1)).split(" - ")[0].split("｜")[0].strip()
    lead = strip_html(lead_m.group(1)) if lead_m else ""
    parser = SectionExtractor()
    main_m = re.search(r"<main[^>]*>(.*)</main>", raw, re.I | re.DOTALL)
    parser.feed(main_m.group(1) if main_m else raw)
    parser.close()
    sections = [(h, "\n\n".join(ps)) for h, ps in parser.sections if h and "信頼性" not in h][:7]
    row = guide_row_from_batch(
        {
            "slug": slug,
            "title": title,
            "description": desc_m.group(1) if desc_m else lead[:155],
            "lead": lead or title,
            "eyebrow": eyebrow_m.group(1).strip() if eyebrow_m else "",
            "toc": [],
            "body": "",
        },
        priority,
    )
    for i in range(1, 8):
        if i - 1 < len(sections):
            row[f"section_{i}_heading"] = sections[i - 1][0]
            row[f"section_{i}_body"] = sections[i - 1][1]
    apply_faqs(row, extract_faq_from_html(raw))
    return row


def write_csv(path: Path, header: list[str], rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=header, lineterminator="\n")
        w.writeheader()
        for row in rows:
            w.writerow({k: row.get(k, "") for k in header})
    print(f"wrote {path} ({len(rows)} rows)")


def export_glossary() -> None:
    items = parse_glossary_js(GLOSSARY_JS)
    rows: list[dict[str, str]] = []
    seen: dict[tuple[str, str], dict[str, str]] = {}
    for item in items:
        term = str(item.get("term") or "").strip()
        if not term:
            continue
        cat = CAT_TO_CATEGORY.get(str(item.get("cat") or ""), "試験対策")
        summary = str(item.get("summary") or "").strip()
        desc = str(item.get("desc") or "").strip()
        reading = str(item.get("reading") or "").strip()
        key = (term, reading)
        row = {
            "term": term,
            "reading": reading,
            "category": cat,
            "tags": cat,
            "short_def": summary or desc[:80],
            "definition": desc or summary,
            "related_terms": "",
            "legal_basis": "",
            "importance": "A",
            "explanation": desc,
            "article_title": f"{term}とは",
            "article_lead": summary or desc[:120],
            "term_detail_body": desc,
            "exam_points": desc,
            "common_mistakes": "",
            "memory_tip": "",
            "example_question": "",
            "example_answer": "",
            "faq_1_question": "",
            "faq_1_answer": "",
            "faq_2_question": "",
            "faq_2_answer": "",
        }
        prev = seen.get(key)
        if prev is None or len(row["definition"]) > len(prev["definition"]):
            seen[key] = row
    write_csv(GLOSSARY_CSV, GLOSSARY_HEADER, list(seen.values()))


def export_past() -> None:
    rows = rows_from_master_js(MASTER_JS)
    write_csv(PAST_CSV, PAST_HEADER, rows)


def export_guide() -> None:
    rows_by_slug: dict[str, dict[str, str]] = {}
    priority = 10
    for article in batch_articles():
        rows_by_slug[article["slug"]] = guide_row_from_batch(article, priority)
        priority += 10

    for slug_dir in sorted(TAKKEN_DIR.iterdir()):
        if not slug_dir.is_dir():
            continue
        slug = slug_dir.name
        html_path = slug_dir / "index.html"
        if not html_path.is_file() or slug in rows_by_slug:
            continue
        row = guide_row_from_html(slug, html_path, priority)
        if row:
            rows_by_slug[slug] = row
            priority += 10

    write_csv(GUIDE_CSV, GUIDE_HEADER, list(rows_by_slug.values()))


def main() -> int:
    export_glossary()
    export_past()
    export_guide()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
