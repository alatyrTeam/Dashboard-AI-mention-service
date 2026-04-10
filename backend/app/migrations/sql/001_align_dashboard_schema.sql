CREATE TABLE IF NOT EXISTS "Dashboard_AI_check_profiles" (
    id uuid PRIMARY KEY,
    user_id uuid NOT NULL,
    username text NOT NULL,
    created_at timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS "Dashboard_AI_check_drafts" (
    id uuid PRIMARY KEY,
    user_id uuid NOT NULL,
    keyword text,
    domain text,
    brand text,
    prompt text,
    project text,
    rows_json text,
    updated_at timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS "Dashboard_AI_check_runs" (
    id uuid PRIMARY KEY,
    user_id uuid NOT NULL,
    keyword text NOT NULL,
    domain text NOT NULL,
    brand text NOT NULL,
    prompt text NOT NULL,
    project text,
    status text NOT NULL DEFAULT 'queued',
    total_iterations integer NOT NULL DEFAULT 3,
    completed_iterations integer NOT NULL DEFAULT 0,
    error_messages text,
    created_at timestamptz NOT NULL DEFAULT now(),
    started_at timestamptz,
    finished_at timestamptz
);

CREATE TABLE IF NOT EXISTS "Dashboard_AI_check_outputs" (
    id uuid PRIMARY KEY,
    user_id uuid NOT NULL,
    run_id uuid NOT NULL,
    iteration_number integer NOT NULL,
    gpt_output text,
    gem_output text,
    gpt_domain_mention boolean NOT NULL DEFAULT false,
    gem_domain_mention boolean NOT NULL DEFAULT false,
    gpt_brand_mention boolean NOT NULL DEFAULT false,
    gem_brand_mention boolean NOT NULL DEFAULT false,
    response_count double precision,
    brand_list text,
    citation_format text,
    project text,
    created_at timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS "Dashboard_AI_check_run_results" (
    id uuid PRIMARY KEY,
    user_id uuid NOT NULL,
    run_id uuid NOT NULL,
    project text,
    gpt_domain_mention boolean NOT NULL DEFAULT false,
    gem_domain_mention boolean NOT NULL DEFAULT false,
    gpt_brand_mention boolean NOT NULL DEFAULT false,
    gem_brand_mention boolean NOT NULL DEFAULT false,
    response_count_avg double precision,
    brand_list text,
    citation_format text,
    sentiment_analysis text,
    created_at timestamptz NOT NULL DEFAULT now()
);

DO $$
BEGIN
    IF EXISTS (
        SELECT 1
        FROM information_schema.columns
        WHERE table_name = 'Dashboard_AI_check_outputs'
          AND column_name = 'responce_count'
    ) AND NOT EXISTS (
        SELECT 1
        FROM information_schema.columns
        WHERE table_name = 'Dashboard_AI_check_outputs'
          AND column_name = 'response_count'
    ) THEN
        ALTER TABLE "Dashboard_AI_check_outputs" RENAME COLUMN responce_count TO response_count;
    END IF;
END $$;

ALTER TABLE "Dashboard_AI_check_outputs" ADD COLUMN IF NOT EXISTS response_count double precision;
ALTER TABLE "Dashboard_AI_check_outputs" ADD COLUMN IF NOT EXISTS brand_list text;
ALTER TABLE "Dashboard_AI_check_outputs" ADD COLUMN IF NOT EXISTS citation_format text;
ALTER TABLE "Dashboard_AI_check_outputs" ADD COLUMN IF NOT EXISTS iteration_number integer;
ALTER TABLE "Dashboard_AI_check_outputs" ADD COLUMN IF NOT EXISTS gpt_domain_mention boolean DEFAULT false;
ALTER TABLE "Dashboard_AI_check_outputs" ADD COLUMN IF NOT EXISTS gem_domain_mention boolean DEFAULT false;
ALTER TABLE "Dashboard_AI_check_outputs" ADD COLUMN IF NOT EXISTS gpt_brand_mention boolean DEFAULT false;
ALTER TABLE "Dashboard_AI_check_outputs" ADD COLUMN IF NOT EXISTS gem_brand_mention boolean DEFAULT false;
ALTER TABLE "Dashboard_AI_check_outputs" ADD COLUMN IF NOT EXISTS created_at timestamptz DEFAULT now();

ALTER TABLE "Dashboard_AI_check_run_results" ADD COLUMN IF NOT EXISTS response_count_avg double precision;
ALTER TABLE "Dashboard_AI_check_run_results" ADD COLUMN IF NOT EXISTS brand_list text;
ALTER TABLE "Dashboard_AI_check_run_results" ADD COLUMN IF NOT EXISTS citation_format text;
ALTER TABLE "Dashboard_AI_check_run_results" ADD COLUMN IF NOT EXISTS sentiment_analysis text;
ALTER TABLE "Dashboard_AI_check_run_results" ADD COLUMN IF NOT EXISTS created_at timestamptz DEFAULT now();

ALTER TABLE "Dashboard_AI_check_runs" ADD COLUMN IF NOT EXISTS status text DEFAULT 'queued';
ALTER TABLE "Dashboard_AI_check_runs" ADD COLUMN IF NOT EXISTS total_iterations integer DEFAULT 3;
ALTER TABLE "Dashboard_AI_check_runs" ADD COLUMN IF NOT EXISTS completed_iterations integer DEFAULT 0;
ALTER TABLE "Dashboard_AI_check_runs" ADD COLUMN IF NOT EXISTS error_messages text;
ALTER TABLE "Dashboard_AI_check_runs" ADD COLUMN IF NOT EXISTS started_at timestamptz;
ALTER TABLE "Dashboard_AI_check_runs" ADD COLUMN IF NOT EXISTS finished_at timestamptz;
ALTER TABLE "Dashboard_AI_check_runs" ADD COLUMN IF NOT EXISTS created_at timestamptz DEFAULT now();

ALTER TABLE "Dashboard_AI_check_drafts" ADD COLUMN IF NOT EXISTS updated_at timestamptz DEFAULT now();
ALTER TABLE "Dashboard_AI_check_drafts" ADD COLUMN IF NOT EXISTS rows_json text;
ALTER TABLE "Dashboard_AI_check_profiles" ADD COLUMN IF NOT EXISTS created_at timestamptz DEFAULT now();

UPDATE "Dashboard_AI_check_profiles" SET created_at = now() WHERE created_at IS NULL;
UPDATE "Dashboard_AI_check_drafts" SET updated_at = now() WHERE updated_at IS NULL;
UPDATE "Dashboard_AI_check_drafts"
SET rows_json = json_build_array(
    json_build_object(
        'keyword', COALESCE(keyword, ''),
        'domain', COALESCE(domain, ''),
        'brand', COALESCE(brand, ''),
        'prompt', COALESCE(prompt, ''),
        'project', COALESCE(project, '')
    )
)::text
WHERE rows_json IS NULL;
UPDATE "Dashboard_AI_check_runs" SET created_at = now() WHERE created_at IS NULL;
UPDATE "Dashboard_AI_check_runs" SET status = 'queued' WHERE status IS NULL;
UPDATE "Dashboard_AI_check_runs" SET total_iterations = 3 WHERE total_iterations IS NULL;
UPDATE "Dashboard_AI_check_runs" SET completed_iterations = 0 WHERE completed_iterations IS NULL;
UPDATE "Dashboard_AI_check_outputs" SET created_at = now() WHERE created_at IS NULL;
UPDATE "Dashboard_AI_check_run_results" SET created_at = now() WHERE created_at IS NULL;

DO $$
BEGIN
    IF EXISTS (
        SELECT 1
        FROM information_schema.columns
        WHERE table_name = 'Dashboard_AI_check_outputs'
          AND column_name = 'gpt_domain_mention'
          AND data_type <> 'boolean'
    ) THEN
        ALTER TABLE "Dashboard_AI_check_outputs"
            ALTER COLUMN gpt_domain_mention TYPE boolean USING (gpt_domain_mention::integer <> 0);
    END IF;
    IF EXISTS (
        SELECT 1
        FROM information_schema.columns
        WHERE table_name = 'Dashboard_AI_check_outputs'
          AND column_name = 'gem_domain_mention'
          AND data_type <> 'boolean'
    ) THEN
        ALTER TABLE "Dashboard_AI_check_outputs"
            ALTER COLUMN gem_domain_mention TYPE boolean USING (gem_domain_mention::integer <> 0);
    END IF;
    IF EXISTS (
        SELECT 1
        FROM information_schema.columns
        WHERE table_name = 'Dashboard_AI_check_outputs'
          AND column_name = 'gpt_brand_mention'
          AND data_type <> 'boolean'
    ) THEN
        ALTER TABLE "Dashboard_AI_check_outputs"
            ALTER COLUMN gpt_brand_mention TYPE boolean USING (gpt_brand_mention::integer <> 0);
    END IF;
    IF EXISTS (
        SELECT 1
        FROM information_schema.columns
        WHERE table_name = 'Dashboard_AI_check_outputs'
          AND column_name = 'gem_brand_mention'
          AND data_type <> 'boolean'
    ) THEN
        ALTER TABLE "Dashboard_AI_check_outputs"
            ALTER COLUMN gem_brand_mention TYPE boolean USING (gem_brand_mention::integer <> 0);
    END IF;
    IF EXISTS (
        SELECT 1
        FROM information_schema.columns
        WHERE table_name = 'Dashboard_AI_check_run_results'
          AND column_name = 'gpt_domain_mention'
          AND data_type <> 'boolean'
    ) THEN
        ALTER TABLE "Dashboard_AI_check_run_results"
            ALTER COLUMN gpt_domain_mention TYPE boolean USING (gpt_domain_mention::integer <> 0);
    END IF;
    IF EXISTS (
        SELECT 1
        FROM information_schema.columns
        WHERE table_name = 'Dashboard_AI_check_run_results'
          AND column_name = 'gem_domain_mention'
          AND data_type <> 'boolean'
    ) THEN
        ALTER TABLE "Dashboard_AI_check_run_results"
            ALTER COLUMN gem_domain_mention TYPE boolean USING (gem_domain_mention::integer <> 0);
    END IF;
    IF EXISTS (
        SELECT 1
        FROM information_schema.columns
        WHERE table_name = 'Dashboard_AI_check_run_results'
          AND column_name = 'gpt_brand_mention'
          AND data_type <> 'boolean'
    ) THEN
        ALTER TABLE "Dashboard_AI_check_run_results"
            ALTER COLUMN gpt_brand_mention TYPE boolean USING (gpt_brand_mention::integer <> 0);
    END IF;
    IF EXISTS (
        SELECT 1
        FROM information_schema.columns
        WHERE table_name = 'Dashboard_AI_check_run_results'
          AND column_name = 'gem_brand_mention'
          AND data_type <> 'boolean'
    ) THEN
        ALTER TABLE "Dashboard_AI_check_run_results"
            ALTER COLUMN gem_brand_mention TYPE boolean USING (gem_brand_mention::integer <> 0);
    END IF;
END $$;

UPDATE "Dashboard_AI_check_outputs" SET gpt_domain_mention = false WHERE gpt_domain_mention IS NULL;
UPDATE "Dashboard_AI_check_outputs" SET gem_domain_mention = false WHERE gem_domain_mention IS NULL;
UPDATE "Dashboard_AI_check_outputs" SET gpt_brand_mention = false WHERE gpt_brand_mention IS NULL;
UPDATE "Dashboard_AI_check_outputs" SET gem_brand_mention = false WHERE gem_brand_mention IS NULL;
UPDATE "Dashboard_AI_check_run_results" SET gpt_domain_mention = false WHERE gpt_domain_mention IS NULL;
UPDATE "Dashboard_AI_check_run_results" SET gem_domain_mention = false WHERE gem_domain_mention IS NULL;
UPDATE "Dashboard_AI_check_run_results" SET gpt_brand_mention = false WHERE gpt_brand_mention IS NULL;
UPDATE "Dashboard_AI_check_run_results" SET gem_brand_mention = false WHERE gem_brand_mention IS NULL;

ALTER TABLE "Dashboard_AI_check_profiles" ALTER COLUMN username SET NOT NULL;
ALTER TABLE "Dashboard_AI_check_profiles" ALTER COLUMN created_at SET NOT NULL;

ALTER TABLE "Dashboard_AI_check_drafts" ALTER COLUMN user_id SET NOT NULL;
ALTER TABLE "Dashboard_AI_check_drafts" ALTER COLUMN updated_at SET NOT NULL;

ALTER TABLE "Dashboard_AI_check_runs" ALTER COLUMN user_id SET NOT NULL;
ALTER TABLE "Dashboard_AI_check_runs" ALTER COLUMN keyword SET NOT NULL;
ALTER TABLE "Dashboard_AI_check_runs" ALTER COLUMN domain SET NOT NULL;
ALTER TABLE "Dashboard_AI_check_runs" ALTER COLUMN brand SET NOT NULL;
ALTER TABLE "Dashboard_AI_check_runs" ALTER COLUMN prompt SET NOT NULL;
ALTER TABLE "Dashboard_AI_check_runs" ALTER COLUMN status SET NOT NULL;
ALTER TABLE "Dashboard_AI_check_runs" ALTER COLUMN total_iterations SET NOT NULL;
ALTER TABLE "Dashboard_AI_check_runs" ALTER COLUMN completed_iterations SET NOT NULL;
ALTER TABLE "Dashboard_AI_check_runs" ALTER COLUMN created_at SET NOT NULL;

ALTER TABLE "Dashboard_AI_check_outputs" ALTER COLUMN user_id SET NOT NULL;
ALTER TABLE "Dashboard_AI_check_outputs" ALTER COLUMN run_id SET NOT NULL;
ALTER TABLE "Dashboard_AI_check_outputs" ALTER COLUMN iteration_number SET NOT NULL;
ALTER TABLE "Dashboard_AI_check_outputs" ALTER COLUMN gpt_domain_mention SET NOT NULL;
ALTER TABLE "Dashboard_AI_check_outputs" ALTER COLUMN gem_domain_mention SET NOT NULL;
ALTER TABLE "Dashboard_AI_check_outputs" ALTER COLUMN gpt_brand_mention SET NOT NULL;
ALTER TABLE "Dashboard_AI_check_outputs" ALTER COLUMN gem_brand_mention SET NOT NULL;
ALTER TABLE "Dashboard_AI_check_outputs" ALTER COLUMN created_at SET NOT NULL;

ALTER TABLE "Dashboard_AI_check_run_results" ALTER COLUMN user_id SET NOT NULL;
ALTER TABLE "Dashboard_AI_check_run_results" ALTER COLUMN run_id SET NOT NULL;
ALTER TABLE "Dashboard_AI_check_run_results" ALTER COLUMN gpt_domain_mention SET NOT NULL;
ALTER TABLE "Dashboard_AI_check_run_results" ALTER COLUMN gem_domain_mention SET NOT NULL;
ALTER TABLE "Dashboard_AI_check_run_results" ALTER COLUMN gpt_brand_mention SET NOT NULL;
ALTER TABLE "Dashboard_AI_check_run_results" ALTER COLUMN gem_brand_mention SET NOT NULL;
ALTER TABLE "Dashboard_AI_check_run_results" ALTER COLUMN created_at SET NOT NULL;

CREATE UNIQUE INDEX IF NOT EXISTS idx_dashboard_profiles_user_id_unique
    ON "Dashboard_AI_check_profiles" (user_id);
CREATE UNIQUE INDEX IF NOT EXISTS idx_dashboard_drafts_user_id_unique
    ON "Dashboard_AI_check_drafts" (user_id);
CREATE UNIQUE INDEX IF NOT EXISTS idx_dashboard_run_results_run_id_unique
    ON "Dashboard_AI_check_run_results" (run_id);

CREATE INDEX IF NOT EXISTS idx_dashboard_drafts_user_id
    ON "Dashboard_AI_check_drafts" (user_id);
CREATE INDEX IF NOT EXISTS idx_dashboard_runs_user_id
    ON "Dashboard_AI_check_runs" (user_id);
CREATE INDEX IF NOT EXISTS idx_dashboard_runs_status
    ON "Dashboard_AI_check_runs" (status);
CREATE INDEX IF NOT EXISTS idx_dashboard_runs_created_at
    ON "Dashboard_AI_check_runs" (created_at);
CREATE INDEX IF NOT EXISTS idx_dashboard_outputs_run_id
    ON "Dashboard_AI_check_outputs" (run_id);
CREATE INDEX IF NOT EXISTS idx_dashboard_outputs_user_id
    ON "Dashboard_AI_check_outputs" (user_id);
CREATE INDEX IF NOT EXISTS idx_dashboard_outputs_iteration_number
    ON "Dashboard_AI_check_outputs" (iteration_number);
CREATE INDEX IF NOT EXISTS idx_dashboard_run_results_run_id
    ON "Dashboard_AI_check_run_results" (run_id);
CREATE INDEX IF NOT EXISTS idx_dashboard_run_results_user_id
    ON "Dashboard_AI_check_run_results" (user_id);
