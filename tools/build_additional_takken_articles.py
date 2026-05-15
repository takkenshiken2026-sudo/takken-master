#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""勉強計画まわりの宅建ガイド記事を生成する。"""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

ARTICLE_CSS = """*{box-sizing:border-box;margin:0;padding:0}html{background:#fff;min-height:100%;color-scheme:light}body{font-family:'Noto Sans JP',sans-serif;background:#fff;color:#111;-webkit-font-smoothing:antialiased;line-height:1.75;min-height:100vh;color-scheme:light}.topnav{position:sticky;top:0;z-index:30;background:#fff;border-bottom:1px solid rgba(0,0,0,.08)}.topnav-inner{max-width:900px;margin:0 auto;padding:0 20px;height:54px;display:flex;align-items:center}.logo{display:flex;align-items:center;gap:9px;text-decoration:none;color:#111;margin-right:auto}.logo-mark{width:28px;height:28px;border-radius:7px;background:#333;display:flex;align-items:center;justify-content:center;font-size:12px;font-weight:700;color:#fff}.logo-text{font-size:17px;font-weight:700}.nav-links{display:flex;align-items:center;gap:2px}.nav-link{padding:6px 12px;border-radius:6px;font-size:14px;color:#555;text-decoration:none;white-space:nowrap}.nav-link:hover{background:#efefef;color:#111}.article-wrap{max-width:760px;margin:0 auto;padding:40px 20px 96px;background:#fff}.breadcrumb{margin-bottom:24px}.breadcrumb-list{display:flex;align-items:center;flex-wrap:wrap;list-style:none}.breadcrumb-list li{display:flex;align-items:center;font-size:13px;color:#999}.breadcrumb-list li+li::before{content:'›';margin:0 6px}.breadcrumb-list a{color:#999;text-decoration:none}.breadcrumb-list a:hover{color:#555}.breadcrumb-list li[aria-current]{color:#555}.article-eyebrow{font-size:11px;font-weight:700;color:#888;letter-spacing:.12em;margin-bottom:12px}.article-h1{font-size:32px;font-weight:800;line-height:1.32;margin-bottom:16px;color:#111}.article-meta{display:flex;align-items:center;gap:16px;flex-wrap:wrap;font-size:13px;color:#999;margin-bottom:32px;padding-bottom:24px;border-bottom:1px solid #e0e0e0}.article-lead{font-size:16px;line-height:1.9;color:#333;margin-bottom:40px;padding:20px 24px;background:#fff;border:1px solid rgba(0,0,0,.1);border-radius:8px;box-shadow:0 1px 3px rgba(0,0,0,.06)}.toc{background:#fff;border:1px solid rgba(0,0,0,.1);border-radius:8px;padding:20px 24px;margin-bottom:40px}.toc-title{font-size:14px;font-weight:700;color:#555;margin-bottom:12px}.toc-list{list-style:none;display:flex;flex-direction:column;gap:7px}.toc-list a{font-size:14px;color:#333;text-decoration:none}.toc-list a:hover{text-decoration:underline}.article-section{margin-bottom:48px}.article-h2{font-size:22px;font-weight:800;margin-bottom:16px;padding-bottom:12px;border-bottom:2px solid #e0e0e0;color:#111;display:flex;align-items:center;gap:10px}.article-h2-num{width:28px;height:28px;background:#333;color:#fff;border-radius:6px;display:flex;align-items:center;justify-content:center;font-size:13px;font-weight:700;flex-shrink:0}.article-h3{font-size:17px;font-weight:700;margin:24px 0 10px;color:#111;padding-bottom:6px;border-bottom:1px solid #e0e0e0}.article-p{font-size:15px;line-height:1.9;color:#333;margin-bottom:16px}.article-table-wrap{overflow-x:auto;margin:16px 0}.article-table{width:100%;border-collapse:collapse;font-size:14px;min-width:480px}.article-table th{background:#f0f0f0;padding:10px 12px;text-align:left;font-weight:700;border:1px solid #ddd}.article-table td{padding:10px 12px;border:1px solid #ddd;vertical-align:top}.article-table tr:nth-child(even) td{background:#fafafa}.highlight-box{background:#fff;border:1px solid rgba(0,0,0,.1);border-radius:8px;padding:20px 24px;margin:20px 0;box-shadow:0 1px 3px rgba(0,0,0,.06)}.highlight-box-title{font-size:13px;font-weight:700;color:#555;margin-bottom:10px}.highlight-list{list-style:none;display:flex;flex-direction:column;gap:8px}.highlight-item{display:flex;align-items:flex-start;gap:10px;font-size:14px;line-height:1.7;color:#333}.highlight-item::before{content:'−';color:#333;font-weight:700;flex-shrink:0;margin-top:1px}.warn-box,.point-box{border:1px solid #ddd;border-radius:8px;padding:14px 18px;margin:16px 0;font-size:14px;line-height:1.7;color:#333}.warn-box{background:#f9f9f9}.point-box{background:#f5f5f5}.warn-box-label,.point-box-label{font-weight:700;color:#333;margin-right:6px}.cta-section{background:#111;color:#fff;border-radius:10px;padding:28px 32px;text-align:center;margin:48px 0 0}.cta-title{font-size:20px;font-weight:800;margin-bottom:8px}.cta-desc{font-size:14px;color:#bbb;margin-bottom:20px;line-height:1.7}.cta-btn{display:inline-flex;align-items:center;gap:8px;padding:12px 28px;background:#f5f5f5;color:#111;border:1px solid #ddd;border-radius:8px;font-size:15px;font-weight:700;text-decoration:none}.site-footer{border-top:1px solid rgba(0,0,0,.08);background:#fff;padding:14px 20px}.site-footer-inner{max-width:900px;margin:0 auto;display:flex;align-items:center;gap:20px;flex-wrap:wrap}.footer-logo{display:flex;align-items:center;gap:7px;text-decoration:none;color:#111}.footer-logo-mark{width:22px;height:22px;border-radius:5px;background:#333;display:flex;align-items:center;justify-content:center;font-size:10px;font-weight:700;color:#fff}.footer-logo-text{font-size:13px;font-weight:700}.footer-links{display:flex;gap:20px;flex-wrap:wrap}.footer-links a{font-size:13px;color:#999;text-decoration:none}.footer-copy{font-size:12px;color:#999;margin-left:auto}@media(max-width:640px){.article-wrap{padding-top:28px}.article-h1{font-size:24px}.article-h2{font-size:18px}.nav-links{display:none}.cta-section{padding:24px 20px}}@media(prefers-color-scheme:dark){html,body,.article-wrap{background:#fff!important;color:#111!important}}"""

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
]


