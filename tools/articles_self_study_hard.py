# -*- coding: utf-8 -*-
"""宅建の独学がきつい人向けアフィリエイト記事（通信講座より安く学ぶ）."""

from __future__ import annotations

import html
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COURSE_IMAGE_DIR = ROOT / "images" / "courses"
COURSE_IMAGE_REL = "../../images/courses/"

SELF_STUDY_HARD_SLUG = "takken-jikugaku-kitsui"

COURSE_IMAGE_SIZES: dict[str, tuple[int, int]] = {
    "shikakutaisaku": (700, 329),
    "onsuku": (545, 307),
    "square": (800, 418),
    "yotsuya": (960, 402),
}

SELF_STUDY_HARD_CSV_ROW = {
    "slug": SELF_STUDY_HARD_SLUG,
    "genre": "独学対策",
    "title": "宅建の独学がきつい人へ：通信講座より安く学ぶ方法",
    "meta_description": (
        "宅建の独学がきつい人向けに、通信講座より費用を抑えて学習を立て直す方法を解説。"
        "資格対策ドットコム・オンスク・資格スクエア・四谷学院の選び方と組み合わせ勉強法を整理。"
    ),
    "lead": (
        "宅建を独学で始めたものの、「テキストを読んでも頭に入らない」「過去問を解いても点数が伸びない」"
        "「仕事や家事で勉強が続かない」と感じていませんか。"
        "この記事では、通信講座より費用を抑えながら学習を立て直す方法と、自分に合うサービスの選び方を解説します。"
    ),
    "priority": "125",
    "tags": "宅建;独学;通信講座;オンライン講座",
    "author_name": "宅建マスター編集部",
    "author_profile": "宅建試験対策サイトの編集チーム",
    "reviewer_name": "公式情報確認担当",
    "reviewer_profile": "公開前に一次情報との照合を行う担当者",
    "fact_checked_at": "2026-05-21",
    "primary_sources": (
        "不動産適正取引推進機構（RETIO）|https://www.retio.or.jp/;"
        "国土交通省|https://www.mlit.go.jp/"
    ),
    "original_note": "アフィリエイト記事（A8・通信講座比較）",
    "user_intent": (
        "独学がきつく感じているが、高額な通信講座に申し込む前に、"
        "費用を抑えた学習サービスで勉強を立て直したい。"
    ),
    "action_items": (
        "つまずきの原因を整理する;"
        "主導線の講座を1つ選ぶ;"
        "過去問演習と組み合わせる"
    ),
    "update_policy": "各講座の料金・キャンペーン変更時にリンク先と本文を見直します。",
    "last_reviewed_at": "2026-05-21",
    "next_review_at": "2026-06-21",
    "source_checked_at": "2026-05-21",
    "content_status": "published",
    "revision_note": "初版公開（独学×低価格講座アフィリエイト）",
    "affiliate_disclosure": "a8",
    "faq_1_question": "独学がきついときは通信講座に申し込むべきですか？",
    "faq_1_answer": (
        "必ずしも高額な通信講座が必要ではありません。"
        "まずは低価格のオンライン講座や月額制サービスで、勉強を再開できるか確認するのが現実的です。"
    ),
    "faq_2_question": "一番おすすめのサービスはどれですか？",
    "faq_2_answer": (
        "独学の補助として安く始めたい人には資格対策ドットコムが第一候補です。"
        "月額制で試したい人はオンスク.JP、講座としてしっかり比較したい人は資格スクエア、"
        "サポート重視なら四谷学院も候補になります。"
    ),
    "faq_3_question": "有料サービスだけに頼っても合格できますか？",
    "faq_3_answer": (
        "講義で理解し、過去問で定着させる組み合わせが大切です。"
        "有料サービスは独学の弱点を補う位置づけで使い、宅建業法と過去問演習は自分でも続けましょう。"
    ),
    "related_links": (
        "takken-ocita:宅建に落ちた・不合格だった場合の対策と再受験の進め方;"
        "takken-chokuzen:宅建試験の直前対策｜1ヶ月・1週間・前日でやること;"
        "takken-dokugaku:宅建を独学で合格する方法;"
        "takken-tsushin-hikaku:宅建の通信講座・独学・通学の比較"
    ),
}

