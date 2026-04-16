from __future__ import annotations

import typing

from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker
from sqlalchemy.pool import NullPool, StaticPool

from backend.app.config import get_settings


class Base(DeclarativeBase):
    pass


def build_engine(
    database_url: str,
    *,
    pool_mode: typing.Optional[str] = None,
    pool_size: int = 1,
    max_overflow: int = 0,
):
    kwargs: dict[str, object] = {"future": True}
    if database_url.startswith("sqlite"):
        kwargs["connect_args"] = {"check_same_thread": False}
        if ":memory:" in database_url:
            kwargs["poolclass"] = StaticPool
    else:
        kwargs["pool_pre_ping"] = True
        normalized_pool_mode = (pool_mode or "null").strip().lower()
        if normalized_pool_mode == "null":
            # Avoid keeping idle Postgres connections checked out across reloads,
            # workers, and multiple local processes on low-connection providers.
            kwargs["poolclass"] = NullPool
        elif normalized_pool_mode == "queue":
            kwargs["pool_size"] = max(pool_size, 1)
            kwargs["max_overflow"] = max(max_overflow, 0)
            kwargs["pool_timeout"] = 30
            kwargs["pool_recycle"] = 1800
        else:
            raise ValueError(f"Unsupported DB_POOL_MODE: {pool_mode}")
    return create_engine(database_url, **kwargs)


settings = get_settings()
# settings.database_url is the runtime URL and may be rewritten to the
# Supabase transaction pooler on port 6543 by config.py.
engine = build_engine(
    settings.database_url,
    pool_mode=settings.db_pool_mode,
    pool_size=settings.db_pool_size,
    max_overflow=settings.db_max_overflow,
)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, expire_on_commit=False)


def get_db_session() -> Generator[Session, None, None]:
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()
