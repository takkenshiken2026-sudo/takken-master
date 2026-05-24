# 過去問 CSV（静的ページ生成）

静的な過去問一覧・問題ページ（`q/index.html` および `q/past/...`）は、`past_questions.csv` を置いてからビルドします。

```bash
python3 tools/build_past_question_pages.py
```

## CSV の形式

列は賃管マスター（chintaikanrishi-master）の `data/past_questions.csv` と同一のヘッダーを想定しています。

参考ヘッダー:

```
exam_year,exam_wareki,question_no,type,category,tags,stem,preamble,statement_a,statement_b,statement_c,statement_d,choice_1,choice_2,choice_3,choice_4,correct,is_exempt,is_invalidated,note,explanation
```

このファイルを **`data/past_questions.csv`** に保存するか、`python3 tools/build_past_question_pages.py --csv /path/to/past_questions.csv` でパスを指定してください。

`past_questions.csv` が無い、または空のときは、`takken-master-data-past.js` をフォールバックに使えます（`--no-js-fallback` で無効化）。

## 実践演習 CSV

`practice_questions.csv` は `takken-data-original.js` から次で生成します。

```bash
python3 tools/export_orig_to_practice_csv.py
python3 tools/build_practice_question_pages.py
```

静的ページは `q/orig/id{問題ID}/index.html`（全1,000問）に出力されます。`build_all.py` でも上記が自動実行されます。

追加列: `level`, `unit`, `unit_label`, `field`（ビルド用。`question_no` は ORIG の id と同一）

## 模試セット CSV

```bash
python3 tools/generate_mock_sets.py
python3 tools/build_mock_pages.py
```

静的ページは `q/mock/index.html` および `q/mock/{1..5}/index.html`（各50問のリンク一覧）に出力されます。アプリ連携ハッシュ: `#mock-play-{回}`, `#past-play-{appId}`, `#orig-play-{id}`。

