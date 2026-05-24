#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""takken-data-original.js の ORIG_QUESTIONS → data/practice_questions.csv"""

from __future__ import annotations

import csv
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from tools.build_past_question_pages import master_question_correct, norm  # noqa: E402
from tools.orig_units import FIELD_LABELS, unit_label  # noqa: E402

ORIG_JS = ROOT / "takken-data-original.js"
OUT_CSV = ROOT / "data" / "practice_questions.csv"

PRACTICE_HEADER = [
    "question_no",
    "type",
    "category",
    "level",
    "unit",
    "unit_label",
    "field",
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
    "explanation",
]


def load_orig_questions(js_path: Path) -> list[dict]:
    script = f"""
const fs = require('fs');
const code = fs.readFileSync({json.dumps(str(js_path))}, 'utf8');
const fn = new Function(code + '; return ORIG_QUESTIONS;');
const o = fn();
const all = [...(o[1]||[]),...(o[2]||[]),...(o[3]||[])];
process.stdout.write(JSON.stringify(all));
"""
    proc = subprocess.run(
        ["node", "-e", script],
        capture_output=True,
        text=True,
        check=True,
    )
    data = json.loads(proc.stdout)
    if not isinstance(data, list):
        raise ValueError("ORIG_QUESTIONS の展開結果が配列ではありません")
    return data


def question_to_row(q: dict) -> dict[str, str] | None:
    qid = int(q["id"])
    opts = q.get("opts") or []
    if len(opts) != 4:
        return None
    ci = master_question_correct(q)
    if ci is None:
        try:
            ans = int(q.get("ans"))
        except (TypeError, ValueError):
            return None
        if 0 <= ans <= 3:
            ci = ans + 1
        else:
            return None
    field = norm(q.get("field"))
    unit = norm(q.get("unit"))
    level = int(q.get("level", 1))
    return {
        "question_no": str(qid),
        "type": "single",
        "category": FIELD_LABELS.get(field, field or "その他"),
        "level": str(level),
        "unit": unit,
        "unit_label": unit_label(unit),
        "field": field,
        "tags": unit_label(unit),
        "stem": norm(q.get("text")),
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
        "explanation": norm(q.get("exp")) or "（解説は未入力です。）",
    }


def main() -> int:
    import argparse

    ap = argparse.ArgumentParser(description="ORIG_QUESTIONS を practice_questions.csv に書き出す")
    ap.add_argument("--js", type=Path, default=ORIG_JS)
    ap.add_argument("--out", type=Path, default=OUT_CSV)
    args = ap.parse_args()
    js_path = args.js.resolve()
    if not js_path.is_file():
        print(f"Missing {js_path}", file=sys.stderr)
        return 1

    items = load_orig_questions(js_path)
    rows: list[dict[str, str]] = []
    skipped = 0
    for q in items:
        row = question_to_row(q)
        if row is None:
            skipped += 1
            continue
        rows.append(row)
    rows.sort(key=lambda r: int(r["question_no"]))

    out_path = args.out.resolve()
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=PRACTICE_HEADER, lineterminator="\n")
        w.writeheader()
        w.writerows(rows)

    print(f"Wrote {out_path} ({len(rows)} rows, skipped {skipped})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
