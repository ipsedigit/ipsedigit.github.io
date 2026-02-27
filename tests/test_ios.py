import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from ios import _pick_spotlight, _clean_summary, _format_date, _generate_page


def _item(title, url="http://example.com", published="2026-01-01T00:00:00+00:00", source="Swift Blog"):
    return {"title": title, "url": url, "published": published, "summary": "Test summary.", "source": source, "source_key": "test"}


def test_pick_spotlight_prefers_keyword_match():
    items = [
        _item("Random article"),
        _item("Swift 6 is here"),
        _item("Another article"),
    ]
    result = _pick_spotlight(items)
    assert result["title"] == "Swift 6 is here"


def test_pick_spotlight_falls_back_to_first():
    items = [_item("No keywords here"), _item("Also nothing")]
    result = _pick_spotlight(items)
    assert result == items[0]


def test_pick_spotlight_empty():
    assert _pick_spotlight([]) is None


def test_clean_summary_strips_html():
    result = _clean_summary("<p>Hello <b>world</b></p>")
    assert "<" not in result
    assert "Hello world" in result


def test_clean_summary_truncates():
    long_text = "x" * 300
    result = _clean_summary(long_text)
    assert len(result) <= 203  # 200 + "…"
    assert result.endswith("\u2026")


def test_format_date_parses_iso():
    result = _format_date("2026-01-15T10:00:00+00:00")
    assert "Jan" in result
    assert "2026" in result


def test_format_date_empty():
    assert _format_date("") == ""


def test_generate_page_contains_permalink():
    data = {
        "generated_at": "2026-01-01 00:00:00 UTC",
        "spotlight": _item("Swift 6 released"),
        "apple_official": [_item("News item 1"), _item("News item 2")],
        "community": [_item("Community post", source="NSHipster")],
    }
    page = _generate_page(data)
    assert "permalink: /ios/" in page
    assert "Swift 6 released" in page
    assert "Community" in page


def test_generate_page_no_spotlight():
    data = {
        "generated_at": "2026-01-01 00:00:00 UTC",
        "spotlight": None,
        "apple_official": [],
        "community": [],
    }
    page = _generate_page(data)
    assert "permalink: /ios/" in page
