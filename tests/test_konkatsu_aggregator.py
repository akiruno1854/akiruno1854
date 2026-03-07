import json
import tempfile
import unittest
from pathlib import Path

from konkatsu_poc.aggregate_parties import merge_and_filter


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


if __name__ == "__main__":
    unittest.main()
