#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""宅建 知識ハブ CSV 統合出力（CSVベース + S31-S44 追加分、再実行で重複しない）."""

from __future__ import annotations

import csv
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from tools.hub_faq_expand import expand_all as expand_short_faqs  # noqa: E402
from tools.write_takken_hub_s30 import (  # noqa: E402
    DATA,
    HEADER_COMPARE,
    HEADER_MISTAKES,
    HEADER_NUMBERS,
)
from tools.write_takken_hub_s31_content import (  # noqa: E402
    COMPARISONS_ADD as COMPARISONS_ADD_S31,
    MISTAKES_ADD as MISTAKES_ADD_S31,
    NUMBERS_ADD as NUMBERS_ADD_S31,
)
from tools.write_takken_hub_s32_content import (  # noqa: E402
    COMPARISONS_ADD as COMPARISONS_ADD_S32,
    MISTAKES_ADD as MISTAKES_ADD_S32,
    NUMBERS_ADD as NUMBERS_ADD_S32,
)
from tools.write_takken_hub_s33_content import (  # noqa: E402
    COMPARISONS_ADD as COMPARISONS_ADD_S33,
    MISTAKES_ADD as MISTAKES_ADD_S33,
    NUMBERS_ADD as NUMBERS_ADD_S33,
)
from tools.write_takken_hub_s34_content import (  # noqa: E402
    COMPARISONS_ADD as COMPARISONS_ADD_S34,
    MISTAKES_ADD as MISTAKES_ADD_S34,
    NUMBERS_ADD as NUMBERS_ADD_S34,
)
from tools.write_takken_hub_s35_content import (  # noqa: E402
    COMPARISONS_ADD as COMPARISONS_ADD_S35,
    MISTAKES_ADD as MISTAKES_ADD_S35,
    NUMBERS_ADD as NUMBERS_ADD_S35,
)
from tools.write_takken_hub_s36_content import (  # noqa: E402
    COMPARISONS_ADD as COMPARISONS_ADD_S36,
    MISTAKES_ADD as MISTAKES_ADD_S36,
    NUMBERS_ADD as NUMBERS_ADD_S36,
)
from tools.write_takken_hub_s37_content import (  # noqa: E402
    COMPARISONS_ADD as COMPARISONS_ADD_S37,
    MISTAKES_ADD as MISTAKES_ADD_S37,
    NUMBERS_ADD as NUMBERS_ADD_S37,
)
from tools.write_takken_hub_s38_content import (  # noqa: E402
    COMPARISONS_ADD as COMPARISONS_ADD_S38,
    MISTAKES_ADD as MISTAKES_ADD_S38,
    NUMBERS_ADD as NUMBERS_ADD_S38,
)
from tools.write_takken_hub_s39_content import (  # noqa: E402
    COMPARISONS_ADD as COMPARISONS_ADD_S39,
    MISTAKES_ADD as MISTAKES_ADD_S39,
    NUMBERS_ADD as NUMBERS_ADD_S39,
)
from tools.write_takken_hub_s40_content import (  # noqa: E402
    COMPARISONS_ADD as COMPARISONS_ADD_S40,
    MISTAKES_ADD as MISTAKES_ADD_S40,
    NUMBERS_ADD as NUMBERS_ADD_S40,
)
from tools.write_takken_hub_s41_content import (  # noqa: E402
    COMPARISONS_ADD as COMPARISONS_ADD_S41,
    MISTAKES_ADD as MISTAKES_ADD_S41,
    NUMBERS_ADD as NUMBERS_ADD_S41,
)
from tools.write_takken_hub_s42_content import (  # noqa: E402
    COMPARISONS_ADD as COMPARISONS_ADD_S42,
    MISTAKES_ADD as MISTAKES_ADD_S42,
    NUMBERS_ADD as NUMBERS_ADD_S42,
)
from tools.write_takken_hub_s43_content import (  # noqa: E402
    COMPARISONS_ADD as COMPARISONS_ADD_S43,
    MISTAKES_ADD as MISTAKES_ADD_S43,
    NUMBERS_ADD as NUMBERS_ADD_S43,
)
from tools.write_takken_hub_s44_content import (  # noqa: E402
    COMPARISONS_ADD as COMPARISONS_ADD_S44,
    MISTAKES_ADD as MISTAKES_ADD_S44,
    NUMBERS_ADD as NUMBERS_ADD_S44,
)
from tools.write_takken_hub_premium_faqs import apply_all as apply_premium_faqs  # noqa: E402

