-- Goody intent_events migration
-- Safe to re-run (idempotent): all steps use IF EXISTS / IF NOT EXISTS guards.
-- Run in Supabase SQL Editor (as service_role / postgres).

-- ── STEP 1: rename legacy table if it has the old flat schema ──────────────
DO $$
BEGIN
  IF EXISTS (
    SELECT 1 FROM information_schema.columns
    WHERE table_schema = 'public'
      AND table_name   = 'intent_events'
      AND column_name  = 'product_key'
  ) THEN
    ALTER TABLE public.intent_events RENAME TO intent_events_legacy;
    RAISE NOTICE 'Renamed old intent_events → intent_events_legacy';
  ELSE
    RAISE NOTICE 'Old intent_events not found or already migrated — skipping rename';
  END IF;
END $$;

-- ── STEP 2: create new append-only event-sourced table ─────────────────────
CREATE TABLE IF NOT EXISTS public.intent_events (
  id                bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  event_type        text          NOT NULL,
  anonymous_user_id uuid          NOT NULL,
  session_id        uuid          NOT NULL,
  product_canonical text,
  payload           jsonb         NOT NULL DEFAULT '{}'::jsonb,
  is_internal       boolean       NOT NULL DEFAULT false,
  created_at        timestamptz   NOT NULL DEFAULT now()
);

-- ── STEP 3: indexes ─────────────────────────────────────────────────────────
CREATE INDEX IF NOT EXISTS idx_ie_event_ts
  ON public.intent_events (event_type, created_at DESC);

CREATE INDEX IF NOT EXISTS idx_ie_canonical_ts
  ON public.intent_events (product_canonical, created_at DESC)
  WHERE product_canonical IS NOT NULL;

CREATE INDEX IF NOT EXISTS idx_ie_anon_ts
  ON public.intent_events (anonymous_user_id, created_at DESC);

-- ── STEP 4: row-level security ──────────────────────────────────────────────
ALTER TABLE public.intent_events ENABLE ROW LEVEL SECURITY;

-- Only service_role (backend) may insert; nobody reads via anon key.
DROP POLICY IF EXISTS "service_insert" ON public.intent_events;
CREATE POLICY "service_insert" ON public.intent_events
  FOR INSERT TO service_role WITH CHECK (true);

-- ── STEP 5: migrate data from legacy (runs once, skipped if already done) ──
DO $$
BEGIN
  IF EXISTS (
    SELECT 1 FROM information_schema.tables
    WHERE table_schema = 'public' AND table_name = 'intent_events_legacy'
  ) THEN
    INSERT INTO public.intent_events
      (event_type, anonymous_user_id, session_id, product_canonical, payload, is_internal, created_at)
    SELECT
      'search',
      -- legacy rows have no user/session — use fixed migration sentinel UUID
      '00000000-0000-0000-0000-000000000001'::uuid,
      CASE
        WHEN id ~ '^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$'
          THEN id::uuid
        ELSE gen_random_uuid()
      END,
      product_key,
      jsonb_build_object(
        'query_raw',    product_name,
        'method',       COALESCE(input_method, 'text'),
        'language',     COALESCE(language, 'lt'),
        'offers_count', COALESCE(shops_found, 0),
        'min_price',    price_min_eur,
        'max_price',    price_max_eur,
        'legacy',       true
      ),
      false,
      COALESCE(created_at, now())
    FROM public.intent_events_legacy
    WHERE NOT EXISTS (
      -- only migrate once: skip if new table already has data
      SELECT 1 FROM public.intent_events LIMIT 1
    );

    RAISE NOTICE 'Legacy data migrated to intent_events';
  END IF;
END $$;
