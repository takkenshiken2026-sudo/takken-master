#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""宅建ガイド記事を生成する。"""

from __future__ import annotations

import html
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from tools.articles_batch10 import BATCH_ARTICLES as BATCH_ARTICLES_10  # noqa: E402
from tools.articles_batch20 import BATCH_ARTICLES as BATCH_ARTICLES_20  # noqa: E402
from tools.site_config import brand_mark, brand_name, clean_origin, external_links  # noqa: E402

ARTICLE_CSS = """*{box-sizing:border-box;margin:0;padding:0}html{background:#fff;min-height:100%;color-scheme:light}body{font-family:'Noto Sans JP',sans-serif;background:#fff;color:#111;-webkit-font-smoothing:antialiased;line-height:1.75;min-height:100vh;color-scheme:light}.topnav{position:sticky;top:0;z-index:30;background:#fff;border-bottom:1px solid rgba(0,0,0,.08)}.topnav-inner{max-width:900px;margin:0 auto;padding:0 20px;height:54px;display:flex;align-items:center}.logo{display:flex;align-items:center;gap:9px;text-decoration:none;color:#111;margin-right:auto}.logo-mark{width:28px;height:28px;border-radius:7px;background:#333;display:flex;align-items:center;justify-content:center;font-size:12px;font-weight:700;color:#fff}.logo-text{font-size:17px;font-weight:700}.nav-links{display:flex;align-items:center;gap:2px}.nav-link{padding:6px 12px;border-radius:6px;font-size:14px;color:#555;text-decoration:none;white-space:nowrap}.nav-link:hover{background:#efefef;color:#111}.article-wrap{max-width:760px;margin:0 auto;padding:40px 20px 96px;background:#fff}.breadcrumb{margin-bottom:24px}.breadcrumb-list{display:flex;align-items:center;flex-wrap:wrap;list-style:none}.breadcrumb-list li{display:flex;align-items:center;font-size:13px;color:#999}.breadcrumb-list li+li::before{content:'›';margin:0 6px}.breadcrumb-list a{color:#999;text-decoration:none}.breadcrumb-list a:hover{color:#555}.breadcrumb-list li[aria-current]{color:#555}.article-eyebrow{font-size:11px;font-weight:700;color:#888;letter-spacing:.12em;margin-bottom:12px}.article-h1{font-size:32px;font-weight:800;line-height:1.32;margin-bottom:16px;color:#111}.article-meta{display:flex;align-items:center;gap:16px;flex-wrap:wrap;font-size:13px;color:#999;margin-bottom:32px;padding-bottom:24px;border-bottom:1px solid #e0e0e0}.article-lead{font-size:16px;line-height:1.9;color:#333;margin-bottom:40px;padding:20px 24px;background:#fff;border:1px solid rgba(0,0,0,.1);border-radius:8px;box-shadow:0 1px 3px rgba(0,0,0,.06)}.toc{background:#fff;border:1px solid rgba(0,0,0,.1);border-radius:8px;padding:20px 24px;margin-bottom:40px}.toc-title{font-size:14px;font-weight:700;color:#555;margin-bottom:12px}.toc-list{list-style:none;display:flex;flex-direction:column;gap:7px}.toc-list a{font-size:14px;color:#333;text-decoration:none}.toc-list a:hover{text-decoration:underline}.trust-section{margin-bottom:48px}.trust-section .article-h2{margin-bottom:14px}.article-section{margin-bottom:48px}.article-h2{font-size:22px;font-weight:800;margin-bottom:16px;padding-bottom:12px;border-bottom:2px solid #e0e0e0;color:#111;display:flex;align-items:center;gap:10px}.article-h2-num{width:28px;height:28px;background:#333;color:#fff;border-radius:6px;display:flex;align-items:center;justify-content:center;font-size:13px;font-weight:700;flex-shrink:0}.article-h3{font-size:17px;font-weight:700;margin:24px 0 10px;color:#111;padding-bottom:6px;border-bottom:1px solid #e0e0e0}.article-p{font-size:15px;line-height:1.9;color:#333;margin-bottom:16px}.article-table-wrap{overflow-x:auto;margin:16px 0}.article-table{width:100%;border-collapse:collapse;font-size:14px;min-width:480px}.article-table th{background:#333;color:#fff;padding:10px 12px;text-align:left;font-weight:700;border:1px solid #ddd}.article-table td{padding:10px 12px;border:1px solid #ddd;vertical-align:top;color:#333}.article-table tr:nth-child(even) td{background:#fafafa}.trust-table{min-width:0}.trust-table th{width:150px}.trust-table a{color:#333;text-decoration:underline;text-underline-offset:2px}.highlight-box{background:#fff;border:1px solid rgba(0,0,0,.1);border-radius:8px;padding:20px 24px;margin:20px 0;box-shadow:0 1px 3px rgba(0,0,0,.06)}.highlight-box-title{font-size:13px;font-weight:700;color:#555;margin-bottom:10px}.highlight-list{list-style:none;display:flex;flex-direction:column;gap:8px}.highlight-item{display:flex;align-items:flex-start;gap:10px;font-size:14px;line-height:1.7;color:#333}.highlight-item::before{content:'−';color:#333;font-weight:700;flex-shrink:0;margin-top:1px}.warn-box,.point-box{border:1px solid #ddd;border-radius:8px;padding:14px 18px;margin:16px 0;font-size:14px;line-height:1.7;color:#333}.warn-box{background:#f9f9f9}.point-box{background:#f5f5f5}.warn-box-label,.point-box-label{font-weight:700;color:#333;margin-right:6px}.cta-section{background:#111;color:#fff;border-radius:10px;padding:28px 32px;text-align:center;margin:48px 0 0}.cta-title{font-size:20px;font-weight:800;margin-bottom:8px}.cta-desc{font-size:14px;color:#bbb;margin-bottom:20px;line-height:1.7}.cta-btn{display:inline-flex;align-items:center;gap:8px;padding:12px 28px;background:#f5f5f5;color:#111;border:1px solid #ddd;border-radius:8px;font-size:15px;font-weight:700;text-decoration:none}.site-footer{border-top:1px solid rgba(0,0,0,.08);background:#fff;padding:14px 20px}.site-footer-inner{max-width:900px;margin:0 auto;display:flex;align-items:center;gap:20px;flex-wrap:wrap}.footer-logo{display:flex;align-items:center;gap:7px;text-decoration:none;color:#111}.footer-logo-mark{width:22px;height:22px;border-radius:5px;background:#333;display:flex;align-items:center;justify-content:center;font-size:10px;font-weight:700;color:#fff}.footer-logo-text{font-size:13px;font-weight:700}.footer-links{display:flex;gap:20px;flex-wrap:wrap}.footer-links a{font-size:13px;color:#999;text-decoration:none}.footer-copy{font-size:12px;color:#999;margin-left:auto}@media(max-width:640px){.article-wrap{padding-top:28px}.article-h1{font-size:24px}.article-h2{font-size:18px}.nav-links{display:none}.cta-section{padding:24px 20px}.trust-table th{width:110px}}@media(prefers-color-scheme:dark){html,body,.article-wrap{background:#fff!important;color:#111!important}}"""

UPDATED_LABEL = "2026年5月19日"

