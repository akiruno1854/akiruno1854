from dataclasses import dataclass
from datetime import date

from .config import Settings


@dataclass
class PlanResult:
    run_date: date
    candidates: list[str]


@dataclass
class RunResult:
    run_date: date
    executed_orders: int
    mode: str


@dataclass
class ReportResult:
    run_date: date
    pnl_jpy: int
    trades: int


def plan_trading_day(run_date: date, settings: Settings) -> PlanResult:
    universe = settings.screening.universe
    return PlanResult(run_date=run_date, candidates=universe[: settings.screening.max_candidates])


def run_trading_day(run_date: date, settings: Settings) -> RunResult:
    return RunResult(run_date=run_date, executed_orders=0, mode=settings.app.mode)


def summarize_trading_day(run_date: date, _settings: Settings) -> ReportResult:
    return ReportResult(run_date=run_date, pnl_jpy=0, trades=0)
