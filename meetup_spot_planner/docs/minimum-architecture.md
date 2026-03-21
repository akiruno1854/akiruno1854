# 最低限アーキテクチャ設計（MVP）

## 1. 全体構成（ローカルWebサーバー前提）
1. フロントエンドが待ち合わせ地点・条件を送信
2. Backend APIが候補検索を実行
3. 外部データソース（Google Maps等）またはFixtureから候補を収集
4. 正規化・重複排除・フィルタを適用
5. 入りやすさスコアを計算
6. 地図描画用データとランキングをレスポンス
7. フロントエンドで地図プロットと一覧表示

## 2. コンポーネント
- Frontend (Map UI)
  - 地図表示、ピン描画、ランキング表示、条件入力
- Search API
  - 地点・条件を受け取って検索パイプラインを実行
- Place Aggregator
  - 地図系/予約系/口コミ系データを統合
- Filter Engine
  - 距離・カテゴリ・営業時間による絞り込み
- Scoring Engine
  - ルールベースで入りやすさを計算
- Presentation Mapper
  - UI表示に必要な整形（ピン情報、理由文）

## 3. データモデル（最小）
- place_id
- name
- lat/lng
- category
- open_status
- reservation_status
- crowd_estimation
- atmosphere_tags
- distance_from_meetup
- easiness_score
- recommendation_reason
- evidence_summary

## 4. API最小仕様
- `POST /api/search`
  - request: meetup_point, time, headcount, purpose_tags
  - response: map_markers[], ranked_places[]
- `GET /api/health`
  - response: service status

## 5. 更新戦略
- 検索時にライブ取得 + 短期キャッシュ
- 変動が少ない店舗基本情報は日次更新
- ユーザー報告（将来）で混雑推定を補正

## 6. 拡張し続けるための設計原則
- 外部連携は `infra` 層に閉じ込め、API依存を局所化する
- `domain/scoring` を独立させ、実験的な重み調整を容易にする
- Fixtureで再現できるテストデータを保持し、API障害時でも検証を継続可能にする

## 7. 初期リスクと対策
- 予約可否の鮮度が低い
  - 対策: 情報更新時刻の表示、予約リンク優先
- カフェ利用可否の判定誤差
  - 対策: 文脈キーワード判定 + ユーザー報告で補正
- 外部API障害で結果が出ない
  - 対策: フィクスチャへのフォールバックとエラーメッセージ明示
