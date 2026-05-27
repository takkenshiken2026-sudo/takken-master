#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""公開コンテンツの誤字・重複・プレースホルダ・リンク切れ候補を一括監査。"""

from __future__ import annotations

import argparse
import csv
import re
import subprocess
import sys
from dataclasses import dataclass
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# 意図的な重複を許容（例: 々、ゝ、ヽ、ゞ）
DUP_CHAR_ALLOW = frozenset("々ゝヽヾぁぃぅぇぉっゃゅょゎー")

# 誤記・不自然表現の検出パターン（誤った文字列, 説明）
BAD_STRING_PATTERNS: list[tuple[str, str]] = [
    # 宅地建物取引業法は正当。単独の「取引業」誤記のみ（後段で法を除外）
    ("取引士業", "「取引士業」の誤記"),
    ("容積綠", "誤字（容積率）"),
    ("民放", "誤字（民法）"),
    ("宅建師", "誤字（宅建士）"),
    ("宅地建物取引師", "誤字（取引士）"),
    ("報酬額額", "重複誤り"),
    ("についてについて", "重複表現"),
    ("することができます", "冗長表現"),
    ("であるである", "重複表現"),
    ("ですです", "重複表現"),
    ("ますます", "重複表現"),
    ("でしたでした", "重複表現"),
    ("。。", "句読点重複"),
    ("、、", "読点重複"),
    ("！！", "記号重複"),
    ("？？", "記号重複"),
]

PLACEHOLDER_PATTERNS = [
    (r"【本文を記入】", "本文差し替えプレースホルダ"),
    (r"【行動\d+】", "行動項目プレースホルダ"),
    (r"◯◯試験", "試験名プレースホルダ"),
    (r"差し替えてください", "編集者向け差し替え指示"),
    (r"受験者が迷いやすい点を具体的に説明し", "テンプレ指示文"),
    (r"\bLorem\b", "Lorem ipsum プレースホルダ"),
    (r"\bTODO\b", "TODO プレースホルダ"),
    (r"\bFIXME\b", "FIXME プレースホルダ"),
    (r"（ここに", "差し替え指示"),
    (r"ここに本文", "差し替え指示"),
    (r"サンプルテキスト", "サンプル文言"),
    (r"ダミー", "ダミー文言"),
    (r"未記入", "未記入プレースホルダ"),
    (r"ああああ", "テスト文字列"),
    (r"xxxx", "テスト文字列"),
]

# 高信頼度の語尾重複のみ（助詞連続は誤検知が多いため対象外）
POLITE_DUP_RE = re.compile(r"(?:ですです|ますます|であるである|でしたでした)")

HREF_EMPTY_RE = re.compile(r"""href\s*=\s*(["'])\s*\1""", re.I)
HREF_HASH_ONLY_RE = re.compile(r"""href\s*=\s*(["'])#\1""", re.I)

REDIRECT_RE = re.compile(r"refresh\s+content\s*=\s*['\"]?0;\s*url=", re.I)

PUBLIC_HTML_GLOBS = [
    "index.html",
    "about.html",
    "privacy.html",
    "related-sites.html",
    "author.html",
    "articles/index.html",
    "articles/*/index.html",
    "terms/index.html",
    "terms/field-*/index.html",
    "terms/g-*.html",
    "q/index.html",
    "q/past/**/index.html",
    "q/mock/**/index.html",
    "q/field/**/index.html",
    "q/orig/**/index.html",
]

CSV_PATHS = [
    "data/past_questions.csv",
    "data/practice_questions.csv",
    "data/glossary_terms.csv",
    "data/guide_articles.csv",
    "data/ichimon_questions.csv",
]


