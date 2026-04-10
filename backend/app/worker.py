from __future__ import annotations

import threading
import time

from backend.app.audit import record_log
from backend.app.config import get_settings
from backend.app.migrations.runner import run_pending_migrations
from backend.app.service_container import get_run_service
from backend.app.utils import compact_error_message


def worker_loop(worker_name: str) -> None:
    settings = get_settings()
    service = get_run_service()

    while True:
        claimed = service.claim_next_run()
        if claimed is None:
            time.sleep(settings.queue_poll_seconds)
            continue

        try:
            record_log(
                category="worker",
                action="run.claimed",
                message=f"{worker_name} claimed run {claimed.id}",
                actor_user_id=claimed.user_id,
                entity_type="run",
                entity_id=str(claimed.id),
                details={
                    "worker": worker_name,
                    "keyword": claimed.keyword,
                    "project": claimed.project,
                },
            )
            final_status = service.process_claimed_run(claimed)
        except Exception as error:
            error_message = compact_error_message(error)
            print(f"[{worker_name}] run {claimed.id} failed: {error_message}")
            record_log(
                level="error",
                category="worker",
                action="run.failed",
                message=f"{worker_name} run {claimed.id} failed",
                actor_user_id=claimed.user_id,
                entity_type="run",
                entity_id=str(claimed.id),
                details={
                    "worker": worker_name,
                    "error": error_message,
                },
            )
        else:
            print(f"[{worker_name}] run {claimed.id} {final_status}")
            record_log(
                level="warning" if final_status == "stopped" else "info",
                category="worker",
                action=f"run.{final_status}",
                message=f"{worker_name} run {claimed.id} {final_status}",
                actor_user_id=claimed.user_id,
                entity_type="run",
                entity_id=str(claimed.id),
                details={
                    "worker": worker_name,
                    "status": final_status,
                },
            )


def main() -> None:
    settings = get_settings()
    run_pending_migrations()

    threads: list[threading.Thread] = []
    for index in range(settings.worker_concurrency):
        thread = threading.Thread(
            target=worker_loop,
            args=(f"worker-{index + 1}",),
            daemon=False,
        )
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()


if __name__ == "__main__":
    main()
