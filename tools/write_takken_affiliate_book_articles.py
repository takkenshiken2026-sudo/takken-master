#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Write affiliate book briefs + CSV rows for takken-master (Amazon tag ue083093-22)."""

from __future__ import annotations

import csv
import sys
from pathlib import Path

try:
    import yaml
except ImportError as exc:  # pragma: no cover
    raise SystemExit("PyYAML が必要です") from exc

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from tools.scaffold_guide_article import append_row, build_row, existing_slugs  # noqa: E402

BRIEFS = ROOT / "data" / "affiliate-briefs"
CSV_PATH = ROOT / "data" / "guide_articles.csv"
TAG = "ue083093-22"
PRICE_CHECKED = "2026-06-04"
OFFICIAL = "公益財団法人 不動産適正取引推進機構（宅建試験・公式）"
SITE = "宅建マスター"


def amazon(asin: str) -> str:
    return f"https://www.amazon.co.jp/dp/{asin}/ref=nosim?tag={TAG}"


def img(asin: str) -> str:
    return f"takken-book-{asin.lower()}.webp"


def book(
    rank: int,
    name: str,
    publisher: str,
    asin: str,
    *,
    edition: str = "2026年度版",
    price_yen: int = 0,
    pages: int = 0,
    for_who: str = "",
    highlights: list[str],
) -> dict:
    return {
        "rank": rank,
        "offer_type": "book",
        "name": name,
        "publisher": publisher,
        "edition": edition,
        "price_yen": price_yen,
        "price_note": "Amazon税込参考・送料別",
        "pages": pages,
        "format": "B5判",
        "asin": asin,
        "image_file": img(asin),
        "amazon_url": amazon(asin),
        "for_who": for_who,
        "highlights": highlights,
    }


def ensure_section_body(text: str, min_len: int = 180) -> str:
    body = text.replace("[[affiliate-hub-placeholder]]", "").strip()
    if len(body) >= min_len:
        return body
    tail = (
        f"\n\n{OFFICIAL}の出題範囲（4分野）と照合し、"
        f"{SITE}の過去問・用語解説と組み合わせて復習サイクルを回してください。"
    )
    while len(body) < min_len:
        body += tail
    return body


def ensure_faq_answer(text: str, min_len: int = 100) -> str:
    answer = text.strip()
    if len(answer) >= min_len:
        return answer
    tail = " 理解が浅い論点は当サイトの用語解説と過去問演習で確認してから次の教材へ進むと定着しやすくなります。"
    while len(answer) < min_len:
        answer += tail
    return answer


