"""API未接続でも動作確認できるモックLLM。"""

from __future__ import annotations

from mini_mirofish.models import Agent


class MockLLM:
    """とても単純なテンプレート応答を返すクラス。"""

    def generate(self, *, agent: Agent, scenario_text: str, round_index: int, others_latest: list[str]) -> str:
        """ラウンドごとにテンプレートを変えて返す。"""
        others_summary = " / ".join(others_latest[:2]) if others_latest else "他者コメントなし"

        if round_index == 1:
            return (
                f"[{agent.name}] 初期反応: {agent.stance}の立場では、"
                f"『{scenario_text[:55]}』は{agent.concern}に影響しそうです。"
            )

        if round_index == 2:
            return (
                f"[{agent.name}] 追加反応: さきほどの議論（{others_summary}）を見て、"
                f"私は{agent.personality}に、短期的な変化を警戒します。"
            )

        return (
            f"[{agent.name}] 見通し: 今後は{agent.concern}が注目点です。"
            f"他者の意見（{others_summary}）も踏まえると、段階的な変化が起きると考えます。"
        )


class MockReporterLLM:
    """レポート要約用のモック。"""

    def summarize(self, scenario_text: str, all_utterances: list[str]) -> str:
        """最終レポートをMarkdownで返す。"""
        preview = "\n".join(f"- {u}" for u in all_utterances[:5])
        return (
            "# シミュレーションレポート（Mock）\n\n"
            "## 入力シナリオ\n"
            f"{scenario_text}\n\n"
            "## 全体の流れ\n"
            "各立場から初期反応が出た後、他者の発言を参照して意見が少し収束しました。\n\n"
            "## 対立点\n"
            "- 家計負担を優先する視点と、企業・投資の成長視点に温度差がありました。\n"
            "- 政策の即効性と副作用に関して慎重論がありました。\n\n"
            "## 起こりそうな結果\n"
            "短期では様子見が増え、中期では政策・価格・投資行動のバランス調整が進みそうです。\n\n"
            "## 発言プレビュー\n"
            f"{preview}\n"
        )
