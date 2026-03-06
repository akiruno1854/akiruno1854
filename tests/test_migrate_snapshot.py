import json
import unittest
from unittest.mock import patch

from scripts.migrate_snapshot import OpenSearchMigrator, wait_until_snapshot_success


class DummyResponse:
    def __init__(self, payload: dict):
        self.payload = payload

    def read(self):
        return json.dumps(self.payload).encode("utf-8")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        return False


class TestMigrateSnapshot(unittest.TestCase):
    def test_create_snapshot_payload(self):
        client = OpenSearchMigrator("http://example.com")

        with patch("urllib.request.urlopen") as mocked:
            mocked.return_value = DummyResponse({"accepted": True})
            client.create_snapshot("repo1", "snap1", "idx-a,idx-b")

            req = mocked.call_args.args[0]
            payload = json.loads(req.data.decode("utf-8"))
            self.assertEqual(payload["indices"], "idx-a,idx-b")
            self.assertFalse(payload["include_global_state"])

    def test_wait_until_snapshot_success(self):
        client = OpenSearchMigrator("http://example.com")

        with patch.object(client, "snapshot_status") as status:
            status.side_effect = [
                {"snapshots": [{"state": "IN_PROGRESS"}]},
                {"snapshots": [{"state": "SUCCESS"}]},
            ]
            wait_until_snapshot_success(client, "repo", "snap", wait_seconds=10)

    def test_wait_until_snapshot_failed(self):
        client = OpenSearchMigrator("http://example.com")

        with patch.object(client, "snapshot_status") as status:
            status.return_value = {"snapshots": [{"state": "FAILED"}]}
            with self.assertRaises(RuntimeError):
                wait_until_snapshot_success(client, "repo", "snap", wait_seconds=2)


if __name__ == "__main__":
    unittest.main()
