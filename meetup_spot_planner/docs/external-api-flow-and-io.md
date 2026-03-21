# 外部API連携フロー（Google Maps Places API準拠）

## 1. 目的
Google Maps APIの実仕様に合わせて、結合時に壊れない前提を固定する。

## 2. 事前確認した仕様ポイント（公式ドキュメント）
- Nearby Search (New) は **HTTP POST** + JSON Body
- エンドポイントは `https://places.googleapis.com/v1/places:searchNearby`
- `X-Goog-FieldMask` は **必須**（未指定はエラー）
- 応答は `results` ではなく **`places` 配列**
- 地点検索（住所→座標）は Geocoding API を併用

## 3. 処理フロー（フローチャート）

```mermaid
flowchart TD
    A[ユーザー入力: meetup_point, tags, headcount] --> B[Search API: 入力バリデーション]
    B -->|OK| C[Geocoding APIで待ち合わせ地点を座標化]
    B -->|NG| Z1[422 Validation Error]

    C --> D[Places Nearby Search(New) POST]
    D --> E[places[] JSON受信]
    E --> F[Normalizer: 内部スキーマへ変換]
    F --> G[Filter: 距離/カテゴリ/営業時間]
    G --> H[Scoring: 入りやすさ算出]
    H --> I[ランキング整形 + 理由生成]
    I --> J[レスポンスJSON返却]

    C -->|失敗| Z2[502 Upstream Error]
    D -->|失敗| L[Fixtureフォールバック]
    L --> F
```

## 4. Google Places Nearby Search(New) リクエスト例
```http
POST https://places.googleapis.com/v1/places:searchNearby
X-Goog-Api-Key: API_KEY
X-Goog-FieldMask: places.id,places.displayName,places.location,places.types,places.currentOpeningHours
Content-Type: application/json
```

```json
{
  "includedTypes": ["cafe", "restaurant"],
  "maxResultCount": 10,
  "locationRestriction": {
    "circle": {
      "center": {"latitude": 35.6895, "longitude": 139.6917},
      "radius": 800.0
    }
  }
}
```

## 5. Google Places Nearby Search(New) 応答例
```json
{
  "places": [
    {
      "id": "ChIJ...",
      "displayName": {"text": "Cafe Example", "languageCode": "ja"},
      "location": {"latitude": 35.68, "longitude": 139.70},
      "types": ["cafe", "food", "point_of_interest"],
      "currentOpeningHours": {"openNow": true}
    }
  ]
}
```

## 6. 正規化後の内部共通スキーマ（下流）
```json
{
  "place_id": "ChIJ...",
  "name": "Cafe Example",
  "lat": 35.68,
  "lng": 139.70,
  "category": "cafe",
  "open_status": true,
  "reservation_status": "unknown",
  "crowd_estimation": "medium",
  "atmosphere_tags": [],
  "distance_from_meetup_m": 380
}
```

## 7. 実装順序（結合失敗を防ぐ順）
1. Nearby Search(New) のリクエスト/ヘッダを固定化（FieldMask含む）
2. `places[]` → 内部スキーマのNormalizer実装
3. 欠損ケース（`displayName`, `currentOpeningHours`なし）をテスト
4. フィルタ/スコアリングに接続
5. 上流エラー時フォールバックと監視ログ追加
