# Rankberry Dashboard

## Production Deployment

The production setup is:

1. Build the frontend with `npm run build`.
2. Serve `dist/` with Nginx.
3. Proxy `/api` to the backend on `127.0.0.1:3001`.
4. Run the backend as a stable `systemd` service.
5. Run the worker as a separate `systemd` service.

The repository includes ready-to-install unit templates at:

- `deploy/systemd/rankberry-dashboard-backend.service`
- `deploy/systemd/rankberry-dashboard-worker.service`

Recommended production commands:

```bash
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
npm ci
npm run migrate
npm run build
```

Use the backend and worker scripts only as service entry points or for manual checks:

```bash
npm run start
npm run worker
```

## Environment

Create a root `.env` file for local runs, or point the systemd units at the same file. The backend reads the repo-root `.env` automatically.

Required runtime values still include:

- `DATABASE_URL` or `RUNTIME_DATABASE_URL`
- `MIGRATION_DATABASE_URL` if migrations should use a different connection string
- `SUPABASE_URL` or `VITE_SUPABASE_URL`
- `SUPABASE_ANON_KEY` or `VITE_SUPABASE_ANON_KEY`

The backend uses FastAPI, SQLAlchemy, a DB-backed run queue, and the shared Supabase/Postgres tables:

- `Dashboard_AI_check_profiles`
- `Dashboard_AI_check_drafts`
- `Dashboard_AI_check_runs`
- `Dashboard_AI_check_outputs`
- `Dashboard_AI_check_run_results`
- `Dashboard_AI_check_logs`

## Database Pooling

Postgres defaults to `DB_POOL_MODE=null`, which releases connections immediately after each session instead of keeping an idle pool open. That is the safer default for Supabase and other low-connection environments.

Optional database pool overrides:

- `DB_POOL_MODE=null` keeps connection usage minimal and is the recommended default.
- `DB_POOL_MODE=queue` enables SQLAlchemy's queue pool when you are on a dedicated database and want persistent pooling.
- `DB_POOL_SIZE=1` and `DB_MAX_OVERFLOW=0` control the queue pool only.

## Logs

The dashboard includes an in-app `Logs` menu instead of the external log monitor.

It shows API requests, run lifecycle events, worker claims, worker completion/failure events, and cleanup activity directly inside the UI.

To grant access, set the comma-separated `LOG_VIEWER_EMAILS` value in `.env`. The admin email from `ADMIN_EMAIL` is always allowed too.

## Maintenance

Delete old raw output rows with:

```bash
npm run cleanup
```

## Tests

Run the backend tests with:

```bash
python -m unittest discover -s tests -v
```
