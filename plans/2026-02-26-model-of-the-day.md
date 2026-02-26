# Model of the Day Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Add a "Model of the Day" spotlight card to `/ai/models/` with like-delta tracking and a weighted selection algorithm, giving the page unique editorial signal over HuggingFace.

**Architecture:** `models.py` gains like-delta tracking via `docs/_data/models_history.json` (same pattern as `github_history.json`). A `_pick_model_of_the_day()` function scores models by recency + momentum + novelty. `_generate_page()` renders a spotlight card at the top, plus `+X` delta badges on the trending list.

**Tech Stack:** Python stdlib, Jekyll/Liquid, `docs/_data/models.json`, `docs/_data/models_history.json`

---

### Task 1: Add like-delta tracking (history snapshots)

**Files:**
- Modify: `models.py` — add `_load_history()`, `_save_history()`, `_compute_like_deltas()`

**Step 1: Add history constants and load/save helpers after the existing constants block**

In `models.py`, after `CATEGORY_COLORS = { ... }`, add:

```python
HISTORY_JSON = os.path.join(DATA_DIR, "models_history.json")
HISTORY_MAX_DAYS = 30
FEATURED_COOLDOWN_DAYS = 30
```

**Step 2: Add `_load_history()` after the constants**

```python
def _load_history():
    """Load models history (like snapshots + featured log)."""
    if os.path.exists(HISTORY_JSON):
        try:
            with open(HISTORY_JSON, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            pass
    return {"snapshots": {}, "featured_models": {}}
```

**Step 3: Add `_save_history()` after `_load_history()`**

```python
def _save_history(history):
    """Save history, pruning snapshots older than HISTORY_MAX_DAYS."""
    cutoff = (datetime.now(timezone.utc) - timedelta(days=HISTORY_MAX_DAYS)).strftime("%Y-%m-%d")
    history["snapshots"] = {
        d: v for d, v in history["snapshots"].items() if d >= cutoff
    }
    with open(HISTORY_JSON, 'w', encoding='utf-8') as f:
        json.dump(history, f, indent=2, ensure_ascii=False)
```

**Step 4: Add `_compute_like_deltas()` after `_save_history()`**

```python
def _compute_like_deltas(models, history):
    """Compute like gain since last snapshot for each model. Returns dict model_id → delta."""
    snapshots = history.get("snapshots", {})
    if not snapshots:
        return {}
    # Use the most recent previous snapshot
    dates = sorted(snapshots.keys(), reverse=True)
    prev = snapshots[dates[0]].get("models", {})
    deltas = {}
    for m in models:
        mid = m["model_id"]
        if mid in prev:
            deltas[mid] = m["likes"] - prev[mid].get("likes", m["likes"])
    return deltas
```

**Step 5: Verify the file parses without errors**

```bash
cd C:/repo/ipsedigit.github.io && python -c "import models; print('ok')"
```
Expected: `ok`

**Step 6: Commit**

```bash
git add models.py
git commit -m "feat: add like-delta history tracking to models.py"
```

---

### Task 2: Add `_pick_model_of_the_day()`

**Files:**
- Modify: `models.py` — add `_pick_model_of_the_day()`
- Create: `tests/test_model_of_the_day.py`

**Step 1: Write the failing test**

Create `tests/test_model_of_the_day.py`:

```python
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
```

**Step 2: Run test to verify it fails**

```bash
cd C:/repo/ipsedigit.github.io && python -m pytest tests/test_model_of_the_day.py -v
```
Expected: `ImportError` or `AttributeError` — function doesn't exist yet.

**Step 3: Implement `_pick_model_of_the_day()` in `models.py`** (add before `_generate_page`)

