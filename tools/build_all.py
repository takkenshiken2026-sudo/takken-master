#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""One-command build for takken-master (exam-site-shell 準拠)."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def run(cmd: list[str]) -> None:
    print("+", " ".join(cmd))
    subprocess.run(cmd, cwd=ROOT, check=True)


def main() -> int:
    py = sys.executable
    run([py, "tools/validate_csv.py"])
    run([py, "tools/apply_site_config.py"])
    run([py, "tools/csv_to_takken_master_js.py"])
    run([py, "tools/csv_to_takken_glossary_js.py"])
    run([py, "tools/csv_to_exam_site_ichimondou_js.py"])
    run([py, "tools/export_orig_to_practice_csv.py"])
    run([py, "tools/build_past_question_pages.py"])
    run([py, "tools/build_practice_ichimon_pages.py"])
    run([py, "tools/build_practice_question_pages.py"])
    run([py, "tools/generate_mock_sets.py"])
    run([py, "tools/build_mock_pages.py"])
    run([py, "tools/build_article_pages.py"])
    run([py, "tools/build_glossary_pages.py"])
    run([py, "tools/build_compare_pages.py"])
    run([py, "tools/build_numbers_mistakes_pages.py"])
    run([py, "tools/build_sitemap.py"])
    run([py, "tools/validate_sitemap.py"])
    run([py, "tools/validate_generated_seo.py"])
    run([py, "tools/validate_site_integration.py"])
    run([py, "tools/validate_internal_links.py"])
    run([py, "tools/validate_internal_links.py", "--deploy"])
    run([py, "tools/validate_public_content.py"])
    run([py, "tools/build_legacy_redirects.py"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