ARTICLES = [
    {
        "slug": "takken-benkyou-jikan",
        "title": "宅建の勉強時間は何時間必要？初学者・社会人・再受験者別の目安",
        "short_title": "宅建の勉強時間は何時間必要？",
        "description": "宅建試験に必要な勉強時間を、初学者・社会人・再受験者・不動産業界経験者に分けて解説。残り期間から逆算する学習量と、時間不足を防ぐ進め方もまとめます。",
        "eyebrow": "宅建 学習計画",
        "lead": "宅建の勉強時間は、知識ゼロなら300〜400時間、学習経験や業界経験がある人なら200〜300時間がひとつの目安です。ただし大事なのは総時間そのものより、宅建業法・過去問演習・復習にどれだけ時間を配分できるかです。",
        "toc": [
            ("hours", "属性別の勉強時間の目安"),
            ("reverse", "残り期間から逆算する"),
            ("breakdown", "分野別の時間配分"),
            ("busy", "忙しい社会人の時間確保"),
            ("shortage", "時間が足りないときの優先順位"),
        ],
        "body": """
<section class="article-section"><h2 class="article-h2" id="hours"><span class="article-h2-num">1</span>属性別の勉強時間の目安</h2>
<p class="article-p">宅建は四肢択一50問の試験ですが、範囲は広く、法律用語に慣れるまで時間がかかります。最初に自分の現在地を見て、必要時間を少し多めに見積もるのが安全です。</p>
<div class="article-table-wrap"><table class="article-table"><thead><tr><th>タイプ</th><th>目安時間</th><th>計画のポイント</th></tr></thead><tbody>
<tr><td>法律初学者</td><td>300〜400時間</td><td>権利関係に時間を吸われやすいので、宅建業法を先に得点源にします。</td></tr>
<tr><td>社会人初学者</td><td>300時間前後</td><td>平日の短時間学習と週末演習をセットにして、6ヶ月以上で組みます。</td></tr>
<tr><td>不動産業界経験者</td><td>200〜300時間</td><td>実務感覚で分かる部分と、試験用の暗記を切り分けます。</td></tr>
<tr><td>再受験者</td><td>150〜250時間</td><td>前回の失点分野を中心に、解ける問題を落とさない設計へ変えます。</td></tr>
</tbody></table></div>
<div class="point-box"><span class="point-box-label">考え方：</span>「何時間やったか」だけでなく、過去問を解いて正解理由まで説明できるかを基準にします。時間は合格の必要条件ですが、復習の質が低いと得点に変わりません。</div></section>
<section class="article-section"><h2 class="article-h2" id="reverse"><span class="article-h2-num">2</span>残り期間から逆算する</h2>
<p class="article-p">試験までの残り期間で、1週間に必要な学習量は大きく変わります。無理な計画は途中で崩れるので、最初から予備日を含めて組みます。</p>
<div class="article-table-wrap"><table class="article-table"><thead><tr><th>残り期間</th><th>週あたりの目安</th><th>向いている人</th></tr></thead><tbody>
<tr><td>1年</td><td>6〜8時間</td><td>初学者、仕事や家庭で忙しい人</td></tr>
<tr><td>6ヶ月</td><td>10〜14時間</td><td>標準的な社会人、4月スタートの人</td></tr>
<tr><td>3ヶ月</td><td>20〜25時間</td><td>再受験者、基礎知識がある人</td></tr>
<tr><td>1ヶ月</td><td>30時間以上</td><td>総復習・直前演習に入っている人</td></tr>
</tbody></table></div></section>
<section class="article-section"><h2 class="article-h2" id="breakdown"><span class="article-h2-num">3</span>分野別の時間配分</h2>
<p class="article-p">宅建では、配点が大きく得点しやすい宅建業法を厚めにします。権利関係は深入りしすぎると時間効率が落ちるため、基本問題を落とさない方針が現実的です。</p>
<div class="highlight-box"><div class="highlight-box-title">300時間で組む場合の例</div><ul class="highlight-list">
<li class="highlight-item">宅建業法：90〜100時間。条文・数字・過去問を反復します。</li>
<li class="highlight-item">権利関係：80〜90時間。民法の頻出テーマを中心にします。</li>
<li class="highlight-item">法令上の制限：50〜60時間。用途地域や建築制限を表で整理します。</li>
<li class="highlight-item">税・その他：30〜40時間。直前期の暗記と統計確認に寄せます。</li>
<li class="highlight-item">模試・総復習：30時間前後。本番形式の時間配分を作ります。</li>
</ul></div></section>
<section class="article-section"><h2 class="article-h2" id="busy"><span class="article-h2-num">4</span>忙しい社会人の時間確保</h2>
<p class="article-p">社会人は、毎日まとまった時間を取るより、学習の開始時刻を固定するほうが続きます。朝・通勤・昼休み・就寝前のどこかに「必ず10問」を置きます。</p>
<h3 class="article-h3">平日は短く、休日は深く</h3>
<p class="article-p">平日は一問一答や過去問の解き直しに向いています。休日は権利関係や法令上の制限など、理解に時間がかかる分野をまとめて扱います。</p>
<h3 class="article-h3">疲れている日は暗記系に切り替える</h3>
<p class="article-p">疲れている日に民法の難問へ進むと消耗します。宅建業法の数字、35条・37条、媒介契約など、短い単位で確認できる論点へ切り替えると継続しやすくなります。</p></section>
<section class="article-section"><h2 class="article-h2" id="shortage"><span class="article-h2-num">5</span>時間が足りないときの優先順位</h2>
<p class="article-p">残り時間が少ない場合は、全範囲をきれいに終わらせる発想を捨てます。得点になりやすい順に、宅建業法、法令上の制限、税・その他、権利関係の基本問題へ絞ります。</p>
<div class="warn-box"><span class="warn-box-label">注意：</span>直前期に新しい教材を増やすと、復習すべき問題が分散します。過去問と間違いノートを中心に、同じ論点を確実に取れる状態へ寄せましょう。</div>
<div class="cta-section"><div class="cta-title">勉強時間を決めたら過去問へ</div><p class="cta-desc">時間配分を作ったあとは、実際の問題で得点に変えていきましょう。</p><a class="cta-btn" href="/quiz/past/">過去問を解く</a></div></section>
""",
    },
    {
        "slug": "takken-goukakuten",
        "title": "宅建の合格点は何点？合格ラインの考え方と目標点の作り方",
        "short_title": "宅建の合格点は何点？",
        "description": "宅建試験の合格点・合格ラインの考え方を解説。年度ごとに点数が変わる理由、目標点の作り方、模試や過去問の点数をどう判断するかをまとめます。",
        "eyebrow": "宅建 合格ライン",
        "lead": "宅建の合格点は年度ごとに変動します。固定の満点基準ではなく、問題の難易度や受験者全体の出来を踏まえて決まるため、学習段階では36〜38点を安定して取る設計を目標にします。",
        "toc": [
            ("line", "合格点は年度で変わる"),
            ("target", "目標点は36〜38点で組む"),
            ("field", "分野別の目標点"),
            ("mock", "模試の点数の見方"),
            ("last", "直前期の点数別対策"),
        ],
        "body": """
<section class="article-section"><h2 class="article-h2" id="line"><span class="article-h2-num">1</span>合格点は年度で変わる</h2>
<p class="article-p">宅建試験は50問中何点以上なら必ず合格、という単純な試験ではありません。合格基準点は年度ごとに発表され、問題の難易度によって上下します。</p>
<div class="point-box"><span class="point-box-label">基本方針：</span>合格点そのものを予想するより、合格点が多少高くなっても届く得点力を作ることが大切です。</div>
<p class="article-p">学習中は「35点で足りるか」ではなく、「38点を狙える構成になっているか」を確認します。この意識だけで、宅建業法や法令上の制限の取りこぼしに敏感になります。</p></section>
<section class="article-section"><h2 class="article-h2" id="target"><span class="article-h2-num">2</span>目標点は36〜38点で組む</h2>
<p class="article-p">本番では緊張や読み間違いで1〜2点落とすことがあります。そのため、普段の演習では合格ラインぎりぎりではなく、36〜38点を安定して出すことを目標にします。</p>
<div class="highlight-box"><div class="highlight-box-title">目標設定の目安</div><ul class="highlight-list">
<li class="highlight-item">初期：25点前後でも問題ありません。まず出題形式に慣れます。</li>
<li class="highlight-item">中期：30点台前半を安定させ、宅建業法の失点を減らします。</li>
<li class="highlight-item">直前期：36〜38点を複数回出せる状態を目指します。</li>
</ul></div></section>
<section class="article-section"><h2 class="article-h2" id="field"><span class="article-h2-num">3</span>分野別の目標点</h2>
<p class="article-p">合格点を超えるには、難しい分野で満点を狙うより、得点源を落とさないことが重要です。</p>
<div class="article-table-wrap"><table class="article-table"><thead><tr><th>分野</th><th>出題数の目安</th><th>目標点</th><th>考え方</th></tr></thead><tbody>
<tr><td>宅建業法</td><td>20問</td><td>17〜19点</td><td>最重要。ここで貯金を作ります。</td></tr>
<tr><td>権利関係</td><td>14問</td><td>7〜9点</td><td>難問を追いすぎず、基本問題を拾います。</td></tr>
<tr><td>法令上の制限</td><td>8問</td><td>6〜7点</td><td>数字と制度比較を整理すれば伸ばしやすい分野です。</td></tr>
<tr><td>税・その他</td><td>8問</td><td>5〜6点</td><td>直前期に知識を更新して取りこぼしを防ぎます。</td></tr>
</tbody></table></div></section>
<section class="article-section"><h2 class="article-h2" id="mock"><span class="article-h2-num">4</span>模試の点数の見方</h2>
<p class="article-p">模試の点数は一喜一憂するためのものではなく、次の2週間で何を直すかを決める材料です。点数だけでなく、分野別の内訳を見ます。</p>
<h3 class="article-h3">30点未満の場合</h3><p class="article-p">基礎知識がまだ散らばっています。宅建業法を優先し、過去問の正解理由を説明できる状態にします。</p>
<h3 class="article-h3">30〜34点の場合</h3><p class="article-p">合格圏まであと少しです。ケアレスミス、数字暗記、法令上の制限の比較表を重点的に潰します。</p>
<h3 class="article-h3">35点以上の場合</h3><p class="article-p">本番で崩れないよう、時間配分と見直し手順を固定します。新しい難問より、落としてはいけない問題を確認します。</p></section>
<section class="article-section"><h2 class="article-h2" id="last"><span class="article-h2-num">5</span>直前期の点数別対策</h2>
<p class="article-p">直前期は伸びる分野を見極めます。宅建業法と法令上の制限は短期間でも点数に反映されやすく、権利関係の難問は時間効率が落ちることがあります。</p>
<div class="warn-box"><span class="warn-box-label">注意：</span>合格点予想に振り回されると、やるべき復習が後回しになります。予想点より、自分が落とした問題の原因を確認しましょう。</div>
<div class="cta-section"><div class="cta-title">分野別に弱点を確認する</div><p class="cta-desc">目標点を決めたら、過去問でどの分野を落としているか確認しましょう。</p><a class="cta-btn" href="/quiz/past/">過去問を解く</a></div></section>
""",
    },
    {
        "slug": "takken-hooreijou-seigen-study",
        "title": "宅建の法令上の制限の勉強法｜用途地域・建ぺい率・開発許可の攻略",
        "short_title": "法令上の制限の勉強法",
        "description": "宅建試験の法令上の制限を効率よく学ぶ方法を解説。都市計画法、建築基準法、国土利用計画法、農地法、宅地造成等規制法の優先順位と覚え方をまとめます。",
        "eyebrow": "宅建 分野別攻略",
        "lead": "法令上の制限は、制度名と数字が多くて苦手に感じやすい分野です。ただし出題範囲は比較的整理しやすく、表で違いを押さえれば得点源にできます。",
        "toc": [
            ("why", "法令上の制限が伸ばしやすい理由"),
            ("priority", "優先順位"),
            ("city", "都市計画法・建築基準法"),
            ("numbers", "数字暗記のコツ"),
            ("routine", "1週間の学習ルーティン"),
        ],
        "body": """
<section class="article-section"><h2 class="article-h2" id="why"><span class="article-h2-num">1</span>法令上の制限が伸ばしやすい理由</h2>
<p class="article-p">法令上の制限は、土地や建物をどのように使えるかを制限するルールです。民法のような複雑な事例判断より、制度の要件や数字を正確に覚える問題が多いため、整理すれば点数に結びつきます。</p>
<div class="point-box"><span class="point-box-label">狙い：</span>満点にこだわるより、8問中6〜7点を安定して取ることを目標にします。</div></section>
<section class="article-section"><h2 class="article-h2" id="priority"><span class="article-h2-num">2</span>優先順位</h2>
<p class="article-p">すべてを同じ重さで読むと時間が足りません。まず出題の中心になる都市計画法と建築基準法を固めます。</p>
<div class="article-table-wrap"><table class="article-table"><thead><tr><th>テーマ</th><th>優先度</th><th>学習ポイント</th></tr></thead><tbody>
<tr><td>都市計画法</td><td>高</td><td>区域区分、用途地域、開発許可を整理します。</td></tr>
<tr><td>建築基準法</td><td>高</td><td>建ぺい率・容積率・道路規制を中心にします。</td></tr>
<tr><td>国土利用計画法</td><td>中</td><td>届出の対象、事後届出、監視区域を比較します。</td></tr>
<tr><td>農地法</td><td>中</td><td>3条・4条・5条の違いを表で覚えます。</td></tr>
<tr><td>宅地造成等工事規制区域</td><td>中</td><td>許可・届出の場面を整理します。</td></tr>
</tbody></table></div></section>
<section class="article-section"><h2 class="article-h2" id="city"><span class="article-h2-num">3</span>都市計画法・建築基準法</h2>
<h3 class="article-h3">用途地域は「建てられるもの」で覚える</h3>
<p class="article-p">用途地域は名前だけを丸暗記すると混乱します。住居系、商業系、工業系に分け、どの建物が制限されるかを問題で確認します。</p>
<h3 class="article-h3">建ぺい率・容積率は計算問題まで解く</h3>
<p class="article-p">建ぺい率と容積率は、定義を覚えるだけでは不十分です。前面道路幅員による容積率制限、防火地域による緩和など、条件が加わった問題で練習します。</p></section>
<section class="article-section"><h2 class="article-h2" id="numbers"><span class="article-h2-num">4</span>数字暗記のコツ</h2>
<p class="article-p">数字は単独で覚えるより、制度の目的とセットにします。例えば農地法は「農地を守る」、国土利用計画法は「大規模な土地取引を監視する」という目的を意識すると、届出や許可の意味がつながります。</p>
<div class="highlight-box"><div class="highlight-box-title">覚え方の型</div><ul class="highlight-list">
<li class="highlight-item">比較表を1枚作り、似ている制度を横並びにします。</li>
<li class="highlight-item">数字だけを赤シートで隠すより、問題文の形で確認します。</li>
<li class="highlight-item">間違えた数字は、なぜその数字なのか一言メモを残します。</li>
</ul></div></section>
<section class="article-section"><h2 class="article-h2" id="routine"><span class="article-h2-num">5</span>1週間の学習ルーティン</h2>
<p class="article-p">月曜から木曜は1テーマずつ過去問を解き、金曜に間違いだけ復習します。休日に表を見直し、似ている制度の違いを声に出して確認します。</p>
<div class="warn-box"><span class="warn-box-label">注意：</span>法令上の制限は「分かったつもり」になりやすい分野です。テキストを読むだけでなく、必ず過去問で条件の読み取りを確認しましょう。</div>
<div class="cta-section"><div class="cta-title">法令上の制限を問題で確認する</div><p class="cta-desc">整理した知識を、過去問の条件文で使えるようにしていきましょう。</p><a class="cta-btn" href="/quiz/past/?field=limit">過去問を解く</a></div></section>
""",
    },
    {
        "slug": "takken-zei-sonota-study",
        "title": "宅建の税・その他の勉強法｜直前期に得点を上積みする攻略法",
        "short_title": "税・その他の勉強法",
        "description": "宅建試験の税・その他を効率よく学ぶ方法を解説。不動産取得税、固定資産税、登録免許税、統計、5問免除科目の優先順位と直前期の勉強法をまとめます。",
        "eyebrow": "宅建 分野別攻略",
        "lead": "税・その他は出題数こそ多くありませんが、直前期の確認で点数を上積みしやすい分野です。細かい税率を最初から完璧にするより、頻出テーマと更新情報を押さえることが大切です。",
        "toc": [
            ("scope", "税・その他の範囲"),
            ("tax", "税金分野の優先順位"),
            ("exemption", "5問免除科目の考え方"),
            ("lastmonth", "直前1ヶ月の進め方"),
            ("mistake", "よくある失敗"),
        ],
        "body": """
<section class="article-section"><h2 class="article-h2" id="scope"><span class="article-h2-num">1</span>税・その他の範囲</h2>
<p class="article-p">税・その他には、不動産に関する税金、価格評定、統計、住宅金融、土地建物の知識などが含まれます。範囲が広く見えますが、頻出テーマはある程度決まっています。</p>
<div class="article-table-wrap"><table class="article-table"><thead><tr><th>テーマ</th><th>学習ポイント</th><th>時期</th></tr></thead><tbody>
<tr><td>不動産取得税</td><td>課税主体、課税標準、軽減措置</td><td>中期〜直前</td></tr>
<tr><td>固定資産税</td><td>課税標準、住宅用地の特例、納税義務者</td><td>中期〜直前</td></tr>
<tr><td>登録免許税・印紙税</td><td>課税場面と軽減措置</td><td>直前</td></tr>
<tr><td>統計</td><td>最新資料の数字・増減傾向</td><td>直前</td></tr>
<tr><td>土地・建物</td><td>基本知識と用語</td><td>中期</td></tr>
</tbody></table></div></section>
<section class="article-section"><h2 class="article-h2" id="tax"><span class="article-h2-num">2</span>税金分野の優先順位</h2>
<p class="article-p">税金は細かい数字が多いため、最初からすべてを暗記しようとすると負担が大きくなります。まず「誰に、何に、いつ課税されるか」を押さえます。</p>
<div class="highlight-box"><div class="highlight-box-title">税金の基本フレーム</div><ul class="highlight-list">
<li class="highlight-item">課税主体：国税か地方税かを確認します。</li>
<li class="highlight-item">納税義務者：誰が納める税金かを確認します。</li>
<li class="highlight-item">課税標準：何を基準に税額を計算するかを確認します。</li>
<li class="highlight-item">軽減措置：住宅用地や居住用財産の特例を整理します。</li>
</ul></div></section>
<section class="article-section"><h2 class="article-h2" id="exemption"><span class="article-h2-num">3</span>5問免除科目の考え方</h2>
<p class="article-p">登録講習修了者は一部の問題が免除されますが、一般受験者は統計や土地建物の知識も対策が必要です。ここは深追いより、直前期に最新情報を確認して取りやすい問題を拾う方針が向いています。</p>
<div class="point-box"><span class="point-box-label">コツ：</span>統計は古い教材の数字を覚え込まないようにします。試験年度に対応した直前資料で確認しましょう。</div></section>
<section class="article-section"><h2 class="article-h2" id="lastmonth"><span class="article-h2-num">4</span>直前1ヶ月の進め方</h2>
<p class="article-p">税・その他は直前期に伸ばしやすい反面、早く覚えすぎると忘れやすい分野です。9月以降に集中的に確認し、10月は間違えた論点だけを短く回します。</p>
<div class="article-table-wrap"><table class="article-table"><thead><tr><th>時期</th><th>やること</th><th>目標</th></tr></thead><tbody>
<tr><td>9月前半</td><td>税金の頻出テーマを1周</td><td>基本用語を説明できる</td></tr>
<tr><td>9月後半</td><td>過去問と統計資料を確認</td><td>取りやすい問題を落とさない</td></tr>
<tr><td>10月</td><td>間違いノートと数字の最終確認</td><td>5〜6点を狙う</td></tr>
</tbody></table></div></section>
<section class="article-section"><h2 class="article-h2" id="mistake"><span class="article-h2-num">5</span>よくある失敗</h2>
<h3 class="article-h3">税率だけを丸暗記する</h3><p class="article-p">税率の暗記だけでは、問題文の課税場面を読み取れません。まずどの税金の話かを判断できるようにします。</p>
<h3 class="article-h3">統計を古い数字で覚える</h3><p class="article-p">統計は年度により更新されます。古い教材の数字をそのまま信じず、直前期の最新情報で確認します。</p>
<h3 class="article-h3">時間をかけすぎる</h3><p class="article-p">税・その他は大切ですが、宅建業法ほど配点は大きくありません。直前期の上積み分野として、過去問中心に効率よく進めます。</p>
<div class="cta-section"><div class="cta-title">税・その他を短く確認する</div><p class="cta-desc">頻出テーマを押さえたら、過去問で出題の形に慣れましょう。</p><a class="cta-btn" href="/quiz/past/?field=tax">過去問を解く</a></div></section>
""",
    },
    {
        "slug": "takken-gakusei",
        "title": "大学生・専門学生が宅建を取るメリット｜就活での活かし方と勉強計画",
        "short_title": "大学生・専門学生が宅建を取るメリット",
        "description": "大学生・専門学生が宅建を取得するメリット、就職活動での活かし方、学年別の勉強計画を解説。不動産・金融・建設志望の学生向けに、無理なく合格を狙う進め方をまとめます。",
        "eyebrow": "宅建 学生向け",
        "lead": "学生の宅建取得は、不動産業界だけでなく金融、建設、住宅、保険などの就職活動でも説明しやすい強みになります。時間を作りやすい一方で先延ばしもしやすいので、学年と就活時期に合わせた計画が大切です。",
        "toc": [
            ("merit", "学生が宅建を取るメリット"),
            ("job", "就活でどう伝えるか"),
            ("grade", "学年別の計画"),
            ("study", "学生向けの勉強法"),
            ("caution", "注意点"),
        ],
        "body": """
<section class="article-section"><h2 class="article-h2" id="merit"><span class="article-h2-num">1</span>学生が宅建を取るメリット</h2>
<p class="article-p">宅建は受験資格がなく、学生でも受けられる国家資格です。不動産取引、契約、民法、税金、法令制限の基礎を学べるため、就職前にビジネスの土台を作れる点が大きなメリットです。</p>
<div class="highlight-box"><div class="highlight-box-title">学生にとっての主なメリット</div><ul class="highlight-list">
<li class="highlight-item">就職活動で、継続して学習した実績を説明しやすい。</li>
<li class="highlight-item">不動産・金融・建設・住宅業界への志望理由に具体性が出る。</li>
<li class="highlight-item">契約や不動産広告を見る力がつき、社会人になってからも役立つ。</li>
<li class="highlight-item">社会人よりまとまった勉強時間を取りやすい。</li>
</ul></div></section>
<section class="article-section"><h2 class="article-h2" id="job"><span class="article-h2-num">2</span>就活でどう伝えるか</h2>
<p class="article-p">履歴書に資格名を書くことも大切ですが、面接では「なぜ取ったのか」「どう学んだのか」「仕事でどう活かすのか」まで話せると強くなります。</p>
<div class="article-table-wrap"><table class="article-table"><thead><tr><th>志望業界</th><th>伝え方</th><th>つなげる知識</th></tr></thead><tbody>
<tr><td>不動産仲介</td><td>重要事項説明や宅建業法への関心を伝える</td><td>35条書面、37条書面、媒介契約</td></tr>
<tr><td>金融</td><td>担保不動産や住宅ローンへの理解を伝える</td><td>抵当権、税金、登記</td></tr>
<tr><td>建設・住宅</td><td>土地利用や建築制限への関心を伝える</td><td>用途地域、建ぺい率、容積率</td></tr>
</tbody></table></div></section>
<section class="article-section"><h2 class="article-h2" id="grade"><span class="article-h2-num">3</span>学年別の計画</h2>
<p class="article-p">就活で使いたいなら、できれば大学2〜3年生のうちに合格しておくと説明しやすくなります。4年生でも内定後や卒業前の学習として価値があります。</p>
<div class="article-table-wrap"><table class="article-table"><thead><tr><th>学年</th><th>おすすめ方針</th><th>注意点</th></tr></thead><tbody>
<tr><td>1〜2年生</td><td>余裕を持って6ヶ月〜1年計画</td><td>試験が遠く感じて中断しやすい</td></tr>
<tr><td>3年生</td><td>就活前の合格を狙う</td><td>インターンや授業予定と重ならないようにする</td></tr>
<tr><td>4年生</td><td>内定後・卒業前に集中</td><td>入社後に活かす業務イメージまで持つ</td></tr>
</tbody></table></div></section>
<section class="article-section"><h2 class="article-h2" id="study"><span class="article-h2-num">4</span>学生向けの勉強法</h2>
<p class="article-p">学生は時間を確保しやすい反面、毎日の強制力が弱くなりがちです。授業の空きコマ、通学時間、図書館に行く曜日を固定すると続きます。</p>
<h3 class="article-h3">夏休みを使う</h3><p class="article-p">7〜8月はまとまった演習に向いています。ここで宅建業法と過去問を大きく進めると、9月以降の直前期が安定します。</p>
<h3 class="article-h3">友人と進捗を共有する</h3><p class="article-p">同じ資格を目指す友人がいれば、週1回だけ進捗を確認します。競争より、学習を止めない仕組みとして使うのがコツです。</p></section>
<section class="article-section"><h2 class="article-h2" id="caution"><span class="article-h2-num">5</span>注意点</h2>
<p class="article-p">宅建に合格しても、すぐ宅建士として働くには登録や宅建士証の交付など別の手続きが必要です。就活では「合格」と「宅建士証の保有」を区別して説明しましょう。</p>
<div class="cta-section"><div class="cta-title">学生のうちに過去問へ慣れる</div><p class="cta-desc">まずは出題形式を知るところから始めましょう。</p><a class="cta-btn" href="/quiz/past/">過去問を解く</a></div></section>
""",
    },
    {
        "slug": "takken-mikeiken-tenshoku",
        "title": "未経験から宅建で不動産業界へ転職する方法｜求人選びと準備の進め方",
        "short_title": "未経験から宅建で不動産業界へ転職する方法",
        "description": "未経験から宅建を活かして不動産業界へ転職する方法を解説。職種別の違い、求人の見方、面接での伝え方、入社前に準備しておきたい知識をまとめます。",
        "eyebrow": "宅建 転職",
        "lead": "宅建は未経験転職の入口として使いやすい資格です。ただし、資格だけで転職が決まるわけではありません。職種ごとの仕事内容を理解し、自分の経験と宅建知識をどうつなげるかを準備することが重要です。",
        "toc": [
            ("value", "未経験転職で宅建が評価される理由"),
            ("jobs", "職種別の向き不向き"),
            ("resume", "履歴書・面接での伝え方"),
            ("prepare", "入社前の準備"),
            ("avoid", "避けたい求人選び"),
        ],
        "body": """
<section class="article-section"><h2 class="article-h2" id="value"><span class="article-h2-num">1</span>未経験転職で宅建が評価される理由</h2>
<p class="article-p">不動産会社では、一定数の専任の宅建士が必要です。また、重要事項説明や契約書面など宅建業法に関わる場面が多いため、宅建合格者は基礎知識を持つ人材として評価されやすくなります。</p>
<div class="point-box"><span class="point-box-label">現実的な見方：</span>宅建は強い材料ですが、営業力、接客経験、事務処理力、継続力などの職務経験と組み合わせて伝えることで評価が上がります。</div></section>
<section class="article-section"><h2 class="article-h2" id="jobs"><span class="article-h2-num">2</span>職種別の向き不向き</h2>
<div class="article-table-wrap"><table class="article-table"><thead><tr><th>職種</th><th>仕事内容</th><th>向いている人</th></tr></thead><tbody>
<tr><td>売買仲介</td><td>物件提案、内見、契約、重要事項説明</td><td>提案営業や高額商材の営業に挑戦したい人</td></tr>
<tr><td>賃貸仲介</td><td>部屋探し、内見、申込み、契約</td><td>接客経験を活かしたい人</td></tr>
<tr><td>不動産管理</td><td>入居者対応、オーナー対応、修繕調整</td><td>調整力や事務処理力を活かしたい人</td></tr>
<tr><td>不動産事務</td><td>契約書類、更新、重要事項説明の補助</td><td>正確な作業やサポート業務が得意な人</td></tr>
</tbody></table></div></section>
<section class="article-section"><h2 class="article-h2" id="resume"><span class="article-h2-num">3</span>履歴書・面接での伝え方</h2>
<p class="article-p">未経験の場合は、資格名だけでなく「なぜ不動産業界に移りたいのか」「前職の経験がどう活きるのか」を具体化します。</p>
<div class="highlight-box"><div class="highlight-box-title">面接で話しやすい材料</div><ul class="highlight-list">
<li class="highlight-item">宅建業法を学び、契約の重要性を理解した。</li>
<li class="highlight-item">前職の接客・営業・事務経験を、不動産の顧客対応に活かしたい。</li>
<li class="highlight-item">入社後は重要事項説明や契約実務まで担当できる人材を目指したい。</li>
</ul></div></section>
<section class="article-section"><h2 class="article-h2" id="prepare"><span class="article-h2-num">4</span>入社前の準備</h2>
<p class="article-p">合格後すぐ実務ができるわけではないので、入社前には仕事内容に近い知識を補強します。売買なら重要事項説明、賃貸なら借地借家法、管理なら設備や修繕の基本を確認します。</p>
<h3 class="article-h3">実務用語に慣れる</h3><p class="article-p">媒介契約、レインズ、重説、37条書面、原状回復など、現場で使う言葉を早めに確認しておくと入社後の吸収が早くなります。</p></section>
<section class="article-section"><h2 class="article-h2" id="avoid"><span class="article-h2-num">5</span>避けたい求人選び</h2>
<p class="article-p">未経験歓迎だけで判断せず、教育体制、休日、歩合比率、担当範囲、宅建手当の条件を確認します。資格手当がある場合も、専任登録が条件かどうかを見ておきましょう。</p>
<div class="warn-box"><span class="warn-box-label">注意：</span>高収入だけを見て応募すると、営業スタイルや勤務時間が合わないことがあります。仕事内容と生活リズムまで含めて選ぶのが現実的です。</div>
<div class="cta-section"><div class="cta-title">転職前に知識を固める</div><p class="cta-desc">宅建業法と重要事項説明の基礎を、過去問で確認しましょう。</p><a class="cta-btn" href="/quiz/past/?field=law">過去問を解く</a></div></section>
""",
    },
    {
        "slug": "takken-fudosan-gyokai",
        "title": "不動産業界で宅建をどう活かす？営業・管理・事務で役立つ場面",
        "short_title": "不動産業界で宅建をどう活かす？",
        "description": "不動産業界で宅建資格が役立つ場面を、売買仲介、賃貸仲介、管理、事務、開発・住宅会社に分けて解説。資格手当やキャリアアップの考え方もまとめます。",
        "eyebrow": "宅建 キャリア",
        "lead": "宅建は不動産業界で広く使える資格ですが、職種によって活かし方は違います。営業で信頼を得るために使う場合もあれば、管理や事務で契約書類を正確に扱うために使う場合もあります。",
        "toc": [
            ("scene", "宅建が役立つ場面"),
            ("sales", "営業職での活かし方"),
            ("manage", "管理・事務での活かし方"),
            ("allowance", "資格手当と評価"),
            ("next", "次に伸ばすスキル"),
        ],
        "body": """
<section class="article-section"><h2 class="article-h2" id="scene"><span class="article-h2-num">1</span>宅建が役立つ場面</h2>
<p class="article-p">宅建の知識は、物件調査、広告、契約、重要事項説明、顧客対応、トラブル予防で役立ちます。試験知識をそのまま読むだけでなく、実務の流れの中で使える形に変えることが大切です。</p>
<div class="article-table-wrap"><table class="article-table"><thead><tr><th>場面</th><th>役立つ知識</th><th>実務での意味</th></tr></thead><tbody>
<tr><td>物件調査</td><td>登記、法令上の制限</td><td>説明漏れや調査不足を防ぐ</td></tr>
<tr><td>広告</td><td>宅建業法の広告規制</td><td>誇大広告や表示ミスを避ける</td></tr>
<tr><td>契約</td><td>35条・37条、媒介契約</td><td>顧客に正確に説明できる</td></tr>
<tr><td>顧客対応</td><td>民法、借地借家法</td><td>相談の背景を理解しやすくなる</td></tr>
</tbody></table></div></section>
<section class="article-section"><h2 class="article-h2" id="sales"><span class="article-h2-num">2</span>営業職での活かし方</h2>
<p class="article-p">営業職では、宅建を持っていること自体より、説明の説得力が上がることが大きな価値です。重要事項説明の担当、契約前の注意点整理、買主・借主の不安解消に活かせます。</p>
<h3 class="article-h3">売買仲介</h3><p class="article-p">権利関係、道路、用途地域、建ぺい率・容積率などを理解していると、物件のリスクを早めに確認できます。</p>
<h3 class="article-h3">賃貸仲介</h3><p class="article-p">借地借家法、原状回復、契約更新、重要事項説明の基本を押さえることで、入居前後のトラブルを減らしやすくなります。</p></section>
<section class="article-section"><h2 class="article-h2" id="manage"><span class="article-h2-num">3</span>管理・事務での活かし方</h2>
<p class="article-p">管理や事務では、契約書類の正確性、更新・解約の手続き、オーナーや入居者への説明で宅建知識が役立ちます。営業ほど表に出ない場面でも、ミスを防ぐ力として評価されます。</p>
<div class="point-box"><span class="point-box-label">強み：</span>宅建を持つ事務職は、単なる入力担当ではなく、契約の意味を理解して確認できる人材として見られやすくなります。</div></section>
<section class="article-section"><h2 class="article-h2" id="allowance"><span class="article-h2-num">4</span>資格手当と評価</h2>
<p class="article-p">宅建手当の有無や金額は会社によって異なります。合格だけで支給される場合もあれば、専任の宅建士として登録することが条件の会社もあります。</p>
<div class="warn-box"><span class="warn-box-label">確認：</span>求人票では、宅建手当の金額だけでなく、支給条件、専任登録の有無、重要事項説明の担当範囲を確認しましょう。</div></section>
<section class="article-section"><h2 class="article-h2" id="next"><span class="article-h2-num">5</span>次に伸ばすスキル</h2>
<p class="article-p">宅建の次は、営業なら提案力と住宅ローン、管理なら賃貸管理と修繕、事務なら契約書類と法改正対応を伸ばすと実務で使いやすくなります。</p>
<div class="cta-section"><div class="cta-title">宅建業法を実務目線で確認する</div><p class="cta-desc">まずは重要事項説明と契約書面の出題を復習しましょう。</p><a class="cta-btn" href="/quiz/past/?field=law">過去問を解く</a></div></section>
""",
    },
    {
        "slug": "takken-fukugyo-dokuritsu",
        "title": "宅建は副業・独立に使える？開業前に知るべき現実と準備",
        "short_title": "宅建は副業・独立に使える？",
        "description": "宅建資格を副業や独立に活かせるかを解説。宅建業免許、専任の宅建士、保証協会、実務経験、集客、開業前に準備すべきことを現実的にまとめます。",
        "eyebrow": "宅建 独立",
        "lead": "宅建は副業や独立の可能性を広げる資格ですが、資格だけで不動産業を始められるわけではありません。宅建業免許、事務所、保証協会、集客、実務経験など、開業前に確認すべき現実があります。",
        "toc": [
            ("reality", "宅建だけで独立できるわけではない"),
            ("side", "副業で活かす方法"),
            ("open", "開業に必要な準備"),
            ("risk", "独立前のリスク"),
            ("roadmap", "現実的なロードマップ"),
        ],
        "body": """
<section class="article-section"><h2 class="article-h2" id="reality"><span class="article-h2-num">1</span>宅建だけで独立できるわけではない</h2>
<p class="article-p">宅建試験に合格しても、それだけで不動産仲介業を始められるわけではありません。不動産業として反復継続して取引を行うには、宅建業免許や事務所、営業保証金または保証協会加入などが必要です。</p>
<div class="warn-box"><span class="warn-box-label">注意：</span>宅建士資格と宅建業免許は別物です。個人で不動産業を開業する場合は、免許制度と開業コストを確認する必要があります。</div></section>
<section class="article-section"><h2 class="article-h2" id="side"><span class="article-h2-num">2</span>副業で活かす方法</h2>
<p class="article-p">副業としては、いきなり仲介業を開業するより、不動産知識を活かした周辺業務から始めるほうが現実的です。</p>
<div class="article-table-wrap"><table class="article-table"><thead><tr><th>活かし方</th><th>内容</th><th>注意点</th></tr></thead><tbody>
<tr><td>不動産会社の補助</td><td>重要事項説明、契約補助、物件調査</td><td>勤務先や登録条件を確認する</td></tr>
<tr><td>不動産ライティング</td><td>用語解説、物件・制度の記事作成</td><td>法令情報の正確性が必要</td></tr>
<tr><td>不動産投資の自己判断</td><td>重説や法令制限の確認</td><td>投資判断は別の知識も必要</td></tr>
</tbody></table></div></section>
<section class="article-section"><h2 class="article-h2" id="open"><span class="article-h2-num">3</span>開業に必要な準備</h2>
<p class="article-p">開業を考えるなら、宅建業免許、事務所要件、専任の宅建士、保証協会、帳簿・書類管理、広告規制、顧客対応の流れを確認します。</p>
<div class="highlight-box"><div class="highlight-box-title">開業前に確認すること</div><ul class="highlight-list">
<li class="highlight-item">宅建士登録と宅建士証の交付を済ませる。</li>
<li class="highlight-item">宅建業免許の要件と費用を確認する。</li>
<li class="highlight-item">保証協会加入や営業保証金の資金計画を作る。</li>
<li class="highlight-item">集客方法と得意分野を決める。</li>
</ul></div></section>
<section class="article-section"><h2 class="article-h2" id="risk"><span class="article-h2-num">4</span>独立前のリスク</h2>
<p class="article-p">不動産仲介は、契約金額が大きく、説明漏れや調査不足が大きなトラブルにつながります。資格知識だけでなく、実務経験と確認体制が重要です。</p>
<h3 class="article-h3">集客が最大の課題</h3><p class="article-p">免許や資格があっても、顧客がいなければ事業は成り立ちません。地域、物件種別、ターゲットを絞り、どう相談を得るかを考える必要があります。</p></section>
<section class="article-section"><h2 class="article-h2" id="roadmap"><span class="article-h2-num">5</span>現実的なロードマップ</h2>
<p class="article-p">まず宅建に合格し、不動産会社で実務を経験し、契約と調査の流れを身につけます。その後、得意分野と集客経路が見えてから副業・独立を検討すると失敗しにくくなります。</p>
<div class="cta-section"><div class="cta-title">独立前に基礎を固める</div><p class="cta-desc">宅建業法と重要事項説明の問題を復習し、実務の土台を作りましょう。</p><a class="cta-btn" href="/quiz/past/?field=law">過去問を解く</a></div></section>
""",
    },
    {
        "slug": "takken-chokuzen",
        "title": "宅建試験の直前対策｜1ヶ月・1週間・前日でやること",
        "short_title": "宅建試験の直前対策",
        "description": "宅建試験の直前期（1ヶ月・1週間・前日）にやるべきことを整理。過去問と間違いノートで得点を固める進め方を解説します。",
        "eyebrow": "宅建 直前対策",
        "lead": "直前期は落とした問題を減らすことが最優先です。宅建業法と法令上の制限を中心に、時間配分と見直し手順を固定しましょう。",
        "toc": [("month", "試験1ヶ月前"), ("week", "試験1週間前"), ("day", "試験前日"), ("avoid", "避けること"), ("check", "当日の確認")],
        "body": """
<section class="article-section"><h2 class="article-h2" id="month"><span class="article-h2-num">1</span>試験1ヶ月前</h2>
<p class="article-p">過去問を本番形式で解き、分野別の失点を記録します。権利関係の難問より、宅建業法・法令上の制限の取りこぼしを優先します。</p></section>
<section class="article-section"><h2 class="article-h2" id="week"><span class="article-h2-num">2</span>試験1週間前</h2>
<p class="article-p">新しいテキストは閉じ、間違いノートと数字の表だけを回します。</p></section>
<section class="article-section"><h2 class="article-h2" id="day"><span class="article-h2-num">3</span>試験前日</h2>
<p class="article-p">会場・交通・持ち物を確認し、長時間演習は避けます。</p></section>
<section class="article-section"><h2 class="article-h2" id="avoid"><span class="article-h2-num">4</span>避けること</h2>
<p class="article-p">未読の参考書の追加や徹夜での範囲拡大は得点につながりにくいです。</p></section>
<section class="article-section"><h2 class="article-h2" id="check"><span class="article-h2-num">5</span>当日の確認</h2>
<p class="article-p">マークの仕方と見直し順を紙上で一度シミュレーションします。</p>
<div class="cta-section"><div class="cta-title">過去問で手を慣らす</div><p class="cta-desc">最新年度から演習できます。</p><a class="cta-btn" href="/q/index.html">過去問一覧</a></div></section>
""",
    },
    {
        "slug": "takken-gokaku-ritsu",
        "title": "宅建の合格率は？年度別の傾向と合格ラインの読み方",
        "short_title": "宅建の合格率は？",
        "description": "宅建試験の合格率・合格ラインの読み方を解説。数字に一喜一憂せず、学習計画に活かす考え方をまとめます。",
        "eyebrow": "宅建 合格率",
        "lead": "合格率は参考指標です。自分が安定して取れる点数と、落としやすい分野を把握することが大切です。",
        "toc": [("rate", "合格率の見方"), ("line", "合格ライン"), ("use", "活かし方"), ("myth", "誤解"), ("next", "次にやること")],
        "body": """
<section class="article-section"><h2 class="article-h2" id="rate"><span class="article-h2-num">1</span>合格率の見方</h2>
<p class="article-p">受験者数や難易度で変動します。年度比較は取るべき問題を考える材料に留めます。</p></section>
<section class="article-section"><h2 class="article-h2" id="line"><span class="article-h2-num">2</span>合格ライン</h2>
<p class="article-p">学習中は36〜38点を安定して出す設計を目標にします。</p></section>
<section class="article-section"><h2 class="article-h2" id="use"><span class="article-h2-num">3</span>活かし方</h2>
<p class="article-p">模試の点数で次の2週間に直す分野を決めます。</p></section>
<section class="article-section"><h2 class="article-h2" id="myth"><span class="article-h2-num">4</span>誤解</h2>
<p class="article-p">合格率だけで勉強量を増減しないでください。</p></section>
<section class="article-section"><h2 class="article-h2" id="next"><span class="article-h2-num">5</span>次にやること</h2>
<p class="article-p">過去問に戻り、説明できる正解を増やします。</p>
<div class="cta-section"><div class="cta-title">過去問で確認</div><p class="cta-desc">年度別ページから演習できます。</p><a class="cta-btn" href="/q/index.html">過去問一覧</a></div></section>
""",
    },
    {
        "slug": "takken-shiken-schedule-2026",
        "title": "2026年度 宅建試験日程・申込み・合格発表スケジュール",
        "short_title": "2026年度 宅建試験日程",
        "description": "2026年度宅建試験の予定日程と学習計画への落とし込み方。公式情報の確認先も整理します。",
        "eyebrow": "宅建 2026年度",
        "lead": "試験日程はRETIOの公式サイトで最新情報を確認してください。本記事は学習カレンダー用の整理です。",
        "toc": [("schedule", "主な日程"), ("apply", "申込み"), ("study", "逆算"), ("official", "公式確認"), ("link", "関連")],
        "body": """
<section class="article-section"><h2 class="article-h2" id="schedule"><span class="article-h2-num">1</span>主な日程</h2>
<p class="article-p">実施公告・申込み・試験・合格発表は公式サイトで確認してください。</p>
<div class="warn-box"><span class="warn-box-label">重要：</span>締切・会場・受験票は必ず公式案内で確認してください。</div></section>
<section class="article-section"><h2 class="article-h2" id="apply"><span class="article-h2-num">2</span>申込み</h2>
<p class="article-p">最終日は混みやすいため早めの手続きが無難です。</p></section>
<section class="article-section"><h2 class="article-h2" id="study"><span class="article-h2-num">3</span>逆算</h2>
<p class="article-p">6ヶ月前なら週10時間、3ヶ月前なら週20時間前後が目安です。</p></section>
<section class="article-section"><h2 class="article-h2" id="official"><span class="article-h2-num">4</span>公式確認</h2>
<p class="article-p">RETIOの宅建試験ページで要項・過去問・合格発表を確認します。</p></section>
<section class="article-section"><h2 class="article-h2" id="link"><span class="article-h2-num">5</span>関連</h2>
<p class="article-p"><a href="../takken-moshikomi/index.html">申込みガイド</a>・<a href="../takken-toujitsu/index.html">当日の注意</a>も参照してください。</p>
<div class="cta-section"><div class="cta-title">試験ガイドへ</div><p class="cta-desc">分野別の勉強法も確認しましょう。</p><a class="cta-btn" href="/articles/">一覧</a></div></section>
""",
    },
]


