# takken-master

宅建マスター（[takken-master.jp](https://takken-master.jp)）の静的サイトです。構成・ビルド・検証は [exam-site-shell](https://github.com/takkenshiken2026-sudo/exam-site-shell) テンプレートに準拠しています。

## よく使うコマンド

```bash
# 初回または既存 JS/HTML から CSV を再生成する場合
python3 tools/export_legacy_data_to_csv.py

# 本番ビルド（検証込み）
python3 tools/build_all.py

# ローカル確認
python3 -m http.server 8765
```

## データの正本（`data/`）

| CSV | 内容 |
|-----|------|
| `past_questions.csv` | 過去問（481問） |
| `glossary_terms.csv` | 用語（304件） |
| `guide_articles.csv` | 試験ガイド（既存51本＋カタログ追補で約180 slug） |
| `ichimon_questions.csv` | 一問一答（サンプル行あり・増やす場合は編集） |
| `practice_questions.csv` | 実践演習（任意） |

カタログ不足分の追記: `python3 tools/scaffold_catalog_gaps.py`（初回のみ・重複実行しないこと）

## 生成される主なページ

- `articles/{slug}/index.html` … 試験ガイド（旧 `takken/` URL から移行）
- `terms/g-*.html` … 用語解説（旧 `terms/{slug}/` からハッシュ ID に変更）
- `terms/field-*/index.html` … 分野別用語ハブ
- `q/past/...` … 過去問の静的ページ

トップの SPA（`index.html`）は次を読み込みます（`build_all.py` で CSV から再生成）。

- `takken-master-data-core.js` … 分野定義・`SIMPLE_EXP`
- `takken-master-data-past.js` … 過去問（`past_questions.csv`）
- `takken-data-glossary.js` … 用語（`glossary_terms.csv`）
- `exam-site-data-ichimondou.js` … 一問一答 CSV（任意・現状は過去問からの変換が主）

`applyCsvImportedQuestions()` で過去問を SPA に反映します。静的 `q/past/` も同じ CSV から生成されます。

レガシー単体ファイル `takken-master-data.js` は参照用に残している場合がありますが、トップでは使いません。

## 設定

- `site-config.json` … サイト名・分野・`guideArticleGenres`（12区分）・ナビ・テーマ
- `privacy.html` … プライバシー（旧 `privacy-terms.html` から複製）

## レガシー URL

`build_all.py` の最後で `tools/build_legacy_redirects.py` が次へリダイレクト用 HTML を上書きします。

| 旧パス | 新パス |
|--------|--------|
| `takken/{slug}/` | `/articles/{slug}/` |
| `terms/{16桁ハッシュ}/` | `/terms/g-{hash}.html` |
| `terms/{読みやすいslug}/`（例: `junkentoshi-keikaku/`） | 対応する `/terms/g-*.html` |
| `glossary/{slug}/` | 上記と同じ `g-*.html` |
| `privacy-terms.html` | `/privacy.html` |

旧ディレクトリ本体（記事 HTML など）は残る場合があります。公開環境ではリダイレクトを有効にし、整理後に不要ファイルを削除してください。
