# アフィリエイト運用メモ — 宅建マスター（takken-master）

手順の正本: [multi-site-affiliate-workflow.md](./multi-site-affiliate-workflow.md)  
リポジトリ: https://github.com/takkenshiken2026-sudo/takken-master

## サイト情報

| 項目 | 値 |
|------|-----|
| site-id | `takken-master` |
| ドメイン | https://takken-master.jp |
| 棚卸し日 | 2026-06-19 |
| 目標 | ASP リンク済み比較記事 **10 本前後**（現在 **4 本**） |

---

## フェーズA 棚卸し結果（2026-06-19）

### サマリー

| 指標 | 値 |
|------|-----|
| アフィリエイト行（CSV） | 5（公開 4 + draft 1） |
| `content_status=published` | 5 |
| **ASP リンク済み（ビルド可能）** | **5**（公開 5） |
| brief YAML | 5 |
| `images/affiliate/` | 14 webp |
| `guideIndexPicks` | **設定済み**（grid-3・3 枚） |
| 通常ガイド published | 46 |
| 通常ガイド → 比較記事（related_links） | **36 / 46** |
| 通常ガイド → 比較記事（本文 slug） | **36 / 46** |
| リライトスクリプト | 4 本（公開 slug と 1:1） |

`validate_csv.py`: **passed**（アフィリエイト 4/10 本の WARN のみ）

---

## 公開済み比較記事

| slug | comparison_kind | ASP | brief | rewrite |
|------|-----------------|-----|-------|---------|
| `affiliate-textbooks-recommend` | books | Amazon | ✅ | ✅ |
| `affiliate-problem-books` | books | Amazon | ✅ | ✅ |
| `affiliate-mock-exam-materials` | books | Amazon | ✅ | ✅ |
| `affiliate-correspondence-course` | courses | A8 | ✅ | ✅ |

---

## 未着手（標準 slug・6 本）

ASP URL 確定前は **brief だけ下書き可**。CSV 追記・HTML 生成は URL 確定後。

| 優先 | slug | genre | 主 ASP | 検索意図・備考 | ブロッカー |
|------|------|-------|--------|----------------|------------|
| 1 | `affiliate-beginner-material-set` | 学習計画 | mixed | 初学者の 3 点セット。既存 3 比較記事へのハブ記事 | セット構成・Amazon/A8 URL |
| 2 | `affiliate-online-course-compare` | 独学対策 | mixed | **公開済**（スタディング afb + 資格スクエア A8） | — |
| 3 | `affiliate-cram-school` | 独学対策 | A8 | 予備校・通学/オンライン塾 | A8 プログラム有無 |
| 4 | `affiliate-retake-short-course` | 学習計画 | A8 | 再受験短期。`takken-saishuken` から導線 | 講座・教材 URL |
| 5 | `affiliate-free-vs-paid-study` | 独学対策 | internal | 無料演習 vs 有料教材。ASP 弱め可 | 内部導線設計 |
| 6 | `affiliate-qualification-support-service` | 受験・申込 | A8 | 申込代行系。**宅建は RETIO 直申込が正本のため省略可** | 該当サービス有無 |

### 重複回避メモ

- **`affiliate-correspondence-course`（公開済）** = 通信講座 4 社比較
- **`affiliate-online-course-compare`** = 買い切り/月額型オンライン講座に寄せる（SMART 等）。通信 4 選の写しにしない
- **`affiliate-beginner-material-set`** = 既存 3 比較記事（テキスト・問題集・模試）＋通信講座への導線ハブ

---

## guideIndexPicks（現状）

`site-config.json` — layout: `grid-3`、3 枚固定

| kind | href | 画像 |
|------|------|------|
| 講座 | `affiliate-correspondence-course/` | `takken-course-shikaku-square.webp` |
| テキスト | `affiliate-textbooks-recommend/` | `takken-book-b0gln6zmnf.webp` |
| 問題集 | `affiliate-problem-books/` | `takken-book-4300119287.webp` |

