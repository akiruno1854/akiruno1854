from datetime import date
from pathlib import Path

import typer
from rich import print

from .config import load_settings
from .workflow import plan_trading_day, run_trading_day, summarize_trading_day

app = typer.Typer(help="Daily trading workflow CLI")


def _resolve_settings(settings_path: str) -> Path:
    path = Path(settings_path)
    if not path.exists():
        raise typer.BadParameter(f"settings file not found: {path}")
    return path


@app.command("plan")
def plan(
    run_date: date = typer.Option(..., "--date", help="Execution date (YYYY-MM-DD)"),
    settings: str = typer.Option("config/settings.local.toml", "--settings"),
):
    cfg = load_settings(_resolve_settings(settings))
    result = plan_trading_day(run_date, cfg)
    print({"date": str(result.run_date), "candidates": result.candidates})


@app.command("run")
def run(
    run_date: date = typer.Option(..., "--date", help="Execution date (YYYY-MM-DD)"),
    settings: str = typer.Option("config/settings.local.toml", "--settings"),
):
    cfg = load_settings(_resolve_settings(settings))
    result = run_trading_day(run_date, cfg)
    print(
        {
            "date": str(result.run_date),
            "mode": result.mode,
            "executed_orders": result.executed_orders,
        }
    )


@app.command("report")
def report(
    run_date: date = typer.Option(..., "--date", help="Execution date (YYYY-MM-DD)"),
    settings: str = typer.Option("config/settings.local.toml", "--settings"),
):
    cfg = load_settings(_resolve_settings(settings))
    result = summarize_trading_day(run_date, cfg)
    print({"date": str(result.run_date), "pnl_jpy": result.pnl_jpy, "trades": result.trades})


if __name__ == "__main__":
    app()
