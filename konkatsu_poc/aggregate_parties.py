#!/usr/bin/env python3
"""Party aggregator for local PoC.

This script auto-discovers site manifests, loads party rows from each enabled site,
filters by target age, sorts by date/time, and writes a unified JSON feed for the
local web app.
"""

from __future__ import annotations

import argparse
import json
from dataclasses import asdict, dataclass
from datetime import datetime
from pathlib import Path
from typing import Iterable


@dataclass(frozen=True)
class Party:
    id: str
    site: str
    title: str
    date: str
    start_time: str
    end_time: str
    location: str
    age_min: int
    age_max: int
    price_male: int
    price_female: int
    url: str

    def starts_at(self) -> datetime:
        return datetime.strptime(f"{self.date} {self.start_time}", "%Y-%m-%d %H:%M")

    def matches_age(self, age: int) -> bool:
        return self.age_min <= age <= self.age_max


@dataclass(frozen=True)
class SiteManifest:
    site_id: str
    display_name: str
    official_url: str
    search_url: str
    data_path: str


def load_json(path: Path) -> dict | list:
    with path.open("r", encoding="utf-8") as fp:
        return json.load(fp)


def load_site_manifests(manifest_dir: Path) -> list[SiteManifest]:
    manifests: list[SiteManifest] = []
    for path in sorted(manifest_dir.glob("*.json")):
        payload = load_json(path)
        manifests.append(
            SiteManifest(
                site_id=payload["site_id"],
                display_name=payload["display_name"],
                official_url=payload["official_url"],
                search_url=payload["search_url"],
                data_path=payload["data_path"],
            )
        )
    return manifests


def load_user_settings(path: Path) -> dict:
    if path.exists():
        payload = load_json(path)
        if not isinstance(payload, dict):
            raise ValueError(f"invalid user settings format: {path}")
        return payload

    raise FileNotFoundError(
        f"user settings not found: {path} (copy user_settings.example.json to user_settings.local.json)"
    )


def load_parties(path: Path, *, fallback_site_name: str) -> list[Party]:
    payload = load_json(path)
    if not isinstance(payload, list):
        raise ValueError(f"invalid parties data format: {path}")

    rows: list[Party] = []
    for row in payload:
        normalized = dict(row)
        normalized.setdefault("site", fallback_site_name)
        rows.append(Party(**normalized))
    return rows


def merge_and_filter(paths: Iterable[Path], target_age: int) -> list[Party]:
    rows: list[Party] = []
    for path in paths:
        rows.extend(load_parties(path, fallback_site_name="Unknown"))
    filtered = [row for row in rows if row.matches_age(target_age)]
    return sorted(filtered, key=lambda row: row.starts_at())


def merge_and_filter_from_manifests(
    manifests: Iterable[SiteManifest],
    *,
    enabled_site_ids: set[str],
    target_age: int,
    repo_root: Path,
) -> list[Party]:
    rows: list[Party] = []
    for manifest in manifests:
        if enabled_site_ids and manifest.site_id not in enabled_site_ids:
            continue
        data_path = (repo_root / manifest.data_path).resolve()
        rows.extend(load_parties(data_path, fallback_site_name=manifest.display_name))

    filtered = [row for row in rows if row.matches_age(target_age)]
    return sorted(filtered, key=lambda row: row.starts_at())


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Aggregate and filter party candidates")
    parser.add_argument(
        "--user-config",
        default="konkatsu_poc/config/user_settings.local.json",
        help="User settings JSON path",
    )
    parser.add_argument(
        "--site-manifests-dir",
        default="konkatsu_poc/sites",
        help="Directory containing per-site manifest JSON files",
    )
    parser.add_argument(
        "--output",
        default="konkatsu_poc/web/aggregated_parties.json",
        help="Output JSON file",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    repo_root = Path(__file__).resolve().parent.parent

    user_settings = load_user_settings((repo_root / args.user_config).resolve())
    target_age = int(user_settings.get("target_age", 35))
    enabled_site_ids = set(user_settings.get("enabled_site_ids", []))

    manifests = load_site_manifests((repo_root / args.site_manifests_dir).resolve())
    merged = merge_and_filter_from_manifests(
        manifests,
        enabled_site_ids=enabled_site_ids,
        target_age=target_age,
        repo_root=repo_root,
    )

    output_path = (repo_root / args.output).resolve()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8") as fp:
        json.dump([asdict(row) for row in merged], fp, ensure_ascii=False, indent=2)

    print(f"wrote {len(merged)} rows -> {output_path}")


if __name__ == "__main__":
    main()
