-- SECURITY FIX: remove public write access to price_history and bestsellers.
-- Run in Supabase SQL Editor.
--
-- Why: RLS policies are PERMISSIVE by default in Postgres — multiple
-- permissive policies on the same command are combined with OR, so an
-- existing "no_anon"-style restrictive-looking policy does NOT block
-- anon_insert/anon_update if those also exist as permissive policies.
-- The anon (public) key ships inside the frontend bundle, so anyone can
-- read it and use it to write directly to these tables via Supabase's
-- REST API — e.g. rewriting bestsellers.url to a phishing site, or
-- inserting fake price_history rows to spoof the price chart / fake-
-- discount detector.
--
-- The backend (Render) writes with the `secret`/service_role key, which
-- bypasses RLS entirely — removing these policies does not affect it.
-- The frontend never talks to Supabase directly (confirmed: no supabase.co
-- reference in index.html), so public write access serves no purpose here.

DROP POLICY IF EXISTS "anon_insert" ON public.bestsellers;
DROP POLICY IF EXISTS "anon_update" ON public.bestsellers;

DROP POLICY IF EXISTS "anon_insert" ON public.price_history;
DROP POLICY IF EXISTS "anon_update" ON public.price_history;

-- Sanity check after running: this should return ONLY "anon_read" (SELECT)
-- rows for both tables — no INSERT/UPDATE/ALL policy naming "anon".
SELECT schemaname, tablename, policyname, cmd, permissive
FROM pg_policies
WHERE tablename IN ('bestsellers', 'price_history')
ORDER BY tablename, cmd;
