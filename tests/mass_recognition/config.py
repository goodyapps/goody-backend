"""Thresholds and constants for the mass recognition test harness."""

# Pass thresholds (fraction, 0–1)
THRESHOLD_LEGO       = 0.98   # numbered-set products
THRESHOLD_GENERIC    = 0.90   # generic household without model numbers
THRESHOLD_ELECTRONICS= 0.95
THRESHOLD_HARD_CASE  = 0.85   # hard cases may be inherently harder
THRESHOLD_LOYALTY    = 0.90
THRESHOLD_OVERALL    = 0.93   # across all categories

# Staged sample sizes
SAMPLE_SIZES = [50, 200, 500]

# Budget caps (live modes only)
MAX_VISION_CALLS   = 550
MAX_SCRAPER_CALLS  = 4000

# Concurrency limit
MAX_CONCURRENT = 5

# Cache directory
import pathlib
CACHE_DIR = pathlib.Path(__file__).parent.parent / "fixtures" / "cache"
FIXTURE_PATH = pathlib.Path(__file__).parent.parent / "fixtures" / "mass_test_products.json"

# Category → threshold mapping
CATEGORY_THRESHOLDS = {
    "lego":           THRESHOLD_LEGO,
    "electronics":    THRESHOLD_ELECTRONICS,
    "generic":        THRESHOLD_GENERIC,
    "hard_case":      THRESHOLD_HARD_CASE,
    "loyalty_pricing":THRESHOLD_LOYALTY,
}
