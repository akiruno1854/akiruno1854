"""ファイル保存（JSON / Markdown）を担当。"""

from __future__ import annotations

import json
from pathlib import Path

from mini_mirofish.models import SimulationResult


def save_simulation_log(result: SimulationResult, path: str = "simulation_log.json") -> Path:
    """シミュレーション全体をJSONで保存。"""
    out_path = Path(path)
    out_path.write_text(json.dumps(result.to_dict(), ensure_ascii=False, indent=2), encoding="utf-8")
    return out_path


def save_report_markdown(report_markdown: str, path: str = "report.md") -> Path:
    """最終レポートをMarkdownで保存。"""
    out_path = Path(path)
    out_path.write_text(report_markdown, encoding="utf-8")
    return out_path
