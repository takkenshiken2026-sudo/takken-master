/* takken-data-glossary.js — GLOSSARY データのみ（UI は index.html 側）
 * articleSlug … 公開サイト https://takken-master.jp/glossary/{slug}/ と対応。
 * 一覧は takken-master-seo/glossary/index.html（170テーマ）と同期。詳細本文・図解がある項目は下記にそのまま保持。
 */

// ===== GLOSSARY =====
const GLOSSARY_DATA = [
  {
    "id": "ishihyoji",
    "cat": "rights",
    "term": "意思表示",
    "reading": "いしひょうじ",
    "summary": "意思表示の概要",
    "desc": "契約や遺言など、一定の法律効果を発生させたい意思を、相手方が認識できるように外部に表すことです。取消し・追認・説明義務などとセットで宅建でも頻出です。",
    "articleSlug": "ishihyoji"
  },
  {
    "id": "dairi",
    "cat": "rights",
    "term": "代理",
    "reading": "だいり",
    "summary": "本人の代わりに法律行為をする制度",
    "desc": "代理人が本人の名前で相手方と契約すると、その効果が直接本人に帰属する。「顕名（けんめい）」つまり「本人の代理として」と示すことが必要。任意代理（本人が選ぶ）と法定代理（未成年の親権者など）がある。無権代理（代理権がない）の場合、本人が追認しない限り本人に効果は帰属しない。",
    "diagram": {
      "type": "flow",
      "steps": [
        "本人がCに代理権を授与",
        "CがAの代理人としてBと契約（顕名）",
        "契約の効果がAに帰属"
      ]
    },
    "articleSlug": "dairi"
  },
  {
    "id": "seigen",
    "cat": "rights",
    "term": "制限行為能力者",
    "reading": "せいげんこういのうりょくしゃ",
    "summary": "制限行為能力者の概要",
    "desc": "未成年者や成年被後見人など、単独では有効な法律行為が制限される場合がある地位にある人をいいます。保護者の同意・取消しや消費者契約の特例が試験で問われます。",
    "articleSlug": "seigen"
  },
  {
    "id": "jiko",
    "cat": "rights",
    "term": "時効",
    "reading": "じこう",
    "summary": "一定期間が経つと権利が変動する制度",
    "desc": "①取得時効：他人の物を一定期間占有し続けると自分のものになる（善意・無過失なら10年、それ以外は20年）。②消滅時効：権利を使わないでいると権利が消える（債権は知った時から5年・客観的に行使できる時から10年）。時効の援用（「時効を使います」の意思表示）があってはじめて効力が生じる。",
    "diagram": {
      "type": "flow",
      "steps": [
        "占有/権利不行使の開始",
        "時効期間が経過（10年・5年等）",
        "時効完成",
        "援用（意思表示）",
        "権利変動確定"
      ]
    },
    "articleSlug": "jiko"
  },
  {
    "id": "bukken_hendo",
    "cat": "rights",
    "term": "物権変動",
    "reading": "ぶっけんへんどう",
    "summary": "物権変動の概要",
    "desc": "所有権・抵当権などの物権が、誰から誰へ、いつ移転するかという問題です。不動産では原則として登記が対抗要件となり、第三者との関係がポイントになります。",
    "articleSlug": "bukken-hendo"
  },
  {
    "id": "kyoyu",
    "cat": "rights",
    "term": "共有",
    "reading": "きょうゆう",
    "summary": "共有の概要",
    "desc": "複数人が一つの不動産や権利を共同で持つ形態です。持分割合（持分）や共有物の分割・優先承認などが頻出論点です。",
    "articleSlug": "kyoyu"
  },
  {
    "id": "teito",
    "cat": "rights",
    "term": "抵当権",
    "reading": "ていとうけん",
    "summary": "占有を移さずに不動産を担保にする権利",
    "desc": "お金を貸した人（抵当権者）が、借りた人（設定者）の不動産に設定する担保権。設定者は住み続けながら担保に入れられる（非占有担保）。返済できなければ競売にかけて優先的に弁済を受けられる。登記が対抗要件（当事者間では登記なくても成立）。",
    "diagram": {
      "type": "compare",
      "left": {
        "title": "抵当権",
        "items": [
          "占有を移さない（住み続けられる）",
          "登記が対抗要件",
          "競売で優先弁済を受ける",
          "土地・建物どちらにも設定可"
        ]
      },
      "right": {
        "title": "質権",
        "items": [
          "占有を移す（物を渡す）",
          "不動産でも動産でも設定可",
          "収益も取れる（用益質）",
          "留置的効力あり"
        ]
      }
    },
    "articleSlug": "teito"
  },
  {
    "id": "shichi_sakidori",
    "cat": "rights",
    "term": "質権・先取特権・留置権",
    "reading": "しちけん・さきどりとっけん",
    "summary": "質権・先取特権・留置権の概要",
    "desc": "質権は目的物を預けて担保とする権利、先取特権は法律が順位を定める優先権、留置権は報酬未払いのとき仕事の成果物を留置できる権利です。それぞれ成立要件が異なります。",
    "articleSlug": "shichi-sakidori"
  },
  {
    "id": "chijo_chiekiken",
    "cat": "rights",
    "term": "地上権・地役権",
    "reading": "ちじょうけん・ちえきけん",
    "summary": "地上権・地役権の概要",
    "desc": "地上権は他人の土地に建物等を所有するための使用収益権、地役権は通行や眺望確保など隣地の便宜のために他人の土地を使う権利です。",
    "articleSlug": "chijo-chiekiken"
  },
  {
    "id": "chintaiborrow",
    "cat": "rights",
    "term": "賃貸借",
    "reading": "ちんたいしゃく",
    "summary": "賃貸借の概要",
    "desc": "賃貸人が建物や土地を目的物として貸し、賃借人が賃料を払って使用収益する契約の総称です。定期借地・借家や更新・原状回復がセットで学習します。",
    "articleSlug": "chintaiborrow"
  },
  {
    "id": "shakuchi",
    "cat": "rights",
    "term": "借地借家法",
    "reading": "しゃくちしゃっかほう",
    "summary": "借地借家法の概要",
    "desc": "建物賃貸借や土地賃借を対象に、更新・解約・費用負担・残置物など当事者の利害を調整する法律です。宅建業の実務とも直結します。",
    "articleSlug": "shakuchi"
  },
  {
    "id": "houtei_koshin",
    "cat": "rights",
    "term": "法定更新",
    "reading": "ほうていこうしん",
    "summary": "法定更新の概要",
    "desc": "借地・借家で契約期間が満了しても、法定の要件を満たすと同じ条件で契約が続く仕組みです。更新料や再賃借人への対抗力が論点になります。",
    "articleSlug": "houtei-koshin"
  },
  {
    "id": "shikikin_reikin",
    "cat": "rights",
    "term": "敷金・礼金",
    "reading": "しききん・れいきん",
    "summary": "敷金・礼金の概要",
    "desc": "敷金は原則として退去時に返還を受ける預り金、礼金は契約成立時に渡す金銭で性格が異なります。償却・精算の考え方が試験で問われます。",
    "articleSlug": "shikikin-reikin"
  },
  {
    "id": "tentaishaku",
    "cat": "rights",
    "term": "転貸借",
    "reading": "てんたいしゃく",
    "summary": "転貸借の概要",
    "desc": "賃借人が貸主の承諾を得て、さらに第三者に賃貸目的物を転貸する関係です。原賃貸借との効力関係がポイントです。",
    "articleSlug": "tentaishaku"
  },
  {
    "id": "zosaku_kaitori",
    "cat": "rights",
    "term": "造作買取請求権",
    "reading": "ぞうさくかいとりせいきゅうけん",
    "summary": "造作買取請求権の概要",
    "desc": "借地権が消滅するとき、借地人が土地に付した建物などの造作について、買い取ってほしいと請求できる権利です。",
    "articleSlug": "zosaku-kaitori"
  },
  {
    "id": "chinryo_zogen",
    "cat": "rights",
    "term": "賃料増減額請求",
    "reading": "ちんりょうぞうげんがくせいきゅう",
    "summary": "賃料増減額請求の概要",
    "desc": "周辺の地代・家賃の推移などに照らし、賃料の増減を裁判所に請求できる制度です。要件と手続のイメージが問われます。",
    "articleSlug": "chinryo-zogen"
  },
  {
    "id": "karite_hogo",
    "cat": "rights",
    "term": "借主の保護規定",
    "reading": "かりてほごきてい",
    "summary": "借主の保護規定の概要",
    "desc": "借家人を弱い当事者として、貸主の解約・更新拒絶や立ち退きを制限する借地借家法上の規定の総称です。",
    "articleSlug": "karite-hogo"
  },
  {
    "id": "souzoku",
    "cat": "rights",
    "term": "相続分と代襲相続",
    "reading": "そうぞくぶんとだいしゅうそうぞく",
    "summary": "遺産を誰がどれだけ受け取るか",
    "desc": "法定相続分：配偶者＋子なら配偶者1/2・子全体で1/2。子が先に死亡していて孫がいれば、孫が子の代わりに相続（代襲相続）。相続放棄した人の子は代襲できない（放棄すると最初から相続人でなかったことになる）。遺留分（最低限の相続分）を侵害されたら金銭請求できる。",
    "diagram": {
      "type": "table",
      "head": [
        "相続人の組合せ",
        "配偶者",
        "その他"
      ],
      "rows": [
        [
          "配偶者＋子",
          "1/2",
          "子全体で1/2"
        ],
        [
          "配偶者＋父母等",
          "2/3",
          "父母等で1/3"
        ],
        [
          "配偶者＋兄弟姉妹",
          "3/4",
          "兄弟姉妹で1/4"
        ],
        [
          "配偶者のみ",
          "全部",
          "—"
        ],
        [
          "子のみ",
          "—",
          "全部"
        ]
      ]
    },
    "articleSlug": "souzoku"
  },
  {
    "id": "isan_bunkatsu",
    "cat": "rights",
    "term": "遺産分割",
    "reading": "いさんぶんかつ",
    "summary": "遺産分割の概要",
    "desc": "相続が開始した後、共同相続人が遺産をどのように分けるか決める手続です。遺言や協議・調停・審判が試験で頻出です。",
    "articleSlug": "isan-bunkatsu"
  },
  {
    "id": "hosho_debt",
    "cat": "rights",
    "term": "保証と連帯保証",
    "reading": "ほしょうとれんたいほしょう",
    "summary": "保証と連帯保証の概要",
    "desc": "保証人は主たる債務者に履行を催告できる抗弁がある場合がありますが、連帯保証人は催告・検索の抗弁がなく責任が重いです。",
    "articleSlug": "hosho-debt"
  },
  {
    "id": "renzai",
    "cat": "rights",
    "term": "連帯保証",
    "reading": "れんたいほしょう",
    "summary": "通常の保証より責任が重い保証形態",
    "desc": "連帯保証人には「催告の抗弁権（まず主債務者に請求してください）」と「検索の抗弁権（主債務者に財産があります）」がない。つまり債権者はいきなり連帯保証人に全額請求できる。一方、通常の保証人にはこれらの権利がある。アパートの入居で保証人になる際はほぼ連帯保証。",
    "diagram": {
      "type": "table",
      "head": [
        "権利",
        "普通保証",
        "連帯保証"
      ],
      "rows": [
        [
          "催告の抗弁権",
          "あり（主債務者へ先に請求しては）",
          "なし"
        ],
        [
          "検索の抗弁権",
          "あり（主債務者に財産がある）",
          "なし"
        ],
        [
          "分別の利益",
          "あり（複数保証人で割り勘）",
          "なし"
        ],
        [
          "直接請求",
          "催告後",
          "いきなりOK"
        ]
      ]
    },
    "articleSlug": "hosho-debt"
  },
  {
    "id": "saimu_furikoh",
    "cat": "rights",
    "term": "債務不履行",
    "reading": "さいむふりこう",
    "summary": "債務不履行の概要",
    "desc": "約束した給付が期限までに行われないことです。催告・解除・損害賠償とセットで理解します。",
    "articleSlug": "saimu-furikoh"
  },
  {
    "id": "futekigo",
    "cat": "rights",
    "term": "契約不適合責任",
    "reading": "けいやくふてきごうせきにん",
    "summary": "契約不適合責任の概要",
    "desc": "目的物に契約内容どおりの品質・性能がないときに、修補・代金減額・損害賠償などを請求できる責任です（民法上の体系）。",
    "articleSlug": "futekigo"
  },
  {
    "id": "fuhoto",
    "cat": "rights",
    "term": "不法行為",
    "reading": "ふほうこうい",
    "summary": "不法行為の概要",
    "desc": "他人の生命・身体・財産を侵害した場合に、故意・過失に基づき損害を賠償する責任です。近隣トラブルや説明不足とも関連します。",
    "articleSlug": "fuhoto"
  },
  {
    "id": "baibai_keiyaku",
    "cat": "rights",
    "term": "売買契約",
    "reading": "ばいばいけいやく",
    "summary": "売買契約の概要",
    "desc": "売主が目的物の所有権を移転し、買主が代金を支払う契約です。危険負担・解除・手付などが宅建の中心論点です。",
    "articleSlug": "baibai-keiyaku"
  },
  {
    "id": "ukeoi_inin",
    "cat": "rights",
    "term": "請負・委任",
    "reading": "うけおい・いにん",
    "summary": "請負・委任の概要",
    "desc": "請負は成果完成を目的とする契約、委任は事務の処理を委ねる契約です。不完全履行や報酬の発生時期の考え方が異なります。",
    "articleSlug": "ukeoi-inin"
  },
  {
    "id": "bensai_sousai",
    "cat": "rights",
    "term": "弁済・相殺",
    "reading": "べんさい・そうさい",
    "summary": "弁済・相殺の概要",
    "desc": "弁済は債務を目的どおりに消滅させること、相殺は互いに反対債権があるときに差し引いて消滅させることです。",
    "articleSlug": "bensai-sousai"
  },
  {
    "id": "joken_kigen",
    "cat": "rights",
    "term": "条件・期限",
    "reading": "じょうけん・きげん",
    "summary": "条件・期限の概要",
    "desc": "条件は将来不確定の事実によって効力が左右され、期限は確実に来る時点で効力が生じます。停止・解除条件が頻出です。",
    "articleSlug": "joken-kigen"
  },
  {
    "id": "sorin_kankei",
    "cat": "rights",
    "term": "相隣関係",
    "reading": "そうりんかんけい",
    "summary": "相隣関係の概要",
    "desc": "隣地との境界・日照・通行・樹枝など、土地と土地の接する関係をめぐる民法の規定です。",
    "articleSlug": "sorin-kankei"
  },
  {
    "id": "kubun_shoyuken",
    "cat": "rights",
    "term": "区分所有権",
    "reading": "くぶんしょゆうけん",
    "summary": "区分所有権の概要",
    "desc": "マンションの専有部分の所有と共用部分の共有持分、管理組合などを規律する制度です。",
    "articleSlug": "kubun-shoyuken"
  },
  {
    "id": "sashiosae_kyosei",
    "cat": "rights",
    "term": "差押え・強制執行",
    "reading": "さしおさえ・きょうせいしっこう",
    "summary": "差押え・強制執行の概要",
    "desc": "金銭債権を実行するため、債務者の財産を差し押さえたうえで換金する強制執行の流れを理解します。",
    "articleSlug": "sashiosae-kyosei"
  },
  {
    "id": "touki",
    "cat": "rights",
    "term": "不動産登記",
    "reading": "ふどうさんとうき",
    "summary": "不動産登記の概要",
    "desc": "不動産の物理的・法的状況を公示する制度です。第三者への対抗要件として登記が極めて重要です。",
    "articleSlug": "touki"
  },
  {
    "id": "buken",
    "cat": "rights",
    "term": "物権と債権",
    "reading": "ぶっけんとさいけん",
    "summary": "権利の性質の違い",
    "desc": "物権は「物に対する権利」で、誰に対しても主張できる（絶対性）。債権は「特定の人に何かを請求する権利」で、その人にしか主張できない。例えば土地の所有権（物権）は誰にでも「私の土地です」と言えるが、賃借権（債権）は原則として貸主にしか使えない。",
    "diagram": {
      "type": "compare",
      "left": {
        "title": "物権",
        "items": [
          "誰にでも主張できる（絶対性）",
          "種類は法律で限定（物権法定主義）",
          "登記で対抗力を持つ",
          "例：所有権・抵当権・地上権"
        ]
      },
      "right": {
        "title": "債権",
        "items": [
          "特定の相手にのみ主張できる",
          "当事者が自由に設定できる",
          "登記原則不要（賃借権は例外あり）",
          "例：売買代金請求権・賃料請求権"
        ]
      }
    },
    "articleSlug": "bukken-saiken"
  },
  {
    "id": "mukohitokechi",
    "cat": "rights",
    "term": "無効と取消し",
    "reading": "むこうととりけし",
    "summary": "契約の効力を否定する2つの方法",
    "desc": "無効：最初から効力がない（通謀虚偽表示、公序良俗違反など）。追認しても有効にならない。取消し：一応有効だが、後から取り消せる（詐欺・強迫・錯誤・制限行為能力など）。取消しは取消権者が行使して初めて遡及的に無効になる。取消し後は追認できない。",
    "diagram": {
      "type": "table",
      "head": [
        "項目",
        "無効",
        "取消し"
      ],
      "rows": [
        [
          "効力",
          "最初からない",
          "一応有効、遡及的無効"
        ],
        [
          "誰でも主張可?",
          "原則○",
          "取消権者のみ"
        ],
        [
          "追認",
          "不可",
          "可（確定的に有効になる）"
        ],
        [
          "時効",
          "消えない",
          "取消権は5年/20年で消滅"
        ],
        [
          "例",
          "通謀虚偽表示・公序良俗違反",
          "詐欺・強迫・錯誤・制限行為能力"
        ]
      ]
    },
    "articleSlug": "muko-torikeshi"
  },
  {
    "id": "hoteichijoken",
    "cat": "rights",
    "term": "法定地上権",
    "reading": "ほうていちじょうけん",
    "summary": "競売後に建物所有者が土地を使う権利",
    "desc": "土地に抵当権を設定した時に建物が存在し、競売で土地と建物の所有者が別々になった場合、建物の所有者が土地を使える「地上権」が自動的（法定）に発生する。そうしないと建物を取り壊さなければならなくなるため。成立要件：①設定時に建物が存在、②土地・建物が同一所有者、③競売で所有者が分離。",
    "diagram": {
      "type": "flow",
      "steps": [
        "Aが甲土地に抵当権設定（建物あり）",
        "AがBから借金返済できず",
        "競売でCが土地取得、Aが建物を保持",
        "法定地上権が自動成立（Aが建物を使い続けられる）"
      ]
    },
    "articleSlug": "hoteichijoken"
  },
  {
    "id": "kenri_nouryoku",
    "cat": "rights",
    "term": "権利能力",
    "reading": "けんりのうりょく",
    "summary": "権利能力の概要",
    "desc": "権利義務の主体となる法律上の地位です。原則として自然人・法人は出生・成立から権利能力を有します。",
    "articleSlug": "kenri-nouryoku"
  },
  {
    "id": "koui_nouryoku",
    "cat": "rights",
    "term": "行為能力",
    "reading": "こういのうりょく",
    "summary": "行為能力の概要",
    "desc": "単独で有効な法律行為ができるかどうかの能力です。成年・未成年・後見などとセットで学習します。",
    "articleSlug": "koui-nouryoku"
  },
  {
    "id": "hyogen_dairi",
    "cat": "rights",
    "term": "表見代理",
    "reading": "ひょうげんだいり",
    "summary": "表見代理の概要",
    "desc": "代理権はなくても、本人に代理権があると信じさせる外観があるときに本人に効果を帰せる制度です。",
    "articleSlug": "hyogen-dairi"
  },
  {
    "id": "jiko_jiko_dairi",
    "cat": "rights",
    "term": "自己契約・双方代理",
    "reading": "じこけいやく・そうほうだいり",
    "summary": "自己契約・双方代理の概要",
    "desc": "代理人が同一の双方代理となり、または本人と契約する場合に利益相反となり得るため原則禁止されます。",
    "articleSlug": "jiko-jiko-dairi"
  },
  {
    "id": "konkyo_houtei",
    "cat": "rights",
    "term": "混同",
    "reading": "こんどう",
    "summary": "混同の概要",
    "desc": "債権と債務が同一人に帰属したときに債権が消滅することです。混同によって担保権も消える場合があります。",
    "articleSlug": "konkyo-houtei"
  },
  {
    "id": "menjo",
    "cat": "rights",
    "term": "免除",
    "reading": "めんじょ",
    "summary": "免除の概要",
    "desc": "債権者が債務者に債務を免除する意思表示をすることで債務が消滅します。",
    "articleSlug": "menjo"
  },
  {
    "id": "koukai",
    "cat": "rights",
    "term": "更改",
    "reading": "こうかい",
    "summary": "更改の概要",
    "desc": "既存の債権を消滅させずに新たな債権を成立させる契約です。旧債務との関係が論点になります。",
    "articleSlug": "koukai"
  },
  {
    "id": "nedan_no_shitsugi",
    "cat": "rights",
    "term": "錯誤",
    "reading": "しつぎ",
    "summary": "錯誤の概要",
    "desc": "意思表示の内容について錯誤があった場合に、その意思表示を取り消せることがあります。動機の錯誤との区別がポイントです。",
    "articleSlug": "nedan-no-shitsugi"
  },
  {
    "id": "sagi_kyoho",
    "cat": "rights",
    "term": "詐欺・強迫",
    "reading": "さぎ・きょうはく",
    "summary": "詐欺・強迫の概要",
    "desc": "意思を屈服させる不正な行為による意思表示は取消しが可能になる場合があります。",
    "articleSlug": "sagi-kyoho"
  },
  {
    "id": "nekon_teito",
    "cat": "rights",
    "term": "根抵当権",
    "reading": "ねていとうけん",
    "summary": "根抵当権の概要",
    "desc": "一定の範囲の金銭債権を担保するため、極度額を定めて設定する抵当権です。継続的な融資取引で使われます。",
    "articleSlug": "nekon-teito"
  },
  {
    "id": "teito_junni",
    "cat": "rights",
    "term": "抵当権の順位",
    "reading": "ていとうけんのじゅんい",
    "summary": "抵当権の順位の概要",
    "desc": "同一不動産に複数の抵当権があるとき、登記の先後などにより受け取り順位が決まります。",
    "articleSlug": "teito-junni"
  },
  {
    "id": "teito_jikko",
    "cat": "rights",
    "term": "抵当権の実行",
    "reading": "ていとうけんのじっこう",
    "summary": "抵当権の実行の概要",
    "desc": "担保権実行として競売を申し立て、売得金から優先弁済を受ける手続です。",
    "articleSlug": "teito-jikko"
  },
  {
    "id": "kyodo_teito",
    "cat": "rights",
    "term": "共同抵当",
    "reading": "きょうどうていとう",
    "summary": "共同抵当の概要",
    "desc": "一つの債権を担保するため、複数の不動産に一体として抵当権を設定する形態です。",
    "articleSlug": "kyodo-teito"
  },
  {
    "id": "kaimodshi",
    "cat": "rights",
    "term": "買戻し",
    "reading": "かいもどし",
    "summary": "買戻しの概要",
    "desc": "売買に付された条件で、売主が一定期間内に買い戻せる特約です。登記の要否などが試験で問われます。",
    "articleSlug": "kaimodshi"
  },
  {
    "id": "shikibukken",
    "cat": "rights",
    "term": "敷地権",
    "reading": "しきちけん",
    "summary": "敷地権の概要",
    "desc": "区分所有建物と一体化した土地の利用権で、建物の処分と一体で譲り渡す必要があります。",
    "articleSlug": "shikibukken"
  },
  {
    "id": "shakuchiken_itiji",
    "cat": "rights",
    "term": "借地権の一体譲渡",
    "reading": "しゃくちけんのいったいじょうと",
    "summary": "借地権の一体譲渡の概要",
    "desc": "土地の上に建物を所有するための借地権を、建物と不可分にして譲渡することです。",
    "articleSlug": "shakuchiken-itiji"
  },
  {
    "id": "teiki_chintaishaku",
    "cat": "rights",
    "term": "定期借地権・定期借家権",
    "reading": "ていきしゃくちけん・ていきちんたいけん",
    "summary": "定期借地権・定期借家権の概要",
    "desc": "存続期間が当初から定められ、更新がなく原則として期間満了で終了する借地・借家権です。",
    "articleSlug": "teiki-chintaishaku"
  },
  {
    "id": "koshin_kyozetsu_jiyuu",
    "cat": "rights",
    "term": "更新拒絶の正当な事由",
    "reading": "こうしんきょぜつのせいとうなじゆう",
    "summary": "更新拒絶の正当な事由の概要",
    "desc": "貸主が借地・借家の更新を拒みうる場合として法律が限定列挙している正当な事由です。",
    "articleSlug": "koshin-kyozetsu-jiyuu"
  },
  {
    "id": "shuzai_ninyou",
    "cat": "rights",
    "term": "収去義務",
    "reading": "しゅうきょぎむ",
    "summary": "収去義務の概要",
    "desc": "賃借権が消滅した後、借主が地上物や附属物をどう処理するかについての義務です。",
    "articleSlug": "shuzai-ninyou"
  },
  {
    "id": "kyodo_shoyuu_bunkatsu",
    "cat": "rights",
    "term": "共有物の分割",
    "reading": "きょうゆうぶつのぶんかつ",
    "summary": "共有物の分割の概要",
    "desc": "共有物を共有者間で実際に分けることです。協議・裁判による分割などが論点です。",
    "articleSlug": "kyodo-shoyuu-bunkatsu"
  },
  {
    "id": "shikibun",
    "cat": "rights",
    "term": "持分",
    "reading": "しきぶん",
    "summary": "持分の概要",
    "desc": "共有持分の割合です。売却・優先買取・抵当権設定などの計算の基礎になります。",
    "articleSlug": "shikibun"
  },
  {
    "id": "yuusen_jounin",
    "cat": "rights",
    "term": "優先承認権",
    "reading": "ゆうせんじょうにんけん",
    "summary": "優先承認権の概要",
    "desc": "共有人が持分を第三者に売却するとき、他の共有人が同等条件で買い受ける権利です。",
    "articleSlug": "yuusen-jounin"
  },
  {
    "id": "ryouchi_toku",
    "cat": "rights",
    "term": "留置的効力",
    "reading": "りゅうちてきこうりょく",
    "summary": "留置的効力の概要",
    "desc": "抵当権者が抵当物を占有しないにもかかわらず、質権のような留置効果を認める場合がある考え方です。",
    "articleSlug": "ryouchi-toku"
  },
  {
    "id": "shuppatsu_jiko",
    "cat": "rights",
    "term": "取得時効",
    "reading": "しゅとくじこう",
    "summary": "取得時効の概要",
    "desc": "一定期間他人の物を平穏に占有し続けることで、その所有権を取得する時効です。",
    "articleSlug": "shuppatsu-jiko"
  },
  {
    "id": "shoumetsu_jiko",
    "cat": "rights",
    "term": "消滅時効",
    "reading": "しょうめつじこう",
    "summary": "消滅時効の概要",
    "desc": "権利を行使しないことが続くと権利が消滅する時効です。債権や解除権などで期間が異なります。",
    "articleSlug": "shoumetsu-jiko"
  },
  {
    "id": "iyaku_kin",
    "cat": "rights",
    "term": "違約金",
    "reading": "いやくきん",
    "summary": "違約金の概要",
    "desc": "債務不履行時に事前に定めたペナルティの額です。過高な場合の減額請求が問題になります。",
    "articleSlug": "iyaku-kin"
  },
  {
    "id": "insonkin",
    "cat": "rights",
    "term": "慰謝料",
    "reading": "いしゃりょう",
    "summary": "慰謝料の概要",
    "desc": "精神的苦痛に対する金銭賠償です。不法行為や債務不履行とともに頻出です。",
    "articleSlug": "insonkin"
  },
  {
    "id": "ryuuchi_seinin",
    "cat": "rights",
    "term": "履行遅滞による解除",
    "reading": "りょうちいたいによるかいじょ",
    "summary": "履行遅滞による解除の概要",
    "desc": "履行の催告をしても履行がないときに契約を解除できる場合があります。",
    "articleSlug": "ryuuchi-seinin"
  },
  {
    "id": "seigen_kaburan",
    "cat": "rights",
    "term": "制限行為能力者の保護",
    "reading": "せいげんこういのうりょくしゃのほご",
    "summary": "制限行為能力者の保護の概要",
    "desc": "未成年者などの法律行為を取り消した場合の相手方保護や原状回復などの規定です。",
    "articleSlug": "seigen-kaburan"
  },
  {
    "id": "zengo_kashitsu",
    "cat": "rights",
    "term": "履行補助者の故意過失",
    "reading": "りょうこほじょしゃのこいかしつ",
    "summary": "履行補助者の故意過失の概要",
    "desc": "代理人や履行補助者の故意過失が債務不履行の原因となったときの本人の責任です。",
    "articleSlug": "zengo-kashitsu"
  },
  {
    "id": "iryuubun",
    "cat": "rights",
    "term": "遺留分",
    "reading": "いりゅうぶん",
    "summary": "遺留分の概要",
    "desc": "一定の相続人が最低限確保されるべき相続分を侵害されたときに金銭請求できる制度です。",
    "articleSlug": "iryuubun"
  },
  {
    "id": "tokuyaku_seigen",
    "cat": "rights",
    "term": "消費者契約における特約の制限",
    "reading": "とくやくのせいげん",
    "summary": "消費者契約における特約の制限の概要",
    "desc": "消費者と事業者の契約で、不当に不利な免責や損害賠償予定などを無効とする規制です。",
    "articleSlug": "tokuyaku-seigen"
  },
  {
    "id": "menkyo",
    "cat": "law",
    "term": "宅建業の免許",
    "reading": "たっけんぎょうのめんきょ",
    "summary": "宅建業の免許の概要",
    "desc": "宅地建物取引業を営むために国土交通大臣などから受ける許可です。欠格事由や更新が試験で問われます。",
    "articleSlug": "menkyo"
  },
  {
    "id": "takkenshi",
    "cat": "law",
    "term": "宅建士",
    "reading": "たっけんし",
    "summary": "宅建士の概要",
    "desc": "宅建業者が設置し、重要事項説明など法令上の業務を担う国家資格者です。",
    "articleSlug": "takkenshi"
  },
  {
    "id": "takuchi_tatemono_teigi",
    "cat": "law",
    "term": "宅地・建物の定義",
    "reading": "たくち・たてものていぎ",
    "summary": "宅地・建物の定義の概要",
    "desc": "宅建業法上「宅地」「建物」がどこまで含まれるかの定義です。登記・説明対象の前提になります。",
    "articleSlug": "takuchi-tatemono-teigi"
  },
  {
    "id": "hosho",
    "cat": "law",
    "term": "営業保証金と弁済業務保証金",
    "reading": "えいぎょうほしょうきんとべんさいぎょうむほしょうきん",
    "summary": "宅建業者が備える2つの補償制度",
    "desc": "営業保証金：自分で法務局（供託所）に供託する。主たる事務所1000万円＋従たる事務所500万円/所。弁済業務保証金：保証協会に加入して分担金を納める。主たる事務所60万円＋従たる事務所30万円/所。保証協会加入なら営業保証金は不要。どちらも宅建業者以外の者だけが還付を受けられる。",
    "diagram": {
      "type": "table",
      "head": [
        "方式",
        "主たる事務所",
        "従たる事務所/所",
        "還付対象"
      ],
      "rows": [
        [
          "営業保証金（自己供託）",
          "1,000万円",
          "500万円",
          "宅建業者以外"
        ],
        [
          "弁済業務保証金（協会加入）",
          "60万円（分担金）",
          "30万円（分担金）",
          "宅建業者以外"
        ]
      ]
    },
    "articleSlug": "hosho"
  },
  {
    "id": "hoshokyo_shosai",
    "cat": "law",
    "term": "保証協会",
    "reading": "ほしょうきょうかい",
    "summary": "保証協会の概要",
    "desc": "宅建業者が供託する保証金や、株式会社住宅履約保証協会との契約などによる取引保護です。",
    "articleSlug": "hoshokyo-shosai"
  },
  {
    "id": "jusetsu",
    "cat": "law",
    "term": "重要事項説明（35条書面）",
    "reading": "じゅうようじこうせつめい",
    "summary": "契約前に宅建士が必ず説明する書面",
    "desc": "宅建士が宅建士証を提示し、契約前に説明する義務がある。買主・借主側に交付。記載内容は「登記情報・法令制限・代金以外の費用・建物の状況等」。IT重説（テレビ会議等）も認められる。相手方が宅建業者でも書面交付は必要（説明は省略可）。押印不要。相手方の承諾など所定の要件を満たせば電子書面での交付も可能（2022年5月施行）。",
    "diagram": {
      "type": "table",
      "head": [
        "書面",
        "交付相手",
        "作成者",
        "タイミング"
      ],
      "rows": [
        [
          "35条書面（重要事項）",
          "買主・借主",
          "宅建士が記名",
          "契約前"
        ],
        [
          "37条書面（契約書）",
          "売主と買主の両方",
          "宅建士が記名",
          "契約後遅滞なく"
        ]
      ]
    },
    "articleSlug": "jusetsu"
  },
  {
    "id": "37jo",
    "cat": "law",
    "term": "37条書面",
    "reading": "さんじゅうしちじょうしょめん",
    "summary": "37条書面の概要",
    "desc": "仲介・代理で契約成立前に、書面で重要事項・報酬など法定記載事項を交付する義務に関する規定です。",
    "articleSlug": "37jo"
  },
  {
    "id": "reins",
    "cat": "law",
    "term": "レインズ",
    "reading": "れいんず",
    "summary": "レインズの概要",
    "desc": "指定流通機構が運営する不動産情報の登録システムです。広告前の登録など実務・試験ともに重要です。",
    "articleSlug": "reins"
  },
  {
    "id": "baikai",
    "cat": "law",
    "term": "媒介契約の種類",
    "reading": "ばいかいけいやくのしゅるい",
    "summary": "一般・専任・専属専任の3種類",
    "desc": "一般媒介：複数業者に依頼OK。レインズ登録義務なし。専任媒介：1社のみ。自己発見の買主との直接取引OK。レインズ登録7日以内・報告2週間に1回。専属専任媒介：1社のみ。自己発見でも直接取引不可。レインズ登録5日以内・報告1週間に1回。いずれも有効期間は最長3か月。",
    "diagram": {
      "type": "table",
      "head": [
        "種類",
        "複数依頼",
        "自己発見",
        "レインズ",
        "報告"
      ],
      "rows": [
        [
          "一般",
          "○",
          "○",
          "義務なし",
          "任意"
        ],
        [
          "専任",
          "×",
          "○（OK）",
          "7日以内",
          "2週に1回"
        ],
        [
          "専属専任",
          "×",
          "×（NG）",
          "5日以内",
          "1週に1回"
        ]
      ]
    },
    "articleSlug": "baikai-compare"
  },
  {
    "id": "hoshu",
    "cat": "law",
    "term": "報酬の計算（売買）",
    "reading": "ほうしゅうのけいさん",
    "summary": "売買仲介でもらえる報酬の上限",
    "desc": "売買代金に応じた速算式：200万円以下→5%、200万超400万以下→4%+2万円、400万超→3%+6万円（いずれも税別、一方の依頼者から）。例：1000万円の物件なら3%+6万=36万円が一方からの上限。低廉な空家等（代金800万円以下の宅地・建物）は、媒介契約時に説明し合意を得た範囲で、売主等から受ける報酬を税込33万円までとする特例がある（2024年7月1日施行）。依頼者の同意があっても告示の上限超過は不可。",
    "diagram": {
      "type": "table",
      "head": [
        "代金",
        "一方からの報酬上限（税別）"
      ],
      "rows": [
        [
          "200万円以下",
          "代金×5%"
        ],
        [
          "200万超400万以下",
          "代金×4%＋2万円"
        ],
        [
          "400万超",
          "代金×3%＋6万円"
        ],
        [
          "低廉空き家（800万以下等）",
          "税込33万円まで等（2024年7月〜）"
        ]
      ]
    },
    "articleSlug": "hoshu"
  },
  {
    "id": "hook",
    "cat": "law",
    "term": "手付の種類",
    "reading": "ておつのしゅるい",
    "summary": "契約時に支払う手付金の3つの意味",
    "desc": "証約手付：契約が成立した証拠。違約手付：違約した場合に没収される罰。解約手付：買主は放棄、売主は倍返しで解除できる。宅建業者が自ら売主の場合、手付は解約手付として機能し、相手方が履行に着手するまでに行使しなければならない。手付額の上限は代金の20%。",
    "diagram": {
      "type": "compare",
      "left": {
        "title": "買主から解除する場合",
        "items": [
          "手付金を放棄する",
          "例：100万円払っていたら諦める",
          "売主への損害賠償は不要"
        ]
      },
      "right": {
        "title": "売主から解除する場合",
        "items": [
          "手付の倍額を返還する",
          "例：受け取った100万円を返して+さらに100万円",
          "手付倍返しと呼ぶ"
        ]
      }
    },
    "articleSlug": "tetsuke"
  },
  {
    "id": "coolingoff",
    "cat": "law",
    "term": "クーリングオフ",
    "reading": "くーりんぐおふ",
    "summary": "一定期間内に一方的に解除できる制度",
    "desc": "宅建業者が自ら売主の場合、事務所等以外（喫茶店・買主自宅など）で申込みや契約をした買主は、告知を受けた日から8日以内に書面で解除できる。解除の効力は書面を発送した時点で生じる（発信主義）。解除後は全額返還が必要で、業者は違約金・損害賠償を請求できない。",
    "diagram": {
      "type": "table",
      "head": [
        "場所",
        "クーリングオフ"
      ],
      "rows": [
        [
          "宅建業者の事務所",
          "適用なし"
        ],
        [
          "案内所・展示場（届出済）",
          "適用なし"
        ],
        [
          "買主の希望で自宅・勤務先",
          "適用なし"
        ],
        [
          "上記以外（喫茶店等）",
          "適用あり（告知から8日以内）"
        ]
      ]
    },
    "articleSlug": "cooling"
  },
  {
    "id": "kantoktosho",
    "cat": "law",
    "term": "監督処分",
    "reading": "かんとくしょぶん",
    "summary": "監督処分の概要",
    "desc": "国土交通大臣や知事が業者に業務改善命令・営業停止などを命じる処分です。",
    "articleSlug": "kantoktosho"
  },
  {
    "id": "koukoku_kisei",
    "cat": "law",
    "term": "広告規制",
    "reading": "こうこくきせい",
    "summary": "広告規制の概要",
    "desc": "虚偽・誇大な広告を禁止し、表示すべき事項を定めるなど広告の適正化を図る規制です。",
    "articleSlug": "koukoku-kisei"
  },
  {
    "id": "gyomujoh_kisei",
    "cat": "law",
    "term": "業務上の規制",
    "reading": "ぎょうむじょうのきせい",
    "summary": "業務上の規制の概要",
    "desc": "取引の公正・安全を守るため、仲介手続や書面交付など業務遂行上の具体的義務です。",
    "articleSlug": "gyomujoh-kisei"
  },
  {
    "id": "jiko_syoyu",
    "cat": "law",
    "term": "自己所有外物件の制限",
    "reading": "じこしょゆうにぞくしないぶっけん",
    "summary": "自己所有外物件の制限の概要",
    "desc": "業者が自分の所有ではない物件を売買・交換の媒介してはならないなどの制限です。",
    "articleSlug": "jiko-syoyu"
  },
  {
    "id": "warihukehanbai",
    "cat": "law",
    "term": "割賦販売",
    "reading": "わりふけはんばい",
    "summary": "割賦販売の概要",
    "desc": "代金を分割して支払う方式による土地・建物の販売で、割賦販売法の適用や説明義務があります。",
    "articleSlug": "warihukehanbai"
  },
  {
    "id": "hinshitsu_kakuho",
    "cat": "law",
    "term": "住宅品質確保法",
    "reading": "じゅうたくひんしつかくほほう",
    "summary": "住宅品質確保法の概要",
    "desc": "新築住宅の瑕疵担保責任や検査など、住宅の品質確保と購入者保護を目的とする法律です。",
    "articleSlug": "hinshitsu-kakuho"
  },
  {
    "id": "hachishu",
    "cat": "law",
    "term": "8種制限",
    "reading": "はっしゅせいげん",
    "summary": "自ら売主の宅建業者に課される8つの制限",
    "desc": "宅建業者が自ら売主で買主が一般消費者（非業者）の場合に適用される消費者保護ルール。①損害賠償予定額の制限（上限20%）②手付金の制限（上限20%・保全措置）③クーリングオフ④他人物売買の制限⑤手付解除の特則⑥担保責任の特例⑦未完成物件の制限⑧解除・損害賠償の特則。業者間取引には適用されない。",
    "diagram": {
      "type": "table",
      "head": [
        "制限",
        "内容"
      ],
      "rows": [
        [
          "手付金の上限",
          "代金の20%以下"
        ],
        [
          "損害賠償予定額",
          "代金の20%以下"
        ],
        [
          "クーリングオフ",
          "告知から8日以内は解除可"
        ],
        [
          "手付解除",
          "相手方の履行着手前のみ可"
        ],
        [
          "保全措置",
          "手付等を保全（未完成5%超等）"
        ],
        [
          "担保責任",
          "引渡しから2年以上の特約は有効"
        ]
      ]
    },
    "articleSlug": "hasshu-seigen"
  },
  {
    "id": "juuyou_jikou_hani",
    "cat": "law",
    "term": "重要事項の範囲",
    "reading": "じゅうようじこうのはんい",
    "summary": "重要事項の範囲の概要",
    "desc": "重要事項説明に含めるべき法令上の事項の範囲です。物件・権利関係・取引条件などが対象です。",
    "articleSlug": "juuyou-jikou-hani"
  },
  {
    "id": "baikai_genba_setumei",
    "cat": "law",
    "term": "売買現場での説明",
    "reading": "ばいばいげんばでのせつめい",
    "summary": "売買現場での説明の概要",
    "desc": "現地での物件説明や資料確認など、重要事項以外にも説明すべき内容と実務上の留意点です。",
    "articleSlug": "baikai-genba-setumei"
  },
  {
    "id": "keiyaku_seikyuu_tetsuzuki",
    "cat": "law",
    "term": "契約書の作成・交付（37条）",
    "reading": "けいやくしょのさくせい・こうふ",
    "summary": "契約書の作成・交付（37条）の概要",
    "desc": "契約書に記載する事項や署名捺印、書面の交付時期など宅建業法37条関連の手続です。",
    "articleSlug": "keiyaku-seikyuu-tetsuzuki"
  },
  {
    "id": "meikaku_ka_houshin",
    "cat": "law",
    "term": "報酬の明瞭化",
    "reading": "ほうしゅうのめいりょうか",
    "summary": "報酬の明瞭化の概要",
    "desc": "報酬額やその支払条件を当事者にわかりやすく示す義務です。",
    "articleSlug": "meikaku-ka-houshin"
  },
  {
    "id": "tainou_koui",
    "cat": "law",
    "term": "宅建業者の賠償責任",
    "reading": "たっけんぎょうしゃのばいしょうせきにん",
    "summary": "宅建業者の賠償責任の概要",
    "desc": "説明義務違反や善良な管理者の注意義務違反などに基づく不法行為・契約責任です。",
    "articleSlug": "tainou-koui"
  },
  {
    "id": "kyakka_chintaishaku",
    "cat": "law",
    "term": "貸室・貸パークの賃貸借",
    "reading": "かしつ・かしパークのちんたいしゃく",
    "summary": "貸室・貸パークの賃貸借の概要",
    "desc": "区分所有建物の一部や駐車場などの賃貸借に関する媒介上の留意点です。",
    "articleSlug": "kyakka-chintaishaku"
  },
  {
    "id": "tajinbutsu_baibai",
    "cat": "law",
    "term": "他人物売買",
    "reading": "たにんぶつばいばい",
    "summary": "他人物売買の概要",
    "desc": "他人の所有する物を売る売買です。売主に権利取得義務や追認が関係します。",
    "articleSlug": "tajinbutsu-baibai"
  },
  {
    "id": "mikansei_bukken",
    "cat": "law",
    "term": "未完成物件の取引",
    "reading": "みかんせいぶっけんのとりひき",
    "summary": "未完成物件の取引の概要",
    "desc": "未完成の建物などを対象とする取引で、完成時期・設計変更など説明・特約が重要です。",
    "articleSlug": "mikansei-bukken"
  },
  {
    "id": "teiki_jouhou_teikyou",
    "cat": "law",
    "term": "定期報告（媒介）",
    "reading": "ていきほうこく",
    "summary": "定期報告（媒介）の概要",
    "desc": "媒介契約に基づき、取引の進捗などを定期的に報告する義務です。",
    "articleSlug": "teiki-jouhou-teikyou"
  },
  {
    "id": "reins_touroku_jiki",
    "cat": "law",
    "term": "レインズ登録の期限",
    "reading": "れいんずとうろくのきげん",
    "summary": "レインズ登録の期限の概要",
    "desc": "広告に先立ってレインズへ登録すべき情報と、その期限に関する規定です。",
    "articleSlug": "reins-touroku-jiki"
  },
  {
    "id": "baikai_keiyaku_shuryou",
    "cat": "law",
    "term": "媒介契約の終了事由",
    "reading": "ばいかいけいやくのしゅうりょうじゆう",
    "summary": "媒介契約の終了事由の概要",
    "desc": "専属・一般など媒介契約が終了する事由や着手義務の範囲です。",
    "articleSlug": "baikai-keiyaku-shuryou"
  },
  {
    "id": "tokutei_denkijou",
    "cat": "law",
    "term": "特定電磁的手段による提供",
    "reading": "とくていでんじてきしゅだんによるていきょう",
    "summary": "特定電磁的手段による提供の概要",
    "desc": "電磁的記録により情報を提供する場合の同意・確認などの要件です。",
    "articleSlug": "tokutei-denkijou"
  },
  {
    "id": "akuden_kisei",
    "cat": "law",
    "term": "悪徳業者への規制",
    "reading": "あくとくぎょうしゃへのきせい",
    "summary": "悪徳業者への規制の概要",
    "desc": "不当な勧誘や契約から消費者を守るための業者側の禁止・説明義務です。",
    "articleSlug": "akuden-kisei"
  },
  {
    "id": "kojin_jouhou_hogo",
    "cat": "law",
    "term": "個人情報の取扱い",
    "reading": "こじんじょうほうのあつかい",
    "summary": "個人情報の取扱いの概要",
    "desc": "取引を通じて知り得た個人データの適切な取得・保管・第三者提供の制限です。",
    "articleSlug": "kojin-jouhou-hogo"
  },
  {
    "id": "akiya_toriatsukai",
    "cat": "law",
    "term": "空き家・低廉物件の特例",
    "reading": "あきや・ていれんぶっけんのとくれい",
    "summary": "空き家・低廉物件の特例の概要",
    "desc": "空き家や低廉物件を対象とする場合の調査・説明・契約上の留意点です。",
    "articleSlug": "akiya-toriatsukai"
  },
  {
    "id": "chinhoushou_nintei",
    "cat": "law",
    "term": "賃貸住宅管理業の登録",
    "reading": "ちんたいじゅうたくかんりぎょうのとうろく",
    "summary": "賃貸住宅管理業の登録の概要",
    "desc": "賃貸住宅の管理を業として行う登録制度と、その義務です。",
    "articleSlug": "chinhoushou-nintei"
  },
  {
    "id": "kanri_itaku_keiyaku",
    "cat": "law",
    "term": "管理委託契約",
    "reading": "かんりいたくけいやく",
    "summary": "管理委託契約の概要",
    "desc": "貸主から管理業務を委託される契約の内容と報酬です。",
    "articleSlug": "kanri-itaku-keiyaku"
  },
  {
    "id": "shakuchi_chinju",
    "cat": "law",
    "term": "借地・借家の譲渡・転貸",
    "reading": "しゃくち・ちんたいのじょうと・てんたい",
    "summary": "借地・借家の譲渡・転貸の概要",
    "desc": "借地権・賃借権の譲渡や転貸に関する同意・対抗要件などです。",
    "articleSlug": "shakuchi-chinju"
  },
  {
    "id": "baikyaku_daikin",
    "cat": "law",
    "term": "売却代金の決済",
    "reading": "ばいきゃくだいきんのけっさい",
    "summary": "売却代金の決済の概要",
    "desc": "売買代金の支払時期・決済場所・残代金と登記の関係などです。",
    "articleSlug": "baikyaku-daikin"
  },
  {
    "id": "takken_shuninsha",
    "cat": "law",
    "term": "宅建業主任者",
    "reading": "たっけんぎょうしゅにんしゃ",
    "summary": "宅建業主任者の概要",
    "desc": "事務所ごとに置く法令遵守と業務統括の責任者です。資格・業務範囲が問われます。",
    "articleSlug": "takken-shuninsha"
  },
  {
    "id": "toshi",
    "cat": "limit",
    "term": "都市計画法",
    "reading": "としけいかくほう",
    "summary": "都市計画法の概要",
    "desc": "都市の開発・再開発や用途地域など市街化を計画的に進めるための法律です。",
    "articleSlug": "toshi"
  },
  {
    "id": "yoto",
    "cat": "limit",
    "term": "用途地域13種類",
    "reading": "ようとちいき",
    "summary": "土地の使い方を13種類に区分するルール",
    "desc": "住居系（8種）：第一種低層から田園住居まで。商業系（2種）：近隣商業・商業。工業系（3種）：準工業・工業・工業専用。大原則：低層住居専用地域では大学・病院は建てられない。工業専用地域では住宅・病院・学校は建てられない（倉庫は可）。商業地域では大部分の建物が建てられるが風俗施設の規制あり。",
    "diagram": {
      "type": "table",
      "head": [
        "系統",
        "種類",
        "ポイント"
      ],
      "rows": [
        [
          "住居系",
          "第一種・二種低層",
          "住宅・学校中心。大学・病院不可（一種低層）"
        ],
        [
          "住居系",
          "第一種・二種中高層",
          "病院・大学可（中高層）"
        ],
        [
          "住居系",
          "第一種・二種住居・準住居・田園住居",
          "大型施設が徐々に可に"
        ],
        [
          "商業系",
          "近隣商業・商業",
          "ほぼ何でも建てられる"
        ],
        [
          "工業系",
          "準工業・工業",
          "住宅も可"
        ],
        [
          "工業系",
          "工業専用",
          "住宅・病院・学校は不可"
        ]
      ]
    },
    "articleSlug": "yoto"
  },
  {
    "id": "kenpeiritsu",
    "cat": "limit",
    "term": "建ぺい率・容積率",
    "reading": "けんぺいりつ・ようせきりつ",
    "summary": "敷地に対する建物の大きさの制限",
    "desc": "建ぺい率：敷地面積に対する建築面積（1階の床面積）の割合。「この土地の何%まで建物を建てられるか」。容積率：敷地面積に対する延べ床面積の割合。「全フロア合計の床面積が敷地の何%まで」。前面道路が12m未満の場合、容積率は「指定容積率」と「道路幅員×0.4（住居系）」の小さい方。",
    "diagram": {
      "type": "table",
      "head": [
        "指標",
        "計算式",
        "加算・緩和"
      ],
      "rows": [
        [
          "建ぺい率",
          "建築面積÷敷地面積×100",
          "防火地域耐火建築物+10%、角地+10%"
        ],
        [
          "容積率",
          "延べ床面積÷敷地面積×100",
          "前面道路12m未満→幅員×0.4（住居系）との小さい方"
        ],
        [
          "地下室（住宅）",
          "—",
          "延べ面積の1/3まで容積率から除外"
        ]
      ]
    },
    "articleSlug": "kenpei"
  },
  {
    "id": "yoseki",
    "cat": "limit",
    "term": "容積率",
    "reading": "ようせきりつ",
    "summary": "容積率の概要",
    "desc": "敷地面積に対する延べ床面積の比率で、建築可能な規模を制限します。",
    "articleSlug": "yoseki"
  },
  {
    "id": "kenchiku",
    "cat": "limit",
    "term": "建築基準法",
    "reading": "けんちくきじゅんほう",
    "summary": "建築基準法の概要",
    "desc": "建物の構造・用途・敷地・防火など最低限の安全・衛生を定める法律です。",
    "articleSlug": "kenchiku"
  },
  {
    "id": "kaihatsu",
    "cat": "limit",
    "term": "開発許可",
    "reading": "かいはつきょか",
    "summary": "宅地造成等の工事をするときの許可",
    "desc": "「建物を建てる目的で土地の区画・形質を変える（造成等）」行為が開発行為。市街化区域では原則1000㎡以上の開発行為に知事等の許可が必要。市街化調整区域では原則全ての開発行為に許可が必要（例外：農林漁業者の農業用建物等）。工事完了公告後でなければ原則として建物を建てられない。",
    "diagram": {
      "type": "table",
      "head": [
        "区域",
        "面積要件",
        "主な例外"
      ],
      "rows": [
        [
          "市街化区域",
          "1,000㎡以上",
          "農林漁業用施設・公共施設等"
        ],
        [
          "市街化調整区域",
          "原則全て",
          "農林漁業者の農業用建物等"
        ],
        [
          "非線引き区域",
          "3,000㎡以上",
          "同上"
        ],
        [
          "準都市計画区域",
          "3,000㎡以上",
          "同上"
        ],
        [
          "区域外",
          "10,000㎡以上（大規模）",
          "同上"
        ]
      ]
    },
    "articleSlug": "kaihatsu"
  },
  {
    "id": "kaihatsu_kakunin",
    "cat": "limit",
    "term": "建築確認",
    "reading": "けんちくかくにん",
    "summary": "建築確認の概要",
    "desc": "建築基準法に適合するかを行政が確認する手続です。確認済証がなければ建築できません。",
    "articleSlug": "kaihatsu-kakunin"
  },
  {
    "id": "nouchi",
    "cat": "limit",
    "term": "農地法3条・4条・5条",
    "reading": "のうちほう",
    "summary": "農地の売買・転用に必要な許可",
    "desc": "3条（権利移動）：農地を農地のまま売買・賃貸する→農業委員会の許可。4条（自己転用）：自分の農地を農地以外（宅地等）にする→都道府県知事等の許可（市街化区域は農業委員会への届出のみ）。5条（転用目的の権利移動）：農地を農地以外にする目的で売買→都道府県知事等の許可（市街化区域は届出）。",
    "diagram": {
      "type": "table",
      "head": [
        "条文",
        "行為",
        "許可・届出先",
        "市街化区域特例"
      ],
      "rows": [
        [
          "3条",
          "権利移動（農地→農地）",
          "農業委員会（許可）",
          "なし"
        ],
        [
          "4条",
          "自己転用（農地→宅地等）",
          "都道府県知事等（許可）",
          "農業委員会へ届出のみ"
        ],
        [
          "5条",
          "転用目的の権利移動",
          "都道府県知事等（許可）",
          "農業委員会へ届出のみ"
        ],
        [
          "3条の3",
          "相続による取得",
          "農業委員会（届出3か月以内）",
          "—"
        ]
      ]
    },
    "articleSlug": "nochi"
  },
  {
    "id": "kukaku_seiri",
    "cat": "limit",
    "term": "土地区画整理法",
    "reading": "とちくかくせいりほう",
    "summary": "土地区画整理法の概要",
    "desc": "土地区画整理事業によって土地を整理し換地・清算金などを定める制度です。",
    "articleSlug": "kukaku-seiri"
  },
  {
    "id": "kokudo_riyoh",
    "cat": "limit",
    "term": "国土利用計画法",
    "reading": "こくどりようけいかくほう",
    "summary": "国土利用計画法の概要",
    "desc": "土地の利用を調整し、投機的な転売を抑える届出・監視などの枠組みです。",
    "articleSlug": "kokudo-riyoh"
  },
  {
    "id": "morijoken",
    "cat": "limit",
    "term": "盛土規制法",
    "reading": "もりどきせいほう",
    "summary": "盛土規制法の概要",
    "desc": "盛土・切土による土砂災害を防ぐための規制・届出・技術基準です。",
    "articleSlug": "morijoken"
  },
  {
    "id": "keikan",
    "cat": "limit",
    "term": "景観法",
    "reading": "けいかんほう",
    "summary": "景観法の概要",
    "desc": "景観行政計画や協定、条例による景観の保全・形成です。",
    "articleSlug": "keikan"
  },
  {
    "id": "chikunikeikaku",
    "cat": "limit",
    "term": "地区計画",
    "reading": "ちくけいかく",
    "summary": "街区単位でのきめ細かい街づくりルール",
    "desc": "用途地域より細かく、地域の特性に応じた街づくりのルール。用途地域内外を問わず定めることができる（市街化調整区域にも可）。地区計画の区域内で建築等の行為を行う場合は、着手の30日前までに市町村長に届け出る必要がある（許可ではなく届出）。市町村長は勧告はできるが強制はできない。",
    "diagram": {
      "type": "flow",
      "steps": [
        "建築等の行為を予定",
        "着手30日前までに市町村長へ届出",
        "審査→勧告可（強制力なし)",
        "地区計画の趣旨に合った開発を促進"
      ]
    },
    "articleSlug": "chiku-keikaku"
  },
  {
    "id": "nikage_shamen",
    "cat": "limit",
    "term": "日影規制・斜線制限",
    "reading": "にかげきせい・しゃせんせいげん",
    "summary": "日影規制・斜線制限の概要",
    "desc": "隣地への日影や道路斜線など、建物の高さを制限する規制です。",
    "articleSlug": "nikage-shamen"
  },
  {
    "id": "shigaichi_kuiki",
    "cat": "limit",
    "term": "市街化区域・市街化調整区域",
    "reading": "しがいかくいき・ちょうせいくいき",
    "summary": "市街化区域・市街化調整区域の概要",
    "desc": "市街化を進める区域と抑制する調整区域の区分で、開発行為の可否が変わります。",
    "articleSlug": "shigaichi-kuiki"
  },
  {
    "id": "hisen_yuki_kuiki",
    "cat": "limit",
    "term": "非線引き区域",
    "reading": "ひせんいんきくいき",
    "summary": "非線引き区域の概要",
    "desc": "都市計画区域線が引かれていない地域での開発行為の扱いです。",
    "articleSlug": "hisen-yuki-kuiki"
  },
  {
    "id": "junkentoshi_keikaku",
    "cat": "limit",
    "term": "準都市計画区域",
    "reading": "じゅんとしけいかくくいき",
    "summary": "準都市計画区域の概要",
    "desc": "都市計画区域に準ずる計画区域で、開発に関する基本的な方針を定めます。",
    "articleSlug": "junkentoshi-keikaku"
  },
  {
    "id": "kenchiku_seigen_hourei",
    "cat": "limit",
    "term": "建築協定・地区計画等の関係",
    "reading": "けんちくきょうてい・ちくけいかくとのかんけい",
    "summary": "建築協定・地区計画等の関係の概要",
    "desc": "建築協定・地区計画・高度地区など周辺法令との関係を整理します。",
    "articleSlug": "kenchiku-seigen-hourei"
  },
  {
    "id": "kasen_takuchi",
    "cat": "limit",
    "term": "河川区域・堤外地",
    "reading": "かせんくいき・ていがいち",
    "summary": "河川区域・堤外地の概要",
    "desc": "河川区域内や堤外地での建築・工作物に関する河川法上の制限です。",
    "articleSlug": "kasen-takuchi"
  },
  {
    "id": "dosya_saigai",
    "cat": "limit",
    "term": "土砂災害警戒区域",
    "reading": "どしゃさいがいけいかいくいき",
    "summary": "土砂災害警戒区域の概要",
    "desc": "土石流などの危険が高い区域での建築・居住に関する規制です。",
    "articleSlug": "dosya-saigai"
  },
  {
    "id": "tsunami_takashio",
    "cat": "limit",
    "term": "津波・高潮対策区域",
    "reading": "つなみ・たかしおたいさくくいき",
    "summary": "津波・高潮対策区域の概要",
    "desc": "津波浸水想定や高潮リスク区域における防災上の配慮です。",
    "articleSlug": "tsunami-takashio"
  },
  {
    "id": "shizen_hogo_kuiki",
    "cat": "limit",
    "term": "自然公園・保全地域",
    "reading": "しぜんこうえん・ほぜんちいき",
    "summary": "自然公園・保全地域の概要",
    "desc": "自然公園法や保全地域における行為制限の概要です。",
    "articleSlug": "shizen-hogo-kuiki"
  },
  {
    "id": "bunkazai_chiku",
    "cat": "limit",
    "term": "文化財保護法の規制",
    "reading": "ぶんかざいほごほうのきせい",
    "summary": "文化財保護法の規制の概要",
    "desc": "史跡・名勝など文化財周辺での色彩・形態・高さなどの制限です。",
    "articleSlug": "bunkazai-chiku"
  },
  {
    "id": "juutaku_seisan_kuiki",
    "cat": "limit",
    "term": "住宅生産確保計画区域",
    "reading": "じゅうたくせいさんかくほけいかくくいき",
    "summary": "住宅生産確保計画区域の概要",
    "desc": "住宅市街地の健全な発展のために計画的に造成・誘導する区域です。",
    "articleSlug": "juutaku-seisan-kuiki"
  },
  {
    "id": "tokutei_shiro_shisan",
    "cat": "limit",
    "term": "特定用途制限地域",
    "reading": "とくていようとせいげんちいき",
    "summary": "特定用途制限地域の概要",
    "desc": "用途を限定して土地利用を誘導する地域区分です。",
    "articleSlug": "tokutei-shiro-shisan"
  },
  {
    "id": "bouka_yoto",
    "cat": "limit",
    "term": "防火地域・準防火地域",
    "reading": "ぼうかちいき・じゅんぼうかちいき",
    "summary": "防火地域・準防火地域の概要",
    "desc": "延焼抑制のため耐火建築の義務などが課される地域区分です。",
    "articleSlug": "bouka-yoto"
  },
  {
    "id": "taikaku_jogen",
    "cat": "limit",
    "term": "高さの限度（絶対高さ・斜線・道路）",
    "reading": "たかさのげんど",
    "summary": "高さの限度（絶対高さ・斜線・道路）の概要",
    "desc": "絶対高さ、道路斜線、北側斜線など複合的な高さ制限です。",
    "articleSlug": "taikaku-jogen"
  },
  {
    "id": "shuyoukaidou_setback",
    "cat": "limit",
    "term": "前面道路とセットバック",
    "reading": "ぜんめんどうろとセットバック",
    "summary": "前面道路とセットバックの概要",
    "desc": "前面道路から後退して建物を建てることで道路幅員や防火上有効な空地を確保します。",
    "articleSlug": "shuyoukaidou-setback"
  },
  {
    "id": "kenchiku_kakunin_shinsei",
    "cat": "limit",
    "term": "建築確認申請",
    "reading": "けんちくかくにんしんせい",
    "summary": "建築確認申請の概要",
    "desc": "確認申請の提出先・図書・建築主・事前協議などの流れです。",
    "articleSlug": "kenchiku-kakunin-shinsei"
  },
  {
    "id": "kanryou_kensa",
    "cat": "limit",
    "term": "完了検査（建築基準法）",
    "reading": "かんりょうけんさ",
    "summary": "完了検査（建築基準法）の概要",
    "desc": "建築完了後に適法に建ったか検査し、検査済証を経て使用開始できます。",
    "articleSlug": "kanryou-kensa"
  },
  {
    "id": "ijou_kenchiku",
    "cat": "limit",
    "term": "既存不適格建築物",
    "reading": "きそんふてきかくけんちくぶつ",
    "summary": "既存不適格建築物の概要",
    "desc": "現存するが現在の条例には適合しない建物の維持・改修・移転の扱いです。",
    "articleSlug": "ijou-kenchiku"
  },
  {
    "id": "tokutei_kenchiku",
    "cat": "limit",
    "term": "特定建築物等の定期調査",
    "reading": "とくていけんちくぶつちょうさ",
    "summary": "特定建築物等の定期調査の概要",
    "desc": "エレベーター等の設備を持つ建物の定期調査・報告義務です。",
    "articleSlug": "tokutei-kenchiku"
  },
  {
    "id": "shuuzen_jourei",
    "cat": "limit",
    "term": "修繕・保存に関する条例",
    "reading": "しゅうぜん・ほぞんにかんするじょうれい",
    "summary": "修繕・保存に関する条例の概要",
    "desc": "伝統的建造物群保存地区などでの修繕・色彩に関する条例です。",
    "articleSlug": "shuuzen-jourei"
  },
  {
    "id": "koeki_yoto",
    "cat": "limit",
    "term": "公益的施設の立地調整",
    "reading": "こうえきてきしせつのりちちょうせい",
    "summary": "公益的施設の立地調整の概要",
    "desc": "学校・福祉施設など公益施設の立地を計画的に誘導する仕組みです。",
    "articleSlug": "koeki-yoto"
  },
  {
    "id": "tochi_saiken",
    "cat": "limit",
    "term": "土地区画整理事業の換地",
    "reading": "とちくかくせいりじぎょうのかんち",
    "summary": "土地区画整理事業の換地の概要",
    "desc": "整理事業で旧土地が消え新たな権利が付与される換地・清算の概念です。",
    "articleSlug": "tochi-saiken"
  },
  {
    "id": "shinetsei_seiri",
    "cat": "limit",
    "term": "新住宅市街地開発事業",
    "reading": "しんじゅうたくしがいちかいはつじぎょう",
    "summary": "新住宅市街地開発事業の概要",
    "desc": "新住宅市街地開発事業による土地利用・道路・公園の造成です。",
    "articleSlug": "shinetsei-seiri"
  },
  {
    "id": "rinkai_setchi",
    "cat": "limit",
    "term": "臨港地区計画",
    "reading": "りんこうちくけいかく",
    "summary": "臨港地区計画の概要",
    "desc": "港湾・産業立地などを一体計画する臨港地区の概要です。",
    "articleSlug": "rinkai-setchi"
  },
  {
    "id": "koudo_riyouchiku",
    "cat": "limit",
    "term": "高度利用地区",
    "reading": "こうどりようちく",
    "summary": "高度利用地区の概要",
    "desc": "商業・業務の集積を誘導し容積率や建蔽率を特例する地区です。",
    "articleSlug": "koudo-riyouchiku"
  },
  {
    "id": "nougyou_seisan",
    "cat": "limit",
    "term": "農業振興地域・農地転用",
    "reading": "のうぎょうしんこうちいき",
    "summary": "農業振興地域・農地転用の概要",
    "desc": "農地を農業以外に転用するときの許可・農振・農用地区などの枠組みです。",
    "articleSlug": "nougyou-seisan"
  },
  {
    "id": "fudousantokuzetsu",
    "cat": "tax",
    "term": "不動産取得税",
    "reading": "ふどうさんしゅとくぜい",
    "summary": "不動産を取得したときに一度だけかかる税",
    "desc": "都道府県が課す地方税（国税ではない）。申告不要（都道府県から通知が来る普通徴収）。相続・合併による取得は非課税。標準税率は4%だが住宅・土地は特例で3%。新築住宅は評価額から最大1200万円を控除した額が課税標準になる特例あり（認定長期優良住宅は1300万円）。",
    "diagram": {
      "type": "table",
      "head": [
        "取得原因",
        "課税・非課税"
      ],
      "rows": [
        [
          "売買・贈与",
          "課税"
        ],
        [
          "相続",
          "非課税"
        ],
        [
          "法人の合併",
          "非課税"
        ],
        [
          "共有物分割（増分なし）",
          "非課税"
        ]
      ]
    },
    "articleSlug": "fudosantax"
  },
  {
    "id": "kotei",
    "cat": "tax",
    "term": "固定資産税",
    "reading": "こていしさんぜい",
    "summary": "毎年1月1日の所有者に課税される税",
    "desc": "市町村が課す地方税（東京23区は都）。毎年1月1日時点の所有者に課税される（賦課期日）。評価替えは3年に1度。標準税率1.4%（市町村条例で変更可）。住宅用地の特例：200㎡以下の小規模住宅用地は課税標準が6分の1、200㎡超の一般住宅用地は3分の1。",
    "diagram": {
      "type": "table",
      "head": [
        "区分",
        "課税標準の特例"
      ],
      "rows": [
        [
          "小規模住宅用地（200㎡以下）",
          "評価額の1/6"
        ],
        [
          "一般住宅用地（200㎡超の部分）",
          "評価額の1/3"
        ],
        [
          "非住宅用地",
          "評価額の全額"
        ]
      ]
    },
    "articleSlug": "kotei"
  },
  {
    "id": "kotei_noufu",
    "cat": "tax",
    "term": "固定資産税の納付",
    "reading": "こていしさんぜいののうふ",
    "summary": "固定資産税の納付の概要",
    "desc": "固定資産税の納税義務者・申告・延滞などの基本です。",
    "articleSlug": "kotei-noufu"
  },
  {
    "id": "insho",
    "cat": "tax",
    "term": "印紙税",
    "reading": "いんしぜい",
    "summary": "契約書などの文書に課される国税",
    "desc": "課税文書に収入印紙を貼付して納める国税。不動産の売買契約書・建物の賃貸借契約書・金銭消費貸借契約書などが課税対象。電子契約（電磁的記録）は「文書」ではないため印紙税は不要。1通ごとに課税されるため、原本2通を作成すれば各1通に印紙が必要。1万円未満の契約書は非課税。",
    "diagram": {
      "type": "table",
      "head": [
        "文書の種類",
        "課税"
      ],
      "rows": [
        [
          "不動産売買契約書",
          "課税"
        ],
        [
          "建物賃貸借契約書",
          "課税"
        ],
        [
          "電子契約（データ）",
          "非課税"
        ],
        [
          "記載金額1万円未満",
          "非課税"
        ]
      ]
    },
    "articleSlug": "inshi"
  },
  {
    "id": "torokumenkyozei",
    "cat": "tax",
    "term": "登録免許税",
    "reading": "とうろくめんきょぜい",
    "summary": "登記を行うときに必要な国税",
    "desc": "国税。登記の種類によって税率が異なる。所有権保存登記は評価額の0.4%、売買による所有権移転は2%、相続による移転は0.4%。住宅の特例（新築）：一定要件を満たす場合は軽減税率あり（保存登記0.15%、移転0.3%）。抵当権設定登記の課税標準は「不動産の価額」ではなく「債権（ローン）の金額」。",
    "diagram": {
      "type": "table",
      "head": [
        "登記の種類",
        "原則税率",
        "軽減税率（住宅要件あり）"
      ],
      "rows": [
        [
          "所有権保存登記",
          "0.4%",
          "0.15%"
        ],
        [
          "所有権移転（売買）",
          "2.0%",
          "0.3%"
        ],
        [
          "所有権移転（相続）",
          "0.4%",
          "軽減なし"
        ],
        [
          "抵当権設定登記",
          "0.4%（債権額）",
          "0.1%"
        ]
      ]
    },
    "articleSlug": "toroku"
  },
  {
    "id": "joto",
    "cat": "tax",
    "term": "譲渡所得（長期・短期）",
    "reading": "じょうとしょとく",
    "summary": "不動産を売ったときの利益に対する税",
    "desc": "売却益（譲渡所得）は分離課税（他の収入と合算しない）。譲渡した年の1月1日時点で5年以下の保有は短期（所得税30%+住民税9%、復興特別所得税を含めると39.63%）、5年超は長期（所得税15%+住民税5%、復興特別所得税を含めると20.315%）。居住用財産の3000万円特別控除：住まなくなってから3年を経過する日の属する年末までの売却が対象（配偶者への売却は不可）。",
    "diagram": {
      "type": "table",
      "head": [
        "区分",
        "基準",
        "所得税+住民税",
        "復興特別所得税込み"
      ],
      "rows": [
        [
          "短期譲渡所得",
          "譲渡年1/1で5年以下",
          "30%+9%",
          "39.63%"
        ],
        [
          "長期譲渡所得",
          "譲渡年1/1で5年超",
          "15%+5%",
          "20.315%"
        ],
        [
          "居住用軽減（10年超）",
          "10年超・6000万以下分",
          "10%+4%",
          "14%"
        ]
      ]
    },
    "articleSlug": "joto"
  },
  {
    "id": "kaikae_tokubetsu",
    "cat": "tax",
    "term": "居住用財産の買換え特例",
    "reading": "きょじゅうようざいさんのかいかえとくれい",
    "summary": "居住用財産の買換え特例の概要",
    "desc": "居住用財産を売却して一定期間内に居住用を買い替えたときの譲渡所得の特例です。",
    "articleSlug": "kaikae-tokubetsu"
  },
  {
    "id": "loan_control",
    "cat": "tax",
    "term": "住宅ローン控除",
    "reading": "じゅうたくろーんこうじょ",
    "summary": "住宅ローン控除の概要",
    "desc": "住宅ローン残高に応じた所得税の控除要件・控除期間・適用限度です。",
    "articleSlug": "loan-control"
  },
  {
    "id": "jutaku_zouyo",
    "cat": "tax",
    "term": "住宅取得等資金の贈与税非課税",
    "reading": "じゅうたくしゅとくとうしきん",
    "summary": "住宅取得等資金の贈与税非課税の概要",
    "desc": "住宅取得資金の贈与に係る非課税枠や要件です。",
    "articleSlug": "jutaku-zouyo"
  },
  {
    "id": "souzoku_zeikin",
    "cat": "tax",
    "term": "相続税",
    "reading": "そうぞくぜいきん",
    "summary": "相続税の概要",
    "desc": "相続・遺贈により財産を取得したときに課される税の概要です。",
    "articleSlug": "souzoku-zeikin"
  },
  {
    "id": "shohi_zei_fudosan",
    "cat": "tax",
    "term": "消費税と不動産",
    "reading": "しょうひぜいとふどうさん",
    "summary": "消費税と不動産の概要",
    "desc": "不動産売買・賃貸・工事などで課税・非課税となる典型的パターンです。",
    "articleSlug": "shohi-zei-fudosan"
  },
  {
    "id": "chika_koji",
    "cat": "tax",
    "term": "地価公示・不動産鑑定",
    "reading": "ちかこうじ・ふどうさんかんてい",
    "summary": "地価公示・不動産鑑定の概要",
    "desc": "路線価や鑑定評価など、固定資産税・相続税の評価の根拠となる公示です。",
    "articleSlug": "chika-koji"
  },
  {
    "id": "shisanzei_kojogaku",
    "cat": "tax",
    "term": "固定資産税の課税標準と控除",
    "reading": "こていしさんぜいのかぜいひょうじゅん",
    "summary": "固定資産税の課税標準と控除の概要",
    "desc": "小規模宅地等の特例など課税標準を抑える制度の概要です。",
    "articleSlug": "shisanzei-kojogaku"
  },
  {
    "id": "kotei_chousei",
    "cat": "tax",
    "term": "固定資産税評価の調整",
    "reading": "こていしさんぜいひょうかのちょうせい",
    "summary": "固定資産税評価の調整の概要",
    "desc": "固定資産評価基準による標準地選定や評価の調整の考え方です。",
    "articleSlug": "kotei-chousei"
  },
  {
    "id": "shutoku_jiki_kazei",
    "cat": "tax",
    "term": "取得時期と課税関係",
    "reading": "しゅとくじきとかぜいかんけい",
    "summary": "取得時期と課税関係の概要",
    "desc": "取得時期によって適用される税制・特例が異なる場合の留意点です。",
    "articleSlug": "shutoku-jiki-kazei"
  },
  {
    "id": "shisan_keisan_kiso",
    "cat": "tax",
    "term": "譲渡所得の計算の基本",
    "reading": "じょうとしょとくのけいさんのきほん",
    "summary": "譲渡所得の計算の基本の概要",
    "desc": "譲渡所得の収入金額から必要経費を差し引いて算出する基本です。",
    "articleSlug": "shisan-keisan-kiso"
  },
  {
    "id": "tokurei_jouto",
    "cat": "tax",
    "term": "居住用財産の譲渡特例（概要）",
    "reading": "きょじゅうようざいさんのじょうととくれい",
    "summary": "居住用財産の譲渡特例（概要）の概要",
    "desc": "居住用財産を譲渡したときの3,000万円控除など代表的な軽減措置の概要です。",
    "articleSlug": "tokurei-jouto"
  },
  {
    "id": "shisan_sisan_kojyo",
    "cat": "tax",
    "term": "譲渡所得と損失の繰越控除",
    "reading": "じょうとそんしつのくりこしこうじょ",
    "summary": "譲渡所得と損失の繰越控除の概要",
    "desc": "譲渡損失を将来の譲渡所得と損益通算できる場合のイメージです。",
    "articleSlug": "shisan-sisan-kojyo"
  },
  {
    "id": "shohi_zei_keisan",
    "cat": "tax",
    "term": "不動産取引における消費税",
    "reading": "ふどうさんとりひきにおけるしょうひぜい",
    "summary": "不動産取引における消費税の概要",
    "desc": "課税売上・税率・課税仕入れの関係など取引別の消費税の考え方です。",
    "articleSlug": "shohi-zei-keisan"
  },
  {
    "id": "sozoku_mokuhyou",
    "cat": "tax",
    "term": "相続税の財産評価（不動産）",
    "reading": "そうぞくぜいのざいさんひょうか",
    "summary": "相続税の財産評価（不動産）の概要",
    "desc": "路線価方式・鑑定評価など相続財産の評価の基本です。",
    "articleSlug": "sozoku-mokuhyou"
  },
  {
    "id": "zoki_joto_kazei",
    "cat": "tax",
    "term": "敷地権の譲渡と所得税",
    "reading": "しきちけんのじょうととしょとくぜい",
    "summary": "敷地権の譲渡と所得税の概要",
    "desc": "借地権割合など敷地権譲渡所得の計算上の留意点です。",
    "articleSlug": "zoki-joto-kazei"
  },
  {
    "id": "shisan_hyouka_chika",
    "cat": "tax",
    "term": "地価公示・基準地価",
    "reading": "ちかこうじ・きじゅんちか",
    "summary": "地価公示・基準地価の概要",
    "desc": "公示価格・基準地価が評価や一般市場の参考になる関係です。",
    "articleSlug": "shisan-hyouka-chika"
  },
  {
    "id": "jutaku_loan_gensen",
    "cat": "tax",
    "term": "住宅ローンの所得税控除と源泉",
    "reading": "じゅうたくろーんのこうじょとげんせん",
    "summary": "住宅ローンの所得税控除と源泉の概要",
    "desc": "住宅ローン控除を受ける際の源泉徴収・年末調整の関係です。",
    "articleSlug": "jutaku-loan-gensen"
  },
  {
    "id": "fudosan_toshi_zeikin",
    "cat": "tax",
    "term": "不動産所得・譲渡所得・雑所得の区分",
    "reading": "ふどうさんしょとくのくぶん",
    "summary": "不動産所得・譲渡所得・雑所得の区分の概要",
    "desc": "賃貸収入・売却益・一時金など所得区分ごとの所得税の考え方です。",
    "articleSlug": "fudosan-toshi-zeikin"
  },
  {
    "id": "toki_reitenzei",
    "cat": "tax",
    "term": "登記関係の国税のまとめ",
    "reading": "とうきかんけいのこくぜいのまとめ",
    "summary": "登記関係の国税のまとめの概要",
    "desc": "登記時に課される登録免許税など国税の概要です。",
    "articleSlug": "toki-reitenzei"
  },
  {
    "id": "shisan_jojo_kisan",
    "cat": "tax",
    "term": "償却資産税",
    "reading": "しょうきゃくしさんぜい",
    "summary": "償却資産税（概要）の概要",
    "desc": "償却資産に対して課される地方税で、誰が納税義務者かの基本です。",
    "articleSlug": "shisan-jojo-kisan"
  }
];
