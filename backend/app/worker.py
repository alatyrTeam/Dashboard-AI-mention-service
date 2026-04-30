from __future__ import annotations

import logging
import threading
import time

from sqlalchemy.exc import OperationalError

from backend.app.config import get_settings
from backend.app.logging_config import configure_logging
from backend.app.migrations.runner import run_pending_migrations
from backend.app.service_container import get_run_service
from backend.app.utils import compact_error_message


logger = logging.getLogger("rankberry.worker")


def worker_loop(worker_name: str) -> None:
    settings = get_settings()
    service = get_run_service()
    logger.info("worker_loop_started worker=%s poll_seconds=%s", worker_name, settings.queue_poll_seconds)

    while True:
        try:
            claimed = service.claim_next_run()
        except OperationalError as error:
            error_message = compact_error_message(error)
            logger.exception("run_claim_failed worker=%s error=%s", worker_name, error_message)
            time.sleep(settings.queue_poll_seconds)
            continue

        if claimed is None:
            time.sleep(settings.queue_poll_seconds)
            continue

        try:
            logger.info(
                "run_claimed worker=%s run_id=%s user_id=%s project=%s keyword=%s",
                worker_name,
                claimed.id,
                claimed.user_id,
                claimed.project or "-",
                claimed.keyword,
            )
            final_status = service.process_claimed_run(claimed)
        except Exception as error:
            error_message = compact_error_message(error)
            logger.exception(
                "run_failed worker=%s run_id=%s user_id=%s project=%s error=%s",
                worker_name,
                claimed.id,
                claimed.user_id,
                claimed.project or "-",
                error_message,
            )
        else:
            log_method = logger.warning if final_status == "stopped" else logger.info
            log_method(
                "run_finished worker=%s run_id=%s user_id=%s project=%s status=%s",
                worker_name,
                claimed.id,
                claimed.user_id,
                claimed.project or "-",
                final_status,
            )


def main() -> None:
    configure_logging()
    settings = get_settings()
    logger.info("worker_startup concurrency=%s", settings.worker_concurrency)
    run_pending_migrations()
    logger.info("worker_startup migrations=complete")

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
