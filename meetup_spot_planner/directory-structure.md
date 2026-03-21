# ディレクトリ構成検討メモ

## 方針
- 新規サービスを独立サブフォルダ `meetup_spot_planner/` として管理する
- 構想・要件・設計資料はこのサブフォルダ直下の `docs/` に集約する
- 将来的な実装（API / Web / バッチ）を見据え、最初から「拡張し続けられる骨格」を定義する

## 推奨構成（実装開始時）

```text
meetup_spot_planner/
├── concept.md
├── directory-structure.md
├── docs/
│   ├── review-and-readiness.md
│   ├── minimum-requirements.md
│   ├── minimum-architecture.md
│   ├── implementation-plan.md
│   ├── minimum-test-cases.md
│   ├── external-api-flow-and-io.md
│   ├── test-cases-input-output.md
│   ├── google-api-compatibility-checklist.md
│   └── tech-stack.md
├── app/
│   ├── backend/              # Webサーバー/API
│   └── frontend/             # 地図表示UI
├── domain/
│   ├── models/               # Place等のドメインモデル
│   └── scoring/              # 入りやすさスコア
├── infra/
│   ├── maps/                 # Google Maps等の取得アダプタ
│   ├── reservation/          # 予約可否データ連携
│   └── cache/                # キャッシュ実装
├── tests/
│   ├── unit/
│   ├── integration/
│   └── e2e/
└── data/
    ├── fixtures/             # テスト用固定データ
    └── snapshots/            # 検証用スナップショット
```

## ドキュメント配置の決定
- **決定**: ドキュメント系フォルダは `meetup_spot_planner/docs/` に配置する。
- 理由:
  - 新サービス単位で自己完結し、既存プロジェクトへ影響しない
  - 企画→要件→設計→実装→テストの導線が分かりやすい
  - 実装開始後も同一ツリーで更新しやすく、拡張方針を保ちやすい
