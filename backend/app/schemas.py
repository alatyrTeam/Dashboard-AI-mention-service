from __future__ import annotations

import uuid

from pydantic import BaseModel, Field


class ProfileUpsertRequest(BaseModel):
    username: str = Field(min_length=1, max_length=80)


class DraftRowPayload(BaseModel):
    keyword: str = ""
    domain: str = ""
    brand: str = ""
    prompt: str = ""
    project: str = ""


class DraftPayload(BaseModel):
    keyword: str = ""
    domain: str = ""
    brand: str = ""
    prompt: str = ""
    project: str = ""
    rows: list[DraftRowPayload] = Field(default_factory=list)


class DraftAppendPayload(BaseModel):
    rows: list[DraftRowPayload] = Field(default_factory=list)


class RunStartRequest(BaseModel):
    keyword: str
    domain: str
    brand: str
    prompt: str
    project: str = ""


class BulkRunActionResponse(BaseModel):
    run_ids: list[str] = Field(default_factory=list)
    total_runs: int = 0
    status: str


class HistoryForwardRequest(BaseModel):
    run_ids: list[uuid.UUID] = Field(min_length=1)
    target_user_id: uuid.UUID


class HistoryForwardResponse(BaseModel):
    run_ids: list[str] = Field(default_factory=list)
    total_runs: int = 0
    outputs_updated: int = 0
    results_updated: int = 0
    target_user_id: str
