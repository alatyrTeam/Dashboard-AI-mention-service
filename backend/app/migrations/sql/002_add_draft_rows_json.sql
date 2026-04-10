ALTER TABLE "Dashboard_AI_check_drafts"
    ADD COLUMN IF NOT EXISTS rows_json text;

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
