#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""学習系ガイドへ比較記事導線を追加し、アフィリエイト4本の相互リンクを整える。"""

from __future__ import annotations

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CSV_PATH = ROOT / "data" / "guide_articles.csv"

AFFILIATE_TITLES = {
    "affiliate-textbooks-recommend": "宅建士のおすすめテキスト3選【2026年度版・独学】",
    "affiliate-problem-books": "宅建士のおすすめ問題集3選【論点別・分野別過去問2026】",
    "affiliate-correspondence-course": "宅建士のおすすめ通信講座4選【2026年度・独学併用】",
    "affiliate-mock-exam-materials": "宅建士の模試・一問一答3選【厳選模試・セレクト1000・2026】",
}

# slug → (affiliate_slug, section_N, body追記文)
GUIDE_UPDATES: dict[str, tuple[str, int, str]] = {
    "takken-hooreijou-seigen-study": (
        "affiliate-problem-books",
        3,
        "法令8問の過去問演習は、affiliate-problem-books で分野別・論点別の収録差を確認してから1冊に固定すると周回が楽になります。",
    ),
    "takken-zei-sonota-study": (
        "affiliate-problem-books",
        4,
        "税・統計の短問演習は、affiliate-problem-books で一問一答系と過去問系の使い分けを先に決めると直前期の得点が安定しやすいです。",
    ),
    "takken-shiken-schedule-2026": (
        "affiliate-textbooks-recommend",
        5,
        "逆算学習を始める前にテキスト1冊を決める場合は、affiliate-textbooks-recommend で2026年度版3冊の章立てを比較してから選ぶと計画が崩れにくいです。",
    ),
    "takken-moshikomi": (
        "affiliate-textbooks-recommend",
        4,
        "申込完了後は教材を増やさず、affiliate-textbooks-recommend で選んだテキスト1冊と過去問演習に集中する設計が安全です。",
    ),
    "takken-schedule": (
        "affiliate-correspondence-course",
        5,
        "週次ルーティンが続かない場合は、affiliate-correspondence-course で通信講座4社の学習設計の違いを確認し、過去問演習は週15問以上を維持したまま1社に絞ってください。",
    ),
    "takken-goukakuten": (
        "affiliate-mock-exam-materials",
        4,
        "模試目標36点以上の記録には、affiliate-mock-exam-materials で模試冊と一問一答の役割分担を確認してから週1回の120分演習に組み込むと判断しやすいです。",
    ),
    "takken-saishuken": (
        "affiliate-problem-books",
        5,
        "再受験で新しい参考書を増やす前に、affiliate-problem-books で演習1冊を固定し、誤答解き直しに週の7割を充てる運用が得点に直結します。",
    ),
    "takken-tokkuten": (
        "affiliate-problem-books",
        3,
        "頻出表に行を足す過去問演習は、affiliate-problem-books で論点別・分野別の収録形式を比較してから1冊に決めると迷いが減ります。",
    ),
    "takken-mikeiken-tenshoku": (
        "affiliate-correspondence-course",
        4,
        "仕事と並行して学習ペースを守りたい場合は、affiliate-correspondence-course で週次サポートの違いを確認し、過去問15問/週は維持したまま1社に絞ると続きやすいです。",
    ),
    "takken-35jou-gyakushu": (
        "affiliate-problem-books",
        4,
        "35条・37条の過去問演習は、affiliate-problem-books で業法タグの解説量を比較してから1冊に固定すると混同パターンの解き直しが速くなります。",
    ),
    "takken-toukei-mondai": (
        "affiliate-problem-books",
        4,
        "問46〜50の演習は、affiliate-problem-books で統計・税タグの収録を確認してから週末5問サイクルに組み込むと継続しやすいです。",
    ),
    "takken-baisho": (
        "affiliate-problem-books",
        4,
        "報酬計算ドリルは、affiliate-problem-books で業法・報酬タグの過去問解説を比較してから1冊に絞るとケアレスミスが減ります。",
    ),
    "takken-baikai-keiyaku": (
        "affiliate-problem-books",
        4,
        "媒介契約の数字演習は、affiliate-problem-books で業法過去問の解説形式を確認してから週10問ペースで回すと定着が早まります。",
    ),
    "takken-8shu-seigen": (
        "affiliate-problem-books",
        4,
        "8種制限の正誤演習は、affiliate-problem-books で業法タグの収録を比較してから1冊に固定すると当事者図の練習が続きやすいです。",
    ),
    "takken-yoto-chiiki": (
        "affiliate-problem-books",
        4,
        "用途地域の暗記後は、affiliate-problem-books で法令タグの過去問を週10問から入れ、表に追記する運用が効率的です。",
    ),
    "takken-kenpei-yoseki": (
        "affiliate-problem-books",
        4,
        "建ぺい率・容積率の計算ドリルは、affiliate-problem-books で法令計算タグの解説量を比較してから火曜3問ペースで回してください。",
    ),
    "takken-jikan-haibun": (
        "affiliate-mock-exam-materials",
        4,
        "120分の時間感覚を鍛える演習冊は、affiliate-mock-exam-materials で模試形式と一問一答の違いを確認してから週1回に組み込むと本番に近づきます。",
    ),
    "takken-hoshokin": (
        "affiliate-problem-books",
        4,
        "報酬・手数料の正誤演習は、affiliate-problem-books で業法タグの過去問を比較してから週10問で回すと上限判断が安定します。",
    ),
    "takken-40dai": (
        "affiliate-correspondence-course",
        4,
        "記憶負荷を下げたい場合は、affiliate-correspondence-course で動画・テキスト併用の講座を1社に絞り、過去問演習量は週15問以上を維持してください。",
    ),
    "takken-nanido": (
        "affiliate-textbooks-recommend",
        5,
        "初学者が最初に迷いやすいテキスト選びは、affiliate-textbooks-recommend で解説量と章立てを比較してから1冊に固定すると学習時間の見積もりが立てやすいです。",
    ),
    "takken-kenri-kankei": (
        "affiliate-problem-books",
        4,
        "権利14問の長文演習は、affiliate-problem-books で分野別過去問の解説量を比較してから1冊に決めると90秒ルールの練習が続きます。",
    ),
    "takken-jukenhi": (
        "affiliate-textbooks-recommend",
        3,
        "教材費の予算を組むときは、affiliate-textbooks-recommend でテキスト候補の価格帯を比較し、過去問・模試は別枠で確保すると予算超過を防げます。",
    ),
}

