from __future__ import annotations

from pathlib import Path
from urllib.parse import urlencode

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from starlette.responses import RedirectResponse

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
async def normalize_supabase_auth_confirm_path(request: Request, call_next):
    stripped_path = request.scope.get("path", "").lstrip("/")
    if stripped_path == "auth/confirm":
        request.scope["path"] = "/auth/confirm"
    return await call_next(request)


@app.on_event("startup")
def startup() -> None:
    run_pending_migrations()


@app.get("//auth/confirm", include_in_schema=False)
@app.get("/auth/confirm", include_in_schema=False)
def confirm_supabase_auth_link(request: Request) -> RedirectResponse:
    query_params = request.query_params
    params = {
        key: value
        for key, value in {
            "token_hash": query_params.get("token_hash"),
            "type": query_params.get("type"),
            "error": query_params.get("error"),
            "error_code": query_params.get("error_code"),
            "error_description": query_params.get("error_description"),
        }.items()
        if value
    }
    target = f"/?{urlencode(params)}" if params else "/"
    return RedirectResponse(url=target, status_code=303)


if DIST_DIR.exists():
    app.mount("/", StaticFiles(directory=str(DIST_DIR), html=True), name="frontend")
