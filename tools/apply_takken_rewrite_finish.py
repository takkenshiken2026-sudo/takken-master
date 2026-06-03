#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""宅建 guide 残り30本の手書きリライトを一括適用。"""

from __future__ import annotations

import csv
import importlib.util
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TODAY = "2026-06-04"
REVISION = f"{TODAY}: 手書きリライト"

BATCH_MODULES = [
    "apply_takken_rewrite_batch5",
    "apply_takken_rewrite_batch6",
    "apply_takken_rewrite_batch7",
    "apply_takken_rewrite_batch8",
    "apply_takken_rewrite_batch9",
    "apply_takken_rewrite_batch10",
]


def load_rewrites() -> dict[str, dict[str, str]]:
    merged: dict[str, dict[str, str]] = {}
    tools = ROOT / "tools"
    for name in BATCH_MODULES:
        path = tools / f"{name}.py"
        spec = importlib.util.spec_from_file_location(name, path)
        if spec is None or spec.loader is None:
            raise SystemExit(f"missing {path}")
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        block = getattr(mod, "REWRITES", {})
        overlap = set(merged) & set(block)
        if overlap:
            raise SystemExit(f"duplicate slugs in {name}: {overlap}")
        merged.update(block)
    return merged


def apply_rewrites(csv_path: Path, rewrites: dict[str, dict[str, str]]) -> int:
    rows = list(csv.DictReader(csv_path.open(encoding="utf-8-sig")))
    fieldnames = rows[0].keys()
    n = 0
    for row in rows:
        slug = row.get("slug", "")
        if slug not in rewrites:
            continue
        patch = rewrites[slug]
        row["revision_note"] = REVISION
        row["fact_checked_at"] = TODAY
        row["last_reviewed_at"] = TODAY
        row["source_checked_at"] = TODAY
        row["original_note"] = f"手書きリライト {TODAY}。"
        for k, v in patch.items():
            row[k] = v
        n += 1
    with csv_path.open("w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames, lineterminator="\n")
        w.writeheader()
        w.writerows(rows)
    return n


def main() -> int:
    rewrites = load_rewrites()
    csv_path = ROOT / "data" / "guide_articles.csv"
    n = apply_rewrites(csv_path, rewrites)
    print(f"patched {n} rows ({len(rewrites)} defined)")
    if n != len(rewrites):
        print("WARN: patched count != defined count", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
