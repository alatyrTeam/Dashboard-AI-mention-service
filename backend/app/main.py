from __future__ import annotations

import time
from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from backend.app.audit import record_log
from backend.app.api.routes import router
from backend.app.migrations.runner import run_pending_migrations


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DIST_DIR = PROJECT_ROOT / "dist"


app = FastAPI(title="Rankberry Dashboard API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(router)


@app.middleware("http")
async def audit_api_requests(request: Request, call_next):
    path = request.url.path
    if not path.startswith("/api/"):
        return await call_next(request)
    if path in {"/api/health", "/api/logs"}:
        return await call_next(request)
    if request.headers.get("x-audit-source", "").strip().lower() == "auto":
        return await call_next(request)
    if request.method.upper() == "OPTIONS":
        return await call_next(request)

    started_at = time.perf_counter()
    try:
        response = await call_next(request)
    except Exception as error:
        duration_ms = max(int((time.perf_counter() - started_at) * 1000), 0)
        actor = getattr(request.state, "current_user", None)
        record_log(
            level="error",
            category="api",
            action=f"{request.method.upper()} {path}",
            message=f"{request.method.upper()} {path} failed",
            actor_user_id=getattr(actor, "user_id", None),
            actor_email=getattr(actor, "email", None),
            path=path,
            method=request.method.upper(),
            status_code=500,
            duration_ms=duration_ms,
            details={
                "query": dict(request.query_params),
                "error": str(error),
            },
        )
        raise

    duration_ms = max(int((time.perf_counter() - started_at) * 1000), 0)
    actor = getattr(request.state, "current_user", None)
    status_code = int(response.status_code)
    level = "info"
    if status_code >= 500:
        level = "error"
    elif status_code >= 400:
        level = "warning"

    record_log(
        level=level,
        category="api",
        action=f"{request.method.upper()} {path}",
        message=f"{request.method.upper()} {path} -> {status_code}",
        actor_user_id=getattr(actor, "user_id", None),
        actor_email=getattr(actor, "email", None),
        path=path,
        method=request.method.upper(),
        status_code=status_code,
        duration_ms=duration_ms,
        details={
            "query": dict(request.query_params),
            "source": request.headers.get("x-audit-source", "user").strip().lower() or "user",
        },
    )
    return response


@app.on_event("startup")
def startup() -> None:
    run_pending_migrations()


if DIST_DIR.exists():
    app.mount("/", StaticFiles(directory=str(DIST_DIR), html=True), name="frontend")
