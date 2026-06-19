-- =============================================================================
-- INTENT DATA MIGRATION
-- Data: 2026-06-20 | Šaka: intent-data
-- STATUSAS: PERŽIŪRAI — NE PALEISTI BE PATVIRTINIMO
-- Vykdyti: Supabase dashboard → SQL Editor (NE Render, NE server.py)
-- =============================================================================

-- =============================================================================
-- ETAPAS 1: price_history išplėtimas (SAUGU — tik kolona pridedama)
-- Rizika: NULINĖ — SELECT/INSERT/UPDATE nepaliestas
-- Kada: Galima dabar
-- =============================================================================

-- 1a. Pridėti product_key koloną (nullable — nereikia backfill iš karto)
ALTER TABLE price_history
    ADD COLUMN IF NOT EXISTS product_key TEXT;

-- 1b. Backfill esami įrašai: product_key = normalized product_name
--     Tai yra laikinas sprendimas — serveris pradės siųsti tikslesnį product_key
UPDATE price_history
    SET product_key = LOWER(TRIM(product_name))
    WHERE product_key IS NULL
      AND product_name IS NOT NULL;

-- 1c. Indeksas greičiui
CREATE INDEX IF NOT EXISTS idx_price_history_product_key
    ON price_history(product_key, checked_at DESC);

-- Patikrinimas po 1 etapo:
-- SELECT COUNT(*), COUNT(product_key) FROM price_history;
-- Turi matyti: abu skaičiai vienodi (visi backfilled)


-- =============================================================================
-- ETAPAS 2: intent_events lentelė (NAUJA — nekeičia esamos struktūros)
-- Rizika: NULINĖ — nauja lentelė, esamas kodas jos nenaudoja
-- Kada: Galima dabar
-- =============================================================================

CREATE TABLE IF NOT EXISTS intent_events (
    -- Pirminis raktas
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    -- Produkto identifikacija (normalizuota)
    product_key     TEXT NOT NULL,
        -- Formatas: 'brand:model_code' arba 'brand:name' arba ':model_code'
        -- Pavyzdžiai: 'lego:76430', 'sony:wh-1000xm5', 'nutella:ferrero'
    product_name    TEXT NOT NULL,
        -- Raw paieška, lowercase (max 200 simbolių)
    product_type    TEXT,
        -- NULL, 'MAIN', 'ACCESSORY', 'BOOK', 'FOOD', 'COSMETICS', 'CLOTHING'

    -- Ketinimo signalas
    input_method    TEXT NOT NULL DEFAULT 'text',
        -- 'text' | 'photo' | 'barcode' | 'voice'
    scan_confidence TEXT,
        -- NULL (jei text/voice) | 'high' | 'medium' | 'low' (jei photo/barcode)
    language        TEXT NOT NULL DEFAULT 'lt',
        -- 'lt' | 'de' | 'pl' | 'en' | 'ru'

    -- Laiko kontekstas (anonimizuotas — nėra tikslaus laiko)
    hour_of_day     SMALLINT CHECK (hour_of_day BETWEEN 0 AND 23),
    day_of_week     SMALLINT CHECK (day_of_week BETWEEN 0 AND 6),
        -- 0 = Pirmadienis, 6 = Sekmadienis (Python weekday() konvencija)
    week_of_year    SMALLINT CHECK (week_of_year BETWEEN 1 AND 53),

    -- Sprendimo signalas
    verdict         TEXT,
        -- 'BUY' | 'WAIT' | 'OK' | 'NOT_FOUND'
    price_min_eur   NUMERIC(10,2),
        -- Žemiausia kaina EUR (konvertuota)
    price_max_eur   NUMERIC(10,2),
        -- Aukščiausia kaina EUR (konvertuota)
    shops_found     SMALLINT DEFAULT 0,
        -- Kiek parduotuvių grąžino bent vieną rezultatą
    cheapest_shop   TEXT,
        -- Kurią parduotuvę buvo pigiausias variantas
    has_history     BOOLEAN DEFAULT FALSE,
        -- Ar buvo kainų istorijos duomenų kai generuotas verdiktas

    -- Veiksmo signalas (papildo /api/track)
    clicked_shop    TEXT DEFAULT NULL,
        -- Kurią parduotuvę paspaudė "Buy Now" (NULL jei nebuvo paspaudimo)
    clicked_at      TIMESTAMPTZ DEFAULT NULL,
    added_watchlist BOOLEAN DEFAULT FALSE,
        -- Ar išsaugojo watchlist stebėjimui
    watchlist_target_eur NUMERIC(10,2) DEFAULT NULL,
        -- Tikslinė kaina (NULL jei nenustatyta)

    -- Metaduomenys
    created_at      TIMESTAMPTZ DEFAULT NOW()

    -- SAUGUMAS: Nėra IP, nėra user_id, nėra jokio asmeninio identifikatoriaus
    -- Teisinis pagrindas: GDPR 6(1)(f) Teisėtas interesas (agreguota statistika)
);

-- Indeksai greičiui
CREATE INDEX IF NOT EXISTS idx_intent_product_key
    ON intent_events(product_key, created_at DESC);
    -- Naudojamas: "Kokia ši produkto kainos istorija?" (JOIN su price_history)

CREATE INDEX IF NOT EXISTS idx_intent_created
    ON intent_events(created_at DESC);
    -- Naudojamas: "Paskutinių 30 dienų paieškos"

