# 婚活パーティー統合アプリ PoC (ローカル再現用)

「IBJ / TMS など複数サイトの候補を一画面にまとめ、年代フィルターし、予定管理する」ための最小プロトタイプです。

## できること（PoC）

- 複数ソースのパーティーJSONを統合 (`aggregate_parties.py`)
- 年代（20/30/40代）で候補表示を切り替え（Web UI）
- 「予定に入れる」でローカルスケジュール管理（`localStorage`）
- 予定を `ICS` として出力し、Google/Apple カレンダーへ取り込み可能

## すぐ試す

```bash
# 1) 候補データを統合
python konkatsu_poc/aggregate_parties.py --target-age 35

# 2) 静的サーバー起動
python -m http.server 8000

# 3) ブラウザで開く
# http://localhost:8000/konkatsu_poc/web/
```

## なぜこの形にしたか

- **最短で再現テスト**できるよう、バックエンドを省いた静的Web中心の構成
- まずはモックデータでUX検証し、次段階でAPI連携を差し替え

## 実運用に向けた拡張案

1. 公式APIがある媒体はAPI連携へ移行
2. APIがない媒体は利用規約を確認し、許可範囲で取得手段を設計
3. バックエンド（FastAPI等）でユーザー認証/申込み状態管理
4. Google Calendar API連携で双方向同期
5. スマホ版は React Native / Flutter で同一APIを利用

## 注意

- 本PoCのデータはサンプルです。
- 各サイトへの自動アクセス/スクレイピングは、利用規約・法令・robots への準拠が必要です。
