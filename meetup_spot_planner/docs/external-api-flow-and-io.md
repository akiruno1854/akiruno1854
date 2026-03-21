# 外部API連携フロー（OpenSearch/Map API想定）

## 1. 目的
外部APIから返るJSONの揺れを吸収し、アプリ内部で一貫した処理を行うためのフローを定義する。

## 2. 処理フロー（フローチャート）

```mermaid
flowchart TD
    A[ユーザー入力: meetup_point, tags, headcount] --> B[Search API: 入力バリデーション]
    B -->|OK| C[Geocoding APIで待ち合わせ地点を座標化]
    B -->|NG| Z1[400 Bad Request]

    C --> D[Place Search API呼び出し]
    D --> E[Reservation/Review API呼び出し(任意)]

    D --> F[生データJSON受信]
    E --> F

    F --> G[Normalizer: 共通スキーマへ変換]
    G --> H[Filter: 距離/カテゴリ/営業時間]
    H --> I[Scoring: 入りやすさ算出]
    I --> J[ランキング整形 + 理由生成]
    J --> K[レスポンスJSON返却]

    C -->|失敗| Z2[502 Upstream Error]
    D -->|失敗| L[Fixtureフォールバック]
    E -->|失敗| L
    L --> G
```

## 3. 外部APIレスポンス例（想定）

### 3.1 Place Search API（上流）
```json
{
  "results": [
    {
      "id": "abc123",
      "name": "Cafe Example",
      "geometry": {"location": {"lat": 35.68, "lng": 139.70}},
      "types": ["cafe", "restaurant"],
      "opening_hours": {"open_now": true},
      "rating": 4.1,
      "user_ratings_total": 212
    }
  ]
}
```

### 3.2 Reservation API（上流）
```json
{
  "shop_id": "abc123",
  "reservation": {
    "status": "bookable",
    "next_available": "2026-03-21T10:30:00+09:00"
  }
}
```

## 4. 正規化後の内部共通スキーマ（下流）
```json
{
  "place_id": "abc123",
  "name": "Cafe Example",
  "lat": 35.68,
  "lng": 139.70,
  "category": "cafe",
  "open_status": true,
  "reservation_status": "bookable",
  "crowd_estimation": "medium",
  "atmosphere_tags": ["conversation"],
  "distance_from_meetup_m": 380
}
```

## 5. OpenSearch/Map API連携で先にやるべき順序
1. バリデーション + エラーレスポンス統一
2. GeocodingとPlace Searchの最小連携
3. Normalizer実装（欠損・型ブレ吸収）
4. Filter/Scoring実装
5. Reservation/Review API統合
6. 失敗時フォールバックと観測ログ追加