```python
def _pick_model_of_the_day(models, deltas, featured_log):
    """
    Select Model of the Day using weighted score:
      +30 created in last 7 days, +15 created in last 30 days (recency)
      +delta * 2  (momentum: like gain since last run)
      +10 if category not in last 3 featured (novelty)
    No repeats within FEATURED_COOLDOWN_DAYS.
    """
    if not models:
        return None

    now = datetime.now(timezone.utc)
    cutoff = (now - timedelta(days=FEATURED_COOLDOWN_DAYS)).strftime("%Y-%m-%d")
    today = now.strftime("%Y-%m-%d")
    week_ago = (now - timedelta(days=7)).strftime("%Y-%m-%d")
    month_ago = (now - timedelta(days=30)).strftime("%Y-%m-%d")

    # Models featured recently (within cooldown)
    recent_featured = {mid for mid, date in featured_log.items() if date >= cutoff}

    # Last 3 featured categories
    recent_by_date = sorted(
        [(mid, d) for mid, d in featured_log.items() if d >= cutoff],
        key=lambda x: x[1], reverse=True
    )[:3]
    recent_categories = set()
    for mid, _ in recent_by_date:
        for m in models:
            if m["model_id"] == mid:
                recent_categories.add(m["category"])
                break

    candidates = [m for m in models if m["model_id"] not in recent_featured]
    if not candidates:
        candidates = list(models)

    def score(m):
        s = 0.0
        created = m.get("created_at") or ""
        if created >= week_ago:
            s += 30
        elif created >= month_ago:
            s += 15
        delta = deltas.get(m["model_id"], 0)
        s += max(delta, 0) * 2
        if m.get("category") not in recent_categories:
            s += 10
        return s

    candidates.sort(key=score, reverse=True)
    return candidates[0]
```

**Step 4: Run tests to verify they pass**

```bash
cd C:/repo/ipsedigit.github.io && python -m pytest tests/test_model_of_the_day.py -v
```
Expected: 4 tests PASS

**Step 5: Commit**

```bash
git add models.py tests/test_model_of_the_day.py
git commit -m "feat: add _pick_model_of_the_day() with recency+momentum+novelty scoring"
```

---

### Task 3: Wire history + featured model into `publish_models()`

**Files:**
- Modify: `models.py` — update `publish_models()`

**Step 1: Update `publish_models()` to load history, compute deltas, pick featured, save snapshot**

Replace the end of `publish_models()` — from the `# Category stats` block through `json.dump` — with:

```python
    # Load history, compute deltas
    history = _load_history()
    all_models = trending + new_releases
    deltas = _compute_like_deltas(all_models, history)

    # Snapshot today's likes
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    history["snapshots"][today] = {
        "models": {m["model_id"]: {"likes": m["likes"]} for m in all_models}
    }

    # Pick Model of the Day
    featured_log = history.get("featured_models", {})
    featured = _pick_model_of_the_day(trending + new_releases, deltas, featured_log)
    if featured:
        history["featured_models"][featured["model_id"]] = today
        featured["like_delta"] = deltas.get(featured["model_id"], 0)

    _save_history(history)

    # Attach deltas to trending list for display
    for m in trending:
        m["like_delta"] = deltas.get(m["model_id"], 0)

    # Category stats
    from collections import Counter
    cat_counts = Counter(m['category'] for m in trending)
    top_categories = [{"category": c, "count": n}
                      for c, n in cat_counts.most_common(5)]

    now = datetime.now(timezone.utc)
    output = {
        "generated_at": now.strftime("%Y-%m-%d %H:%M:%S UTC"),
        "featured_model": featured,
        "trending": trending,
        "new_releases": new_releases[:20],
        "top_categories": top_categories,
    }

    with open(OUTPUT_JSON, 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    print(f"✅ Models JSON written: {OUTPUT_JSON}")

    page_content = _generate_page()
    with open(OUTPUT_PAGE, 'w', encoding='utf-8') as f:
        f.write(page_content)
    print(f"✅ Models page written: {OUTPUT_PAGE}")
```

**Step 2: Verify it parses**

```bash
cd C:/repo/ipsedigit.github.io && python -c "import models; print('ok')"
```
Expected: `ok`

**Step 3: Commit**

```bash
git add models.py
git commit -m "feat: wire history snapshots and featured model into publish_models()"
```

---

### Task 4: Add spotlight card and delta badges to `_generate_page()`

**Files:**
- Modify: `models.py` — update `_generate_page()`

**Step 1: Replace `_generate_page()` entirely with the updated version**

