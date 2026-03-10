"""CLIエントリーポイント。

実行例:
    python -m mini_mirofish.main --text "政府が新しい補助金政策を発表した"

モックモード(既定):
    LLM_MODE=mock

APIモード:
    LLM_MODE=api OPENAI_API_KEY=... OPENAI_API_BASE=... OPENAI_MODEL=...
"""

from __future__ import annotations

import argparse
import os

from mini_mirofish.agent_builder import build_default_agents
from mini_mirofish.llm_client import OpenAICompatibleLLM, OpenAICompatibleReporter
from mini_mirofish.mock_llm import MockLLM, MockReporterLLM
from mini_mirofish.models import SimulationResult
from mini_mirofish.reporter import Reporter
from mini_mirofish.scenario_loader import load_scenario_text
from mini_mirofish.simulator import Simulator
from mini_mirofish.storage import save_report_markdown, save_simulation_log


def parse_args() -> argparse.Namespace:
    """CLI引数を定義。"""
    parser = argparse.ArgumentParser(description="MiroFish超ミニマム版（学習用）")
    parser.add_argument("--text", required=True, help="ニュースや政策などの短い入力テキスト")
    return parser.parse_args()


def pick_llm_clients():
    """環境変数 LLM_MODE に応じて LLM 実装を選ぶ。"""
    mode = os.getenv("LLM_MODE", "mock").lower()

    if mode == "api":
        llm = OpenAICompatibleLLM()
        reporter_llm = OpenAICompatibleReporter(llm)
        return llm, reporter_llm, mode

    llm = MockLLM()
    reporter_llm = MockReporterLLM()
    return llm, reporter_llm, "mock"


def main() -> None:
    """一連の処理を順番に実行。"""
    args = parse_args()
    scenario_text = load_scenario_text(args.text)
    agents = build_default_agents()

    llm_client, reporter_llm, mode = pick_llm_clients()
    simulator = Simulator(llm_client)
    utterances = simulator.run(scenario_text, agents, total_rounds=3)

    reporter = Reporter(reporter_llm)
    report_markdown = reporter.create_report(scenario_text, utterances)

    result = SimulationResult(
        scenario_text=scenario_text,
        agents=agents,
        utterances=utterances,
        report_markdown=report_markdown,
    )

    log_path = save_simulation_log(result, path="simulation_log.json")
    report_path = save_report_markdown(report_markdown, path="report.md")

    print("\n=== MiroFish超ミニマム版: 実行結果 ===")
    print(f"モード: {mode}")
    print(f"入力: {scenario_text}\n")

    for utter in utterances:
        print(f"[Round {utter.round_index}] {utter.agent_name}: {utter.text}")

    print("\n--- レポート ---")
    print(report_markdown)
    print(f"\n保存完了: {log_path} / {report_path}")


if __name__ == "__main__":
    main()
