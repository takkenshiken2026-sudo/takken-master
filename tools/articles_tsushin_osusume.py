# -*- coding: utf-8 -*-
"""宅建の通信講座おすすめ（A8アフィリエイト）記事."""

from __future__ import annotations

import html

from tools.articles_affiliate_courses import (
    COURSE_PRODUCTS,
    affiliate_cta,
    affiliate_pr_notice_html,
    course_compare_cards,
    course_compare_table_rows,
    course_hero_html,
    course_products_ranked,
    course_section,
)

TSUSHIN_OSUSUME_SLUG = "takken-tsushin-osusume"

TSUSHIN_OSUSUME_CSV_ROW = {
    "slug": TSUSHIN_OSUSUME_SLUG,
    "genre": "教材選び",
    "title": "宅建の通信講座おすすめ4選【2026年版】社会人・独学向け比較",
    "meta_description": (
        "2026年度宅建試験向けの通信講座・オンライン講座を4社比較。"
        "社会人・独学からの受講に向く講座の選び方、料金の目安、テキスト・過去問との組み合わせを解説。"
    ),
    "lead": (
        "「宅建の通信講座、どれを選べばいいか分からない」という方向けに、"
        "2026年版で検討しやすいオンライン講座を4つに絞って比較します。"
        "結論を先に言うと、費用を抑えて独学を補助したい人には資格対策ドットコム、"
        "本格的な通信講座として比較したい人には資格スクエアが候補になります。"
    ),
    "priority": "118",
    "tags": "通信講座;オンライン講座;おすすめ;2026年度;社会人",
    "author_name": "宅建マスター編集部",
    "author_profile": "宅建試験対策サイトの編集チーム",
    "reviewer_name": "公式情報確認担当",
    "reviewer_profile": "公開前に一次情報との照合を行う担当者",
    "fact_checked_at": "2026-05-27",
    "primary_sources": (
        "不動産適正取引推進機構（RETIO）|https://www.retio.or.jp/;"
        "国土交通省|https://www.mlit.go.jp/"
    ),
    "original_note": "アフィリエイト記事（A8・通信講座おすすめ比較）",
    "user_intent": (
        "宅建の通信講座・オンライン講座を比較し、社会人や独学から受講する自分に合う1社を選びたい。"
    ),
    "action_items": "比較表で候補を絞る;主講座を1つ決める;テキストと過去問で演習する",
    "update_policy": "各講座の料金・キャンペーン変更時にリンク先と本文を見直します。",
    "last_reviewed_at": "2026-05-27",
    "next_review_at": "2026-06-27",
    "source_checked_at": "2026-05-27",
    "content_status": "published",
    "revision_note": "初版公開（通信講座おすすめアフィリエイト）",
    "affiliate_disclosure": "a8",
    "faq_1_question": "宅建の通信講座は独学より合格しやすいですか？",
    "faq_1_answer": (
        "講義で理解を深め、過去問で定着させる組み合わせができれば、独学だけより学習の迷いは減りやすいです。"
        "ただし合格の鍵は最終的に過去問演習量にあるため、講座だけに頼らないことが大切です。"
    ),
    "faq_2_question": "社会人におすすめの通信講座はどれですか？",
    "faq_2_answer": (
        "仕事しながら費用を抑えたい人には資格対策ドットコムやオンスク.JPが入りやすく、"
        "計画立てや質問サポートまで含めて比較したい人には資格スクエアや四谷学院も候補になります。"
    ),
    "faq_3_question": "テキストだけ買って通信講座は不要ですか？",
    "faq_3_answer": (
        "テキストと過去問だけでも合格は可能です。"
        "ただし「何から手を付けるか分からない」「勉強が続かない」場合は、"
        "オンライン講座で学習の型を借りる価値があります。"
    ),
    "related_links": (
        "takken-textbook-osusume:宅建のテキストおすすめ3選【2026年版】独学合格者が選ぶ比較ランキング;"
        "takken-jikugaku-kitsui:宅建の独学がきつい人へ：通信講座より安く学ぶ方法;"
        "takken-tsushin-hikaku:宅建の通信講座・独学・通学の比較｜自分に合う学習スタイル;"
        "takken-shakaijin:社会人が仕事しながら宅建に合格する方法"
    ),
}

TSUSHIN_TOC_EXTRA = [
    ("choose", "通信講座の選び方"),
    ("compare", "おすすめ通信講座比較表"),
    ("pick-shikakutaisaku", "1位：資格対策ドットコム"),
    ("pick-onsuku", "2位：オンスク.JP"),
    ("pick-square", "3位：資格スクエア"),
    ("pick-yotsuya", "4位：四谷学院"),
    ("by-type", "タイプ別の選び方"),
    ("with-books", "テキスト・過去問との組み合わせ"),
    ("summary", "まとめ"),
]


