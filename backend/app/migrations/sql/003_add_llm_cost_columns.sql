ALTER TABLE "Dashboard_AI_check_outputs"
    ADD COLUMN IF NOT EXISTS openai_generation_cost_usd double precision;

ALTER TABLE "Dashboard_AI_check_outputs"
    ADD COLUMN IF NOT EXISTS gemini_generation_cost_usd double precision;

ALTER TABLE "Dashboard_AI_check_outputs"
    ADD COLUMN IF NOT EXISTS gemini_analysis_cost_usd double precision;

ALTER TABLE "Dashboard_AI_check_run_results"
    ADD COLUMN IF NOT EXISTS gemini_sentiment_cost_usd double precision;
