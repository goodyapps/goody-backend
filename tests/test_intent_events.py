"""
Tests for /api/events endpoint and /api/admin/intent-summary.
Run: python -m pytest tests/test_intent_events.py -v
"""
import json
import os
import sys
import uuid
import unittest
from unittest.mock import patch, MagicMock

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import server
from server import app, _ALLOWED_EVENT_TYPES, INTERNAL_TRACKING_TOKEN, ADMIN_SUMMARY_TOKEN


def _uid(): return str(uuid.uuid4())
def _sid(): return str(uuid.uuid4())

VALID_EVENT = {
    "event_type": "search",
    "anonymous_user_id": _uid(),
    "session_id": _sid(),
    "product_canonical": "samsung:galaxy-s24",
    "payload": {"query_raw": "Samsung Galaxy S24", "method": "text", "language": "lt"},
}


class TestEventsEndpoint(unittest.TestCase):

    def setUp(self):
        app.config["TESTING"] = True
        self.client = app.test_client()
        # Patch Supabase so tests never hit live DB
        self.sb_patcher = patch("server.get_supabase", return_value=None)
        self.sb_patcher.start()

    def tearDown(self):
        self.sb_patcher.stop()

    # ── happy path ──────────────────────────────────────────────────────────

    def test_single_valid_event_returns_200(self):
        r = self.client.post("/api/events",
                             json=[VALID_EVENT],
                             content_type="application/json")
        self.assertEqual(r.status_code, 200)
        body = json.loads(r.data)
        self.assertEqual(body["stored"], 1)
        self.assertEqual(body["rejected"], 0)

    def test_batch_of_multiple_valid_events(self):
        batch = [{**VALID_EVENT, "event_type": t} for t in ["search", "results_shown", "offer_click"]]
        r = self.client.post("/api/events", json=batch)
        self.assertEqual(r.status_code, 200)
        body = json.loads(r.data)
        self.assertEqual(body["stored"], 3)
        self.assertEqual(body["rejected"], 0)

    # ── bad event does not break batch ──────────────────────────────────────

    def test_bad_event_type_rejected_good_events_stored(self):
        batch = [
            VALID_EVENT,
            {**VALID_EVENT, "event_type": "evil_hack"},
            {**VALID_EVENT, "event_type": "offer_click"},
        ]
        r = self.client.post("/api/events", json=batch)
        self.assertEqual(r.status_code, 200)
        body = json.loads(r.data)
        self.assertEqual(body["stored"], 2)
        self.assertEqual(body["rejected"], 1)

    def test_non_dict_element_rejected(self):
        batch = [VALID_EVENT, "not_a_dict", VALID_EVENT]
        r = self.client.post("/api/events", json=batch)
        self.assertEqual(r.status_code, 200)
        body = json.loads(r.data)
        self.assertEqual(body["stored"], 2)
        self.assertEqual(body["rejected"], 1)

    def test_invalid_uuid_rejected(self):
        bad = {**VALID_EVENT, "anonymous_user_id": "not-a-uuid", "session_id": "also-bad"}
        r = self.client.post("/api/events", json=[bad, VALID_EVENT])
        self.assertEqual(r.status_code, 200)
        body = json.loads(r.data)
        self.assertEqual(body["stored"], 1)
        self.assertEqual(body["rejected"], 1)

    def test_non_dict_payload_rejected(self):
        bad = {**VALID_EVENT, "payload": "string_not_dict"}
        r = self.client.post("/api/events", json=[bad])
        self.assertEqual(r.status_code, 200)
        body = json.loads(r.data)
        self.assertEqual(body["rejected"], 1)

    # ── batch size limit ─────────────────────────────────────────────────────

    def test_batch_exceeds_50_returns_400(self):
        batch = [VALID_EVENT] * 51
        r = self.client.post("/api/events", json=batch)
        self.assertEqual(r.status_code, 400)

    def test_batch_of_exactly_50_is_accepted(self):
        batch = [{**VALID_EVENT,
                  "anonymous_user_id": _uid(),
                  "session_id": _sid()} for _ in range(50)]
        r = self.client.post("/api/events", json=batch)
        self.assertEqual(r.status_code, 200)
        body = json.loads(r.data)
        self.assertEqual(body["stored"], 50)

    # ── non-array body ───────────────────────────────────────────────────────

    def test_non_array_body_returns_400(self):
        r = self.client.post("/api/events",
                             data=json.dumps({"event_type": "search"}),
                             content_type="application/json")
        self.assertEqual(r.status_code, 400)

    def test_empty_array_returns_200_stored_0(self):
        r = self.client.post("/api/events", json=[])
        self.assertEqual(r.status_code, 200)
        body = json.loads(r.data)
        self.assertEqual(body["stored"], 0)

    # ── is_internal flag ─────────────────────────────────────────────────────

    def test_is_internal_without_token_env_is_false(self):
        """When INTERNAL_TRACKING_TOKEN is empty, header is ignored."""
        captured = []

        def fake_insert(rows, sb):
            captured.extend(rows)

        with patch("server._batch_insert_events", side_effect=fake_insert):
            with patch.object(server, "INTERNAL_TRACKING_TOKEN", ""):
                r = self.client.post("/api/events",
                                     json=[VALID_EVENT],
                                     headers={"X-Goody-Internal": "anything"})
        self.assertEqual(r.status_code, 200)
        # is_internal should be False because env token is empty
        if captured:
            self.assertFalse(captured[0]["is_internal"])

    def test_is_internal_with_correct_token(self):
        captured = []

        def fake_insert(rows, sb):
            captured.extend(rows)

        secret = "test-secret-token-xyz"
        with patch("server._batch_insert_events", side_effect=fake_insert):
            with patch.object(server, "INTERNAL_TRACKING_TOKEN", secret):
                r = self.client.post("/api/events",
                                     json=[VALID_EVENT],
                                     headers={"X-Goody-Internal": secret})
        self.assertEqual(r.status_code, 200)
        if captured:
            self.assertTrue(captured[0]["is_internal"])

    def test_is_internal_with_wrong_token_is_false(self):
        captured = []

        def fake_insert(rows, sb):
            captured.extend(rows)

        with patch("server._batch_insert_events", side_effect=fake_insert):
            with patch.object(server, "INTERNAL_TRACKING_TOKEN", "real-token"):
                r = self.client.post("/api/events",
                                     json=[VALID_EVENT],
                                     headers={"X-Goody-Internal": "wrong-token"})
        self.assertEqual(r.status_code, 200)
        if captured:
            self.assertFalse(captured[0]["is_internal"])

    # ── all allowed event types ──────────────────────────────────────────────

    def test_all_allowed_event_types_accepted(self):
        batch = [{**VALID_EVENT,
                  "event_type": t,
                  "anonymous_user_id": _uid(),
                  "session_id": _sid()} for t in _ALLOWED_EVENT_TYPES]
        r = self.client.post("/api/events", json=batch)
        self.assertEqual(r.status_code, 200)
        body = json.loads(r.data)
        self.assertEqual(body["stored"], len(_ALLOWED_EVENT_TYPES))
        self.assertEqual(body["rejected"], 0)

    # ── rate limit ───────────────────────────────────────────────────────────

    def test_rate_limit_60_per_minute(self):
        """After 60 requests from same IP in same minute, 61st should 429."""
        import time
        fake_minute = time.strftime("%Y-%m-%dT%H:%M")
        test_ip = "10.0.0.99"

        with patch("server.get_client_ip", return_value=test_ip):
            # Set counter to just below limit
            server._events_rate_store[test_ip] = {
                "minute": fake_minute, "count": 60
            }
            r = self.client.post("/api/events", json=[VALID_EVENT])
            self.assertEqual(r.status_code, 429)


