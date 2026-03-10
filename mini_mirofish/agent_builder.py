"""5人の固定エージェントを作るモジュール。"""

from __future__ import annotations

from mini_mirofish.models import Agent


def build_default_agents() -> list[Agent]:
    """学習用に固定の5人を返す。"""
    return [
        Agent(
            name="個人投資家・葵",
            stance="資産を増やしたい個人投資家",
            personality="慎重だがチャンスには敏感",
            concern="株価、金利、為替の変化",
            memory=[],
        ),
        Agent(
            name="政策担当者・誠",
            stance="社会の安定を重視する政策担当者",
            personality="ロジカルで公平性を重視",
            concern="物価、雇用、社会的な影響",
            memory=[],
        ),
        Agent(
            name="消費者・遥",
            stance="家計を守りたい一般消費者",
            personality="現実的で生活目線",
            concern="生活費、賃金、サービス価格",
            memory=[],
        ),
        Agent(
            name="記者・蓮",
            stance="事実を整理して伝える記者",
            personality="好奇心が強く客観的",
            concern="世論、信頼できる情報、論点整理",
            memory=[],
        ),
        Agent(
            name="企業経営者・凛",
            stance="利益と持続成長を目指す企業経営者",
            personality="決断が速く実務的",
            concern="コスト、需要、投資計画",
            memory=[],
        ),
    ]
