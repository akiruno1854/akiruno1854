#!/usr/bin/env python3
import argparse
import base64
import json
import time
import urllib.error
import urllib.request
from typing import Optional


class OpenSearchMigrator:
    def __init__(self, base_url: str, auth: Optional[tuple[str, str]] = None) -> None:
        self.base_url = base_url.rstrip("/")
        self.auth = auth

    def _request(self, method: str, path: str, payload: Optional[dict] = None) -> dict:
        url = f"{self.base_url}{path}"
        body = None if payload is None else json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(url=url, data=body, method=method)
        req.add_header("Content-Type", "application/json")
        if self.auth:
            token = base64.b64encode(f"{self.auth[0]}:{self.auth[1]}".encode("utf-8")).decode("ascii")
            req.add_header("Authorization", f"Basic {token}")

        try:
            with urllib.request.urlopen(req, timeout=30) as res:
                text = res.read().decode("utf-8")
                return json.loads(text) if text else {}
        except urllib.error.HTTPError as e:
            detail = e.read().decode("utf-8", errors="ignore")
            raise RuntimeError(f"{method} {url} failed: {e.code} {detail}") from e

    def create_or_update_repo(self, repo_name: str, repo_body: dict) -> dict:
        return self._request("PUT", f"/_snapshot/{repo_name}", repo_body)

    def create_snapshot(self, repo_name: str, snapshot_name: str, indices: str) -> dict:
        payload = {
            "indices": indices,
            "ignore_unavailable": True,
            "include_global_state": False,
        }
        return self._request("PUT", f"/_snapshot/{repo_name}/{snapshot_name}", payload)

    def snapshot_status(self, repo_name: str, snapshot_name: str) -> dict:
        return self._request("GET", f"/_snapshot/{repo_name}/{snapshot_name}")

    def restore_snapshot(self, repo_name: str, snapshot_name: str, indices: str) -> dict:
        payload = {
            "indices": indices,
            "ignore_unavailable": True,
            "include_global_state": False,
            "rename_pattern": "^(.+)$",
            "rename_replacement": "$1",
        }
        return self._request("POST", f"/_snapshot/{repo_name}/{snapshot_name}/_restore", payload)


def wait_until_snapshot_success(client: OpenSearchMigrator, repo_name: str, snapshot_name: str, wait_seconds: int) -> None:
    deadline = time.time() + wait_seconds
    while time.time() < deadline:
        result = client.snapshot_status(repo_name, snapshot_name)
        state = result.get("snapshots", [{}])[0].get("state")
        if state == "SUCCESS":
            return
        if state in {"FAILED", "PARTIAL"}:
            raise RuntimeError(f"snapshot ended with state={state}: {result}")
        time.sleep(3)
    raise TimeoutError(f"snapshot did not complete within {wait_seconds} seconds")


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="OpenSearch snapshot migration helper")
    p.add_argument("--source-url", required=True)
    p.add_argument("--target-url", required=True)
    p.add_argument("--source-user")
    p.add_argument("--source-pass")
    p.add_argument("--target-user")
    p.add_argument("--target-pass")
    p.add_argument("--repo-name", required=True)
    p.add_argument("--repo-settings-json", help='Repository JSON body. If omitted, uses fs repo with --repo-path')
    p.add_argument("--repo-path", help="Used only when --repo-settings-json is omitted")
    p.add_argument("--snapshot-name", required=True)
    p.add_argument("--indices", required=True, help="comma separated indices")
    p.add_argument("--wait-seconds", type=int, default=300)
    return p.parse_args()


def main() -> None:
    args = parse_args()

    if args.repo_settings_json:
        repo_body = json.loads(args.repo_settings_json)
    else:
        if not args.repo_path:
            raise ValueError("--repo-path is required when --repo-settings-json is not set")
        repo_body = {"type": "fs", "settings": {"location": args.repo_path, "compress": True}}

    source_auth = (args.source_user, args.source_pass) if args.source_user and args.source_pass else None
    target_auth = (args.target_user, args.target_pass) if args.target_user and args.target_pass else None

    source = OpenSearchMigrator(args.source_url, source_auth)
    target = OpenSearchMigrator(args.target_url, target_auth)

    print("[1/4] configuring snapshot repository on source")
    source.create_or_update_repo(args.repo_name, repo_body)

    print("[2/4] configuring snapshot repository on target")
    target.create_or_update_repo(args.repo_name, repo_body)

    print("[3/4] creating snapshot")
    source.create_snapshot(args.repo_name, args.snapshot_name, args.indices)

    print("[3.5/4] waiting snapshot completion")
    wait_until_snapshot_success(source, args.repo_name, args.snapshot_name, args.wait_seconds)

    print("[4/4] restoring snapshot on target")
    result = target.restore_snapshot(args.repo_name, args.snapshot_name, args.indices)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