# 再実行時に CSV に残った S31-S44 以外の追加分を base に含めない（原本10件のみ）
_BASE_COMPARE_SLUGS = {
    "ju35-ju37-hikaku",
    "baikai-dairi-hikaku",
    "senren-baikai-shurui",
    "futsu-teiki-chitai",
    "kenpei-yoseki",
    "toji-chintai-ken",
    "tetsuki-iwayoku",
    "kotei-toshizei",
    "futsu-teiki-chintai",
    "teito-konteito",
}
_BASE_NUMBER_SLUGS = {
    "takken-shiken-goukaku-shutsudai",
    "ju35-ju37-kigen",
    "tetsuki-hoshu-jogen",
    "teitiku-nensu-koushin",
    "seinin-hogo-nenrei",
    "zeiritsu-kotei-toshi",
    "yoto-kenpei-yoseki",
    "takken-haczei-karyou",
    "touki-souzoku-touki-kigen",
    "senren-hokoku-kikan",
}
_BASE_MISTAKE_SLUGS = {
    "toji-ken-tochi-chintai-ken-kon",
    "kotei-shisanzei-toshikeikakuzei-kon",
    "cooling-off-tetsuke-kaijo-kon",
    "kenpeiritsu-yosekiritsu-keisan",
    "sennin-baikai-ippan-baikai",
    "seinin-18-vs-20",
    "takkenshi-menkyo-kon",
    "ju35-ju37-shomen-kon",
    "futsu-teiki-chintai-kon",
    "teito-konteito-kon",
}

_ADD_GROUPS = (
    COMPARISONS_ADD_S31,
    NUMBERS_ADD_S31,
    MISTAKES_ADD_S31,
    COMPARISONS_ADD_S32,
    NUMBERS_ADD_S32,
    MISTAKES_ADD_S32,
    COMPARISONS_ADD_S33,
    NUMBERS_ADD_S33,
    MISTAKES_ADD_S33,
    COMPARISONS_ADD_S34,
    NUMBERS_ADD_S34,
    MISTAKES_ADD_S34,
    COMPARISONS_ADD_S35,
    NUMBERS_ADD_S35,
    MISTAKES_ADD_S35,
    COMPARISONS_ADD_S36,
    NUMBERS_ADD_S36,
    MISTAKES_ADD_S36,
    COMPARISONS_ADD_S37,
    NUMBERS_ADD_S37,
    MISTAKES_ADD_S37,
    COMPARISONS_ADD_S38,
    NUMBERS_ADD_S38,
    MISTAKES_ADD_S38,
    COMPARISONS_ADD_S39,
    NUMBERS_ADD_S39,
    MISTAKES_ADD_S39,
    COMPARISONS_ADD_S40,
    NUMBERS_ADD_S40,
    MISTAKES_ADD_S40,
    COMPARISONS_ADD_S41,
    NUMBERS_ADD_S41,
    MISTAKES_ADD_S41,
    COMPARISONS_ADD_S42,
    NUMBERS_ADD_S42,
    MISTAKES_ADD_S42,
    COMPARISONS_ADD_S43,
    NUMBERS_ADD_S43,
    MISTAKES_ADD_S43,
    COMPARISONS_ADD_S44,
    NUMBERS_ADD_S44,
    MISTAKES_ADD_S44,
)


