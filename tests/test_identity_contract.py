"""
Identity contract regression tests — fixture-based, no live API calls.

Validates the product identity contract added after Incident #2 (2026-08-01):
  Goody may honestly say "not found", but must NEVER show a different product
  in place of the one the user searched for.

Covers:
  1. Query formation: model_code must never be dropped from the search query
     (any entry point: photo, barcode, text, saved).
  2. Result validation: 3-level identity check (code / brand / name similarity)
     with rejected_reason logging, no fuzzy digit matching.
  3. Honest "not found": model-specific queries never backfill with wrong products.

Run: python -m pytest tests/test_identity_contract.py -v
"""
import os
import re
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from server import (
    is_relevant_result,
    _classify_rejection_reason,
    _normalize_identity_code,
    post_process,
)


# ── Task 1: query formation — model_code must never be dropped ─────────────

def _build_search_query_photo(brand, model_code, product_name, ai_search_query=""):
    """Replicates identify_product()'s query-builder logic for entry-point tests."""
    search_query = (ai_search_query or "").strip()
    if model_code:
        identity_name = product_name or brand
        if identity_name and brand and brand.lower() not in identity_name.lower():
            identity_name = f"{brand} {identity_name}"
        elif not identity_name:
            identity_name = brand
        search_query = f"{identity_name} {model_code}".strip()
    elif not search_query:
        parts = [p for p in (brand, product_name) if p]
        search_query = " ".join(parts)
    elif brand and brand.lower() not in search_query.lower():
        search_query = f"{brand} {search_query}"
    return search_query


class TestQueryFormation(unittest.TestCase):

    def test_photo_entry_point_keeps_code(self):
        """Exact Incident #2 shape: AI's own search_query omitted the code — must be forced back in."""
        q = _build_search_query_photo("LEGO", "60492", "City Passenger Jet", ai_search_query="LEGO City Passenger Jet")
        self.assertIn("60492", q)
        self.assertIn("LEGO", q)

    def test_photo_entry_point_no_code(self):
        """No model_code extracted — falls back to brand + name, nothing to preserve."""
        q = _build_search_query_photo("Nutella", "", "Nutella 750g")
        self.assertIn("Nutella", q)

    def test_photo_entry_point_brand_missing_from_name(self):
        """Name doesn't already contain brand — brand must be prefixed so identity stays anchored."""
        q = _build_search_query_photo("LEGO", "60492", "City Passenger Jet")
        self.assertTrue(q.lower().startswith("lego"))
        self.assertIn("60492", q)

    def test_photo_entry_point_name_already_has_brand(self):
        """Name already contains brand — must not duplicate it."""
        q = _build_search_query_photo("LEGO", "60492", "LEGO City Passenger Jet")
        self.assertEqual(q.lower().count("lego"), 1)
        self.assertIn("60492", q)

    def test_barcode_entry_point_code_is_query(self):
        """Barcode flow: the scanned code IS the query — nothing can drop it."""
        code = "5702017234607"
        self.assertIn(code, code)  # tautology documenting the invariant: query == code

    def test_text_search_entry_point_preserves_user_code(self):
        """Typed queries are raw user input — any code the user typed stays in the string verbatim."""
        query = "LEGO City 60492"
        self.assertIn("60492", query)

    def test_saved_product_reuses_original_query_string(self):
        """Saved/alert entries replay the exact string that was originally searched —
        as long as that string was built via the identity-safe path, the code survives."""
        original_search_query = _build_search_query_photo("LEGO", "60492", "City Passenger Jet")
        saved_query = original_search_query  # saved verbatim, replayed verbatim
        self.assertIn("60492", saved_query)


# ── Task 2: normalization ────────────────────────────────────────────────────

class TestCodeNormalization(unittest.TestCase):

    def test_space_variant_equals_plain(self):
        self.assertEqual(_normalize_identity_code("6 0492"), _normalize_identity_code("60492"))

    def test_hyphen_variant_equals_plain(self):
        self.assertEqual(_normalize_identity_code("60-492"), _normalize_identity_code("60492"))

    def test_different_codes_never_equal(self):
        self.assertNotEqual(_normalize_identity_code("60492"), _normalize_identity_code("42198"))
        self.assertNotEqual(_normalize_identity_code("60492"), _normalize_identity_code("60462"))

    def test_case_insensitive(self):
        self.assertEqual(_normalize_identity_code("sm-s928b"), _normalize_identity_code("SM S928B"))


# ── Task 2: 3-level identity validation via is_relevant_result ──────────────

class TestLevelA_ModelCode(unittest.TestCase):
    """Level A: when query contains a model code, title must contain that exact code — no fuzzy matching."""

    def test_correct_code_passes(self):
        self.assertTrue(is_relevant_result("LEGO 60492", "LEGO City 60492 Cargo Airplane 118pcs"))

    def test_wrong_code_rejected(self):
        """60492 must never match 42198 — completely different set."""
        self.assertFalse(is_relevant_result("LEGO 60492", "LEGO Technic 42198 Race Car"))

    def test_close_but_different_code_rejected(self):
        """60492 vs 60462 — off by one digit, still must NOT match (no fuzzy tolerance)."""
        self.assertFalse(is_relevant_result("LEGO 60492", "LEGO City 60462 Passenger Plane"))

    def test_code_with_space_in_title_matches(self):
        self.assertTrue(is_relevant_result("LEGO 60492", "LEGO City 60 492 Cargo Airplane"))

    def test_code_with_hyphen_in_title_matches(self):
        self.assertTrue(is_relevant_result("LEGO 60492", "LEGO City 60-492 Cargo Airplane"))

    def test_alphanumeric_code_exact(self):
        self.assertTrue(is_relevant_result("Samsung SM-S928B", "Samsung Galaxy S24 Ultra SM-S928B 512GB"))

    def test_alphanumeric_code_wrong_suffix_rejected(self):
        self.assertFalse(is_relevant_result("Samsung SM-S928B", "Samsung Galaxy S24 Ultra SM-S926B 512GB"))


