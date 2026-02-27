from datetime import datetime, timezone, timedelta
from outages import _parse_incident, _is_recent_resolved, _generate_page


def test_parse_incident_maps_fields():
    raw = {
        "id": "abc123",
        "name": "API is down",
        "status": "investigating",
        "impact": "critical",
        "created_at": "2026-02-27T09:00:00Z",
        "resolved_at": None,
        "updated_at": "2026-02-27T09:15:00Z",
        "shortlink": "https://stspg.io/abc123",
    }
    result = _parse_incident(raw, "GitHub")
    assert result["id"] == "abc123"
    assert result["name"] == "API is down"
    assert result["status"] == "investigating"
    assert result["impact"] == "critical"
    assert result["service"] == "GitHub"
    assert result["resolved_at"] is None
    assert result["shortlink"] == "https://stspg.io/abc123"


def test_parse_incident_falls_back_to_started_at():
    raw = {
        "id": "x",
        "name": "Test",
        "status": "monitoring",
        "impact": "minor",
        "started_at": "2026-02-27T08:00:00Z",
        "resolved_at": None,
        "updated_at": "",
        "shortlink": "",
    }
    result = _parse_incident(raw, "Stripe")
    assert result["started_at"] == "2026-02-27T08:00:00Z"


def test_is_recent_resolved_within_24h():
    recent = (datetime.now(timezone.utc) - timedelta(hours=2)).isoformat()
    inc = {"resolved_at": recent}
    assert _is_recent_resolved(inc) is True


def test_is_recent_resolved_older_than_24h():
    old = (datetime.now(timezone.utc) - timedelta(hours=25)).isoformat()
    inc = {"resolved_at": old}
    assert _is_recent_resolved(inc) is False


def test_is_recent_resolved_no_resolved_at():
    assert _is_recent_resolved({"resolved_at": None}) is False
    assert _is_recent_resolved({}) is False


def test_generate_page_all_clear():
    page = _generate_page([], [], "2026-02-27 10:00:00 UTC")
    assert "All systems operational" in page
    assert "Active Incidents" not in page
    assert "Resolved" not in page


def test_generate_page_active_incident():
    active = [{
        "service": "GitHub",
        "name": "API slowness",
        "status": "investigating",
        "impact": "critical",
        "started_at": "2026-02-27T09:00:00Z",
        "updated_at": "2026-02-27T09:15:00Z",
        "resolved_at": None,
        "shortlink": "https://stspg.io/x",
    }]
    page = _generate_page(active, [], "2026-02-27 10:00:00 UTC")
    assert "Active Incidents" in page
    assert "GitHub" in page
    assert "CRITICAL" in page
    assert "All systems operational" not in page


def test_generate_page_resolved_section():
    resolved = [{
        "service": "Stripe",
        "name": "Payments degraded",
        "status": "resolved",
        "impact": "major",
        "started_at": "2026-02-27T06:00:00Z",
        "updated_at": "2026-02-27T08:00:00Z",
        "resolved_at": "2026-02-27T08:30:00Z",
        "shortlink": "",
    }]
    page = _generate_page([], resolved, "2026-02-27 10:00:00 UTC")
    assert "Resolved (last 24h)" in page
    assert "Stripe" in page
    assert "Active Incidents" not in page


def test_generate_page_active_count_in_banner():
    active = [
        {"service": "GitHub", "name": "Down", "status": "investigating",
         "impact": "critical", "started_at": "", "updated_at": "", "resolved_at": None, "shortlink": ""},
        {"service": "Stripe", "name": "Slow", "status": "identified",
         "impact": "major", "started_at": "", "updated_at": "", "resolved_at": None, "shortlink": ""},
    ]
    page = _generate_page(active, [], "2026-02-27 10:00:00 UTC")
    assert "2 active incidents" in page
