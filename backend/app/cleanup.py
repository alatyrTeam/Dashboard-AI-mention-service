from __future__ import annotations

from datetime import timedelta

from sqlalchemy import delete, select

from backend.app.audit import record_log
from backend.app.config import get_settings
from backend.app.db import SessionLocal
from backend.app.models import Output, Run
from backend.app.utils import utcnow


def cleanup_old_outputs() -> int:
    settings = get_settings()
    cutoff = utcnow() - timedelta(days=settings.raw_output_retention_days)

    with SessionLocal() as session:
        finished_run_ids = select(Run.id).where(Run.finished_at.is_not(None), Run.finished_at < cutoff)
        result = session.execute(
            delete(Output).where(Output.run_id.in_(finished_run_ids), Output.created_at < cutoff)
        )
        session.commit()
        return int(result.rowcount or 0)


if __name__ == "__main__":
    deleted = cleanup_old_outputs()
    print(f"Deleted {deleted} old raw output rows.")
    if deleted:
        settings = get_settings()
        record_log(
            category="cleanup",
            action="old_outputs.deleted",
            message=f"Deleted {deleted} old raw output rows.",
            entity_type="output",
            details={
                "deleted_rows": deleted,
                "retention_days": settings.raw_output_retention_days,
            },
        )