```python
def _generate_page():
    """Generate the Jekyll markdown page for AI model tracker."""
    lines = [
        "---",
        "layout: page",
        'title: "AI Model Tracker"',
        'description: "Trending and newly released AI models from HuggingFace, tracked daily with cross-references to eof.news coverage."',
        "permalink: /ai/models/",
        "---",
        "",
        "## Stats",
        "",
        '<div style="display:flex; gap:1em; flex-wrap:wrap; margin-bottom:1.5em;">',
        '  <span style="padding:4px 12px; border-radius:12px; background:#dbeafe; color:#1e40af; font-weight:bold;">Trending: {{ site.data.models.trending | size }}</span>',
        '  <span style="padding:4px 12px; border-radius:12px; background:#dcfce7; color:#166534; font-weight:bold;">New Releases: {{ site.data.models.new_releases | size }}</span>',
        "</div>",
        "",
        # ── Model of the Day card ──────────────────────────────────
        "{% if site.data.models.featured_model %}",
        "{% assign f = site.data.models.featured_model %}",
        '<div style="margin-bottom:2em; padding:1.25em; border:2px solid #8b5cf6; border-radius:8px; background:#faf5ff;">',
        '  <div style="display:flex; align-items:center; gap:0.5em; flex-wrap:wrap; margin-bottom:0.75em;">',
        '    <span style="padding:3px 10px; border-radius:12px; font-size:0.78em; font-weight:bold; background:#8b5cf6; color:#fff;">✦ Model of the Day</span>',
        '    <strong style="font-size:1.15em;"><a href="{{ f.url }}" target="_blank" rel="noopener" style="color:#111;">{{ f.model_id }}</a></strong>',
        '    {% if f.category %}<span style="display:inline-block; padding:2px 8px; border-radius:12px; font-size:0.78em; color:#fff; background:#8b5cf6;">{{ f.category }}</span>{% endif %}',
        '    {% if f.like_delta > 0 %}<span style="font-size:0.82em; color:#059669; font-weight:bold;">🔥 +{{ f.like_delta }} likes</span>{% endif %}',
        '  </div>',
        '  <div style="display:flex; gap:1.5em; flex-wrap:wrap; font-size:0.82em; color:#6b7280;">',
        '    <span>by {{ f.author }}</span>',
        '    <span>&#10515; {{ f.downloads }}</span>',
        '    <span>&#9829; {{ f.likes }}</span>',
        '    {% if f.created_at %}<span>Released {{ f.created_at }}</span>{% endif %}',
        '  </div>',
        '  {% if f.tags.size > 0 %}',
        '  <div style="margin-top:0.6em; display:flex; gap:0.4em; flex-wrap:wrap;">',
        '    {% for tag in f.tags limit:4 %}',
        '    <span style="padding:2px 6px; background:#ede9fe; color:#6d28d9; border-radius:4px; font-size:0.75em;">{{ tag }}</span>',
        '    {% endfor %}',
        '  </div>',
        '  {% endif %}',
        "</div>",
        "{% endif %}",
        "",
        # ── Trending list ──────────────────────────────────────────
        "## Trending Models",
        "",
        "{% if site.data.models.trending.size > 0 %}",
        "{% for model in site.data.models.trending %}",
        '<div style="margin-bottom:1.2em; padding:0.75em; border:1px solid #e5e7eb; border-radius:8px;">',
        '  <strong><a href="{{ model.url }}" target="_blank" rel="noopener">{{ model.model_id }}</a></strong>',
        "  {% if model.category %}",
        '    <span style="display:inline-block; padding:2px 8px; border-radius:12px; font-size:0.75em; color:#fff; margin-left:0.5em; background:{% if model.category == \'Language Model\' %}#8b5cf6{% elsif model.category == \'Image Generation\' %}#ec4899{% elsif model.category == \'Computer Vision\' %}#06b6d4{% elsif model.category == \'Speech\' or model.category == \'Audio\' %}#f59e0b{% elsif model.category == \'Embeddings\' %}#10b981{% else %}#6366f1{% endif %};">{{ model.category }}</span>',
        "  {% endif %}",
        '  {% if model.like_delta > 0 %}<span style="font-size:0.78em; color:#059669; margin-left:0.5em;">▲ +{{ model.like_delta }}</span>{% endif %}',
        "  <br>",
        '  <span style="font-size:0.85em; color:#6b7280;">',
        "    by {{ model.author }}",
        "    &middot; &#10515; {{ model.downloads }}",
        "    &middot; &#9829; {{ model.likes }}",
        "  </span>",
        "  {% if model.related_posts.size > 0 %}",
        '  <br><span style="font-size:0.8em;">Coverage: ',
        "  {% for rp in model.related_posts %}",
        '    <a href="{{ rp.url }}" target="_blank" rel="noopener">{{ rp.title | truncate: 50 }}</a>{% unless forloop.last %}, {% endunless %}',
        "  {% endfor %}",
        "  </span>",
        "  {% endif %}",
        "</div>",
        "{% endfor %}",
        "{% else %}",
        "<p>No trending models data yet. Check back after the next update.</p>",
        "{% endif %}",
        "",
        # ── New releases ───────────────────────────────────────────
        "## New Releases (Last 7 Days)",
        "",
        "{% if site.data.models.new_releases.size > 0 %}",
        "{% for model in site.data.models.new_releases %}",
        '<div style="margin-bottom:1em; padding:0.5em 0; border-bottom:1px solid #e5e7eb;">',
        '  <strong><a href="{{ model.url }}" target="_blank" rel="noopener">{{ model.model_id }}</a></strong>',
        "  {% if model.category %}",
        '    <span style="display:inline-block; padding:2px 8px; border-radius:12px; font-size:0.75em; color:#fff; background:{% if model.category == \'Language Model\' %}#8b5cf6{% elsif model.category == \'Image Generation\' %}#ec4899{% elsif model.category == \'Computer Vision\' %}#06b6d4{% elsif model.category == \'Speech\' or model.category == \'Audio\' %}#f59e0b{% elsif model.category == \'Embeddings\' %}#10b981{% else %}#6366f1{% endif %};">{{ model.category }}</span>',
        "  {% endif %}",
        "  <br>",
        '  <span style="font-size:0.85em; color:#6b7280;">',
        "    by {{ model.author }}",
        "    &middot; &#10515; {{ model.downloads }}",
        "    &middot; Created: {{ model.created_at }}",
        "  </span>",
        "</div>",
        "{% endfor %}",
        "{% else %}",
        "<p>No new releases this week.</p>",
        "{% endif %}",
        "",
        "---",
        "",
        '<p style="font-size:0.8em; color:#9ca3af;">',
        'Data from <a href="https://huggingface.co/">HuggingFace</a> &middot; Updated: {{ site.data.models.generated_at }}',
        "</p>",
        "",
    ]
    return "\n".join(lines)
```

