# takken-master

宅建マスター（`takken-master.jp`）の静的サイトです。`exam-site-shell` の構成に合わせ、サイト名・ドメイン・ナビゲーション・テーマなどは `site-config.json` で管理します。

## よく使うコマンド

```bash
python3 tools/build_all.py
python3 -m http.server 8765
```

ローカル確認: `http://127.0.0.1:8765/`

## 主な差し替えポイント

- `site-config.json`: サイト名、試験名、ドメイン、問い合わせ先、GA4 ID、分野名、公式リンク
- `site-config.js`: `site-config.json` から生成されるブラウザ用設定
- `site-theme.css`: `site-config.json` のテーマから生成される共通テーマ
- `tools/build_all.py`: 設定反映、記事・過去問・用語ページ・サイトマップ生成を一括実行

## 生成される主なページ

- `q/past/...`: 過去問の静的ページ
- `q/index.html`: 過去問一覧
- `terms/index.html`: 用語解説一覧
- `glossary/...`: 旧URLから `terms/...` へのリダイレクト
- `sitemap.xml`: index可能なHTMLから生成
