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

`past_questions.csv` が無い、または空のときは、リポジトリ直下の **`takken-master-data.js`** の `BASE_QUESTIONS` を自動的に読み込んで静的ページを生成します（`--no-js-fallback` で無効化）。

