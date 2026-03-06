#!/usr/bin/env bash
set -euo pipefail

: "${SOURCE_URL:?SOURCE_URL is required}"
: "${TARGET_URL:?TARGET_URL is required}"
: "${REPO_NAME:?REPO_NAME is required}"
: "${SNAPSHOT_NAME:?SNAPSHOT_NAME is required}"
: "${INDICES:?INDICES is required}"

ARGS=(
  --source-url "$SOURCE_URL"
  --target-url "$TARGET_URL"
  --repo-name "$REPO_NAME"
  --snapshot-name "$SNAPSHOT_NAME"
  --indices "$INDICES"
  --wait-seconds "${WAIT_SECONDS:-300}"
)

if [[ -n "${REPO_SETTINGS:-}" ]]; then
  ARGS+=(--repo-settings-json "$REPO_SETTINGS")
else
  : "${REPO_PATH:?REPO_PATH is required when REPO_SETTINGS is not set}"
  ARGS+=(--repo-path "$REPO_PATH")
fi

if [[ -n "${SOURCE_USER:-}" && -n "${SOURCE_PASS:-}" ]]; then
  ARGS+=(--source-user "$SOURCE_USER" --source-pass "$SOURCE_PASS")
fi

if [[ -n "${TARGET_USER:-}" && -n "${TARGET_PASS:-}" ]]; then
  ARGS+=(--target-user "$TARGET_USER" --target-pass "$TARGET_PASS")
fi

python3 scripts/migrate_snapshot.py "${ARGS[@]}"