SELF_STUDY_TOC_EXTRA = [
    ("reasons", "独学がきつくなる理由"),
    ("review", "最初に見直すべきこと"),
    ("options", "通信講座より安く学ぶ選択肢"),
    ("pick-shikakutaisaku", "第一候補：資格対策ドットコム"),
    ("pick-onsuku", "安さ重視：オンスク.JP"),
    ("pick-square", "比較重視：資格スクエア"),
    ("pick-yotsuya", "サポート重視：四谷学院"),
    ("which", "どれを選ぶべきか"),
    ("combine", "独学と有料サービスの組み合わせ"),
    ("summary", "まとめ"),
]

COURSE_PRODUCTS: list[dict[str, str]] = [
    {
        "id": "shikakutaisaku",
        "rank": "第一候補",
        "name": "資格対策ドットコム",
        "tag": "低価格オンライン",
        "href": (
            "https://px.a8.net/svt/ejp?a8mat=4B3TF0+DRY3OY+3L4C+BW0YB"
            "&a8ejpredirect=https%3A%2F%2Fwww.shikakutaisaku.com%2Fpersonal%2Ftakken.html"
        ),
        "cta": "資格対策ドットコムの宅建講座を確認する",
        "audience_short": "独学の補助として安く始めたい人",
    },
    {
        "id": "onsuku",
        "rank": "月額制",
        "name": "オンスク.JP",
        "tag": "まず安く試す",
        "href": (
            "https://px.a8.net/svt/ejp?a8mat=4B3TF0+DUX9PU+408S+BW0YB"
            "&a8ejpredirect=https%3A%2F%2Fonsuku.jp%2Ftraining%2Ftakkenshi"
        ),
        "cta": "オンスク.JPの宅建講座を確認する",
        "audience_short": "月額制で試したい人",
    },
    {
        "id": "square",
        "rank": "通信講座",
        "name": "資格スクエア",
        "tag": "しっかり比較",
        "href": (
            "https://px.a8.net/svt/ejp?a8mat=4B3TF0+DXB04Y+373C+BW0YB"
            "&a8ejpredirect=https%3A%2F%2Fwww.shikaku-square.com%2Ftakken"
        ),
        "cta": "資格スクエアの宅建講座を確認する",
        "audience_short": "講座として比較したい人",
    },
    {
        "id": "yotsuya",
        "rank": "サポート",
        "name": "四谷学院",
        "tag": "安心感重視",
        "href": (
            "https://px.a8.net/svt/ejp?a8mat=4B3TF0+DRCO36+5IEI+BW0YB"
            "&a8ejpredirect=https%3A%2F%2Fyotsuyagakuin-tsushin.com%2Ftakken%2F"
        ),
        "cta": "四谷学院の宅建講座を確認する",
        "audience_short": "サポートを重視したい人",
    },
]


def _affiliate_attrs() -> str:
    return 'target="_blank" rel="nofollow sponsored noopener noreferrer"'


def resolve_course_image_src(product_id: str) -> str | None:
    """WebP/JPG/PNG があれば相対パスを返す。なければ None（CSSプレースホルダー用）。"""
    for ext in (".webp", ".jpg", ".jpeg", ".png"):
        path = COURSE_IMAGE_DIR / f"course-{product_id}{ext}"
        if path.is_file():
            return f"{COURSE_IMAGE_REL}{path.name}"
    return None


def _course_image_html(
    product: dict[str, str],
    *,
    hero: bool = False,
    section: bool = False,
    eager: bool = False,
) -> str:
    """講座バナー画像、またはプレースホルダー。"""
    name = product["name"]
    alt = html.escape(f"{name}の宅建講座")
    src = resolve_course_image_src(product["id"])
    width, height = COURSE_IMAGE_SIZES.get(product["id"], (640, 360))
    if src:
        if hero:
            css = "affiliate-course-hero-image"
            sizes = "(max-width: 760px) 42vw, 220px"
        else:
            css = "affiliate-course-section-image"
            sizes = "(max-width: 760px) 100vw, 720px"
        loading = "eager" if eager else "lazy"
        priority = ' fetchpriority="high"' if eager else ""
        return (
            f'<img class="{css}" src="{html.escape(src)}" alt="{alt}" '
            f'width="{width}" height="{height}" sizes="{sizes}" '
            f'loading="{loading}" decoding="async"{priority}>'
        )
    if hero:
        size = "affiliate-course-placeholder--hero"
    else:
        size = "affiliate-course-placeholder--section"
    return (
        f'<div class="affiliate-course-placeholder affiliate-course-placeholder--{product["id"]} {size}" '
        f'role="img" aria-label="{alt}">'
        f'<span class="affiliate-course-placeholder-name">{html.escape(name)}</span>'
        f'<span class="affiliate-course-placeholder-tag">{html.escape(product["tag"])}</span>'
        f"</div>"
    )


