import os
import unittest
from types import SimpleNamespace
from unittest.mock import patch

from sqlalchemy.exc import OperationalError

os.environ.setdefault("DATABASE_URL", "sqlite+pysqlite:///:memory:")

from backend.app.worker import worker_loop


class FakeWorkerService:
    def __init__(self) -> None:
        self.calls = 0

    def claim_next_run(self):
        self.calls += 1
        if self.calls == 1:
            raise OperationalError("SELECT 1", {}, RuntimeError("SSL connection has been closed unexpectedly"))
        return None


class WorkerResilienceTests(unittest.TestCase):
    def test_claim_next_run_transient_sql_error_does_not_kill_loop(self) -> None:
        service = FakeWorkerService()
        settings = SimpleNamespace(queue_poll_seconds=0)

        with (
            patch("backend.app.worker.get_settings", return_value=settings),
            patch("backend.app.worker.get_run_service", return_value=service),
            patch("backend.app.worker.record_log"),
            patch("backend.app.worker.time.sleep", side_effect=[None, StopIteration()]),
        ):
            with self.assertRaises(StopIteration):
                worker_loop("worker-1")

        self.assertEqual(service.calls, 2)


if __name__ == "__main__":
    unittest.main()
