#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""全用語の手作りリライトデータ（分野別モジュールを統合）。"""

from __future__ import annotations

from tools.glossary_hand_rewrite.field_exam import HAND_EXAM
from tools.glossary_hand_rewrite.field_law import HAND_LAW
from tools.glossary_hand_rewrite.field_regs import HAND_REGS
from tools.glossary_hand_rewrite.field_rights import HAND_RIGHTS
from tools.glossary_hand_rewrite.field_tax import HAND_TAX
from tools.glossary_priority_deep import PRIORITY_DEEP

# 後から追加した手書きが同名キーで上書き（PRIORITY_DEEP より新しい編集を優先）
HAND_REWRITE: dict[str, dict[str, str]] = {
    **PRIORITY_DEEP,
    **HAND_RIGHTS,
    **HAND_LAW,
    **HAND_REGS,
    **HAND_TAX,
    **HAND_EXAM,
}

__all__ = ["HAND_REWRITE"]
