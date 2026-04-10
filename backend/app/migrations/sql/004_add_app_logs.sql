CREATE TABLE IF NOT EXISTS "Dashboard_AI_check_logs" (
    id uuid PRIMARY KEY,
    created_at timestamptz NOT NULL DEFAULT now(),
    level text NOT NULL DEFAULT 'info',
    category text NOT NULL DEFAULT 'api',
    action text NOT NULL,
    message text NOT NULL,
    actor_user_id uuid,
    actor_email text,
    actor_username text,
    entity_type text,
    entity_id text,
    path text,
    method text,
    status_code integer,
    duration_ms integer,
    details_json text
);

CREATE INDEX IF NOT EXISTS idx_dashboard_logs_created_at
    ON "Dashboard_AI_check_logs" (created_at);
CREATE INDEX IF NOT EXISTS idx_dashboard_logs_level
    ON "Dashboard_AI_check_logs" (level);
CREATE INDEX IF NOT EXISTS idx_dashboard_logs_category
    ON "Dashboard_AI_check_logs" (category);
CREATE INDEX IF NOT EXISTS idx_dashboard_logs_actor_email
    ON "Dashboard_AI_check_logs" (actor_email);
