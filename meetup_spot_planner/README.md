# meetup_spot_planner

待ち合わせ地点を起点に「入りやすい」候補店を提案する、ローカル実行可能なMVPです。

## 技術スタック（シンプル構成）
- Backend: FastAPI + Uvicorn
- Frontend: 素のHTML/JavaScript + Leaflet（地図表示）
- Data: まずはJSON Fixture（DBなし）

### DB方針
- **現時点ではDBを使わない**（実装速度優先）
- 将来拡張で SQLite/PostgreSQL を追加可能なように、データ取得は `infra` 層に分離

## 起動方法（ローカル）
```bash
cd meetup_spot_planner
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.backend.main:app --reload
```

- API Docs: http://127.0.0.1:8000/docs
- Web UI: http://127.0.0.1:8000/

## 現在のAPI
- `GET /api/health`
- `POST /api/search`
