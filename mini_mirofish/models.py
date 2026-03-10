"""データ構造をまとめるファイル。

難しいフレームワークは使わず、標準ライブラリの dataclass だけで管理します。
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import List


@dataclass
class Agent:
    """エージェント1人分の定義。"""

    name: str
    stance: str
    personality: str
    concern: str
    memory: List[str]


@dataclass
class Utterance:
    """1回の発言ログ。"""

    round_index: int
    agent_name: str
    text: str


@dataclass
class SimulationResult:
    """シミュレーション結果のまとまり。"""

    scenario_text: str
    agents: List[Agent]
    utterances: List[Utterance]
    report_markdown: str

    def to_dict(self) -> dict:
        """JSON保存用に辞書へ変換。"""
        return {
            "scenario_text": self.scenario_text,
            "agents": [asdict(agent) for agent in self.agents],
            "utterances": [asdict(u) for u in self.utterances],
            "report_markdown": self.report_markdown,
        }
