#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""guide-article-catalog の不足 slug を宅建向けタイトルで guide_articles.csv に追記する。"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from tools.scaffold_guide_article import append_row, build_row, existing_slugs  # noqa: E402

EXAM = "宅地建物取引士試験"

# (slug, genre, title) — 既存51本・テンプレ5本と重複する slug はスキップ
CATALOG: list[tuple[str, str, str]] = [
    ("official-info-sources", "試験概要", f"{EXAM}の公式情報の確認先と見る順番"),
    ("learning-app-guide", "試験概要", "宅建マスターの使い方（過去問・用語・記録）"),
    ("exam-purpose-and-career", "試験概要", f"{EXAM}の目的と宅建士としてのキャリア"),
    ("first-time-exam-guide", "試験概要", f"{EXAM}を初めて受ける人向けガイド"),
    ("compare-similar-qualifications", "試験概要", "宅建と類似資格の違い・併願の考え方"),
    ("exam-eligibility", "受験・申込", f"{EXAM}の受験資格と確認方法"),
    ("exemption-system", "受験・申込", "宅建の5問免除制度の要件と手続き"),
    ("work-experience-requirement", "受験・申込", "実務経験と受験資格の関係"),
    ("education-requirement", "受験・申込", "学歴要件と受験資格の読み方"),
    ("concurrent-exam-rules", "受験・申込", "宅建と他資格の同日受験・併願の注意点"),
    ("exam-schedule", "受験・申込", f"{EXAM}の年間日程と学習計画への組み込み"),
    ("exam-fees", "受験・申込", f"{EXAM}の受験手数料と支払いの注意点"),
    ("exam-application-flow", "受験・申込", f"{EXAM}の申込手順（RETIO）"),
    ("application-deadline-checklist", "受験・申込", "申込締切前に確認するチェックリスト"),
    ("exam-venue-and-region", "受験・申込", "受験地・地域と会場情報の確認"),
    ("reschedule-and-absence", "受験・申込", "欠席・再受験時の手続きと学習の立て直し"),
    ("exam-format-overview", "出題・形式", f"{EXAM}の出題形式（50問・四肢択一）"),
    ("subject-breakdown", "出題・形式", "宅建4分野の配点と出題の傾向"),
    ("cbt-computer-exam", "出題・形式", "CBT・マークシート試験の対策の違い"),
    ("time-limit-strategy", "出題・形式", "2時間50問の時間配分戦略"),
    ("exam-scope-overview", "出題・形式", f"{EXAM}の出題範囲の全体像"),
    ("syllabus-how-to-read", "出題・形式", "試験要項・シラバスの読み方"),
    ("scope-revision-history", "出題・形式", "出題範囲の改定と学習への影響"),
    ("weight-by-topic", "出題・形式", "分野別の配点感と優先順位"),
    ("new-topics-trend", "出題・形式", "近年の出題トレンドと法令改正"),
    ("scope-vs-past-questions", "出題・形式", "出題範囲と過去問の対応の見方"),
    ("pass-rate", "合格・難易度", f"{EXAM}の合格率の読み方"),
    ("exam-difficulty", "合格・難易度", f"{EXAM}の難易度と必要な学習量"),
    ("pass-score", "合格・難易度", f"{EXAM}の合格点（合格基準点）の考え方"),
    ("pass-rate-how-to-read", "合格・難易度", "合格率・統計の公式情報の見方"),
    ("difficulty-for-beginners", "合格・難易度", "初学者がつまずきやすいポイント"),
    ("study-plan-3months", "学習計画", "宅建を3ヶ月で仕上げる学習計画"),
    ("study-plan-6months", "学習計画", "宅建を6ヶ月で仕上げる学習計画"),
    ("study-plan-1year", "学習計画", "宅建を1年かけて合格を目指す計画"),
    ("study-plan-working", "学習計画", "働きながら宅建に合格する週間スケジュール"),
    ("study-plan-beginner", "学習計画", "法律初学者の宅建学習ロードマップ"),
    ("first-30-days-plan", "学習計画", "宅建学習の最初の30日でやること"),
    ("balance-work-study", "学習計画", "仕事と宅建勉強の両立のコツ"),
    ("time-management", "学習計画", "宅建勉強の時間管理と習慣化"),
    ("self-study-start", "独学対策", "宅建を独学で始める手順"),
    ("self-study-schedule", "独学対策", "独学の週間・月間スケジュール例"),
    ("self-study-mistakes", "独学対策", "宅建独学でよくある失敗と回避策"),
    ("self-study-environment", "独学対策", "独学に向いた環境づくり"),
    ("self-study-motivation", "独学対策", "長期独学のモチベーション維持"),
    ("self-study-without-school", "独学対策", "資格学校なしで宅建に合格するには"),
    ("textbook-selection", "独学対策", "宅建テキストの選び方"),
    ("problem-book-selection", "独学対策", "問題集・一問一答の選び方"),
    ("correspondence-course-guide", "独学対策", "通信講座と独学の組み合わせ"),
    ("free-materials-online", "独学対策", "無料教材と公式情報の活用"),
    ("textbook-vs-past-questions", "独学対策", "テキストと過去問、どちらを優先するか"),
    ("material-update-cycle", "独学対策", "教材の版・年度更新への対応"),
    ("past-questions-by-year", "過去問活用", "宅建過去問を年度別に解く順番"),
    ("past-questions-by-field", "過去問活用", "分野別に過去問を解くメリット"),
    ("past-questions-review-cycle", "過去問活用", "過去問の解き直しサイクル"),
    ("past-questions-score-analysis", "過去問活用", "過去問の点数分析と弱点把握"),
    ("bookmark-review-method", "過去問活用", "ブックマーク・復習リストの使い方"),
    ("past-questions-first-attempt", "過去問活用", "過去問1周目の正しい解き方"),
    ("past-questions-wrong-reasons", "過去問活用", "間違い理由の分類と復習"),
    ("past-questions-latest-year", "過去問活用", "直近年度の過去問の扱い"),
    ("mock-exam-how-to", "過去問活用", "宅建模試の活用法"),
    ("ichimon-practice", "過去問活用", "一問一答と過去問の組み合わせ"),
    ("drill-volume-guide", "過去問活用", "演習量の目安（何問解くか）"),
    ("timed-practice", "過去問活用", "本番形式の時間計測演習"),
    ("simulation-exam-schedule", "過去問活用", "模試を組み込んだ直前スケジュール"),
    ("glossary-study-method", "用語整理", "宅建用語集の効率的な使い方"),
    ("important-terms-list", "用語整理", "宅建で押さえる重要用語の探し方"),
    ("confusing-terms", "用語整理", "混同しやすい用語の整理術"),
    ("related-terms-navigation", "用語整理", "関連用語リンクで知識を広げる"),
    ("terms-with-past-questions", "用語整理", "過去問と用語解説の往復学習"),
    ("terms-importance-levels", "用語整理", "重要度の見方と優先順位"),
    ("numbers-and-deadlines", "用語整理", "宅建で出る数字・期限のまとめ方"),
    ("formula-memorization", "用語整理", "計算・公式の暗記のコツ"),
    ("calculation-drill", "用語整理", "計算問題の反復ドリル"),
    ("rate-and-percentage", "用語整理", "割合・率の問題の解き方"),
    ("numeric-trap-choices", "用語整理", "数字問題の引っかけ選択肢"),
    ("review-cycle-spaced", "復習・苦手克服", "間隔を空けた復習（スペースド）"),
    ("mistake-notebook", "復習・苦手克服", "間違いノートの作り方"),
    ("weak-field-recovery", "復習・苦手克服", "苦手分野の立て直し手順"),
    ("note-taking-method", "復習・苦手克服", "宅建勉強のノートの取り方"),
    ("almost-correct-review", "復習・苦手克服", "惜しい間違いの見直し方"),
    ("plateau-breakthrough", "復習・苦手克服", "伸び悩みの突破策"),
    ("final-week-prep", "直前・当日", "宅建直前1週間の学習"),
    ("final-day-checklist", "直前・当日", "試験前日のチェックリスト"),
    ("final-scope-narrowing", "直前・当日", "直前期の範囲の絞り込み"),
    ("final-sleep-and-health", "直前・当日", "直前期の睡眠と体調"),
    ("final-mock-last-run", "直前・当日", "直前模試の使い方"),
    ("exam-day-items", "直前・当日", "試験当日の持ち物"),
    ("exam-day-flow", "直前・当日", "試験当日の流れ"),
    ("exam-day-time-allocation", "直前・当日", "試験中の時間配分"),
    ("mental-prep-exam-day", "直前・当日", "本番のメンタル対策"),
    ("exam-day-troubleshooting", "直前・当日", "当日のトラブル対処"),
    ("after-pass-procedure", "注意点・更新", "合格後の手続き"),
    ("pass-announcement-guide", "注意点・更新", "合格発表の確認方法"),
    ("registration-after-pass", "注意点・更新", "宅建士登録の流れ"),
    ("career-after-qualification", "注意点・更新", "合格後のキャリア選択"),
    ("fail-retry-plan", "注意点・更新", "不合格からの再受験計画"),
    ("retake-strategy", "注意点・更新", "再受験の戦略"),
    ("retake-schedule-adjustment", "注意点・更新", "再受験時のスケジュール調整"),
    ("score-gap-analysis", "注意点・更新", "得点差の分析"),
    ("exam-changes", "注意点・更新", "試験制度の変更点"),
    ("legal-revision-impact", "注意点・更新", "法令改正の学習への影響"),
    ("syllabus-update-tracker", "注意点・更新", "シラバス更新の追跡"),
    ("official-info-update-habits", "注意点・更新", "公式情報の確認習慣"),
    ("common-misconceptions", "注意点・更新", "宅建のよくある誤解"),
    ("pass-only-past-questions-myth", "注意点・更新", "過去問だけ神話への注意"),
    ("study-hours-myth", "注意点・更新", "勉強時間の神話"),
    ("eligibility-myths", "注意点・更新", "受験資格の誤解"),
    ("difficulty-myths", "注意点・更新", "難易度の誤解"),
]

# 分野別（law / rights / limit / tax）
for fid, fname in [
    ("law", "宅建業法"),
    ("rights", "権利関係"),
    ("limit", "法令上の制限"),
    ("tax", "税・その他"),
]:
    for suffix, label in [
        ("basics", "基礎の押さえ方"),
        ("frequent-topics", "頻出論点"),
        ("calculation", "計算・数字対策"),
        ("case-study", "事例問題の解き方"),
        ("past-question-focus", "過去問での出方"),
    ]:
        slug = f"field-{fid}-{suffix}"
        CATALOG.append((slug, "分野別対策", f"宅建・{fname}の{label}"))


def main() -> int:
    have = existing_slugs()
    added = 0
    for slug, genre, title in CATALOG:
        if slug in have:
            continue
        row = build_row(slug, genre, title=title)
        row["title"] = title
        row["meta_description"] = title[:120]
        row["lead"] = f"{title}について、公式情報を確認しながら学習を進めるためのガイドです。"
        append_row(row)
        have.add(slug)
        added += 1
    print(f"Appended {added} catalog rows to data/guide_articles.csv (total slugs ~{len(have)})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
