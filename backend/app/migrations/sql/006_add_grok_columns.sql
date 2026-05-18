ALTER TABLE "Dashboard_AI_check_outputs"
    ADD COLUMN IF NOT EXISTS grok_output text;

ALTER TABLE "Dashboard_AI_check_outputs"
    ADD COLUMN IF NOT EXISTS grok_domain_mention boolean DEFAULT false;

ALTER TABLE "Dashboard_AI_check_outputs"
    ADD COLUMN IF NOT EXISTS grok_brand_mention boolean DEFAULT false;

ALTER TABLE "Dashboard_AI_check_outputs"
    ADD COLUMN IF NOT EXISTS grok_generation_cost_usd double precision;

ALTER TABLE "Dashboard_AI_check_run_results"
    ADD COLUMN IF NOT EXISTS grok_domain_mention boolean DEFAULT false;

ALTER TABLE "Dashboard_AI_check_run_results"
    ADD COLUMN IF NOT EXISTS grok_brand_mention boolean DEFAULT false;

UPDATE "Dashboard_AI_check_outputs" SET grok_domain_mention = false WHERE grok_domain_mention IS NULL;
UPDATE "Dashboard_AI_check_outputs" SET grok_brand_mention = false WHERE grok_brand_mention IS NULL;
UPDATE "Dashboard_AI_check_run_results" SET grok_domain_mention = false WHERE grok_domain_mention IS NULL;
UPDATE "Dashboard_AI_check_run_results" SET grok_brand_mention = false WHERE grok_brand_mention IS NULL;

ALTER TABLE "Dashboard_AI_check_outputs" ALTER COLUMN grok_domain_mention SET NOT NULL;
ALTER TABLE "Dashboard_AI_check_outputs" ALTER COLUMN grok_brand_mention SET NOT NULL;
ALTER TABLE "Dashboard_AI_check_run_results" ALTER COLUMN grok_domain_mention SET NOT NULL;
ALTER TABLE "Dashboard_AI_check_run_results" ALTER COLUMN grok_brand_mention SET NOT NULL;
