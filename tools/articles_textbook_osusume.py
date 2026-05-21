# -*- coding: utf-8 -*-
"""宅建テキストおすすめ（Amazonアフィリエイト）記事のHTML本文."""

from __future__ import annotations

TEXTBOOK_OSUSUME_SLUG = "takken-textbook-osusume"

TEXTBOOK_OSUSUME_CSV_ROW = {
    "slug": TEXTBOOK_OSUSUME_SLUG,
    "genre": "学習計画",
    "title": "宅建のテキストおすすめ3選【2026年版】独学合格者が選ぶ比較ランキング",
    "meta_description": (
        "2026年度宅建試験の独学テキストを3冊に厳選して比較。"
        "みんなが欲しかった・合格のトリセツ・らくらく宅建塾の特徴・価格・向いている人を表で整理。"
        "初学者から再受験者まで最適な1冊がわかります。"
    ),
    "lead": (
        "「宅建のテキストが多すぎてどれを選べばいいかわからない」という方向けに、"
        "2026年版の主要テキストを3冊に絞って比較します。"
        "結論を先に言うと、初学者には「みんなが欲しかった！宅建士の教科書」、"
        "スピード重視なら「合格のトリセツ」が最適です。"
    ),
    "priority": "115",
    "tags": "テキスト;教材選び;2026年度",
    "author_name": "宅建マスター編集部",
    "author_profile": "宅建試験対策サイトの編集チーム",
    "reviewer_name": "公式情報確認担当",
    "reviewer_profile": "公開前に一次情報との照合を行う担当者",
    "fact_checked_at": "2026-05-21",
    "primary_sources": (
        "不動産適正取引推進機構（RETIO）|https://www.retio.or.jp/;"
        "国土交通省|https://www.mlit.go.jp/"
    ),
    "original_note": "Amazonアソシエイト記事（takken-textbook-osusume）",
    "user_intent": (
        "2026年度版の宅建テキストを比較し、自分に合う1冊と同シリーズの問題集を選びたい。"
    ),
    "action_items": "テキストを1冊に決める;同シリーズの問題集をセットで用意する;過去問一覧で演習する",
    "update_policy": "試験要項・教材の年度版が更新されたタイミングで本文と参照元を見直します。",
    "last_reviewed_at": "2026-05-21",
    "next_review_at": "2026-06-21",
    "source_checked_at": "2026-05-21",
    "content_status": "published",
    "revision_note": "初版公開（アフィリエイト比較記事）",
    "affiliate_disclosure": "amazon",
    "faq_1_question": "テキストは何周すればいいですか？",
    "faq_1_answer": (
        "最低3周が目安です。1周目は全体像の把握、2周目は理解を深める、"
        "3周目は苦手箇所の集中学習というサイクルが効果的です。"
    ),
    "faq_2_question": "古いテキストでも勉強できますか？",
    "faq_2_answer": (
        "2025年版以前のテキストは法改正に対応していない可能性があります。"
        "必ず2026年度版を使ってください。"
    ),
    "faq_3_question": "電子書籍版はありますか？",
    "faq_3_answer": (
        "3冊とも電子書籍版（Kindle）があります。"
        "ただし試験本番は紙の問題なので、紙のテキストに慣れておくことも大切です。"
    ),
    "related_links": (
        "takken-gokaku-ritsu:宅建の合格率・難易度はこちら;"
        "takken-benkyou-jikan:宅建の勉強時間・スケジュールはこちら;"
        "../../q/index.html:過去問を解いてみる（無料）;"
        "takken-kyozai:宅建の教材の選び方"
    ),
}

TEXTBOOK_TOC_EXTRA = [
    ("choose", "宅建テキストの選び方【3つのポイント】"),
    ("compare", "おすすめテキスト比較表"),
    ("rank1", "1位：みんなが欲しかった！宅建士の教科書"),
    ("rank2", "2位：宅建士 合格のトリセツ 基本テキスト"),
    ("rank3", "3位：らくらく宅建塾 基本テキスト"),
    ("workbook", "テキストと合わせて買うべき問題集"),
]


def _affiliate_attrs() -> str:
    return 'target="_blank" rel="nofollow sponsored noopener noreferrer"'


def _affiliate_product_card(
    href: str,
    rank: str,
    title: str,
    publisher: str,
    price: str,
    pages: str,
    color: str,
    audience: str,
    cta: str,
) -> str:
    attrs = _affiliate_attrs()
    return f"""<a class="affiliate-product-card" href="{href}" {attrs}>
<span class="affiliate-product-card-rank">{rank}</span>
<span class="affiliate-product-card-title">{title}</span>
<span class="affiliate-product-card-meta">{publisher} · {price} · {pages} · {color}</span>
<span class="affiliate-product-card-audience">{audience}</span>
<span class="affiliate-product-card-cta">{cta}</span>
</a>"""