class TextExtractor(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self._skip = 0
        self.parts: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag in ("script", "style", "noscript"):
            self._skip += 1

    def handle_endtag(self, tag: str) -> None:
        if tag in ("script", "style", "noscript") and self._skip:
            self._skip -= 1

    def handle_data(self, data: str) -> None:
        if self._skip:
            return
        t = data.strip()
        if t:
            self.parts.append(t)


@dataclass
class Finding:
    level: str
    source: str
    message: str
    snippet: str = ""

    def format(self) -> str:
        base = f"[{self.level}] {self.source} - {self.message}"
        if self.snippet:
            base += f" | {self.snippet[:120]}"
        return base


def strip_html(text: str) -> str:
    p = TextExtractor()
    try:
        p.feed(text)
    except Exception:
        return text
    return "\n".join(p.parts)


def is_redirect_html(text: str) -> bool:
    return bool(REDIRECT_RE.search(text[:800]))


def collect_html_files() -> list[Path]:
    out: list[Path] = []
    for pattern in PUBLIC_HTML_GLOBS:
        out.extend(ROOT.glob(pattern))
    seen: set[Path] = set()
    unique: list[Path] = []
    for path in sorted(out):
        rp = path.resolve()
        if rp not in seen and path.is_file():
            seen.add(rp)
            unique.append(path)
    return unique


def line_snippet(text: str, pos: int, width: int = 40) -> str:
    start = max(0, pos - width)
    end = min(len(text), pos + width)
    return text[start:end].replace("\n", " ")


def scan_text(
    findings: list[Finding],
    source: str,
    text: str,
    *,
    level_for_typos: str = "ERROR",
) -> None:
    if not text.strip():
        return

    for bad, reason in BAD_STRING_PATTERNS:
        if bad not in text:
            continue
        idx = text.find(bad)
        lvl = "WARN" if bad in ("することができます",) else level_for_typos
        findings.append(
            Finding(
                lvl,
                source,
                f"誤記候補「{bad}」: {reason}",
                line_snippet(text, idx),
            )
        )
    for pat, reason in PLACEHOLDER_PATTERNS:
        for m in re.finditer(pat, text, flags=re.I):
            findings.append(
                Finding(
                    "ERROR",
                    source,
                    reason,
                    line_snippet(text, m.start()),
                )
            )

    if "  " in text:
        findings.append(Finding("WARN", source, "半角スペースが連続", ""))
    if "　　" in text:
        findings.append(Finding("WARN", source, "全角スペースが連続", ""))
    if "。。" in text or "、、" in text:
        findings.append(Finding("ERROR", source, "句読点の重複", ""))

    for m in POLITE_DUP_RE.finditer(text):
        findings.append(
            Finding(
                "ERROR",
                source,
                f"語尾の重複「{m.group()}」",
                line_snippet(text, m.start()),
            )
        )


def scan_html(path: Path, findings: list[Finding]) -> None:
    rel = str(path.relative_to(ROOT))
    raw = path.read_text(encoding="utf-8", errors="replace")
    if is_redirect_html(raw):
        return

    if HREF_EMPTY_RE.search(raw):
        findings.append(Finding("ERROR", rel, "空の href", ""))
    if HREF_HASH_ONLY_RE.search(raw):
        findings.append(Finding("WARN", rel, "href=\"#\" のみ", ""))

    body_text = strip_html(raw)
    scan_text(findings, rel, body_text)

    # title / meta description
    for m in re.finditer(r"<title>([^<]+)</title>", raw, re.I):
        scan_text(findings, f"{rel}:<title>", m.group(1))
    for m in re.finditer(
        r'<meta[^>]+name=["\']description["\'][^>]+content=["\']([^"\']+)',
        raw,
        re.I,
    ):
        scan_text(findings, f"{rel}:meta description", m.group(1))


def scan_csv(path: Path, findings: list[Finding]) -> None:
    """CSV はプレースホルダ・編集指示のみ検査（過去問・解説の正当表現は対象外）。"""
    rel = str(path.relative_to(ROOT))
    placeholder_only = {"guide_articles.csv"}
    with path.open(encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        for i, row in enumerate(reader, start=2):
            for col, val in row.items():
                if not val or col.startswith("_"):
                    continue
                if col in ("slug", "id", "term_id", "hash", "url", "image_url"):
                    continue
                if len(val) < 3:
                    continue
                src = f"{rel}:{i}:{col}"
                if path.name in placeholder_only:
                    scan_text(findings, src, val)
                else:
                    for pat, reason in PLACEHOLDER_PATTERNS:
                        if re.search(pat, val, flags=re.I):
                            findings.append(
                                Finding("ERROR", src, reason, line_snippet(val, 0))
                            )


def run_link_validator(deploy: bool) -> int:
    cmd = [sys.executable, "tools/validate_internal_links.py"]
    if deploy:
        cmd.append("--deploy")
    print("+", " ".join(cmd))
    return subprocess.call(cmd, cwd=ROOT)


def main() -> int:
    parser = argparse.ArgumentParser(description="公開コンテンツ品質監査")
    parser.add_argument("--skip-links", action="store_true")
    parser.add_argument("--deploy-links", action="store_true")
    parser.add_argument("--errors-only", action="store_true")
    args = parser.parse_args()

    findings: list[Finding] = []

    html_files = collect_html_files()
    print(f"Scanning {len(html_files)} HTML file(s)...")
    for path in html_files:
        scan_html(path, findings)

    for rel in CSV_PATHS:
        p = ROOT / rel
        if p.is_file():
            print(f"Scanning CSV {rel}...")
            scan_csv(p, findings)

    levels = ("ERROR",) if args.errors_only else ("ERROR", "WARN")
    shown = [f for f in findings if f.level in levels]
    shown.sort(key=lambda f: (f.level, f.source))

    err_count = sum(1 for f in shown if f.level == "ERROR")
    warn_count = sum(1 for f in shown if f.level == "WARN")

    for f in shown[:500]:
        print(f.format())
    if len(shown) > 500:
        print(f"... and {len(shown) - 500} more")

    print(
        f"\nContent audit: {err_count} error(s), {warn_count} warning(s) "
        f"({len(html_files)} HTML, {len(CSV_PATHS)} CSV sources)"
    )

    link_rc = 0
    if not args.skip_links:
        link_rc = run_link_validator(args.deploy_links)

    if err_count or link_rc:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
