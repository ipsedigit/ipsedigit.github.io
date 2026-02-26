from datetime import datetime, timezone, timedelta
from models import _pick_model_of_the_day

TODAY = datetime.now(timezone.utc).strftime("%Y-%m-%d")
WEEK_AGO = (datetime.now(timezone.utc) - timedelta(days=6)).strftime("%Y-%m-%d")
OLD = (datetime.now(timezone.utc) - timedelta(days=60)).strftime("%Y-%m-%d")


def _make_model(model_id, likes=100, created_at=OLD, category="Language Model"):
    return {"model_id": model_id, "likes": likes, "created_at": created_at,
            "category": category, "author": "test", "downloads": 0,
            "url": f"https://huggingface.co/{model_id}", "tags": [],
            "pipeline_tag": "", "related_posts": []}


def test_returns_none_for_empty():
    assert _pick_model_of_the_day([], {}, {}) is None


def test_new_model_beats_old_popular():
    old_popular = _make_model("org/old", likes=10000, created_at=OLD)
    new_model = _make_model("org/new", likes=50, created_at=TODAY)
    result = _pick_model_of_the_day([old_popular, new_model], {}, {})
    assert result["model_id"] == "org/new"


def test_respects_cooldown():
    m = _make_model("org/recent", likes=500, created_at=TODAY)
    featured = {"org/recent": TODAY}  # featured today, should be skipped
    other = _make_model("org/other", likes=10, created_at=WEEK_AGO)
    result = _pick_model_of_the_day([m, other], {}, featured)
    assert result["model_id"] == "org/other"


def test_high_delta_wins_over_same_age():
    m1 = _make_model("org/m1", likes=100, created_at=WEEK_AGO)
    m2 = _make_model("org/m2", likes=100, created_at=WEEK_AGO)
    deltas = {"org/m1": 5, "org/m2": 200}
    result = _pick_model_of_the_day([m1, m2], deltas, {})
    assert result["model_id"] == "org/m2"
