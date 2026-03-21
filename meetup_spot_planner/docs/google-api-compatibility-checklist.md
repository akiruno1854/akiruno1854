# Google API 互換性チェックリスト（結合前確認）

## 1. Nearby Search(New)
- [ ] Endpoint が `v1/places:searchNearby` になっている
- [ ] HTTP Method が `POST`
- [ ] `X-Goog-Api-Key` を送っている
- [ ] `X-Goog-FieldMask` を送っている
- [ ] Request Body に `locationRestriction.circle.center/radius` がある
- [ ] 応答の `places[]` をパースしている（`results[]` 前提にしていない）

## 2. Geocoding
- [ ] meetup_point から緯度経度を取得できる
- [ ] ゼロ件時に 404/422 相当で扱う

## 3. 正規化
- [ ] `displayName.text` 欠損時のフォールバックあり
- [ ] `currentOpeningHours.openNow` 欠損時の既定値あり
- [ ] `types` から `category` を決定できる

## 4. 障害時
- [ ] 上流 timeout / 5xx 時に fallback 可能
- [ ] fallback 不可時に 502 を返す
- [ ] ログに upstream エラー情報を残す