def tsushin_hero_html() -> str:
    return course_hero_html(
        section_id="tsushin-hero",
        heading="2026年度版 おすすめ通信講座4社",
        note_html="バナーをタップすると各講座の詳細ページを開けます。<strong>1位は資格対策ドットコム</strong>です。",
        products=course_products_ranked(),
        foot_href="#compare",
        foot_label="比較表・詳細はこちら",
    )


def tsushin_sections_html() -> str:
    ranked = course_products_ranked()
    shikaku, onsuku, square, yotsuya = ranked
    compare_cards = course_compare_cards(ranked)
    compare_rows = course_compare_table_rows(ranked)
    return f"""
<section class="seo-article-section" aria-labelledby="choose">
<h2 id="choose"><span class="section-heading-num">1</span>宅建の通信講座の選び方【3つのポイント】</h2>
<h3>① 独学との組み合わせ方を決める</h3>
<p>通信講座は「すべて講座任せ」にする必要はありません。テキストでインプットし、講義で理解を深め、過去問で定着させる流れが基本です。講座を主役にするか、独学の補助にするかを先に決めると選びやすくなります。</p>
<h3>② 料金だけでなく「続けられる仕組み」を見る</h3>
<p>社会人受験者は、勉強時間よりも「勉強が続かないこと」が合格の壁になりやすいです。カリキュラム表、スマホ対応、質問のしやすさ、解約のしやすさなど、生活に合うかを確認しましょう。</p>
<h3>③ 2026年度版の教材・講義に対応しているか</h3>
<p>宅建は毎年4月施行の法改正から出題されます。古い年度の講義だけでは不十分な場合があるため、申込前に2026年度対応かを確認してください。</p>
</section>
<section class="seo-article-section" aria-labelledby="compare">
<h2 id="compare"><span class="section-heading-num">2</span>宅建の通信講座おすすめ比較表</h2>
<p>表の各項目をタップすると講座の詳細ページを開けます。スマホでは下のカードからも選べます。</p>
{compare_cards}
<table class="seo-info-table affiliate-course-compare-table">
<thead><tr><th>順位</th><th>バナー</th><th>講座名</th><th>特徴</th><th>向いている人</th><th></th></tr></thead>
<tbody>
{compare_rows}
</tbody>
</table>
</section>
{course_section(shikaku, 3, "1位：資格対策ドットコム", _shikaku_body())}
{course_section(onsuku, 4, "2位：オンスク.JP", _onsuku_body())}
{course_section(square, 5, "3位：資格スクエア", _square_body())}
{course_section(yotsuya, 6, "4位：四谷学院", _yotsuya_body())}
{_by_type_section()}
{_with_books_section()}
{_summary_section()}
{affiliate_cta(shikaku["href"], shikaku["cta"])}
""".strip()


def _shikaku_body() -> str:
    return """
<p>2026年版の通信講座比較で1位に挙げやすいのが、資格対策ドットコムです。理由は、独学からオンライン講座へ移行しやすく、費用面でも入りやすいからです。</p>
<p>仕事しながら宅建を学ぶ社会人は、「高額な予備校型講座は避けたいが、テキストだけでは不安」という状態になりがちです。資格対策ドットコムは、その中間の選択肢として使いやすいサービスです。</p>
<ul class="term-point-list">
<li>オンラインで講義・教材を進められる</li>
<li>独学の補助として導入しやすい</li>
<li>他社と比べて費用を抑えやすい</li>
<li>スマホ学習にも向く</li>
</ul>
<p>通信講座を初めて検討する人は、まずここから資料請求や無料コンテンツを確認するのがおすすめです。</p>
""".strip()


def _onsuku_body() -> str:
    return """
<p>2位のオンスク.JPは、月額制で宅建学習を始めたい人向けです。「いきなり高額パックは不安だけれど、講義で理解したい」という人に向いています。</p>
<p>通勤時間に動画を見る、帰宅後に短時間復習する、といった社会人の学習スタイルと相性がよい講座です。ただし、本格的な答練や添削まで含めたい人は、資格スクエアや四谷学院もあわせて比較しましょう。</p>
""".strip()


def _square_body() -> str:
    return """
<p>3位の資格スクエアは、「通信講座として」しっかり比較したい人向けです。カリキュラムや問題演習の量を重視する人に向いています。</p>
<p>独学に限界を感じ、今年こそ合格ラインに届けたい人は、低価格サービスだけでなく、通信講座型のサポートがある講座も検討する価値があります。申込前に、含まれる模試・質問対応・学習計画の有無を確認してください。</p>
""".strip()


