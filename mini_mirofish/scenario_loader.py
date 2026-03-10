"""入力テキストを受け取る責務だけを持つモジュール。"""

from __future__ import annotations


def load_scenario_text(raw_text: str) -> str:
    """ユーザー入力を軽く整形して返す。

    - 空白だけの入力はエラー
    - 前後の空白は除去
    """
    text = raw_text.strip()
    if not text:
        raise ValueError("入力テキストが空です。ニュースや政策の文章を1つ入力してください。")
    return text
