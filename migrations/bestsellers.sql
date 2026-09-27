-- Goody bestsellers migration
-- Run in Supabase SQL Editor (as service_role / postgres).
-- Populated daily by refresh_bestsellers() in server.py (scrapes Amazon.de
-- bestseller pages per category — see BESTSELLER_CATEGORIES).

CREATE TABLE IF NOT EXISTS bestsellers (
    category     text NOT NULL,
    rank         int  NOT NULL,
    product_name text NOT NULL,
    price        numeric(10,2),
    currency     text NOT NULL DEFAULT 'EUR',
    url          text,
    image_url    text,
    source       text,
    scraped_at   timestamptz NOT NULL DEFAULT now(),
    PRIMARY KEY (category, rank)
);

CREATE INDEX IF NOT EXISTS idx_bs_scraped_at ON bestsellers (scraped_at DESC);

-- Backend writes with the secret/service_role key (bypasses RLS) — the
-- frontend never talks to Supabase directly, so anon only needs read access.
-- Do NOT add anon_insert/anon_update: the anon key ships in the frontend
-- bundle, so a public write policy would let anyone rewrite bestsellers.url
-- to a phishing link or spoof rank/price.
ALTER TABLE bestsellers ENABLE ROW LEVEL SECURITY;

CREATE POLICY "anon_read" ON bestsellers FOR SELECT USING (true);
