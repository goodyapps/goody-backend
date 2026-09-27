-- Run this in Supabase → SQL Editor

CREATE TABLE IF NOT EXISTS price_history (
    id         bigserial PRIMARY KEY,
    product_name text NOT NULL,
    shop         text NOT NULL,
    price        numeric(10,2) NOT NULL,
    currency     text NOT NULL DEFAULT 'EUR',
    checked_at   timestamptz NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_ph_product_time
    ON price_history (product_name, checked_at DESC);

-- Row Level Security
-- Backend writes with the secret/service_role key (bypasses RLS) — the
-- frontend never talks to Supabase directly, so anon only needs read access.
-- Do NOT add anon_insert/anon_update here: the anon key ships in the
-- frontend bundle, so a public write policy lets anyone forge price rows.
ALTER TABLE price_history ENABLE ROW LEVEL SECURITY;

CREATE POLICY "anon_read"   ON price_history FOR SELECT USING (true);
