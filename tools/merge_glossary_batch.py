#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""data/glossary_batch*.json を takken-data-glossary.js に追記する。"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GLOSSARY_JS = ROOT / "takken-data-glossary.js"


def load_glossary_array() -> list[dict]:
    text = GLOSSARY_JS.read_text(encoding="utf-8")
    m = re.search(r"const\s+GLOSSARY_DATA\s*=\s*(\[.*\])\s*;", text, re.S)
    if not m:
        raise SystemExit("GLOSSARY_DATA not found")
    return json.loads(m.group(1))


def write_glossary_array(data: list[dict]) -> None:
    text = GLOSSARY_JS.read_text(encoding="utf-8")
    payload = json.dumps(data, ensure_ascii=False, indent=2)
    new_text, n = re.subn(
        r"const\s+GLOSSARY_DATA\s*=\s*\[.*\]\s*;",
        f"const GLOSSARY_DATA = {payload};",
        text,
        count=1,
        flags=re.S,
    )
    if n != 1:
        raise SystemExit("failed to replace GLOSSARY_DATA")
    GLOSSARY_JS.write_text(new_text, encoding="utf-8")


def main() -> None:
    batch_path = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "data" / "glossary_batch35.json"
    additions = json.loads(batch_path.read_text(encoding="utf-8"))
    if not isinstance(additions, list):
        raise SystemExit("batch file must be a JSON array")

    data = load_glossary_array()
    existing_slugs = {
        (item.get("articleSlug") or str(item.get("id", "")).replace("_", "-")).strip()
        for item in data
    }
    added = 0
    for item in additions:
        slug = (item.get("articleSlug") or str(item.get("id", "")).replace("_", "-")).strip()
        if not slug:
            continue
        if slug in existing_slugs:
            print(f"skip duplicate slug: {slug}")
            continue
        data.append(item)
        existing_slugs.add(slug)
        added += 1
        print(f"added: {slug}")

    write_glossary_array(data)
    print(f"total entries: {len(data)} (+{added})")


if __name__ == "__main__":
    main()
