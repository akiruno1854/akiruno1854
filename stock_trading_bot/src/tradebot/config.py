from pathlib import Path
import tomllib
from pydantic import BaseModel


class AppConfig(BaseModel):
    mode: str
    timezone: str


class BrokerConfig(BaseModel):
    provider: str
    api_base_url: str
    api_key: str
    api_secret: str


class RiskConfig(BaseModel):
    max_daily_loss_pct: float
    max_position_per_symbol_pct: float
    max_consecutive_losses: int


class ScreeningConfig(BaseModel):
    universe: list[str]
    min_avg_turnover_jpy: int
    max_candidates: int


class ReportConfig(BaseModel):
    output_dir: str


class Settings(BaseModel):
    app: AppConfig
    broker: BrokerConfig
    risk: RiskConfig
    screening: ScreeningConfig
    report: ReportConfig


def load_settings(path: Path) -> Settings:
    with path.open("rb") as f:
        raw = tomllib.load(f)
    return Settings.model_validate(raw)
