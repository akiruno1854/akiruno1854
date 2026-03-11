# stock_trading_bot (isolated workspace)

既存の OpenSearch/婚活/MiroFish サンプルと混在しないように、株取引自動化の検討と実装を独立ディレクトリとして分離しました。

## Isolation policy

- 既存ルートの `requirements.txt` には依存を追加しない
- 本ワークスペースは `stock_trading_bot/` 以下のみで閉じる
- 実売買は `paper` モード完了まで無効化する

## Planned daily workflow

1. `plan` (寄り前): 銘柄スクリーニング
2. `run` (場中): シグナル判定 + 注文実行
3. `report` (引け後): 日次集計

## Quick start

```bash
cd stock_trading_bot
python -m venv .venv
source .venv/bin/activate
pip install -e .
cp config/settings.example.toml config/settings.local.toml
tradebot plan --date 2026-03-11
```

## Safety guardrails (default)

- デフォルトは `paper` 実行
- APIキーが未設定なら注文実行不可
- 日次損失閾値・銘柄別上限・連敗停止を設定必須

## Next steps

- broker adapter 実装（証券APIごとの実装）
- screening strategy 実装
- order/risk/report の結線
- scheduler（cron/Prefect）導入
