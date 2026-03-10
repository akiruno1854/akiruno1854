"""会話ログを要約してMarkdownレポートにするモジュール。"""

from __future__ import annotations

from mini_mirofish.models import Utterance


class Reporter:
    """レポート生成の司令塔。"""

    def __init__(self, reporter_llm) -> None:
        self.reporter_llm = reporter_llm

    def create_report(self, scenario_text: str, utterances: list[Utterance]) -> str:
        """全発言を文字列化して要約を作る。"""
        all_utterances = [f"R{u.round_index} {u.agent_name}: {u.text}" for u in utterances]
        return self.reporter_llm.summarize(scenario_text, all_utterances)
