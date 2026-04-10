from __future__ import annotations

import json
import uuid
from collections.abc import Mapping
from typing import Any

from backend.app.db import SessionLocal
from backend.app.models import AppLog


def _serialize_details(details: Mapping[str, Any] | None) -> str | None:
    if not details:
        return None
    return json.dumps(details, ensure_ascii=False, default=str, separators=(",", ":"))


def decode_details_json(raw_details: str | None) -> dict[str, object]:
    if not raw_details:
        return {}

    try:
        parsed = json.loads(raw_details)
    except json.JSONDecodeError:
        return {"raw": raw_details}

    if isinstance(parsed, dict):
        return parsed
    return {"value": parsed}


def record_log(
    *,
    level: str = "info",
    category: str = "api",
    action: str,
    message: str,
    actor_user_id: uuid.UUID | None = None,
    actor_email: str | None = None,
    actor_username: str | None = None,
    entity_type: str | None = None,
    entity_id: str | None = None,
    path: str | None = None,
    method: str | None = None,
    status_code: int | None = None,
    duration_ms: int | None = None,
    details: Mapping[str, Any] | None = None,
) -> None:
    try:
        with SessionLocal() as session:
            session.add(
                AppLog(
                    level=level.strip().lower() or "info",
                    category=category.strip().lower() or "api",
                    action=action.strip() or "unknown",
                    message=message.strip() or action.strip() or "Log entry",
                    actor_user_id=actor_user_id,
                    actor_email=actor_email.strip().lower() if actor_email else None,
                    actor_username=actor_username.strip() if actor_username else None,
                    entity_type=entity_type.strip() if entity_type else None,
                    entity_id=entity_id.strip() if entity_id else None,
                    path=path.strip() if path else None,
                    method=method.strip().upper() if method else None,
                    status_code=status_code,
                    duration_ms=duration_ms,
                    details_json=_serialize_details(details),
                )
            )
            session.commit()
    except Exception:
        return
