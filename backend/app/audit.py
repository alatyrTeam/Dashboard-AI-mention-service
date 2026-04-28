from __future__ import annotations

import typing

import json
import uuid
from collections.abc import Mapping
from typing import Any


def _serialize_details(details: typing.Optional[Mapping[str, Any]]) -> typing.Optional[str]:
    if not details:
        return None
    return json.dumps(details, ensure_ascii=False, default=str, separators=(",", ":"))


def decode_details_json(raw_details: typing.Optional[str]) -> dict[str, object]:
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
    actor_user_id: typing.Optional[uuid.UUID] = None,
    actor_email: typing.Optional[str] = None,
    actor_username: typing.Optional[str] = None,
    entity_type: typing.Optional[str] = None,
    entity_id: typing.Optional[str] = None,
    path: typing.Optional[str] = None,
    method: typing.Optional[str] = None,
    status_code: typing.Optional[int] = None,
    duration_ms: typing.Optional[int] = None,
    details: typing.Optional[Mapping[str, Any]] = None,
) -> None:
    return
