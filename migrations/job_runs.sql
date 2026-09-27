-- Goody job_runs migration
-- Real (not estimated) telemetry for background jobs — e.g. how many
-- ScraperAPI calls the daily trend-seed job actually made, so credit usage
-- can be checked from real history instead of guessing.
-- Run in Supabase SQL Editor.

CREATE TABLE IF NOT EXISTS job_runs (
    id                        bigserial PRIMARY KEY,
    job_name                  text NOT NULL,
    ran_at                    timestamptz NOT NULL DEFAULT now(),
    items_processed           int,
    items_total               int,
    scraperapi_premium_calls  int,
    scraperapi_render_calls   int,
    scraperapi_basic_calls    int,
    est_credits               int
);

CREATE INDEX IF NOT EXISTS idx_job_runs_name_time ON job_runs (job_name, ran_at DESC);

-- Backend writes with the secret/service_role key (bypasses RLS) — no
-- anon_insert/anon_update here, only public read (see fix_anon_write_rls.sql
-- for why: the anon key ships in the frontend bundle).
ALTER TABLE job_runs ENABLE ROW LEVEL SECURITY;
CREATE POLICY "anon_read" ON job_runs FOR SELECT USING (true);