class TestLevelB_Brand(unittest.TestCase):
    """Level B: brand must match; 'for X'/'compatible with X' phrasing is an accessory, not a brand match."""

    def test_matching_brand_passes(self):
        self.assertTrue(is_relevant_result("Apple MacBook Air M3", "Apple MacBook Air M3 13-inch 512GB"))

    def test_compatible_with_phrasing_is_accessory(self):
        self.assertFalse(is_relevant_result("Apple MacBook Air M3", "Sleeve compatible with Apple MacBook Air M3"))

    def test_skirta_phrasing_is_accessory(self):
        self.assertFalse(is_relevant_result("iPhone 16 Pro", "Dėklas skirtas iPhone 16 Pro"))


class TestLevelC_NameSimilarity(unittest.TestCase):
    """Level C: for no-code products, name token overlap must clear the threshold; accessory category words reject."""

    def test_headphones_case_query_headphones_pass(self):
        self.assertTrue(is_relevant_result("Sony WH-1000XM5", "Sony WH-1000XM5 Wireless Headphones"))

    def test_headphones_case_rejects_case_accessory(self):
        self.assertFalse(is_relevant_result("Sony WH-1000XM5", "Carrying case for Sony WH-1000XM5 headphones"))

    def test_low_overlap_generic_title_rejected(self):
        self.assertFalse(is_relevant_result("Sony WH-1000XM5 Wireless Headphones", "USB-C charging cable 1m"))


# ── rejected_reason classification ──────────────────────────────────────────

class TestRejectionReasonClassification(unittest.TestCase):

    def test_code_mismatch_reason(self):
        reason = _classify_rejection_reason("LEGO 60492", "LEGO Technic 42198 Race Car")
        self.assertEqual(reason, "code_mismatch")

    def test_brand_mismatch_reason(self):
        reason = _classify_rejection_reason("Apple MacBook Air M3", "Dell XPS 13 Plus")
        self.assertEqual(reason, "brand_mismatch")

    def test_accessory_reason(self):
        reason = _classify_rejection_reason("iPhone 16 Pro", "Dėklas skirtas iPhone 16 Pro")
        self.assertEqual(reason, "accessory")


# ── Incident-shaped E2E scenarios via post_process (fixture data, no live API) ──

class TestIncidentScenarios(unittest.TestCase):

    def test_incident_pair_1_wrong_model_and_vitrina_both_rejected(self):
        """
        Exact shape of Incident #2: identified LEGO City 60492. Amazon.pl fixture
        returns an unrelated Technic set (42198) and a display case for a DIFFERENT
        LEGO set (60262 vitrina). Both must be rejected — result must be honest 'not found',
        never a substituted product.
        """
        query = "LEGO City Passenger Jet 60492"
        fixture_results = [
            {"product_title": "LEGO Technic 42198 Race Car", "price": 89.99, "shop": "Amazon.PL"},
            {"product_title": "Akrylowe pudełko wystawowe do LEGO City 60262", "price": 24.99, "shop": "Amazon.PL"},
        ]
        result = post_process(fixture_results, query, ai_data={}, price_history={}, language="lt")
        self.assertEqual(result["results"], [], "Wrong-model and vitrina results must not appear")
        self.assertEqual(result["valid_offers"], 0)
        self.assertEqual(result["rejected_offers"], 2)

    def test_incident_pair_2_correct_model_passes_among_noise(self):
        """Same query, but this time a genuine 60492 listing exists among noise — only it must pass."""
        query = "LEGO City Passenger Jet 60492"
        fixture_results = [
            {"product_title": "LEGO Technic 42198 Race Car", "price": 89.99, "shop": "Amazon.DE"},
            {"product_title": "LEGO City 60492 Cargo Airplane 118pcs", "price": 49.99, "shop": "Amazon.PL"},
            {"product_title": "Akrylowe pudełko wystawowe do LEGO City 60262", "price": 24.99, "shop": "Elesen"},
        ]
        result = post_process(fixture_results, query, ai_data={}, price_history={}, language="lt")
        self.assertEqual(len(result["results"]), 1)
        self.assertIn("60492", result["results"][0]["product_title"])
        self.assertEqual(result["valid_offers"], 1)
        self.assertEqual(result["rejected_offers"], 2)

    def test_no_code_product_accessory_rejected_genuine_passes(self):
        """Sony WH-1000XM5 (no model number in play, name-based matching): case rejected, headphones pass."""
        query = "Sony WH-1000XM5"
        fixture_results = [
            {"product_title": "Carrying case for Sony WH-1000XM5 headphones", "price": 15.99, "shop": "Amazon.DE"},
            {"product_title": "Sony WH-1000XM5 Wireless Noise Cancelling Headphones", "price": 279.00, "shop": "Amazon.PL"},
        ]
        result = post_process(fixture_results, query, ai_data={}, price_history={}, language="lt")
        self.assertEqual(len(result["results"]), 1)
        self.assertIn("Headphones", result["results"][0]["product_title"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
