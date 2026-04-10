from __future__ import annotations

import uuid
from datetime import datetime

from sqlalchemy import DateTime, Float, Integer, String, Text, Uuid, func
from sqlalchemy.orm import Mapped, mapped_column

from backend.app.db import Base
from backend.app.utils import utcnow


class Profile(Base):
    __tablename__ = "Dashboard_AI_check_profiles"

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(Uuid, nullable=False)
    username: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now(), default=utcnow
    )


class Draft(Base):
    __tablename__ = "Dashboard_AI_check_drafts"

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(Uuid, nullable=False)
    keyword: Mapped[str | None] = mapped_column(Text)
    domain: Mapped[str | None] = mapped_column(Text)
    brand: Mapped[str | None] = mapped_column(Text)
    prompt: Mapped[str | None] = mapped_column(Text)
    project: Mapped[str | None] = mapped_column(Text)
    rows_json: Mapped[str | None] = mapped_column(Text)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        default=utcnow,
        onupdate=utcnow,
    )


class Run(Base):
    __tablename__ = "Dashboard_AI_check_runs"

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(Uuid, nullable=False)
    keyword: Mapped[str] = mapped_column(Text, nullable=False)
    domain: Mapped[str] = mapped_column(Text, nullable=False)
    brand: Mapped[str] = mapped_column(Text, nullable=False)
    prompt: Mapped[str] = mapped_column(Text, nullable=False)
    project: Mapped[str | None] = mapped_column(Text)
    status: Mapped[str] = mapped_column(String(32), nullable=False, default="queued", server_default="queued")
    total_iterations: Mapped[int] = mapped_column(Integer, nullable=False, default=3, server_default="3")
    completed_iterations: Mapped[int] = mapped_column(
        Integer, nullable=False, default=0, server_default="0"
    )
    error_messages: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now(), default=utcnow
    )
    started_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    finished_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))


class Output(Base):
    __tablename__ = "Dashboard_AI_check_outputs"

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(Uuid, nullable=False)
    run_id: Mapped[uuid.UUID] = mapped_column(Uuid, nullable=False)
    iteration_number: Mapped[int] = mapped_column(Integer, nullable=False)
    gpt_output: Mapped[str | None] = mapped_column(Text)
    gem_output: Mapped[str | None] = mapped_column(Text)
    gpt_domain_mention: Mapped[bool] = mapped_column(nullable=False, default=False, server_default="false")
    gem_domain_mention: Mapped[bool] = mapped_column(nullable=False, default=False, server_default="false")
    gpt_brand_mention: Mapped[bool] = mapped_column(nullable=False, default=False, server_default="false")
    gem_brand_mention: Mapped[bool] = mapped_column(nullable=False, default=False, server_default="false")
    response_count: Mapped[float | None] = mapped_column(Float)
    brand_list: Mapped[str | None] = mapped_column(Text)
    citation_format: Mapped[str | None] = mapped_column(Text)
    openai_generation_cost_usd: Mapped[float | None] = mapped_column(Float)
    gemini_generation_cost_usd: Mapped[float | None] = mapped_column(Float)
    gemini_analysis_cost_usd: Mapped[float | None] = mapped_column(Float)
    project: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now(), default=utcnow
    )


class RunResult(Base):
    __tablename__ = "Dashboard_AI_check_run_results"

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(Uuid, nullable=False)
    run_id: Mapped[uuid.UUID] = mapped_column(Uuid, nullable=False)
    project: Mapped[str | None] = mapped_column(Text)
    gpt_domain_mention: Mapped[bool] = mapped_column(nullable=False, default=False, server_default="false")
    gem_domain_mention: Mapped[bool] = mapped_column(nullable=False, default=False, server_default="false")
    gpt_brand_mention: Mapped[bool] = mapped_column(nullable=False, default=False, server_default="false")
    gem_brand_mention: Mapped[bool] = mapped_column(nullable=False, default=False, server_default="false")
    response_count_avg: Mapped[float | None] = mapped_column(Float)
    brand_list: Mapped[str | None] = mapped_column(Text)
    citation_format: Mapped[str | None] = mapped_column(Text)
    sentiment_analysis: Mapped[str | None] = mapped_column(Text)
    gemini_sentiment_cost_usd: Mapped[float | None] = mapped_column(Float)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now(), default=utcnow
    )


class AppLog(Base):
    __tablename__ = "Dashboard_AI_check_logs"

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now(), default=utcnow
    )
    level: Mapped[str] = mapped_column(String(16), nullable=False, default="info", server_default="info")
    category: Mapped[str] = mapped_column(String(32), nullable=False, default="api", server_default="api")
    action: Mapped[str] = mapped_column(Text, nullable=False)
    message: Mapped[str] = mapped_column(Text, nullable=False)
    actor_user_id: Mapped[uuid.UUID | None] = mapped_column(Uuid)
    actor_email: Mapped[str | None] = mapped_column(Text)
    actor_username: Mapped[str | None] = mapped_column(Text)
    entity_type: Mapped[str | None] = mapped_column(Text)
    entity_id: Mapped[str | None] = mapped_column(Text)
    path: Mapped[str | None] = mapped_column(Text)
    method: Mapped[str | None] = mapped_column(String(16))
    status_code: Mapped[int | None] = mapped_column(Integer)
    duration_ms: Mapped[int | None] = mapped_column(Integer)
    details_json: Mapped[str | None] = mapped_column(Text)