def _read_csv(path: Path) -> list[dict[str, str]]:
    if not path.is_file():
        return []
    with path.open(encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def _add_slugs(*groups: list[dict]) -> set[str]:
    slugs: set[str] = set()
    for group in groups:
        for row in group:
            slugs.add(row["slug"])
    return slugs


def _base_rows(path: Path, exclude_slugs: set[str], *, allow_slugs: set[str]) -> list[dict[str, str]]:
    rows = [
        row
        for row in _read_csv(path)
        if row.get("slug", "") in allow_slugs and row.get("slug", "") not in exclude_slugs
    ]
    missing = allow_slugs - {r["slug"] for r in rows}
    if missing:
        raise ValueError(f"missing base slugs in {path.name}: {sorted(missing)}")
    return rows


def _merge(*groups: list[dict]) -> list[dict]:
    seen: set[str] = set()
    out: list[dict] = []
    for group in groups:
        for row in group:
            slug = row["slug"]
            if slug in seen:
                raise ValueError(f"duplicate slug: {slug}")
            seen.add(slug)
            out.append(row)
    return out


def write_csv(path: Path, header: list[str], rows: list[dict]) -> None:
    with path.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=header, lineterminator="\n", extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)


def main() -> None:
    exclude = _add_slugs(*_ADD_GROUPS)
    comparisons = expand_short_faqs(
        apply_premium_faqs(
            _merge(
                _base_rows(DATA / "comparisons.csv", exclude, allow_slugs=_BASE_COMPARE_SLUGS),
                COMPARISONS_ADD_S31,
                COMPARISONS_ADD_S32,
                COMPARISONS_ADD_S33,
                COMPARISONS_ADD_S34,
                COMPARISONS_ADD_S35,
                COMPARISONS_ADD_S36,
                COMPARISONS_ADD_S37,
                COMPARISONS_ADD_S38,
                COMPARISONS_ADD_S39,
                COMPARISONS_ADD_S40,
                COMPARISONS_ADD_S41,
                COMPARISONS_ADD_S42,
                COMPARISONS_ADD_S43,
                COMPARISONS_ADD_S44,
            )
        )
    )
    numbers = expand_short_faqs(
        apply_premium_faqs(
            _merge(
                _base_rows(DATA / "numbers.csv", exclude, allow_slugs=_BASE_NUMBER_SLUGS),
                NUMBERS_ADD_S31,
                NUMBERS_ADD_S32,
                NUMBERS_ADD_S33,
                NUMBERS_ADD_S34,
                NUMBERS_ADD_S35,
                NUMBERS_ADD_S36,
                NUMBERS_ADD_S37,
                NUMBERS_ADD_S38,
                NUMBERS_ADD_S39,
                NUMBERS_ADD_S40,
                NUMBERS_ADD_S41,
                NUMBERS_ADD_S42,
                NUMBERS_ADD_S43,
                NUMBERS_ADD_S44,
            )
        )
    )
    mistakes = expand_short_faqs(
        apply_premium_faqs(
            _merge(
                _base_rows(DATA / "mistakes.csv", exclude, allow_slugs=_BASE_MISTAKE_SLUGS),
                MISTAKES_ADD_S31,
                MISTAKES_ADD_S32,
                MISTAKES_ADD_S33,
                MISTAKES_ADD_S34,
                MISTAKES_ADD_S35,
                MISTAKES_ADD_S36,
                MISTAKES_ADD_S37,
                MISTAKES_ADD_S38,
                MISTAKES_ADD_S39,
                MISTAKES_ADD_S40,
                MISTAKES_ADD_S41,
                MISTAKES_ADD_S42,
                MISTAKES_ADD_S43,
                MISTAKES_ADD_S44,
            )
        )
    )
    write_csv(DATA / "comparisons.csv", HEADER_COMPARE, comparisons)
    write_csv(DATA / "numbers.csv", HEADER_NUMBERS, numbers)
    write_csv(DATA / "mistakes.csv", HEADER_MISTAKES, mistakes)
    print(
        f"wrote compare={len(comparisons)} numbers={len(numbers)} mistakes={len(mistakes)}"
    )


if __name__ == "__main__":
    main()
