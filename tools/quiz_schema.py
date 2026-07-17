# -*- coding: utf-8 -*-
"""問題ページ（過去問・実践演習・一問一答）向け schema.org Quiz 構造化データ。

Google の教育リッチリザルト（Practice problems / Education Q&A）対応。
必須要素: Quiz.about, Quiz.hasPart(Question), Question.eduQuestionType,
Question.text, Question.acceptedAnswer, Question.suggestedAnswer。
不正データ（選択肢不足・正答不明・出題無効）では None を返し出力しない。
"""

from __future__ import annotations


def _norm_text(value: object) -> str:
    return str(value or "").strip()


def quiz_jsonld(page: dict, *, question_type: str = "multiple") -> dict | None:
    """page dict から Quiz 構造化データ（1 問）を生成。生成不可なら None。

    question_type:
      "multiple"  … 4択（page["opts"] と 1 始まりの page["correct"]）
      "marubatsu" … ○×一問一答（page["correct_answer"] が bool）
    """
    # 過去問・実践演習は stem_plain、一問一答は statement を問題文に持つ。
    stem = _norm_text(page.get("stem_plain")) or _norm_text(page.get("statement"))
    if not stem:
        return None

    about_name = _norm_text(page.get("category")) or "宅地建物取引士試験"

    if question_type == "marubatsu":
        correct = page.get("correct_answer")
        if correct is None:
            return None
        maru = {"@type": "Answer", "text": "○（正しい）", "position": 0, "encodingFormat": "text/markdown"}
        batsu = {"@type": "Answer", "text": "×（誤り）", "position": 1, "encodingFormat": "text/markdown"}
        accepted = maru if correct else batsu
        suggested = [batsu] if correct else [maru]
    else:
        opts = list(page.get("opts") or [])
        cor = page.get("correct")
        if len(opts) < 2 or cor is None:
            return None
        try:
            idx = int(cor) - 1
        except (TypeError, ValueError):
            return None
        if not (0 <= idx < len(opts)):
            return None
        accepted = {
            "@type": "Answer",
            "text": _norm_text(opts[idx]),
            "position": idx,
            "encodingFormat": "text/markdown",
        }
        suggested = [
            {
                "@type": "Answer",
                "text": _norm_text(o),
                "position": i,
                "encodingFormat": "text/markdown",
            }
            for i, o in enumerate(opts)
            if i != idx
        ]

    if not accepted.get("text") or not suggested:
        return None

    question = {
        "@type": "Question",
        "eduQuestionType": "Multiple choice",
        "text": stem,
        "learningResourceType": "Practice problem",
        "acceptedAnswer": accepted,
        "suggestedAnswer": suggested,
    }
    return {
        "@type": "Quiz",
        "about": {"@type": "Thing", "name": about_name},
        "educationalLevel": "宅地建物取引士試験",
        "hasPart": question,
    }