def affiliate_pr_notice_html() -> str:
    return (
        '<p class="affiliate-pr-notice" role="note">'
        "この記事には広告・PR（アフィリエイト）を含みます。"
        "</p>"
    )


def self_study_hero_html() -> str:
    attrs = _affiliate_attrs()
    items: list[str] = []
    for index, product in enumerate(COURSE_PRODUCTS):
        primary = " affiliate-course-hero-item--primary" if product["id"] == "shikakutaisaku" else ""
        image = _course_image_html(product, hero=True, eager=index == 0)
        items.append(
            f"""<a class="affiliate-course-hero-item affiliate-course-hero-item--{product['id']}{primary}" href="{product['href']}" {attrs}>
<span class="affiliate-course-hero-rank">{html.escape(product['rank'])}</span>
<div class="affiliate-course-hero-media">{image}</div>
<span class="affiliate-course-hero-name">{html.escape(product['name'])}</span>
<span class="affiliate-course-hero-tag">{html.escape(product['tag'])}</span>
</a>"""
        )
    return f"""
<section class="affiliate-course-hero" id="affiliate-course-hero" aria-labelledby="affiliate-course-hero-title">
<h2 id="affiliate-course-hero-title" class="affiliate-course-hero-heading">通信講座より安く始められる学習サービス</h2>
<p class="affiliate-course-hero-note">バナーをタップすると各講座の詳細ページを開けます。主導線は<strong>資格対策ドットコム</strong>です。</p>
<div class="affiliate-course-hero-grid" role="list">{"".join(items)}</div>
<p class="affiliate-course-hero-foot"><a href="#pick-shikakutaisaku">各講座の特徴・比較はこちら</a></p>
</section>""".strip()


def _affiliate_cta(href: str, label: str) -> str:
    return (
        f'<p class="affiliate-cta-wrap">'
        f'<a class="affiliate-cta-btn" href="{html.escape(href)}" {_affiliate_attrs()}>'
        f"{html.escape(label)}</a></p>"
    )


def _course_section_visual(product: dict[str, str]) -> str:
    attrs = _affiliate_attrs()
    image = _course_image_html(product, section=True)
    return (
        f'<div class="affiliate-course-section-visual">'
        f'<a class="affiliate-course-section-link" href="{product["href"]}" {attrs}>{image}</a>'
        f"</div>"
    )


def _course_section(product: dict[str, str], section_num: int, heading: str, body_html: str) -> str:
    anchor = f"pick-{product['id']}"
    return f"""
<section class="seo-article-section" aria-labelledby="{anchor}">
<h2 id="{anchor}"><span class="section-heading-num">{section_num}</span>{html.escape(heading)}</h2>
{_course_section_visual(product)}
{body_html}
{_affiliate_cta(product['href'], product['cta'])}
</section>"""


