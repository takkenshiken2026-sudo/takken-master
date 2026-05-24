#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""実践演習の単元定義（index.html の ORIG_UNITS と同期）。"""

from __future__ import annotations

FIELD_LABELS: dict[str, str] = {
    "rights": "権利関係",
    "law": "宅建業法",
    "limit": "法令上の制限",
    "tax": "税・その他",
}

ORIG_UNITS: dict[str, list[dict[str, str]]] = {
    "rights": [
        {"id": "r_ishi", "label": "意思表示・制限行為能力"},
        {"id": "r_dairi", "label": "代理・無権代理・表見代理"},
        {"id": "r_jiko", "label": "時効"},
        {"id": "r_bukken", "label": "物権変動・登記"},
        {"id": "r_tanpo", "label": "担保物権"},
        {"id": "r_saikensoron", "label": "債権総論・保証・相殺"},
        {"id": "r_baibai", "label": "売買・契約不適合責任"},
        {"id": "r_chinshaku", "label": "賃貸借・使用貸借"},
        {"id": "r_souzoku", "label": "相続・遺言・遺留分"},
        {"id": "r_fuhoko", "label": "不法行為・不当利得"},
        {"id": "r_shakuchi", "label": "借地借家法"},
        {"id": "r_kukku", "label": "区分所有法"},
        {"id": "r_touki", "label": "不動産登記法"},
        {"id": "r_sorin", "label": "相隣関係・共有・地役権"},
    ],
    "law": [
        {"id": "l_menkyo", "label": "免許制度・欠格事由"},
        {"id": "l_takkenshi", "label": "宅建士・登録・宅建士証"},
        {"id": "l_hosho", "label": "営業保証金・保証協会"},
        {"id": "l_baikai", "label": "媒介契約"},
        {"id": "l_jusetsu", "label": "重要事項説明（35条書面）"},
        {"id": "l_37jo", "label": "37条書面"},
        {"id": "l_kokoku", "label": "広告・契約締結時期の制限"},
        {"id": "l_cooling", "label": "クーリングオフ・8種制限"},
        {"id": "l_hoshu", "label": "報酬"},
        {"id": "l_kantoku", "label": "監督処分・罰則・業務規制"},
        {"id": "l_sonota", "label": "住宅瑕疵担保履行法・その他"},
    ],
    "limit": [
        {"id": "k_toshi", "label": "都市計画法"},
        {"id": "k_kenchiku", "label": "建築基準法"},
        {"id": "k_nochi", "label": "農地法"},
        {"id": "k_kokudo", "label": "国土利用計画法"},
        {"id": "k_kukaku", "label": "土地区画整理法"},
        {"id": "k_mori", "label": "盛土規制法・宅造法"},
        {"id": "k_sonota", "label": "その他法令制限"},
    ],
    "tax": [
        {"id": "t_joto", "label": "所得税・譲渡所得"},
        {"id": "t_shutoku", "label": "不動産取得税"},
        {"id": "t_kotei", "label": "固定資産税"},
        {"id": "t_toroku", "label": "登録免許税"},
        {"id": "t_inshi", "label": "印紙税・消費税"},
        {"id": "t_chika", "label": "地価公示・不動産鑑定評価"},
        {"id": "t_kinyu", "label": "住宅金融支援機構"},
        {"id": "t_tokei", "label": "統計・土地・建物の知識"},
    ],
}


def unit_label(unit_id: str) -> str:
    for units in ORIG_UNITS.values():
        for u in units:
            if u["id"] == unit_id:
                return u["label"]
    return unit_id
