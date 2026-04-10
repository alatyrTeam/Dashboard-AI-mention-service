from __future__ import annotations

from functools import lru_cache

from backend.app.config import get_settings
from backend.app.db import SessionLocal
from backend.app.llm import LLMClient
from backend.app.run_service import RunService


@lru_cache(maxsize=1)
def get_run_service() -> RunService:
    settings = get_settings()
    return RunService(settings=settings, session_factory=SessionLocal, llm_client=LLMClient(settings))