新記事公開後も **3 枚固定**（mock-exam 等は一覧カードに載せない設計）。

---

## 通常ガイド導線

- **36 / 46 本** が比較記事へ接続済み（`apply_affiliate_funnel_expansion.py` 実行済み）
- **未接続 10 本**（合格率・合格後・費用・会場・転職等 — 意図的除外含む）
- 新規比較記事公開後: `apply_affiliate_funnel_expansion.py` にマッピング追記 → 再実行

---

## 画像

- ディレクトリ: `images/affiliate/`（13 webp）
- 公開 4 本分は取得済み
- 新規 brief 追加後: `python3 tools/fetch_affiliate_product_images.py --slug {slug}`

---

## ASP メモ（非公開）

| ASP | 識別子 | 使用記事 |
|-----|--------|----------|
| Amazon Associates | `tag=ue083093-22` | textbooks / problem-books / mock-exam |
| A8.net | `a8mat=4B3TF0` 系 | correspondence-course / online-course-compare（資格スクエア） |
| afb | `y7404W-o7286096_2`（banner）/ `y7404W-E506961b`（text・参照） | correspondence-course / online-course-compare（スタディング） |

---

## 1 本追加する手順（チェックリスト）

```bash
# 0. テーマ確認
python3 tools/scaffold_affiliate_article.py --list-themes

# 1. brief 作成（テンプレ or 既存 brief をコピー）
cp docs/affiliate/theme-brief.template.yaml data/affiliate-briefs/affiliate-{theme}.yaml
# → products.*_url / related_links / comparison_kind を編集
# → 各販売ページで価格を確認して price_yen / price_label を反映

# 2. CSV 追記（URL 無しはエラーで止まる — 想定どおり）
python3 tools/scaffold_affiliate_article.py \
  --from-brief data/affiliate-briefs/affiliate-{theme}.yaml \
  --append

# 3. 本文リライト（既存4本を雛形）
#    tools/rewrites/affiliate-{theme}.py を新規作成 → CSV に適用

# 4. 画像
python3 tools/fetch_affiliate_product_images.py --slug affiliate-{theme}

# 5. 公開
#    content_status=published / fact_checked_at 更新
python3 tools/validate_csv.py
python3 tools/build_all.py

# 6. 導線（必要なら）
python3 tools/apply_affiliate_funnel_expansion.py
```

### テンプレ適用（書籍・講座）

```bash
# 書籍比較
python3 tools/apply_affiliate_article_template.py --template affiliate-textbooks-recommend

# オンライン講座比較
python3 tools/apply_affiliate_article_template.py --template affiliate-online-course-compare
```

apply 後に宅建向け商品名・ASP URL・related_links を差し替える。

---

## ロールアウト進捗

| フェーズ | 状態 | 備考 |
|----------|------|------|
| A 現状把握 | **完了** | 2026-06-19 本ファイル |
| B コア 4 本公開 | **完了** | テキスト・問題集・模試・通信講座 |
| C guideIndexPicks | **完了** | grid-3・3 ハブ |
| D 通常ガイド導線 | **部分完了** | 36/46 本 |
| E 残り 6 slug | **進行中** | 5/10 本公開 |
| F 10 本到達 | **未着手** | 目標 10 本前後 |

---

## 次のアクション

1. 残り5 slug（`affiliate-beginner-material-set` 等）の ASP 確定 → brief → リライト
2. 通常ガイドへの導線追加（`apply_affiliate_funnel_expansion.py` にマッピング追記）

---

## 関連ファイル

| パス | 用途 |
|------|------|
| `data/affiliate-briefs/*.yaml` | 商品・ASP URL |
| `data/guide_articles.csv` | 記事メタ・本文 |
| `tools/rewrites/affiliate-*.py` | 本文全面リライト |
| `docs/affiliate/README.md` | ドキュメント索引 |
| `.cursor/rules/affiliate-article.mdc` | Cursor 編集ルール |