CREATE INDEX IF NOT EXISTS idx_intent_verdict_type
    ON intent_events(verdict, product_type, created_at DESC);
    -- Naudojamas: "BUY verdikto statistika ELECTRONICS kategorijoje"

CREATE INDEX IF NOT EXISTS idx_intent_day_hour
    ON intent_events(day_of_week, hour_of_day);
    -- Naudojamas: "Savaitės dienos kainų tendencija"

CREATE INDEX IF NOT EXISTS idx_intent_input_method
    ON intent_events(input_method, created_at DESC);
    -- Naudojamas: "Foto paieška vs tekstas — konversijų palyginimas"

-- Patikrinimas po 2 etapo:
-- SELECT table_name FROM information_schema.tables WHERE table_name = 'intent_events';
-- Turi matyti: intent_events


-- =============================================================================
-- ETAPAS 3: watchlist_server lentelė (NAUJA — ateičiai, neskubant)
-- Rizika: NULINĖ — nauja lentelė
-- Kada: Tik kai bus push pranešimų infrastruktūra
-- =============================================================================

-- KOMENTAS: Šios lentelės DABAR NEKURTI — paruošta ateičiai
-- Aktyvuoti kai bus server-side watchlist (FEATURE_IDEAS.md B1) + Push pranešimai (B2)

/*
CREATE TABLE IF NOT EXISTS watchlist_server (
    id                  UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    product_key         TEXT NOT NULL,
    product_name        TEXT NOT NULL,
    original_price_eur  NUMERIC(10,2),
    target_price_eur    NUMERIC(10,2),
    created_at          TIMESTAMPTZ DEFAULT NOW(),
    hit_at              TIMESTAMPTZ DEFAULT NULL,
    hit_price_eur       NUMERIC(10,2) DEFAULT NULL,
    notified            BOOLEAN DEFAULT FALSE
);

CREATE INDEX IF NOT EXISTS idx_watchlist_product_key
    ON watchlist_server(product_key);

CREATE INDEX IF NOT EXISTS idx_watchlist_active
    ON watchlist_server(hit_at)
    WHERE hit_at IS NULL;
    -- Tik aktyvūs (nesulaukę kainos kritimo) — greitas tikrinimas
*/


-- =============================================================================
-- ETAPAS 4: RLS politikos (REKOMENDUOJAMA — papildoma apsauga)
-- Rizika: ŽEMA — tik riboja prieigą, nekeičia duomenų
-- Kada: Kartu su Etapu 2
-- =============================================================================

-- intent_events: tik serveris gali rašyti (service_role)
ALTER TABLE intent_events ENABLE ROW LEVEL SECURITY;

-- Anon naudotojai (pvz., tiesioginiai Supabase API kvietimai) negali rašyti
CREATE POLICY "intent_events_service_only" ON intent_events
    FOR ALL
    TO service_role
    USING (true)
    WITH CHECK (true);

-- anon rolė neturi prieigos
CREATE POLICY "intent_events_no_anon" ON intent_events
    FOR ALL
    TO anon
    USING (false);

-- price_history: tas pats
ALTER TABLE price_history ENABLE ROW LEVEL SECURITY;

CREATE POLICY "price_history_service_only" ON price_history
    FOR ALL
    TO service_role
    USING (true)
    WITH CHECK (true);

CREATE POLICY "price_history_no_anon" ON price_history
    FOR ALL
    TO anon
    USING (false);

-- searches: tas pats
ALTER TABLE searches ENABLE ROW LEVEL SECURITY;

CREATE POLICY "searches_service_only" ON searches
    FOR ALL
    TO service_role
    USING (true)
    WITH CHECK (true);

CREATE POLICY "searches_no_anon" ON searches
    FOR ALL
    TO anon
    USING (false);


-- =============================================================================
-- VERIFIKACIJOS UŽKLAUSOS (paleisti po migracijos)
-- =============================================================================

-- Patikrinti price_history struktūrą:
-- SELECT column_name, data_type FROM information_schema.columns
-- WHERE table_name = 'price_history' ORDER BY ordinal_position;

-- Patikrinti intent_events lentelę:
-- SELECT column_name, data_type, is_nullable FROM information_schema.columns
-- WHERE table_name = 'intent_events' ORDER BY ordinal_position;

-- Patikrinti RLS:
-- SELECT schemaname, tablename, policyname, roles FROM pg_policies
-- WHERE tablename IN ('intent_events', 'price_history', 'searches');

-- Patikrinti indeksus:
-- SELECT indexname, indexdef FROM pg_indexes
-- WHERE tablename IN ('intent_events', 'price_history') ORDER BY tablename, indexname;


-- =============================================================================
-- ROLLBACK PLANAS (jei kažkas nepavyksta)
-- =============================================================================

-- Atšaukti Etapą 2 (intent_events):
-- DROP TABLE IF EXISTS intent_events CASCADE;

-- Atšaukti Etapą 1 (price_history kolona):
-- ALTER TABLE price_history DROP COLUMN IF EXISTS product_key;
-- DROP INDEX IF EXISTS idx_price_history_product_key;

-- Atšaukti RLS (jei sukelia problemų su serverio prisijungimu):
-- ALTER TABLE intent_events DISABLE ROW LEVEL SECURITY;
-- ALTER TABLE price_history DISABLE ROW LEVEL SECURITY;
-- ALTER TABLE searches DISABLE ROW LEVEL SECURITY;
