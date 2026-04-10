from __future__ import annotations

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