def self_study_sections_html() -> str:
    shikaku, onsuku, square, yotsuya = COURSE_PRODUCTS
    intro = """
<section class="seo-article-section" aria-labelledby="reasons">
<h2 id="reasons"><span class="section-heading-num">1</span>宅建の独学がきつくなる理由</h2>
<p>宅建の独学がきつい理由は、単に内容が難しいからではありません。多くの場合、何をどの順番で勉強すればよいか分からなくなることが原因です。</p>
<p>宅建は、宅建業法、権利関係、法令上の制限、税その他と範囲が広く、それぞれ勉強のコツが違います。特に権利関係は民法の理解が必要なので、最初から丁寧に読み込もうとすると時間がかかります。</p>
<p>さらに、独学では自分の弱点を客観的に見つけにくいです。過去問を何周しても点数が伸びない人は、解説を読んで理解したつもりになっているだけで、実際には本番で使える知識になっていない可能性があります。</p>
</section>
<section class="seo-article-section" aria-labelledby="review">
<h2 id="review"><span class="section-heading-num">2</span>独学がきつい人が最初に見直すべきこと</h2>
<p>まず見直したいのは、教材の量ではなく勉強の流れです。教材を増やす前に、今の勉強が得点につながっているかを確認しましょう。</p>
<p>独学でつまずいている人は、次の状態になりがちです。</p>
<ul class="term-point-list">
<li>テキストを読む時間が長く、問題演習が少ない</li>
<li>権利関係に時間を使いすぎている</li>
<li>宅建業法で満点近くを狙う意識が弱い</li>
<li>過去問の正解番号だけ覚えている</li>
<li>勉強計画を立てても続かない</li>
</ul>
<p>宅建で合格点に近づくには、宅建業法を得点源にして、法令上の制限や税その他で取りこぼしを減らすことが大切です。権利関係は重要ですが、深追いしすぎると時間を奪われます。</p>
<p>独学がきついと感じたら、すべてを一人で抱えるのではなく、講義やオンライン教材を一部だけ使う方法も考えてみましょう。</p>
</section>
<section class="seo-article-section" aria-labelledby="options">
<h2 id="options"><span class="section-heading-num">3</span>通信講座より安く学ぶ選択肢</h2>
<p>宅建の学習サービスには、高額な通信講座だけでなく、低価格のオンライン教材や月額制サービスもあります。独学を完全にやめるのではなく、苦手な部分だけ有料サービスで補う形なら、費用を抑えながら学習を立て直せます。</p>
<table class="seo-info-table">
<thead><tr><th>選択肢</th><th>向いている人</th></tr></thead>
<tbody>
<tr><td>低価格オンライン講座</td><td>独学の補助がほしい人</td></tr>
<tr><td>月額制サービス</td><td>まず安く試したい人</td></tr>
<tr><td>本格的な通信講座</td><td>今年こそ合格したい人</td></tr>
<tr><td>サポート重視の講座</td><td>添削や質問対応も重視したい人</td></tr>
</tbody>
</table>
<p>費用を抑えたい人は、最初から高額講座だけを比較する必要はありません。自分がつまずいている原因に合わせて、必要なサポートだけ足すのが現実的です。</p>
</section>
""".strip()
    shikaku_body = """
<p>独学がきついけれど、いきなり高額な通信講座には申し込みにくい人には、資格対策ドットコムが候補になります。</p>
<p>資格対策ドットコムは、オンラインで宅建学習を進めたい人に向いています。無料教材だけでは不安だけれど、予備校型の講座ほど費用をかけたくない人にとって、独学と通信講座の中間のような使い方ができます。</p>
<ul class="term-point-list">
<li>テキストだけでは理解しにくい</li>
<li>スマホやパソコンで学習したい</li>
<li>独学の補助として講義や教材を使いたい</li>
<li>費用を抑えながら有料教材を試したい</li>
</ul>
<p>独学が止まっている人にとって大事なのは、完璧な教材を探すことではなく、勉強を再開できる仕組みを作ることです。</p>
""".strip()
    onsuku_body = """
<p>とにかく費用を抑えて始めたい人には、オンスク.JPも候補になります。月額制で利用しやすく、宅建学習をまず有料サービスで試してみたい人に向いています。</p>
<p>オンスク.JPは、独学の補助として使いやすいサービスです。スキマ時間に講義を見たり、基本知識を確認したりする用途に向いています。</p>
<p>ただし、再受験で本格的に合格を狙う人や、模試・答練まで含めて対策したい人は、オンスクだけに頼るより、過去問集や模試教材を組み合わせたほうが安心です。</p>
""".strip()
    square_body = """
<p>低価格サービスだけでなく、通信講座としてしっかり比較したい人は、資格スクエアも候補に入ります。</p>
<p>資格スクエアは、オンライン講座として検討しやすいサービスです。独学に限界を感じていて、講義を軸に学習を組み直したい人に向いています。</p>
<p>資格対策ドットコムやオンスク.JPよりも、通信講座としての位置づけで比較したい場合に見ておきたい候補です。費用だけでなく、講義の分かりやすさ、カリキュラム、問題演習の量を確認して選びましょう。</p>
""".strip()
    yotsuya_body = """
<p>一人で勉強を進めるのが不安な人は、四谷学院の宅建講座も候補になります。通信講座でも、サポートや学習の進めやすさを重視したい人に向いています。</p>
<p>独学がきつい理由が「何をすればよいか分からない」「質問できないのが不安」「一人だと続かない」というタイプなら、価格だけで選ばず、サポート面も見たほうがよいです。</p>
<p>ただし、費用を抑えたい人にとっては、資格対策ドットコムやオンスク.JPのほうが入りやすい可能性があります。四谷学院は、安さよりも安心感や学習サポートを重視する人向けとして比較しましょう。</p>
""".strip()
    tail = """
<section class="seo-article-section" aria-labelledby="which">
<h2 id="which"><span class="section-heading-num">8</span>どれを選ぶべきか</h2>
<p>迷ったら、次のように選ぶと分かりやすいです。</p>
<table class="seo-info-table affiliate-pick-table">
<thead><tr><th>状況</th><th>おすすめ候補</th></tr></thead>
<tbody>
<tr><td>独学の補助として安く始めたい</td><td><strong>資格対策ドットコム</strong></td></tr>
<tr><td>月額制でまず試したい</td><td>オンスク.JP</td></tr>
<tr><td>通信講座としてしっかり比較したい</td><td>資格スクエア</td></tr>
<tr><td>サポートや安心感を重視したい</td><td>四谷学院</td></tr>
</tbody>
</table>
<p>独学がきつい人に一番おすすめしやすいのは、資格対策ドットコムです。理由は、独学からいきなり高額講座へ切り替えるより、費用を抑えながら学習を立て直しやすいからです。</p>
<p>ただし、今年どうしても合格したい人や、過去に何度も不合格になっている人は、通信講座としてのサポートがある資格スクエアや四谷学院も比較したほうがよいでしょう。</p>
</section>
<section class="seo-article-section" aria-labelledby="combine">
<h2 id="combine"><span class="section-heading-num">9</span>独学と有料サービスを組み合わせる勉強法</h2>
<p>有料サービスを使う場合でも、すべてを講座任せにする必要はありません。宅建は、講義で理解して、過去問で定着させる流れが大切です。</p>
<ol class="term-point-list">
<li>講義やオンライン教材で全体像をつかむ</li>
<li>宅建業法を優先して過去問を解く</li>
<li>法令上の制限と税その他を暗記する</li>
<li>権利関係は頻出論点に絞る</li>
<li>直前期は模試や予想問題で時間配分を確認する</li>
</ol>
<p>独学がきつい人ほど、最初から完璧を目指さないことが大切です。まずは宅建業法で点を取れる状態を作り、合格ラインに必要な科目から順番に固めましょう。</p>
</section>
<section class="seo-article-section" aria-labelledby="summary">
<h2 id="summary"><span class="section-heading-num">10</span>まとめ：独学がきついなら、安く補助を入れるのが現実的</h2>
<p>宅建の独学がきついと感じたら、無理に一人で続ける必要はありません。とはいえ、いきなり高額な通信講座に申し込まなくても、低価格のオンライン講座や月額制サービスで学習を立て直す方法があります。</p>
<p>費用を抑えながら独学を補助したい人は、まず資格対策ドットコムを確認するとよいでしょう。月額制で試したい人はオンスク.JP、通信講座として比較したい人は資格スクエア、サポート重視なら四谷学院も候補になります。</p>
<p>独学がきついと感じるのは、合格できないサインではありません。今の勉強法を変えるタイミングです。自分に足りない部分だけ有料サービスで補い、合格点に近づく勉強へ切り替えましょう。</p>
</section>
""".strip()
    return "\n".join(
        [
            intro,
            _course_section(shikaku, 4, "第一候補：資格対策ドットコム", shikaku_body),
            _course_section(onsuku, 5, "安さ重視ならオンスク.JP", onsuku_body),
            _course_section(square, 6, "しっかり講座で比較したいなら資格スクエア", square_body),
            _course_section(yotsuya, 7, "サポート重視なら四谷学院も候補", yotsuya_body),
            tail,
            _affiliate_cta(shikaku["href"], shikaku["cta"]),
        ]
    )


def self_study_hard_toc_html(has_faq: bool) -> str:
    items: list[tuple[str, str]] = [
        ("quality-panel-title", "この記事の信頼性について"),
        ("action-box-title", "この記事でできること"),
        ("affiliate-course-hero", "おすすめの学習サービス"),
        *SELF_STUDY_TOC_EXTRA,
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
