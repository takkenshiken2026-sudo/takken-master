#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""過去問 CSV の正答列と解説本文の整合を検証する。"""

from __future__ import annotations

import argparse
import csv
import re
import sys
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

DEFAULT_CSV = ROOT / "data" / "past_questions.csv"

EXPL_FIELDS = (
    "explanation",
    "explanation_correct",
    "explanation_summary",
)

# 選択肢別解説はビルド時に生成・補完されるため、正答推定の根拠には使わない
EXPL_CHOICE_FIELD = "explanation_choices"

WRONG_MARK = re.compile(r"[（(]?(\d)[）)]?\s*は\s*(?:誤|不正|不適|×)")
STATED_MARK = re.compile(r"正(?:答|解)[はが]\s*[（(]?(\d)[）)]?")
CHOICE_FOCUS = re.compile(r"選択肢\s*(\d)\s*の\s*結論")


def norm(value: object) -> str:
    return str(value or "").strip()


def combined_explanation(row: dict) -> str:
    return " ".join(norm(row.get(field)) for field in EXPL_FIELDS)


def wrong_choices(text: str) -> set[int]:
    return {int(m.group(1)) for m in WRONG_MARK.finditer(text)}


def stated_answers(text: str) -> list[int]:
    return [int(m.group(1)) for m in STATED_MARK.finditer(text)]


def infer_correct_from_explanation(row: dict) -> tuple[int | None, str]:
    text = combined_explanation(row)
    wrong = wrong_choices(text)
    stated = stated_answers(text)
    focus = [int(m.group(1)) for m in CHOICE_FOCUS.finditer(text)]
    not_wrong = {1, 2, 3, 4} - wrong

    if stated:
        return stated[-1], "stated"
    if len(not_wrong) == 1:
        return next(iter(not_wrong)), "not_wrong"
    if focus:
        return focus[-1], "focus"
    return None, ""


@dataclass
class Issue:
    line: int
    year: int
    qno: int
    correct: int
    inferred: int | None
    reason: str
    method: str
    snippet: str

    @property
    def key(self) -> str:
        return f"{self.year}-{self.qno:02d}"

    def format(self) -> str:
        inferred = self.inferred if self.inferred is not None else "?"
        return (
            f"[ERROR] past_questions.csv:{self.line} {self.key} "
            f"correct={self.correct} inferred={inferred} "
            f"({self.reason}/{self.method}) | {self.snippet[:100]}"
        )


def find_issues(rows: list[dict]) -> list[Issue]:
    issues: list[Issue] = []
    for line_no, row in enumerate(rows, start=2):
        if norm(row.get("is_invalidated")).upper() == "TRUE":
            continue
        try:
            correct = int(norm(row.get("correct")))
        except ValueError:
            continue

        text = combined_explanation(row)
        wrong = wrong_choices(text)
        stated = stated_answers(text)
        inferred, method = infer_correct_from_explanation(row)

        reason = ""
        if correct in wrong:
            reason = "correct_marked_wrong"
        elif stated and stated[-1] != correct:
            reason = "stated_mismatch"

        if not reason:
            continue

        snippet = text
        for field in EXPL_FIELDS:
            field_text = norm(row.get(field))
            if not field_text:
                continue
            if correct in wrong and WRONG_MARK.search(field_text):
                snippet = field_text
                break
            if stated and STATED_MARK.search(field_text):
                snippet = field_text
                break

        issues.append(
            Issue(
                line=line_no,
                year=int(row["exam_year"]),
                qno=int(row["question_no"]),
                correct=correct,
                inferred=inferred,
                reason=reason,
                method=method,
                snippet=snippet,
            )
        )
    return issues


def apply_fixes(rows: list[dict], issues: list[Issue]) -> int:
    by_key = {(i.year, i.qno): i for i in issues}
    changed = 0
    for row in rows:
        try:
            key = (int(row["exam_year"]), int(row["question_no"]))
        except ValueError:
            continue
        issue = by_key.get(key)
        if not issue or issue.inferred is None or issue.inferred == issue.correct:
            continue
        row["correct"] = str(issue.inferred)
        changed += 1
    return changed


def load_rows(path: Path) -> list[dict]:
    text = path.read_text(encoding="utf-8-sig")
    return list(csv.DictReader(text.splitlines()))


def write_rows(path: Path, rows: list[dict]) -> None:
    if not rows:
        return
    fieldnames = list(rows[0].keys())
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def main() -> int:
    parser = argparse.ArgumentParser(description="過去問の正答と解説の整合性を検証")
    parser.add_argument("--csv", type=Path, default=DEFAULT_CSV)
    parser.add_argument("--fix", action="store_true", help="解説から推定した正答で CSV を更新")
    args = parser.parse_args()

    if not args.csv.is_file():
        print(f"CSV not found: {args.csv}", file=sys.stderr)
        return 1

    rows = load_rows(args.csv)
    issues = find_issues(rows)

    if args.fix:
        changed = apply_fixes(rows, issues)
        if changed:
            write_rows(args.csv, rows)
            print(f"Updated correct column for {changed} question(s) in {args.csv.relative_to(ROOT)}")
        rows = load_rows(args.csv)
        issues = find_issues(rows)

    for issue in issues:
        print(issue.format())

    print(f"\nPast answer consistency: {len(issues)} error(s)")
    return 1 if issues else 0


if __name__ == "__main__":
    raise SystemExit(main())