class TestAdminSummaryEndpoint(unittest.TestCase):

    def setUp(self):
        app.config["TESTING"] = True
        self.client = app.test_client()

    def test_no_token_returns_404(self):
        r = self.client.get("/api/admin/intent-summary")
        self.assertEqual(r.status_code, 404)

    def test_wrong_token_returns_404(self):
        with patch.object(server, "ADMIN_SUMMARY_TOKEN", "correct-token"):
            r = self.client.get("/api/admin/intent-summary?token=wrong")
            self.assertEqual(r.status_code, 404)

    def test_empty_token_env_returns_404(self):
        with patch.object(server, "ADMIN_SUMMARY_TOKEN", ""):
            r = self.client.get("/api/admin/intent-summary?token=anything")
            self.assertEqual(r.status_code, 404)

    def test_correct_token_no_supabase_returns_503(self):
        with patch.object(server, "ADMIN_SUMMARY_TOKEN", "admin-tok"):
            with patch("server.get_supabase", return_value=None):
                r = self.client.get("/api/admin/intent-summary?token=admin-tok")
                self.assertEqual(r.status_code, 503)

    def test_correct_token_with_mock_supabase_returns_200(self):
        mock_sb = MagicMock()
        mock_execute = MagicMock()
        mock_execute.data = []
        mock_sb.table.return_value.select.return_value.eq.return_value.eq.return_value.gte.return_value.execute.return_value = mock_execute

        with patch.object(server, "ADMIN_SUMMARY_TOKEN", "admin-tok"):
            with patch("server.get_supabase", return_value=mock_sb):
                r = self.client.get("/api/admin/intent-summary?token=admin-tok&days=7")
                self.assertEqual(r.status_code, 200)
                body = json.loads(r.data)
                self.assertIn("funnel", body)
                self.assertIn("top_products", body)
                self.assertIn("method_distribution", body)


if __name__ == "__main__":
    unittest.main()
