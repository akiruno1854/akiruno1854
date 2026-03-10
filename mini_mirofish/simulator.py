"""3ターンの会話シミュレーションを実行するモジュール。"""

from __future__ import annotations

from mini_mirofish.models import Agent, Utterance


class Simulator:
    """エージェント同士を順番に発言させる。"""

    def __init__(self, llm_client) -> None:
        self.llm_client = llm_client

    def run(self, scenario_text: str, agents: list[Agent], total_rounds: int = 3) -> list[Utterance]:
        """ラウンド形式で会話ログを生成。"""
        utterances: list[Utterance] = []

        for round_index in range(1, total_rounds + 1):
            for agent in agents:
                others_latest = self._get_others_latest_comments(agents, current_agent_name=agent.name)
                text = self.llm_client.generate(
                    agent=agent,
                    scenario_text=scenario_text,
                    round_index=round_index,
                    others_latest=others_latest,
                )
                agent.memory.append(text)
                utterances.append(Utterance(round_index=round_index, agent_name=agent.name, text=text))

        return utterances

    @staticmethod
    def _get_others_latest_comments(agents: list[Agent], current_agent_name: str) -> list[str]:
        """他者の直近発言だけを取り出す（長くなりすぎないよう短縮）。"""
        latest: list[str] = []
        for agent in agents:
            if agent.name == current_agent_name:
                continue
            if agent.memory:
                short_text = agent.memory[-1].replace("\n", " ")[:80]
                latest.append(f"{agent.name}: {short_text}")
        return latest