def render_article(article: dict[str, object]) -> str:
    slug = str(article["slug"])
    title = str(article["title"])
    short_title = str(article["short_title"])
    description = str(article["description"])
    eyebrow = str(article["eyebrow"])
    lead = str(article["lead"])
    article_toc = [("trust", "この記事の信頼性について"), *article["toc"]]  # type: ignore[list-item]
    toc = "\n".join(f'<li><a href="#{target}">{label}</a></li>' for target, label in article_toc)
    body = str(article["body"]).strip()
    site_name = brand_name()
    mark = brand_mark()
    origin = clean_origin()
    url = f"{origin}/takken/{slug}/"
    sources = external_links()
    source_links = "、".join(
        f'<a href="{html.escape(item["url"], quote=True)}" target="_blank" rel="noopener noreferrer">{html.escape(item["label"])}</a>'
        for item in sources[:2]
    ) or "公式情報・関連法令"
    trust_block = f"""<section class="trust-section" id="trust">
<h2 class="article-h2">この記事の信頼性について</h2>
<div class="article-table-wrap"><table class="article-table trust-table"><tbody>
<tr><th scope="row">執筆者</th><td>{site_name}編集部</td></tr>
<tr><th scope="row">更新日</th><td>{UPDATED_LABEL}</td></tr>
<tr><th scope="row">主な参照元</th><td>{source_links}</td></tr>
</tbody></table></div>
</section>"""
    return f"""<!DOCTYPE html><html lang="ja"><head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0,maximum-scale=1.0">
<title>{title} - {site_name}</title>
<meta name="description" content="{description}">
<meta name="robots" content="index,follow"><link rel="canonical" href="{url}">
<meta name="color-scheme" content="light">
<meta property="og:type" content="article"><meta property="og:url" content="{url}">
<meta property="og:title" content="{title} - {site_name}"><meta property="og:description" content="{description}">
<meta property="og:locale" content="ja_JP"><meta property="og:site_name" content="{site_name}">
<meta name="twitter:card" content="summary">
<script type="application/ld+json">{{"@context":"https://schema.org","@type":"Article","headline":"{short_title}","description":"{description}","url":"{url}","publisher":{{"@type":"Organization","name":"{site_name}","url":"{origin}/"}}}}</script>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<style>{ARTICLE_CSS}</style></head>
<body><header><nav class="topnav"><div class="topnav-inner"><a class="logo" href="/"><div class="logo-mark">{mark}</div><span class="logo-text">{site_name}</span></a><div class="nav-links"><a class="nav-link" href="/quiz/orig/">オリジナル問題</a><a class="nav-link" href="/quiz/past/">過去問</a><a class="nav-link" href="/dashboard/">分析</a><a class="nav-link" href="/terms/">用語解説</a></div></div></nav></header>
<main><div class="article-wrap"><nav class="breadcrumb" aria-label="パンくず"><ol class="breadcrumb-list"><li><a href="/">{site_name}</a></li><li><a href="/articles/">試験ガイド</a></li><li aria-current="page">{short_title}</li></ol></nav><p class="article-eyebrow">{eyebrow}</p><h1 class="article-h1">{title}</h1><div class="article-meta"><span>{UPDATED_LABEL}</span><span>{site_name}編集部</span></div><p class="article-lead">{lead}</p><nav class="toc" aria-label="目次"><div class="toc-title">目次</div><ul class="toc-list">{toc}</ul></nav>{trust_block}{body}</div></main>
<footer class="site-footer"><div class="site-footer-inner"><a class="footer-logo" href="/"><div class="footer-logo-mark">{mark}</div><span class="footer-logo-text">{site_name}</span></a><nav class="footer-links"><a href="/">問題を解く</a><a href="/quiz/past/">過去問</a><a href="/terms/">用語解説</a><a href="/articles/">試験ガイド</a></nav><span class="footer-copy">2026 {site_name}</span></div></footer>
</body></html>
"""


def all_articles() -> list[dict]:
    seen: set[str] = set()
    out: list[dict] = []
    for article in [*ARTICLES, *BATCH_ARTICLES_10, *BATCH_ARTICLES_20]:
        slug = str(article["slug"])
        if slug in seen:
            continue
        seen.add(slug)
        out.append(article)
    return out


def main() -> None:
    for article in all_articles():
        slug = str(article["slug"])
        path = ROOT / "takken" / slug / "index.html"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(render_article(article), encoding="utf-8")
        print(path.relative_to(ROOT))


if __name__ == "__main__":
    main()
