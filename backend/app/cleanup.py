from __future__ import annotations

import logging
from datetime import timedelta

from sqlalchemy import delete, select

from backend.app.config import get_settings
from backend.app.db import SessionLocal
from backend.app.logging_config import configure_logging
from backend.app.models import Output, Run
from backend.app.utils import utcnow


logger = logging.getLogger("rankberry.cleanup")


def cleanup_old_outputs() -> int:
    settings = get_settings()
    cutoff = utcnow() - timedelta(days=settings.raw_output_retention_days)
    logger.info("cleanup_old_outputs_started retention_days=%s cutoff=%s", settings.raw_output_retention_days, cutoff.isoformat())

    with SessionLocal() as session:
        finished_run_ids = select(Run.id).where(Run.finished_at.is_not(None), Run.finished_at < cutoff)
        result = session.execute(
            delete(Output).where(Output.run_id.in_(finished_run_ids), Output.created_at < cutoff)
        )
        session.commit()
        deleted = int(result.rowcount or 0)
        logger.info("cleanup_old_outputs_finished deleted_rows=%s", deleted)
        return deleted


if __name__ == "__main__":
    configure_logging()
    deleted = cleanup_old_outputs()
    logger.info("cleanup_command_finished deleted_rows=%s", deleted)
