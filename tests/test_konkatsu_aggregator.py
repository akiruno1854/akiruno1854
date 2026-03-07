import json
import tempfile
import unittest
from pathlib import Path

from konkatsu_poc.aggregate_parties import (
    load_site_manifests,
    load_user_settings,
    merge_and_filter,
    merge_and_filter_from_manifests,
)


class TestKonkatsuAggregator(unittest.TestCase):
    def test_merge_and_filter_by_age(self):
        with tempfile.TemporaryDirectory() as d:
            p1 = Path(d) / "a.json"
            p2 = Path(d) / "b.json"
            p1.write_text(
                json.dumps([
                    {
                        "id": "x1",
                        "site": "IBJ",
                        "title": "A",
                        "date": "2026-03-20",
                        "start_time": "19:00",
                        "end_time": "20:00",
                        "location": "Tokyo",
                        "age_min": 30,
                        "age_max": 39,
                        "price_male": 5000,
                        "price_female": 2000,
                        "url": "https://example.com/a",
                    }
                ]),
                encoding="utf-8",
            )
            p2.write_text(
                json.dumps([
                    {
                        "id": "x2",
                        "site": "TMS",
                        "title": "B",
                        "date": "2026-03-19",
                        "start_time": "19:00",
                        "end_time": "20:00",
                        "location": "Tokyo",
                        "age_min": 40,
                        "age_max": 49,
                        "price_male": 5000,
                        "price_female": 2000,
                        "url": "https://example.com/b",
                    }
                ]),
                encoding="utf-8",
            )

            rows = merge_and_filter([p1, p2], target_age=35)
            self.assertEqual([r.id for r in rows], ["x1"])

    def test_auto_discovered_sites_and_user_settings(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            sites_dir = root / "konkatsu_poc" / "sites"
            data_dir = root / "konkatsu_poc" / "data"
            config_dir = root / "konkatsu_poc" / "config"
            sites_dir.mkdir(parents=True)
            data_dir.mkdir(parents=True)
            config_dir.mkdir(parents=True)

            (sites_dir / "site_a.json").write_text(
                json.dumps(
                    {
                        "site_id": "site_a",
                        "display_name": "Site A",
                        "official_url": "https://a.example.com",
                        "search_url": "https://a.example.com/search",
                        "data_path": "konkatsu_poc/data/a.json",
                    }
                ),
                encoding="utf-8",
            )
            (sites_dir / "site_b.json").write_text(
                json.dumps(
                    {
                        "site_id": "site_b",
                        "display_name": "Site B",
                        "official_url": "https://b.example.com",
                        "search_url": "https://b.example.com/search",
                        "data_path": "konkatsu_poc/data/b.json",
                    }
                ),
                encoding="utf-8",
            )

            (data_dir / "a.json").write_text(
                json.dumps([
                    {
                        "id": "a-1",
                        "title": "A event",
                        "date": "2026-03-20",
                        "start_time": "18:00",
                        "end_time": "19:00",
                        "location": "Tokyo",
                        "age_min": 30,
                        "age_max": 39,
                        "price_male": 5000,
                        "price_female": 2000,
                        "url": "https://a.example.com/event",
                    }
                ]),
                encoding="utf-8",
            )
            (data_dir / "b.json").write_text(
                json.dumps([
                    {
                        "id": "b-1",
                        "title": "B event",
                        "date": "2026-03-21",
                        "start_time": "18:00",
                        "end_time": "19:00",
                        "location": "Yokohama",
                        "age_min": 40,
                        "age_max": 49,
                        "price_male": 5000,
                        "price_female": 2000,
                        "url": "https://b.example.com/event",
                    }
                ]),
                encoding="utf-8",
            )

            local_settings = config_dir / "user_settings.local.json"
            local_settings.write_text(
                json.dumps({"target_age": 35, "enabled_site_ids": ["site_a"]}),
                encoding="utf-8",
            )

            settings = load_user_settings(local_settings)
            manifests = load_site_manifests(sites_dir)
            rows = merge_and_filter_from_manifests(
                manifests,
                enabled_site_ids=set(settings["enabled_site_ids"]),
                target_age=settings["target_age"],
                repo_root=root,
            )

            self.assertEqual([r.id for r in rows], ["a-1"])
            self.assertEqual(rows[0].site, "Site A")


if __name__ == "__main__":
    unittest.main()
