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

ALTER TABLE bestsellers ENABLE ROW LEVEL SECURITY;

CREATE POLICY "anon_read"   ON bestsellers FOR SELECT USING (true);
CREATE POLICY "anon_insert" ON bestsellers FOR INSERT WITH CHECK (true);
CREATE POLICY "anon_update" ON bestsellers FOR UPDATE USING (true);
