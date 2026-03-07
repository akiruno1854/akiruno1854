#!/usr/bin/env python3
"""Simple party aggregator for local PoC.

This script merges sample JSON files from multiple matching-party sites,
filters by target age, sorts by date/time, and writes a unified JSON feed
for the demo web app.
"""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass, asdict
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


def load_parties(path: Path) -> list[Party]:
    with path.open("r", encoding="utf-8") as fp:
        payload = json.load(fp)
    return [Party(**row) for row in payload]


def merge_and_filter(paths: Iterable[Path], target_age: int) -> list[Party]:
    rows: list[Party] = []
    for path in paths:
        rows.extend(load_parties(path))
    filtered = [row for row in rows if row.matches_age(target_age)]
    return sorted(filtered, key=lambda row: row.starts_at())


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Aggregate and filter party candidates")
    parser.add_argument("--target-age", type=int, default=35, help="Target age for filtering")
    parser.add_argument(
        "--inputs",
        nargs="+",
        default=["konkatsu_poc/data/ibj_sample.json", "konkatsu_poc/data/tms_sample.json"],
        help="Input JSON files",
    )
    parser.add_argument(
        "--output",
        default="konkatsu_poc/web/aggregated_parties.json",
        help="Output JSON file",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    input_paths = [Path(p) for p in args.inputs]
    merged = merge_and_filter(input_paths, target_age=args.target_age)

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8") as fp:
        json.dump([asdict(row) for row in merged], fp, ensure_ascii=False, indent=2)

    print(f"wrote {len(merged)} rows -> {output_path}")


if __name__ == "__main__":
    main()