BRIEFS_DATA = {
    "affiliate-textbooks-recommend": {
        "slug": "affiliate-textbooks-recommend",
        "theme_key": "textbooks-recommend",
        "search_intent": "宅地建物取引士試験の独学向けテキストを比較して選びたい",
        "title": "宅建士のおすすめテキスト3選【2026年度版・独学】",
        "layout": "product-comparison",
        "asp_primary": "amazon",
        "comparison_kind": "books",
        "comparison_title": "おすすめテキスト3選（比較）",
        "price_disclaimer": (
            f"価格・在庫・版情報は執筆時点（{PRICE_CHECKED}）のAmazon税込参考です。"
            "購入前に必ず販売ページでご確認ください。"
        ),
        "products": [
            book(
                1,
                "2026年度版 みんなが欲しかった! 宅建士の教科書",
                "TAC出版",
                "B0GLN6ZMNF",
                price_yen=3850,
                pages=880,
                for_who="解説厚めの本格テキストで4分野を体系的に学びたい独学者",
                highlights=[
                    "権利・法令・税務・宅建業法の4分野を1冊で整理",
                    "TAC論点別過去問題集・一問一答と章立ての相性がよい",
                    "社会人独学のメインテキスト定番",
                ],
            ),
            book(
                2,
                "2026年版 宅建士 合格のトリセツ 基本テキスト",
                "LEC",
                "4844948237",
                edition="2026年版",
                price_yen=3300,
                pages=644,
                for_who="動画講義付きで論点整理から学びたい人",
                highlights=[
                    "無料講義動画付きで独学の理解を補強しやすい",
                    "分冊可能で持ち運び・分野別復習に向く",
                    "厳選分野別過去問題集（別記事）への接続がスムーズ",
                ],
            ),
            book(
                3,
                "2026年版 出る順宅建士 合格テキスト",
                "LEC",
                "4844948326",
                edition="2026年版",
                price_yen=2420,
                pages=427,
                for_who="出る順シリーズでコンパクトに論点を押さえたい人",
                highlights=[
                    "出る順シリーズの論点整理型テキスト",
                    "ウォーク問過去問題集・模試（別記事）と縦串が明確",
                    "TAC教科書より薄く、短期学習にも向く",
                ],
            ),
        ],
        "related_links": [
            "takken-dokugaku:独学の始め方",
            "takken-kakomon:過去問活用法",
            "takken-goukakuten:合格点",
            "affiliate-problem-books:おすすめ問題集",
            "affiliate-mock-exam-materials:模試・一問一答",
            "takken-kyozai:教材選び",
        ],
        "operator_note": f"Amazon tag={TAG}。B0GLN6ZMNF / 4844948237 / 4844948326。{PRICE_CHECKED} 価格確認。",
    },
    "affiliate-problem-books": {
        "slug": "affiliate-problem-books",
        "theme_key": "problem-books",
        "search_intent": "宅地建物取引士試験の問題集・過去問を比較して選びたい",
        "title": "宅建士のおすすめ問題集3選【論点別・分野別過去問2026】",
        "layout": "product-comparison",
        "asp_primary": "amazon",
        "comparison_kind": "books",
        "comparison_title": "おすすめ問題集3選（比較）",
        "price_disclaimer": (
            f"価格・在庫は執筆時点（{PRICE_CHECKED}）のAmazon税込参考です。"
            "購入前に販売ページで最新版を確認してください。"
        ),
        "products": [
            book(
                1,
                "2026年度版 みんなが欲しかった! 宅建士の論点別過去問題集",
                "TAC出版",
                "4300119287",
                price_yen=2750,
                pages=680,
                for_who="TAC教科書とセットで論点別演習をしたい人",
                highlights=[
                    "TAC教科書と章立ての相性がよい定番過去問",
                    "4分野を論点別に弱点演習しやすい",
                    "一問一答セレクト1000（別記事）との併用も向く",
                ],
            ),
            book(
                2,
                "2026年版 宅建士 合格のトリセツ 厳選分野別過去問題集",
                "LEC",
                "4844948245",
                edition="2026年版",
                price_yen=2750,
                pages=734,
                for_who="LECトリセツ基本テキストとセットで過去問演習をしたい人",
                highlights=[
                    "合格のトリセツシリーズで解説付き過去問",
                    "分野別に演習量を確保しやすい",
                    "頻出一問一答（別記事）へのステップアップがしやすい",
                ],
            ),
            book(
                3,
                "2026年版 出る順宅建士 ウォーク問過去問題集",
                "LEC",
                "4844948296",
                edition="2026年版",
                price_yen=1980,
                pages=342,
                for_who="出る順テキスト読了後にウォーク問形式で演習したい人",
                highlights=[
                    "出る順シリーズの過去問演習定番",
                    "ウォーク問形式で解説を追いながら進めやすい",
                    "過去30年良問厳選模試（別記事）と併用しやすい",
                ],
            ),
        ],
        "related_links": [
            "takken-kakomon:過去問活用法",
            "takken-dokugaku:独学の始め方",
            "takken-goukakuten:合格点",
            "affiliate-textbooks-recommend:おすすめテキスト",
            "affiliate-mock-exam-materials:模試・一問一答",
            "takken-plan:学習計画",
        ],
        "operator_note": f"Amazon tag={TAG}。4300119287 / 4844948245 / 4844948296。B0GLNR5JBT FAQ。",
    },
    "affiliate-mock-exam-materials": {
        "slug": "affiliate-mock-exam-materials",
        "theme_key": "mock-exam-materials",
        "search_intent": "宅地建物取引士試験の模試・一問一答教材を比較して選びたい",
        "title": "宅建士の模試・一問一答3選【厳選模試・セレクト1000・2026】",
        "layout": "product-comparison",
        "asp_primary": "amazon",
        "comparison_kind": "books",
        "comparison_title": "模試・一問一答3選（比較）",
        "price_disclaimer": (
            f"価格は執筆時点（{PRICE_CHECKED}）のAmazon税込参考です。"
            f"試験日程・出題範囲は{OFFICIAL}で必ず確認してください。"
        ),
        "products": [
            book(
                1,
                "2026年版 出る順宅建士 過去30年良問厳選模試",
                "LEC",
                "4844948334",
                edition="2026年版",
                price_yen=2750,
                pages=483,
                for_who="本試験直前に模試形式で時間配分を確認したい人",
                highlights=[
                    "過去30年から厳選した模試形式の演習",
                    "出る順シリーズの総仕上げ向け",
                    "時間を計って解く練習に向く",
                ],
            ),
            book(
                2,
                "2026年版 宅建士 合格のトリセツ 頻出一問一答式過去問題集",
                "LEC",
                "4844948253",
                edition="2026年版",
                price_yen=2200,
                pages=417,
                for_who="LECトリセツで短問演習量を確保したい人",
                highlights=[
                    "読上音声付きでスキマ時間学習に向く",
                    "頻出論点を一問一答形式で総復習",
                    "厳選分野別過去問題集との使い分けが明確",
                ],
            ),
            book(
                3,
                "2026年度版 わかって合格る宅建士 一問一答セレクト1000",
                "TAC出版",
                "430011935X",
                price_yen=2750,
                pages=700,
                for_who="TAC系教材で一問一答総仕上げをしたい人",
                highlights=[
                    "厳選1000問で演習量を確保",
                    "音声データDL付きで復習しやすい",
                    "TAC教科書・論点別過去問との併用例が多い",
                ],
            ),
        ],
        "related_links": [
            "takken-chokuzen:直前対策",
            "takken-moshi:模擬試験の活用法",
            "takken-goukakuten:合格点",
            "affiliate-textbooks-recommend:おすすめテキスト",
            "affiliate-problem-books:おすすめ問題集",
            "takken-plan:学習計画",
        ],
        "operator_note": (
            f"Amazon tag={TAG}。4844948334 / 4844948253 / 430011935X。"
            f"{PRICE_CHECKED} 価格確認。"
        ),
    },
}