**Step 2: Verify it parses**

```bash
cd C:/repo/ipsedigit.github.io && python -c "import models; print(models._generate_page()[:200])"
```
Expected: first 200 chars of the page with frontmatter

**Step 3: Commit**

```bash
git add models.py
git commit -m "feat: add Model of the Day spotlight card and delta badges to models page"
```

---

### Task 5: Seed `models.json` and `models.md` with current data

Since the workflow won't run until tomorrow, manually regenerate the files so the page is live now.

**Step 1: Run publish_models() locally**

```bash
cd C:/repo/ipsedigit.github.io && python -c "from models import publish_models; publish_models()"
```
Expected output:
```
Fetching trending models from HuggingFace...
Fetched 30 trending models
Fetching new releases from HuggingFace...
Found N new releases from last 7 days
✅ Models JSON written: docs/_data/models.json
✅ Models page written: docs/ai/models.md
```

**Step 2: Verify `featured_model` is in the JSON**

```bash
cd C:/repo/ipsedigit.github.io && python -c "
import json
with open('docs/_data/models.json') as f:
    d = json.load(f)
f = d.get('featured_model')
print('Featured:', f['model_id'] if f else 'NONE')
print('Delta:', f.get('like_delta') if f else '-')
"
```
Expected: a model ID and a delta (0 is fine on first run — no previous snapshot yet)

**Step 3: Verify `models_history.json` was created**

```bash
cd C:/repo/ipsedigit.github.io && python -c "
import json
with open('docs/_data/models_history.json') as f:
    d = json.load(f)
print('Snapshots:', list(d['snapshots'].keys()))
print('Featured:', list(d['featured_models'].keys())[:3])
"
```

**Step 4: Commit generated files**

```bash
git add docs/_data/models.json docs/_data/models_history.json docs/ai/models.md
git commit -m "feat: seed Model of the Day data (models.json, models_history.json, models.md)"
```
