#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""CSVから手書き未登録用語のスケルトンを出力（編集補助）。"""

from __future__ import annotations

import csv
import json
from pathlib import Path

from tools.glossary_hand_rewrite import HAND_REWRITE
from tools.glossary_enrich import norm

ROOT = Path(__file__).resolve().parents[1]
GLOSSARY_CSV = ROOT / "data" / "glossary_terms.csv"


def main() -> int:
    rows = list(csv.DictReader(GLOSSARY_CSV.read_text(encoding="utf-8-sig").splitlines()))
    hand = {norm(k) for k in HAND_REWRITE}
    out: list[dict] = []
    for r in rows:
        term = norm(r.get("term"))
        if not term or term in hand:
            continue
        out.append(
            {
                "term": term,
                "category": norm(r.get("category")),
                "related_terms": norm(r.get("related_terms")),
                "legal_basis": norm(r.get("legal_basis")),
                "short_def": norm(r.get("short_def")),
            }
        )
    path = ROOT / "data" / "glossary_hand_missing.json"
    path.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Wrote {len(out)} missing terms to {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
