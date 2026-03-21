# 技術スタック選定（初期）

## 結論
- **Backend: FastAPI**
- **Frontend: HTML + Vanilla JS + Leaflet**
- **Data Store: 当面なし（JSON Fixture）**

## 選定理由
1. FastAPIはAPI定義がシンプルで、`/docs` による確認が速い
2. Vanilla JS + Leafletは学習コストが低く、MVPで地図表示をすぐ実現できる
3. DBを入れないことで初期実装を短期間で完了できる

## DBは使うべきか？
- **MVP段階:** 使わない（運用前の要件変動に対応しやすい）
- **次段階:** SQLite（単一ノード）→ PostgreSQL（サーバー運用）へ移行

## 将来拡張の前提
- データ取得は `infra` 層へ集約し、保存先を差し替え可能にする
- `domain` 層のスコアリングはDB非依存で維持する
