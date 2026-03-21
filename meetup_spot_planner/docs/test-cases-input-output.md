# テストケース（Input / Output 基準）

## 1. API I/Oテスト

### TC-API-001 正常系: 最低限検索
- Input
```json
{
  "meetup_point": "新宿南口",
  "purpose_tags": ["conversation", "quiet"]
}
```
- Expected Output
  - HTTP 200
  - `map_markers` が1件以上
  - `ranked_places` が `easiness_score` 降順

### TC-API-002 異常系: meetup_point欠落
- Input
```json
{
  "purpose_tags": ["conversation"]
}
```
- Expected Output
  - HTTP 422（バリデーションエラー）
  - エラー詳細JSONを返す

### TC-API-003 異常系: headcount範囲外
- Input
```json
{
  "meetup_point": "新宿南口",
  "headcount": 0
}
```
- Expected Output
  - HTTP 422
  - `headcount` の制約違反が含まれる

## 2. 外部API取込テスト

### TC-UP-001 正常系: 上流JSON→内部スキーマ正規化
- Upstream Input
  - Place Search APIのサンプルJSON
- Expected Output
  - `place_id/name/lat/lng/category/open_status` が正規化される

### TC-UP-002 欠損系: opening_hoursが無い
- Upstream Input
```json
{
  "results": [{"id": "x1", "name": "NoHour Cafe", "geometry": {"location": {"lat": 1, "lng": 2}}}]
}
```
- Expected Output
  - `open_status` は既定値（falseまたはunknown相当）
  - 処理継続して候補生成可能

### TC-UP-003 失敗系: 上流APIタイムアウト
- Input
  - 上流API呼び出しがtimeout
- Expected Output
  - fixtureフォールバック動作
  - HTTP 200（fallback結果あり）またはHTTP 502（fallbackなし）
  - ログに `upstream_timeout` を記録

## 3. スコアリングテスト

### TC-SCORE-001 単調性
- Input
  - 同カテゴリ2店: A(近い,予約可,混雑低), B(遠い,予約不可,混雑高)
- Expected Output
  - `score(A) > score(B)`

### TC-SCORE-002 目的タグ加点
- Input
  - 店舗タグに `conversation` を含む候補 + requestで `purpose_tags=[conversation]`
- Expected Output
  - タグ一致店舗に加点が入る

## 4. E2Eテスト

### TC-E2E-001 UIで一連処理
- 手順
  1. Web UIを開く
  2. meetup_point入力
  3. 検索ボタン押下
- Expected Output
  - 地図ピン表示
  - おすすめ一覧表示
  - 1位候補の理由文が表示

## 5. 受け入れ判定（MVP）
- 上記の正常系TCがすべてPass
- 異常系で5xx乱発がない（設計したエラーコードで応答）
- 外部API障害時でもサービス継続戦略（fallback）が機能する
