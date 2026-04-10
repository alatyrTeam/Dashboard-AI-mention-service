# Rankberry Dashboard

## Backend
1. Create a local `.env` in the repo root at [DASHBOARD/.env](/d:/Rankberry/DASHBOARD/.env).
2. Install Python dependencies with `pip install -r requirements.txt`.
3. Run migrations with `npm run migrate`.
4. Start the API with `npm run server`.
5. Start the worker in a second terminal with `npm run worker`.

Postgres now defaults to `DB_POOL_MODE=null`, which releases connections immediately after each session instead of keeping an idle pool open. This is the safer default for Supabase and other low-connection environments, especially when running both the API and worker locally.

Supabase note:
- Session mode on `aws-...pooler.supabase.com:5432` was causing `MaxClientsInSessionMode`.
- Runtime API and worker connections now resolve to Supabase transaction mode on port `6543`.
- SQLAlchemy keeps using `NullPool` for Supabase / non-SQLite runtime connections.
- Migrations can use a separate `MIGRATION_DATABASE_URL`, so they do not have to share the runtime transaction URL.

Optional database pool overrides:
- `DB_POOL_MODE=null` keeps connection usage minimal and is the recommended default.
- `DB_POOL_MODE=queue` enables SQLAlchemy's queue pool when you are on a dedicated database and want persistent pooling.
- `DB_POOL_SIZE=1` and `DB_MAX_OVERFLOW=0` control the queue pool only.

The backend uses FastAPI, SQLAlchemy, a DB-backed run queue, and the existing shared Supabase/Postgres tables:
- `Dashboard_AI_check_profiles`
- `Dashboard_AI_check_drafts`
- `Dashboard_AI_check_runs`
- `Dashboard_AI_check_outputs`
- `Dashboard_AI_check_run_results`
- `Dashboard_AI_check_logs`

## Logs
The dashboard now includes an in-app `Logs` menu instead of the external log monitor.

It shows API requests, run lifecycle events, worker claims, worker completion/failure events, and cleanup activity directly inside the UI.

To grant access, set the comma-separated `LOG_VIEWER_EMAILS` value in `.env`. The admin email from `ADMIN_EMAIL` is always allowed too.

## Frontend
1. Install Node dependencies with `npm install`.
2. Make sure `VITE_SUPABASE_URL` and `VITE_SUPABASE_ANON_KEY` are set.
3. Run the UI with `npm run dev`.

The login modal now creates or reuses a Supabase anonymous session, then syncs the username into the profile row via `/api/profile/upsert`.

## Tests
Run the backend tests with:

```bash
python -m unittest discover -s tests -v
```

## Cleanup
Delete old raw output rows with:

```bash
npm run cleanup
```