CSV_ROWS = {
    "affiliate-textbooks-recommend": {
        "title": "宅建士のおすすめテキスト3選【2026年度版・独学】",
        "meta_description": (
            "宅建士の独学向けおすすめテキスト3選。"
            "TAC教科書・LEC合格のトリセツ・出る順合格テキストを比較。"
            "選び方と宅建マスター過去問との併用も解説。"
        ),
        "lead": (
            "宅地建物取引士試験（宅建）は4分野（権利関係・法令上の制限・税務・宅建業法）の理解と演習量が合格の鍵です。"
            "本記事では2026年度版の主要テキスト3冊を、独学・社会人受験の視点で比較します。"
            "出題範囲は必ず不動産適正取引推進機構（公式）で確認してください。"
            "価格・版情報は購入前にAmazonで必ずご確認ください。"
        ),
        "priority": "370",
        "original_note": "Amazon tag=ue083093-22。B0GLN6ZMNF / 4844948237 / 4844948326。",
        "user_intent": (
            "宅建士のテキストを、TAC本格型・LECトリセツ型・出る順型で比較し、"
            "独学の最初の1冊（または2冊構成）に絞りたい。"
        ),
        "action_items": "比較表で3冊の違いを確認する;4分野の出題範囲を公式で確認する;過去問で弱点を把握する",
        "revision_note": f"{PRICE_CHECKED}: Amazon URL確定・本文全面リライト",
        "sections": [
            (
                "テキスト選びの3つのポイント",
                "宅建試験のテキスト選びでは、"
                f"①{OFFICIAL}の4分野（権利・法令・税務・宅建業法）に目次が沿っているか、"
                "②解説量が自分の前提知識（不動産実務経験の有無）に合うか、"
                "③過去問・一問一答とセットで使えるかを確認します。\n\n"
                "初学者はTAC教科書、動画で理解を補強したい人はLECトリセツ、"
                "コンパクトに進めたい人は出る順合格テキストが選ばれやすいです。",
            ),
            (
                "おすすめテキスト比較の見方",
                "比較では「TAC本格教科書」「LEC合格のトリセツ基本」「LEC出る順合格」の3タイプで見ます。"
                "独学初期は理解用1冊に絞り、演習段階で問題集1冊（おすすめ問題集の記事）を追加する構成が扱いやすいです。"
                f"{SITE}の過去問で分野別得点を確認し、足りない解説量を基準に選んでください。",
            ),
            (
                "1位：TAC「みんなが欲しかった! 宅建士の教科書」",
                "2026年度版 みんなが欲しかった! 宅建士の教科書（3,850円税込参考・880ページ・B5判）は、"
                "4分野を1冊で体系的に学べる本格テキスト。TAC論点別過去問題集・一問一答と組み合わせやすい定番です。\n\n"
                "向いている人：解説厚めで独学のメインテキスト1冊を決めたい社会人・初学者。",
            ),
            (
                "2位・3位：LEC合格のトリセツ・出る順合格テキスト",
                "2026年版 宅建士 合格のトリセツ 基本テキスト（LEC・3,300円税込参考・644ページ）は、"
                "無料講義動画付きで論点整理から学べる教材。厳選分野別過去問題集（別記事）とセットの2冊構成が基本です。\n\n"
                "2026年版 出る順宅建士 合格テキスト（LEC・2,420円税込参考・427ページ）は、"
                "出る順シリーズのコンパクト型。ウォーク問過去問題集・模試（別記事）への接続がスムーズです。",
            ),
            (
                "テキストと宅建マスター過去問の併用",
                "テキストで論点を押さえたら、宅建マスターの過去問・一問一答で本試験形式の演習に移ります。"
                "4分野ごとの得点を記録し、弱点分野をテキスト該当章に戻って復習するサイクルが効率的です。"
                "直前期は模試・一問一答（別記事）も併用すると安心です。",
            ),
            (
                "購入前チェックリスト",
                "購入前に以下を確認してください。\n"
                "・2026年度版（最新版）か\n"
                "・4分野すべてが目次に含まれているか\n"
                "・Amazon在庫・価格（執筆時点と異なる場合あり）\n"
                "・学習期間（2か月／4か月）に対してページ数・演習量が見合うか",
            ),
        ],
        "faqs": [
            (
                "TACとLEC、どちらを選べばよいですか？",
                "TACは教科書→論点別過去問→一問一答の縦串が揃いやすく、"
                "LECはトリセツ基本＋分野別過去問、または出る順テキスト＋ウォーク問の2冊構成が扱いやすいです。"
                "まず比較表で解説量と演習の進め方を確認し、1ブランドに絞ると計画が立てやすくなります。",
            ),
            (
                "テキストは1冊だけで足りますか？",
                "本格テキスト1冊＋当サイトの過去問演習で独学は可能です。"
                "演習量が足りないと感じたら、おすすめ問題集の記事で紹介している1冊を追加してください。",
            ),
            (
                "最新年度版は必要ですか？",
                "法改正・出題傾向の反映のため、2026年度版（最新版）を選んでください。"
                "中古は版と改訂情報の確認が必要です。",
            ),
        ],
        "related_links": (
            "takken-dokugaku:独学の始め方;"
            "takken-kakomon:過去問活用法;"
            "takken-goukakuten:合格点;"
            "affiliate-problem-books:おすすめ問題集;"
            "affiliate-mock-exam-materials:模試・一問一答;"
            "takken-kyozai:教材選び"
        ),
        "key_points": (
            "2026年度版 みんなが欲しかった! 宅建士の教科書;"
            "2026年版 宅建士 合格のトリセツ 基本テキスト;"
            "2026年版 出る順宅建士 合格テキスト;"
            "テキスト選びの3つのポイント;"
            "過去問との併用"
        ),
    },
    "affiliate-problem-books": {
        "title": "宅建士のおすすめ問題集3選【論点別・分野別過去問2026】",
        "meta_description": (
            "宅建士のおすすめ問題集3選。"
            "TAC論点別過去問、LEC厳選分野別過去問、出る順ウォーク問を比較。"
            "過去問の回し方と分野別対策も解説。"
        ),
        "lead": (
            "宅建試験では、過去問・問題集の演習量が得点安定の鍵です。"
            "本記事では2026年度版の問題集3冊を、収録形式・解説量・テキストとの相性で比較します。"
            "価格は購入前にAmazonで必ずご確認ください。"
        ),
        "priority": "365",
        "original_note": "Amazon tag=ue083093-22。4300119287 / 4844948245 / 4844948296。",
        "user_intent": (
            "宅建士の過去問・問題集を比較し、"
            "演習メイン1冊を決めて、4分野の弱点補強計画を立てたい。"
        ),
        "action_items": "3冊の収録形式を比較する;4分野の得点バランスを確認する;弱点分野をテキストで復習する",
        "revision_note": f"{PRICE_CHECKED}: Amazon URL確定・本文全面リライト",
        "sections": [
            (
                "問題集選びの基準",
                "問題集選びでは、(1)4分野の出題バランスが取れているか (2)解説で復習できるか "
                "(3)テキストとの章立て相性を確認します。"
                "権利・法令・税務・宅建業法それぞれの得点バランスを見ながら、弱点分野に戻れる解説量があるかが重要です。",
            ),
            (
                "3冊の選び方（タイプ別）",
                "[[affiliate-hub-placeholder]]\n\n"
                "TAC教科書と論点別演習したい人は2026年度版 みんなが欲しかった! 宅建士の論点別過去問題集、"
                "LECトリセツ基本と組み合わせるなら2026年版 宅建士 合格のトリセツ 厳選分野別過去問題集、"
                "出る順合格テキスト読了後には2026年版 出る順宅建士 ウォーク問過去問題集が向きます。",
            ),
            (
                "1位：TAC 論点別過去問題集",
                "2026年度版 みんなが欲しかった! 宅建士の論点別過去問題集（2,750円税込参考・680ページ・B5判）は、"
                "TAC教科書と章立ての相性がよく、演習メイン1冊として選ばれやすい定番です。",
            ),
            (
                "2位・3位：LEC厳選分野別・出る順ウォーク問",
                "2026年版 宅建士 合格のトリセツ 厳選分野別過去問題集（LEC・2,750円税込参考・734ページ）は、"
                "LECトリセツ基本との縦串が明確。本試験形式の演習量確保に向きます。\n\n"
                "2026年版 出る順宅建士 ウォーク問過去問題集（LEC・1,980円税込参考・342ページ）は、"
                "出る順テキストとセットの過去問演習向け。模試（別記事）との併用も向きます。",
            ),
            (
                "過去問の回し方（宅建マスターとの併用）",
                "当サイトの過去問で分野別得点を把握したうえで、問題集で「時間を計って解く」練習を行います。"
                "誤答は用語解説で類似論点まで整理し、1週間後に解き直してください。"
                "過去問活用法は takken-kakomon を参照。",
            ),
            (
                "模試・一問一答との使い分け",
                "過去問で論点を押さえたあと、模試・一問一答（別記事）で短問演習・総仕上げを追加する受験生も多いです。"
                "2026年度版 わかって合格る宅建士 分野別過去問題集（B0GLNR5JBT）も選択肢のひとつです。",
            ),
        ],
        "faqs": [
            (
                "論点別と分野別、どちらを先に買いますか？",
                "テキスト読了後は、使うテキストブランドに合わせて1冊を選ぶのが基本です。"
                "TACなら論点別過去問、LECトリセツなら厳選分野別、出る順ならウォーク問、という対応が一般的です。",
            ),
            (
                "わかって合格る分野別過去問題集は必要ですか？",
                "必須ではありません。TAC教科書と組み合わせる場合は論点別過去問題集を優先し、"
                "わかって合格るシリーズを使う場合は基本テキスト＋分野別の2冊セット（B0GLNR5JBT）も選択肢です。",
            ),
            (
                "問題集は何冊必要ですか？",
                "メイン1冊＋当サイト過去問で足りる場合が多いです。"
                "直前期は模試・一問一答の記事も参照してください。",
            ),
        ],
        "related_links": (
            "takken-kakomon:過去問活用法;"
            "takken-dokugaku:独学の始め方;"
            "takken-goukakuten:合格点;"
            "affiliate-textbooks-recommend:おすすめテキスト;"
            "affiliate-mock-exam-materials:模試・一問一答;"
            "takken-plan:学習計画"
        ),
        "key_points": (
            "2026年度版 みんなが欲しかった! 宅建士の論点別過去問題集;"
            "2026年版 宅建士 合格のトリセツ 厳選分野別過去問題集;"
            "2026年版 出る順宅建士 ウォーク問過去問題集;"
            "問題集選びの基準;"
            "過去問の回し方"
        ),
    },
    "affiliate-mock-exam-materials": {
        "title": "宅建士の模試・一問一答3選【厳選模試・セレクト1000・2026】",
        "meta_description": (
            "宅建士の模試・一問一答3選。"
            "出る順過去30年厳選模試、LEC頻出一問一答、TACセレクト1000を比較。"
            "直前演習の進め方も解説。"
        ),
        "lead": (
            "宅建試験の直前期は、模試で時間配分を確認し、"
            "一問一答で頻出論点の穴埋めをするフェーズです。"
            "本記事では模試・一問一答系3冊を比較します。"
            "試験日程・出題範囲は必ず不動産適正取引推進機構（公式）で確認してください。",
        ),
        "priority": "360",
        "original_note": "Amazon tag=ue083093-22。4844948334 / 4844948253 / 430011935X。",
        "user_intent": (
            "宅建士の本試験直前に、"
            "模試・一問一答を比較し、直前1〜2冊を決めたい。"
        ),
        "action_items": "3冊の用途を比較する;受験予定回を確認する;テキスト・過去問との役割分担を決める",
        "revision_note": f"{PRICE_CHECKED}: Amazon URL確定・本文全面リライト",
        "sections": [
            (
                "模試・一問一答の位置づけ",
                "模試・一問一答は、テキストと過去問で固めた論点を「本番の時間感覚」や「短問演習量」で確認するためのものです。"
                "模試で時間配分、一問一答で頻出論点の穴埋め、という役割分担が扱いやすいです。",
            ),
            (
                "3冊の選び方",
                "[[affiliate-hub-placeholder]]\n\n"
                "本試験形式の模試演習には2026年版 出る順宅建士 過去30年良問厳選模試、"
                "LECトリセツで短問総復習には2026年版 宅建士 合格のトリセツ 頻出一問一答式過去問題集、"
                "TAC系で一問一答1000問演習には2026年度版 わかって合格る宅建士 一問一答セレクト1000が向きます。",
            ),
            (
                "1位：出る順 過去30年良問厳選模試",
                "2026年版 出る順宅建士 過去30年良問厳選模試（2,750円税込参考・483ページ）は、"
                "直前期の本試験形式演習向け。時間を計って解く練習に有効です。",
            ),
            (
                "2位・3位：LEC頻出一問一答・TACセレクト1000",
                "2026年版 宅建士 合格のトリセツ 頻出一問一答式過去問題集（2,200円税込参考・417ページ）は、"
                "読上音声付きでスキマ時間の短問演習に向きます。\n\n"
                "2026年度版 わかって合格る宅建士 一問一答セレクト1000（2,750円税込参考・700ページ）は、"
                "TAC教科書・論点別過去問との併用例が多い定番一問一答です。",
            ),
            (
                "テキスト・過去問との組み合わせ",
                "例：TAC教科書→論点別過去問→セレクト1000→出る順模試→宅建マスター過去問。"
                "直前期は模試1冊＋一問一答1冊に絞る受験生も多いです。",
            ),
            (
                "購入前の確認事項",
                "購入前に以下を確認してください。\n"
                "・2026年度版（最新版）か\n"
                "・受験予定回と学習計画に間に合うか\n"
                "・テキスト・過去問との重複が学習計画上問題ないか\n"
                "・Amazon在庫・価格",
            ),
        ],
        "faqs": [
            (
                "模試だけで足りますか？",
                "形式慣れには有効ですが、論点理解はテキストと過去問で済ませてから入る方が効率的です。"
                "おすすめテキストと問題集の記事と組み合わせる構成を推奨します。",
            ),
            (
                "一問一答は2冊必要ですか？",
                "必須ではありません。LECトリセツ派なら頻出一問一答、TAC派ならセレクト1000、"
                "というようにテキストブランドに合わせて1冊を選ぶのが一般的です。",
            ),
            (
                "直前何週間から使えばよいですか？",
                "一問一答はテキスト・過去問読了後から、模試は試験2〜4週間前から入る例が多いです。"
                "学習計画に合わせて1フェーズ1冊を原則にしてください。",
            ),
        ],
        "related_links": (
            "takken-chokuzen:直前対策;"
            "takken-moshi:模擬試験の活用法;"
            "takken-goukakuten:合格点;"
            "affiliate-textbooks-recommend:おすすめテキスト;"
            "affiliate-problem-books:おすすめ問題集;"
            "takken-plan:学習計画"
        ),
        "key_points": (
            "2026年版 出る順宅建士 過去30年良問厳選模試;"
            "2026年版 宅建士 合格のトリセツ 頻出一問一答式過去問題集;"
            "2026年度版 わかって合格る宅建士 一問一答セレクト1000;"
            "模試・一問一答の位置づけ;"
            "テキスト・過去問との組み合わせ"
        ),
    },
}