def render_article(article: dict[str, object]) -> str:
    slug = str(article["slug"])
    title = str(article["title"])
    short_title = str(article["short_title"])
    description = str(article["description"])
    eyebrow = str(article["eyebrow"])
    lead = str(article["lead"])
    toc = "\n".join(
        f'<li><a href="#{target}">{label}</a></li>'
        for target, label in article["toc"]  # type: ignore[index]
    )
    body = str(article["body"]).strip()
    url = f"https://takken-master.jp/takken/{slug}/"
    return f"""<!DOCTYPE html><html lang="ja"><head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0,maximum-scale=1.0">
<title>{title} - 宅建マスター</title>
<meta name="description" content="{description}">
<meta name="robots" content="index,follow"><link rel="canonical" href="{url}">
<meta name="color-scheme" content="light">
<meta property="og:type" content="article"><meta property="og:url" content="{url}">
<meta property="og:title" content="{title} - 宅建マスター"><meta property="og:description" content="{description}">
<meta property="og:locale" content="ja_JP"><meta property="og:site_name" content="宅建マスター">
<meta name="twitter:card" content="summary">
<script type="application/ld+json">{{"@context":"https://schema.org","@type":"Article","headline":"{short_title}","description":"{description}","url":"{url}","publisher":{{"@type":"Organization","name":"宅建マスター","url":"https://takken-master.jp/"}}}}</script>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<style>{ARTICLE_CSS}</style></head>
<body><header><nav class="topnav"><div class="topnav-inner"><a class="logo" href="/"><div class="logo-mark">宅建</div><span class="logo-text">宅建マスター</span></a><div class="nav-links"><a class="nav-link" href="/quiz/orig/">オリジナル問題</a><a class="nav-link" href="/quiz/past/">過去問</a><a class="nav-link" href="/dashboard/">分析</a><a class="nav-link" href="/terms/">用語解説</a></div></div></nav></header>
<main><div class="article-wrap"><nav class="breadcrumb" aria-label="パンくず"><ol class="breadcrumb-list"><li><a href="/">宅建マスター</a></li><li><a href="/articles/">試験ガイド</a></li><li aria-current="page">{short_title}</li></ol></nav><p class="article-eyebrow">{eyebrow}</p><h1 class="article-h1">{title}</h1><div class="article-meta"><span>2026年5月</span><span>宅建マスター編集部</span></div><p class="article-lead">{lead}</p><nav class="toc"><div class="toc-title">この記事の目次</div><ul class="toc-list">{toc}</ul></nav>{body}</div></main>
<footer class="site-footer"><div class="site-footer-inner"><a class="footer-logo" href="/"><div class="footer-logo-mark">宅建</div><span class="footer-logo-text">宅建マスター</span></a><nav class="footer-links"><a href="/">問題を解く</a><a href="/quiz/past/">過去問</a><a href="/terms/">用語解説</a><a href="/articles/">試験ガイド</a></nav><span class="footer-copy">2026 宅建マスター</span></div></footer>
</body></html>
"""


def main() -> None:
    for article in ARTICLES:
        slug = str(article["slug"])
        path = ROOT / "takken" / slug / "index.html"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(render_article(article), encoding="utf-8")
        print(path.relative_to(ROOT))


if __name__ == "__main__":
    main()