def _yotsuya_body() -> str:
    return """
<p>4位の四谷学院は、サポートや安心感を重視する人向けです。通信講座でも、質問や学習の進め方に不安がある人が選びやすいタイプです。</p>
<p>価格だけを最優先にするより、「一人で続けられるか」「困ったときに聞けるか」を重視する人に向いています。費用を抑えたい人は、1位の資格対策ドットコムや2位のオンスク.JPと併せて検討するとよいでしょう。</p>
""".strip()


def _by_type_section() -> str:
    return """
<section class="seo-article-section" aria-labelledby="by-type">
<h2 id="by-type"><span class="section-heading-num">7</span>タイプ別｜どの通信講座を選ぶべきか</h2>
<table class="seo-info-table affiliate-pick-table">
<thead><tr><th>あなたの状況</th><th>おすすめ</th></tr></thead>
<tbody>
<tr><td>仕事しながら、費用を抑えて始めたい</td><td><strong>資格対策ドットコム</strong></td></tr>
<tr><td>月額制でまず試したい</td><td>オンスク.JP</td></tr>
<tr><td>通信講座として本気で比較したい</td><td>資格スクエア</td></tr>
<tr><td>質問・サポートを重視したい</td><td>四谷学院</td></tr>
<tr><td>独学がきつくて学習を立て直したい</td><td><a href="../takken-jikugaku-kitsui/">独学がきつい人向けの選び方</a>も参照</td></tr>
</tbody>
</table>
<p>学習スタイル（独学・通信・通学）そのものを比較したい場合は、<a href="../takken-tsushin-hikaku/">通信講座・独学・通学の比較記事</a>もあわせて確認してください。</p>
</section>
""".strip()


def _with_books_section() -> str:
    return """
<section class="seo-article-section" aria-labelledby="with-books">
<h2 id="with-books"><span class="section-heading-num">8</span>テキスト・過去問との組み合わせ</h2>
<p>通信講座は、テキストと過去問とセットで使うと効果が出やすくなります。講座だけに頼ると、演習量が足りず得点が伸びないケースがあります。</p>
<ol class="term-point-list">
<li>テキストで全体像をつかむ（<a href="../takken-textbook-osusume/">テキストおすすめ</a>を参照）</li>
<li>通信講座の講義で理解を深める</li>
<li>一問一答で暗記を定着させる</li>
<li>過去問で本番形式の演習を行う（<a href="../../q/past/">過去問一覧</a>も活用）</li>
</ol>
<p>社会人の場合は、週の学習時間が限られるため、教材を増やしすぎないことが大切です。講座1社＋テキスト1冊＋過去問1冊を基本に、足りない部分だけ追加しましょう。</p>
</section>
""".strip()


def _summary_section() -> str:
    return """
<section class="seo-article-section" aria-labelledby="summary">
<h2 id="summary"><span class="section-heading-num">9</span>まとめ：2026年版の通信講座は「続けられる1社」に絞る</h2>
<p>宅建の通信講座は数が多く、すべてを詳しく比較する必要はありません。2026年度版として、社会人・独学から始めやすい4社に絞って検討するのが現実的です。</p>
<p>費用を抑えてオンライン学習を始めたい人は<strong>資格対策ドットコム</strong>、月額制で試すなら<strong>オンスク.JP</strong>、本格的な通信講座として比較するなら<strong>資格スクエア</strong>、サポート重視なら<strong>四谷学院</strong>が候補になります。</p>
<p>講座を選んだら、テキストと過去問演習まで一気通貫で設計しましょう。通信講座は合格の近道になり得ますが、最後は過去問で点数が決まります。</p>
</section>
""".strip()


def tsushin_osusume_toc_html(has_faq: bool) -> str:
    items: list[tuple[str, str]] = [
        ("quality-panel-title", "この記事の信頼性について"),
        ("action-box-title", "この記事でできること"),
        ("tsushin-hero", "おすすめ通信講座4社"),
        *TSUSHIN_TOC_EXTRA,
    ]
    if has_faq:
        items.append(("article-sec-faq", "よくある質問"))
    items.extend(
        [
            ("article-info-title", "記事の基本情報"),
            ("official-info-title", "公式情報の確認"),
        ]
    )
    links = "".join(f'<li><a href="#{html.escape(anchor)}">{html.escape(label)}</a></li>' for anchor, label in items)
    return (
        '<nav class="seo-toc" aria-labelledby="seo-toc-title">'
        '<h2 id="seo-toc-title">目次</h2>'
        f"<ol>{links}</ol></nav>"
    )