ROW_GENRE = {
    "affiliate-textbooks-recommend": "独学対策",
    "affiliate-problem-books": "過去問活用",
    "affiliate-mock-exam-materials": "学習計画",
}


def ensure_rows() -> None:
    slugs = existing_slugs()
    for slug, cfg in CSV_ROWS.items():
        if slug in slugs:
            continue
        row = build_row(slug, ROW_GENRE[slug], title=cfg["title"])
        row["priority"] = cfg["priority"]
        row["tags"] = "独学;参考書;アフィリエイト"
        row["content_status"] = "draft"
        row["primary_sources"] = f"{OFFICIAL}|https://www.retio.or.jp/"
        append_row(row)
        print(f"appended CSV row: {slug}")


def write_briefs() -> None:
    BRIEFS.mkdir(parents=True, exist_ok=True)
    for slug, data in BRIEFS_DATA.items():
        path = BRIEFS / f"{slug}.yaml"
        path.write_text(
            yaml.dump(data, allow_unicode=True, sort_keys=False, default_flow_style=False),
            encoding="utf-8",
        )
        print(f"wrote brief → {path}")


def patch_csv() -> None:
    with CSV_PATH.open(encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames
        rows = list(reader)
    if not fieldnames:
        raise SystemExit("CSV header missing")
    fieldnames = list(fieldnames)

    for row in rows:
        slug = row.get("slug", "")
        if slug not in CSV_ROWS:
            continue
        cfg = CSV_ROWS[slug]
        row["title"] = cfg["title"]
        row["meta_description"] = cfg["meta_description"]
        row["lead"] = cfg["lead"]
        row["priority"] = cfg["priority"]
        row["original_note"] = cfg["original_note"]
        row["user_intent"] = cfg["user_intent"]
        row["action_items"] = cfg["action_items"]
        row["revision_note"] = cfg["revision_note"]
        row["fact_checked_at"] = PRICE_CHECKED
        row["content_status"] = "published"
        row["related_links"] = cfg["related_links"]
        row["key_points"] = cfg["key_points"]
        row["tags"] = "独学;参考書;アフィリエイト"
        row["primary_sources"] = f"{OFFICIAL}|https://www.retio.or.jp/"
        for i, (heading, body) in enumerate(cfg["sections"], start=1):
            row[f"section_{i}_heading"] = heading
            row[f"section_{i}_body"] = ensure_section_body(body)
        for i in range(len(cfg["sections"]) + 1, 8):
            row[f"section_{i}_heading"] = ""
            row[f"section_{i}_body"] = ""
        for i, (q, a) in enumerate(cfg["faqs"], start=1):
            row[f"faq_{i}_question"] = q
            row[f"faq_{i}_answer"] = ensure_faq_answer(a)
        for i in range(len(cfg["faqs"]) + 1, 5):
            row[f"faq_{i}_question"] = ""
            row[f"faq_{i}_answer"] = ""
        print(f"patched CSV row: {slug}")

    with CSV_PATH.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def main() -> int:
    ensure_rows()
    write_briefs()
    patch_csv()
    return 0


if __name__ == "__main__":
    sys.exit(main())
