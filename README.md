# OpenSearch Index Migration Toolkit

OpenSearch/Elasticsearch 7.x 相当の既存クラスターから、より新しい OpenSearch クラスターへ、
**スナップショット経由でインデックス移行**を行うための最小ツールキットです。

> 想定ユースケース:
> - インポート元: OpenSearch 1.x（Elasticsearch 7.10 互換、7.9 系に近い運用）
> - インポート先: OpenSearch 2.x
> - 実行環境: AWS CloudShell などの Bash + Python 環境

## 構成

- `scripts/migrate_snapshot.py`
  - Snapshot repository 登録
  - Snapshot 作成
  - Snapshot 完了待機
  - 先クラスターで Snapshot restore
- `scripts/migrate_snapshot.sh`
  - CloudShell で実行しやすいラッパー
- `docker-compose.yml`
  - ローカル検証用（source: OpenSearch 1.3 / target: OpenSearch 2.11）
- `tests/test_migrate_snapshot.py`
  - HTTP API 呼び出しロジックのユニットテスト

## クイックスタート

### 1) 依存関係

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 2) ローカル検証環境起動

```bash
docker compose up -d
```

### 3) テストデータ投入（source 側）

```bash
curl -s -X PUT 'http://localhost:9201/demo-index' -H 'Content-Type: application/json' -d '{"settings":{"number_of_shards":1,"number_of_replicas":0}}'
curl -s -X POST 'http://localhost:9201/demo-index/_doc/1?refresh=true' -H 'Content-Type: application/json' -d '{"message":"hello from source"}'
```

### 4) マイグレーション実行

```bash
python scripts/migrate_snapshot.py \
  --source-url http://localhost:9201 \
  --target-url http://localhost:9202 \
  --repo-name localfs \
  --repo-path /snapshots \
  --snapshot-name snap-demo \
  --indices demo-index \
  --wait-seconds 120
```

### 5) 移行結果確認（target 側）

```bash
curl -s 'http://localhost:9202/demo-index/_search?pretty'
```

## CloudShell での使い方

```bash
export SOURCE_URL='https://source.example.com'
export TARGET_URL='https://target.example.com'
export REPO_NAME='s3repo'
export REPO_SETTINGS='{"type":"s3","settings":{"bucket":"my-bucket","base_path":"snapshots","region":"ap-northeast-1"}}'
export SNAPSHOT_NAME='snap-20260306'
export INDICES='index-a,index-b'

bash scripts/migrate_snapshot.sh
```

必要に応じて Basic 認証:

```bash
export SOURCE_USER='admin'
export SOURCE_PASS='password'
export TARGET_USER='admin'
export TARGET_PASS='password'
```

## 注意点

- 異なるメジャーバージョン間移行は、インデックス作成バージョンによって restore 失敗することがあります。
- その場合は、
  1) 中間クラスター経由で再index
  2) `_reindex` from remote
  を検討してください。
- 本ツールは最小実装のため、運用では IAM/証明書/暗号化設定の厳密化を推奨します。
