"""OpenAI互換APIを呼ぶための薄いラッパー。"""

from __future__ import annotations

import json
import os
from urllib import request

from mini_mirofish.models import Agent


class OpenAICompatibleLLM:
    """/chat/completions エンドポイントを叩く最小実装。"""

    def __init__(self) -> None:
        self.api_base = os.getenv("OPENAI_API_BASE", "https://api.openai.com/v1")
        self.api_key = os.getenv("OPENAI_API_KEY", "")
        self.model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

        if not self.api_key:
            raise ValueError("OPENAI_API_KEY が未設定です。APIモードでは必須です。")

    def _chat(self, system_prompt: str, user_prompt: str) -> str:
        """最小のHTTP POSTで応答本文を返す。"""
        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            "temperature": 0.7,
        }

        req = request.Request(
            url=f"{self.api_base}/chat/completions",
            data=json.dumps(payload).encode("utf-8"),
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.api_key}",
            },
            method="POST",
        )

        with request.urlopen(req, timeout=60) as res:
            body = json.loads(res.read().decode("utf-8"))
        return body["choices"][0]["message"]["content"].strip()

    def generate(self, *, agent: Agent, scenario_text: str, round_index: int, others_latest: list[str]) -> str:
        """エージェント発言を生成。"""
        system_prompt = (
            "あなたは社会シミュレーションのエージェントです。"
            "短く具体的に、2〜3文で回答してください。"
        )
        user_prompt = (
            f"シナリオ: {scenario_text}\n"
            f"ラウンド: {round_index}\n"
            f"あなたの名前: {agent.name}\n"
            f"立場: {agent.stance}\n"
            f"性格: {agent.personality}\n"
            f"関心事: {agent.concern}\n"
            f"これまでの自分の発言: {agent.memory}\n"
            f"他者の直近発言: {others_latest}\n"
            "この条件で、あなたの次の発言を1回だけ作ってください。"
        )
        return self._chat(system_prompt, user_prompt)


class OpenAICompatibleReporter:
    """最終レポート要約を作るクラス。"""

    def __init__(self, llm: OpenAICompatibleLLM) -> None:
        self.llm = llm

    def summarize(self, scenario_text: str, all_utterances: list[str]) -> str:
        """Markdown形式の要約を作る。"""
        system_prompt = "あなたは社会動向レポーターです。Markdownで簡潔にまとめてください。"
        user_prompt = (
            f"シナリオ: {scenario_text}\n"
            f"全発言: {all_utterances}\n\n"
            "次の見出しで出力してください:\n"
            "# シミュレーションレポート\n"
            "## 全体の流れ\n"
            "## 対立点\n"
            "## 起こりそうな結果\n"
        )
        return self.llm._chat(system_prompt, user_prompt)