# 4本の比較記事: 相互リンク（ASP URL行は維持）
AFFILIATE_CROSS_LINKS: dict[str, list[str]] = {
    "affiliate-textbooks-recommend": [
        "takken-dokugaku:宅建を独学で合格する方法",
        "takken-kakomon:宅建の過去問の使い方・効果的な解き方を解説",
        "takken-kyozai:宅建の教材の選び方｜テキスト・問題集・通信講座を比較",
        "affiliate-problem-books:宅建士のおすすめ問題集3選【論点別・分野別過去問2026】",
        "affiliate-mock-exam-materials:宅建士の模試・一問一答3選【厳選模試・セレクト1000・2026】",
        "affiliate-correspondence-course:宅建士のおすすめ通信講座4選【2026年度・独学併用】",
    ],
    "affiliate-problem-books": [
        "takken-kakomon:宅建の過去問の使い方・効果的な解き方を解説",
        "takken-dokugaku:宅建を独学で合格する方法",
        "takken-gyoho-study:宅建業法の勉強法・完全攻略",
        "affiliate-textbooks-recommend:宅建士のおすすめテキスト3選【2026年度版・独学】",
        "affiliate-mock-exam-materials:宅建士の模試・一問一答3選【厳選模試・セレクト1000・2026】",
        "affiliate-correspondence-course:宅建士のおすすめ通信講座4選【2026年度・独学併用】",
    ],
    "affiliate-mock-exam-materials": [
        "takken-moshi:宅建の模擬試験の活用法｜何回受ける？点数の見方",
        "takken-chokuzen:宅建試験の直前対策｜1ヶ月・1週間・前日でやること",
        "takken-jikan-haibun:宅建試験の時間配分｜50問・2時間を落とさない解き方",
        "affiliate-textbooks-recommend:宅建士のおすすめテキスト3選【2026年度版・独学】",
        "affiliate-problem-books:宅建士のおすすめ問題集3選【論点別・分野別過去問2026】",
        "affiliate-correspondence-course:宅建士のおすすめ通信講座4選【2026年度・独学併用】",
    ],
    "affiliate-correspondence-course": [
        "takken-tsushin-hikaku:宅建の通信講座・独学・通学の比較｜自分に合う学習スタイル",
        "takken-dokugaku:宅建を独学で合格する方法",
        "takken-shakaijin:社会人が仕事しながら宅建に合格する方法",
        "affiliate-textbooks-recommend:宅建士のおすすめテキスト3選【2026年度版・独学】",
        "affiliate-problem-books:宅建士のおすすめ問題集3選【論点別・分野別過去問2026】",
        "affiliate-mock-exam-materials:宅建士の模試・一問一答3選【厳選模試・セレクト1000・2026】",
    ],
}


