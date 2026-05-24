#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""模試50問セットを data/mock_sets.csv に出力（SPA startMockExam と同じ抽選ロジック）。"""

from __future__ import annotations

import csv
import random
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from tools.build_past_question_pages import FIELD_LABELS_JS, load_rows, norm  # noqa: E402
from tools.mock_exam_config import MOCK_DIST, MOCK_PATTERNS  # noqa: E402

PAST_CSV = ROOT / "data" / "past_questions.csv"
OUT_CSV = ROOT / "data" / "mock_sets.csv"

HEADER = [
    "pattern_id",
    "pattern_title",
    "seq",
    "source",
    "question_id",
    "exam_year",
    "question_no",
    "field",
    "category",
    "stem_preview",
    "static_href",
]


def field_from_category(cat: str) -> str:
    inv = {v: k for k, v in FIELD_LABELS_JS.items()}
    return inv.get(norm(cat), "")


def past_items(rows: list[dict]) -> list[dict]:
    out: list[dict] = []
    for row in rows:
        try:
            year = int(row["exam_year"])
            num = int(row["question_no"])
        except (KeyError, ValueError):
            continue
        field = field_from_category(row.get("category", ""))
        if not field:
            continue
        stem = norm(row.get("stem"))[:52]
        out.append(
            {
                "source": "past",
                "question_id": year * 100 + num,
                "year": year,
                "num": num,
                "field": field,
                "category": norm(row.get("category")),
                "stem_preview": stem,
                "static_href": f"q/past/y{year}/q{num:02d}/index.html",
            }
        )
    return out


def build_queue(pat: dict, pool: list[dict], rng: random.Random) -> list[dict]:
    years = set(pat["years"])
    filtered = [q for q in pool if q["year"] in years]
    queue: list[dict] = []
    used: set[int] = set()
    for field, n in MOCK_DIST.items():
        take: list[dict] = []

        def pick_from(candidates: list[dict]) -> None:
            rng.shuffle(candidates)
            for q in candidates:
                if len(take) >= n:
                    break
                if q["question_id"] in used:
                    continue
                take.append(q)
                used.add(q["question_id"])

        pick_from([q for q in filtered if q["field"] == field])
        if len(take) < n:
            pick_from([q for q in pool if q["field"] == field])
        queue.extend(take)
    rng.shuffle(queue)
    return queue[:50]


def main() -> int:
    rows = load_rows(PAST_CSV)
    if not rows:
        print(f"Missing past data: {PAST_CSV}", file=sys.stderr)
        return 1
    pool = past_items(rows)
    out_rows: list[dict[str, str]] = []
    for pat in MOCK_PATTERNS:
        rng = random.Random(pat["id"] * 10007 + 42)
        queue = build_queue(pat, pool, rng)
        if len(queue) < 50:
            print(
                f"warn: pattern {pat['id']} only {len(queue)} questions "
                f"(years={pat['years']})",
                file=sys.stderr,
            )
        for seq, q in enumerate(queue, start=1):
            out_rows.append(
                {
                    "pattern_id": str(pat["id"]),
                    "pattern_title": pat["title"],
                    "seq": str(seq),
                    "source": q["source"],
                    "question_id": str(q["question_id"]),
                    "exam_year": str(q["year"]),
                    "question_no": str(q["num"]),
                    "field": q["field"],
                    "category": q["category"],
                    "stem_preview": q["stem_preview"],
                    "static_href": q["static_href"],
                }
            )
    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    with OUT_CSV.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=HEADER, lineterminator="\n")
        w.writeheader()
        w.writerows(out_rows)
    print(f"Wrote {OUT_CSV} ({len(out_rows)} rows, {len(MOCK_PATTERNS)} patterns)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