def _affiliate_table_row(
    href: str,
    title: str,
    publisher: str,
    price: str,
    pages: str,
    color: str,
    audience: str,
) -> str:
    attrs = _affiliate_attrs()
    link = f'<a href="{href}" class="affiliate-table-cell-link" {attrs}>'
    end = "</a>"
    return f"""<tr class="affiliate-table-row">
<td>{link}<span class="affiliate-table-title">{title}</span>{end}</td>
<td>{link}{publisher}{end}</td>
<td>{link}{price}{end}</td>
<td>{link}{pages}{end}</td>
<td>{link}{color}{end}</td>
<td>{link}{audience}{end}</td>
<td class="affiliate-table-action">{link}<span class="affiliate-table-btn">Amazonで見る</span>{end}</td>
</tr>"""


def textbook_sections_html() -> str:
    amzn_minna = "https://amzn.to/4tRM0sV"
    amzn_tori = "https://amzn.to/4dp3w2U"
    amzn_raku = "https://amzn.to/4nDe9Ta"
    return f"""
<section class="seo-article-section" aria-labelledby="choose">
<h2 id="choose"><span class="section-heading-num">1</span>宅建テキストの選び方【3つのポイント】</h2>
<h3>① 必ず2026年度版を選ぶ</h3>
<p>宅建試験は毎年4月施行の法改正から出題されます。2024年版・2025年版のテキストでは対応できない問題が出る可能性があります。</p>
<h3>② フルカラーか白黒か</h3>
<p>フルカラーは図解が見やすく理解しやすい反面、価格がやや高め。白黒でも合格できますが、初学者はフルカラーの方が続けやすいです。</p>
<h3>③ 問題集とのセット購入を前提にする</h3>
<p>テキストだけでは合格できません。同じシリーズの問題集とセットで購入すると、テキストの参照ページと問題集のリンクが一致して効率的に学習できます。</p>
</section>
<section class="seo-article-section" aria-labelledby="compare">
<h2 id="compare"><span class="section-heading-num">2</span>おすすめテキスト比較表</h2>
<p>表の各項目をタップするとAmazonの商品ページを開けます。スマホでは下のカードからも選べます。</p>
<div class="affiliate-product-grid" role="list">
{_affiliate_product_card(amzn_minna, "1位", "みんなが欲しかった！宅建士の教科書", "TAC出版", "3,300円", "約700ページ", "フルカラー", "初学者・図解で理解したい人", "Amazonで確認する")}
{_affiliate_product_card(amzn_tori, "2位", "宅建士 合格のトリセツ 基本テキスト", "LEC", "3,300円", "644ページ", "フルカラー", "コンパクトに学びたい人", "Amazonで確認する")}
{_affiliate_product_card(amzn_raku, "3位", "らくらく宅建塾 基本テキスト", "宅建学院", "3,300円", "538ページ", "2色刷り", "再受験者・知識がある人", "Amazonで確認する")}
</div>
<table class="seo-info-table affiliate-compare-table">
<thead><tr><th>テキスト</th><th>出版社</th><th>価格（税込）</th><th>ページ数</th><th>カラー</th><th>向いている人</th><th></th></tr></thead>
<tbody>
{_affiliate_table_row(amzn_minna, "みんなが欲しかった！宅建士の教科書", "TAC出版", "3,300円", "約700ページ", "フルカラー", "<strong>初学者・図解で理解したい人</strong>")}
{_affiliate_table_row(amzn_tori, "宅建士 合格のトリセツ 基本テキスト", "LEC", "3,300円", "644ページ", "フルカラー", "<strong>コンパクトに学びたい人</strong>")}
{_affiliate_table_row(amzn_raku, "らくらく宅建塾 基本テキスト", "宅建学院", "3,300円", "538ページ", "2色刷り", "<strong>再受験者・知識がある人</strong>")}
</tbody>
</table>
</section>
<section class="seo-article-section" aria-labelledby="rank1">
<h2 id="rank1"><span class="section-heading-num">3</span>1位：みんなが欲しかった！宅建士の教科書（TAC出版）</h2>
<p><strong>初学者に最もおすすめのテキストです。</strong></p>
<h3>特徴</h3>
<ul class="term-point-list">
<li>著者は資格テキストで定評のある<strong>滝澤ななみ</strong>氏</li>
<li>フルカラーで図解・イラストが豊富</li>
<li>各章の冒頭に「この章で学ぶこと」がまとめてある</li>
<li>同シリーズの問題集との連携が強く、テキストの参照番号と問題集が完全対応</li>
</ul>
<h3>こんな人に向いている</h3>
<ul class="term-point-list"><li>宅建の勉強が初めて</li><li>法律用語に慣れていない</li><li>視覚的に理解したい</li></ul>
<h3>こんな人には向かない</h3>
<ul class="term-point-list"><li>法律の知識がある（内容がやや丁寧すぎる場合がある）</li><li>薄いテキストでサクサク進めたい</li></ul>
<div class="affiliate-product-grid affiliate-product-grid--single" role="list">
{_affiliate_product_card(amzn_minna, "1位", "みんなが欲しかった！宅建士の教科書 2026年度版", "TAC出版", "3,300円", "約700ページ", "フルカラー", "初学者に最もおすすめ", "Amazonで確認する")}
</div>
</section>
<section class="seo-article-section" aria-labelledby="rank2">
<h2 id="rank2"><span class="section-heading-num">4</span>2位：宅建士 合格のトリセツ 基本テキスト（LEC）</h2>
<p><strong>644ページとコンパクトにまとまっており、効率重視の学習に最適です。</strong></p>
<h3>特徴</h3>
<ul class="term-point-list">
<li>LEC総合研究所の宅建試験チームが執筆</li>
<li>フルカラーで見やすい</li>
<li>動画サポート付き（2026年版はアプリで全問音声読み上げ対応）</li>
<li>一問一答問題集との連携が高評価</li>
</ul>
<h3>こんな人に向いている</h3>
<ul class="term-point-list"><li>短期集中で合格したい（3〜4ヶ月）</li><li>スマホ・アプリ学習を組み合わせたい</li><li>講義動画との併用を考えている</li></ul>
<h3>こんな人には向かない</h3>
<ul class="term-point-list"><li>じっくり読み込むスタイルが好き</li><li>問題数をできるだけ多くこなしたい</li></ul>
<div class="affiliate-product-grid affiliate-product-grid--single" role="list">
{_affiliate_product_card(amzn_tori, "2位", "宅建士 合格のトリセツ 2026年版", "LEC", "3,300円", "644ページ", "フルカラー", "効率重視の学習に最適", "Amazonで確認する")}
</div>
</section>
<section class="seo-article-section" aria-labelledby="rank3">
<h2 id="rank3"><span class="section-heading-num">5</span>3位：らくらく宅建塾 基本テキスト（宅建学院）</h2>
<p><strong>長年のベストセラーで、独特の語呂合わせが特徴的なテキストです。</strong></p>
<h3>特徴</h3>
<ul class="term-point-list">
<li>宅建専門校が作った実績のあるテキスト</li>
<li>覚えにくい数値・条件を語呂合わせで暗記できる</li>
<li>2色刷りでシンプル</li>
<li>538ページとボリュームが控えめ</li>
</ul>
<h3>こんな人に向いている</h3>
<ul class="term-point-list"><li>再受験者（一度宅建の勉強をしたことがある）</li><li>語呂合わせで暗記したい</li><li>シンプルなテキストが好き</li></ul>
<h3>こんな人には向かない</h3>
<ul class="term-point-list"><li>初学者（説明が簡潔すぎる場合がある）</li><li>フルカラーで視覚的に学びたい</li></ul>
<div class="affiliate-product-grid affiliate-product-grid--single" role="list">
{_affiliate_product_card(amzn_raku, "3位", "らくらく宅建塾 2026年版", "宅建学院", "3,300円", "538ページ", "2色刷り", "語呂合わせ暗記が得意な人向け", "Amazonで確認する")}
</div>
</section>
<section class="seo-article-section" aria-labelledby="workbook">
<h2 id="workbook"><span class="section-heading-num">6</span>テキストと合わせて買うべき問題集</h2>
<p>テキストだけでは合格できません。問題集は<strong>同じシリーズ</strong>を選ぶのが鉄則です。</p>
<table class="seo-info-table">
<thead><tr><th>テキスト</th><th>おすすめ問題集</th></tr></thead>
<tbody>
<tr><td>みんなが欲しかった！教科書</td><td>みんなが欲しかった！宅建士の問題集</td></tr>
<tr><td>合格のトリセツ</td><td>合格のトリセツ 厳選分野別過去問題集</td></tr>
<tr><td>らくらく宅建塾</td><td>過去問宅建塾</td></tr>
</tbody>
</table>
<p>各シリーズの問題集もAmazonで確認できます（テキストと同じシリーズを選んでください）。</p>
<div class="affiliate-product-grid" role="list">
<a class="affiliate-product-card affiliate-product-card--workbook" href="{amzn_minna}" {_affiliate_attrs()}>
<span class="affiliate-product-card-title">みんなが欲しかった！宅建士の問題集 2026年度版</span>
<span class="affiliate-product-card-meta">みんなが欲しかった！教科書と同シリーズ</span>
<span class="affiliate-product-card-cta">Amazonで確認する</span>
</a>
<a class="affiliate-product-card affiliate-product-card--workbook" href="{amzn_tori}" {_affiliate_attrs()}>
<span class="affiliate-product-card-title">合格のトリセツ 厳選分野別過去問題集 2026年版</span>
<span class="affiliate-product-card-meta">合格のトリセツと同シリーズ</span>
<span class="affiliate-product-card-cta">Amazonで確認する</span>
</a>
<a class="affiliate-product-card affiliate-product-card--workbook" href="{amzn_raku}" {_affiliate_attrs()}>
<span class="affiliate-product-card-title">過去問宅建塾 2026年版</span>
<span class="affiliate-product-card-meta">らくらく宅建塾と同シリーズ</span>
<span class="affiliate-product-card-cta">Amazonで確認する</span>
</a>
</div>
</section>
""".strip()