def _split_related(value: str) -> list[str]:
    return [x.strip() for x in (value or "").split(";") if x.strip()]


def _append_related(value: str, token: str) -> str:
    parts = _split_related(value)
    slug = token.split(":", 1)[0]
    if any(p.split(":", 1)[0] == slug for p in parts):
        return ";".join(parts)
    parts.append(token)
    return ";".join(parts)


def _merge_affiliate_related(existing: str, internal: list[str]) -> str:
    """内部リンクを先頭に、既存の https ASP 行は末尾に維持。"""
    asp = [p for p in _split_related(existing) if p.startswith("http")]
    merged: list[str] = []
    seen: set[str] = set()
    for token in internal:
        slug = token.split(":", 1)[0]
        if slug in seen:
            continue
        seen.add(slug)
        merged.append(token)
    for token in asp:
        if token not in merged:
            merged.append(token)
    return ";".join(merged)


def apply_guide_updates(rows: list[dict[str, str]]) -> int:
    by_slug = {r["slug"]: r for r in rows}
    changed = 0
    for slug, (aff_slug, sec_n, sentence) in GUIDE_UPDATES.items():
        row = by_slug.get(slug)
        if not row:
            continue
        body_key = f"section_{sec_n}_body"
        body = row.get(body_key, "")
        if aff_slug in body:
            pass
        elif body.rstrip().endswith("。"):
            row[body_key] = body.rstrip() + sentence
        else:
            row[body_key] = (body.rstrip() + "。" + sentence) if body.strip() else sentence

        token = f"{aff_slug}:{AFFILIATE_TITLES[aff_slug]}"
        new_rl = _append_related(row.get("related_links", ""), token)
        if new_rl != row.get("related_links", ""):
            row["related_links"] = new_rl
            changed += 1
        elif aff_slug not in body:
            changed += 1
    return changed


def apply_affiliate_cross_links(rows: list[dict[str, str]]) -> int:
    by_slug = {r["slug"]: r for r in rows}
    changed = 0
    for slug, internal in AFFILIATE_CROSS_LINKS.items():
        row = by_slug.get(slug)
        if not row:
            continue
        new_rl = _merge_affiliate_related(row.get("related_links", ""), internal)
        if new_rl != row.get("related_links", ""):
            row["related_links"] = new_rl
            changed += 1
    return changed


def main() -> None:
    with CSV_PATH.open(encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames
        rows = list(reader)
    if not fieldnames:
        raise SystemExit("guide_articles.csv: no header")

    g = apply_guide_updates(rows)
    a = apply_affiliate_cross_links(rows)

    with CSV_PATH.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)

    print(f"Updated guides: {len(GUIDE_UPDATES)} targets, {g} row(s) touched")
    print(f"Updated affiliate cross-links: {a} row(s)")


if __name__ == "__main__":
    main()
