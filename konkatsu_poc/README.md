# 婚活パーティー統合アプリ PoC (ローカル再現用)

「IBJ / TMS など複数サイトの候補を一画面にまとめ、年代フィルターし、予定管理する」ための最小プロトタイプです。

## できること（PoC）

- サイト設定（`konkatsu_poc/sites/*.json`）を**自動検出**して候補JSONを統合
- ユーザー設定（`target_age`, `enabled_site_ids`）を外部ファイルで管理
- 年代（20/30/40代）で候補表示を切り替え（Web UI）
- 「予定に入れる」でローカルスケジュール管理（`localStorage`）
- 予定を `ICS` として出力し、Google/Apple カレンダーへ取り込み可能

## 公式サイト情報（マニフェストで管理）

PoCでは、以下の公式サイト情報を `konkatsu_poc/sites/*.json` に保持しています。

- IBJ（PARTY☆PARTY）: `https://www.partyparty.jp/`
- TMS（FIORE PARTY）: `https://www.fiore-party.com/`

> 注意: 本PoCはサイトの公開情報・URLを基にしたローカル検証用で、ログイン操作や自動予約は実装していません。

## 環境構築

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## 初期設定（Git管理しない個人設定）

```bash
cp konkatsu_poc/config/user_settings.example.json \
   konkatsu_poc/config/user_settings.local.json
```

`konkatsu_poc/config/user_settings.local.json` は `.gitignore` 済みです。

```json
{
  "target_age": 35,
  "enabled_site_ids": ["ibj_partyparty", "tms_fiore"]
}
```

## 実行手順

```bash
# 1) 候補データを統合（ユーザー設定 + サイト自動検出）
python konkatsu_poc/aggregate_parties.py

# 2) 静的サーバー起動
python -m http.server 8000

# 3) ブラウザで開く
# http://localhost:8000/konkatsu_poc/web/
```

## サイトを追加する方法

1. `konkatsu_poc/sites/` に新しい `<site_id>.json` を追加
2. `data_path` にパーティーJSON（同じスキーマ）を指定
3. `user_settings.local.json` の `enabled_site_ids` に `site_id` を追加

例:

```json
{
  "site_id": "new_site",
  "display_name": "New Site",
  "official_url": "https://example.com/",
  "search_url": "https://example.com/search",
  "data_path": "konkatsu_poc/data/new_site_sample.json"
}
```

## 注意

- 本PoCのイベントデータはサンプルを含みます。
- 各サイトへの自動アクセス/スクレイピングは、利用規約・法令・robots への準拠が必要です。
