"""
AI Model Tracker.
Fetches trending and recent models from HuggingFace API,
cross-references with site posts, and generates docs/_data/models.json and docs/ai/models.md.
"""
import json
import os
import urllib.request
from datetime import datetime, timezone, timedelta

from post_parser import get_recent_posts

DATA_DIR = "docs/_data"
OUTPUT_JSON = os.path.join(DATA_DIR, "models.json")
OUTPUT_DIR = "docs/ai"
OUTPUT_PAGE = os.path.join(OUTPUT_DIR, "models.md")

HF_API_BASE = "https://huggingface.co/api/models"

# Map pipeline_tag to human-readable category
PIPELINE_CATEGORIES = {
    "text-generation": "Language Model",
    "text2text-generation": "Language Model",
    "text-to-image": "Image Generation",
    "image-to-text": "Vision Language",
    "image-classification": "Computer Vision",
    "object-detection": "Computer Vision",
    "image-segmentation": "Computer Vision",
    "automatic-speech-recognition": "Speech",
    "text-to-speech": "Speech",
    "text-to-audio": "Audio",
    "audio-classification": "Audio",
    "translation": "Translation",
    "summarization": "Summarization",
    "question-answering": "Question Answering",
    "fill-mask": "Language Model",
    "zero-shot-classification": "Classification",
    "sentence-similarity": "Embeddings",
    "feature-extraction": "Embeddings",
    "reinforcement-learning": "Reinforcement Learning",
    "video-classification": "Video",
    "depth-estimation": "Computer Vision",
}

# Badge colors per category
CATEGORY_COLORS = {
    "Language Model": "#8b5cf6",
    "Image Generation": "#ec4899",
    "Computer Vision": "#06b6d4",
    "Speech": "#f59e0b",
    "Audio": "#f59e0b",
    "Embeddings": "#10b981",
    "Translation": "#6366f1",
    "Summarization": "#6366f1",
    "Question Answering": "#6366f1",
    "Classification": "#6366f1",
    "Video": "#ef4444",
    "Reinforcement Learning": "#84cc16",
}

HISTORY_JSON = os.path.join(DATA_DIR, "models_history.json")
HISTORY_MAX_DAYS = 30
FEATURED_COOLDOWN_DAYS = 30


def _load_history():
    """Load models history (like snapshots + featured log)."""
    if os.path.exists(HISTORY_JSON):
        try:
            with open(HISTORY_JSON, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, OSError):
            pass
    return {"snapshots": {}, "featured_models": {}}


def _save_history(history):
    """Save history, pruning snapshots older than HISTORY_MAX_DAYS."""
    cutoff = (datetime.now(timezone.utc) - timedelta(days=HISTORY_MAX_DAYS)).strftime("%Y-%m-%d")
    history["snapshots"] = {
        d: v for d, v in history["snapshots"].items() if d >= cutoff
    }
    history["featured_models"] = {
        k: v for k, v in history.get("featured_models", {}).items() if v >= cutoff
    }
    with open(HISTORY_JSON, 'w', encoding='utf-8') as f:
        json.dump(history, f, indent=2, ensure_ascii=False)


def _compute_like_deltas(models, history):
    """Compute like gain since last snapshot for each model. Returns dict model_id -> delta."""
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


def _fetch_models(url):
    """Fetch models from HuggingFace API."""
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "eof.news Model Tracker"})
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode('utf-8'))
    except Exception as e:
        print(f"⚠️ HuggingFace API error: {e}")
        return []


def _parse_model(m):
    """Parse a HuggingFace model API response into our format."""
    model_id = m.get("modelId", m.get("id", ""))
    author = model_id.split("/")[0] if "/" in model_id else ""
    pipeline_tag = m.get("pipeline_tag", "")
    category = PIPELINE_CATEGORIES.get(pipeline_tag, "Other")

    created = m.get("createdAt", "")
    if created:
        created = created[:10]  # Just the date part

    return {
        "model_id": model_id,
        "author": author,
        "downloads": m.get("downloads", 0),
        "likes": m.get("likes", 0),
        "pipeline_tag": pipeline_tag,
        "category": category,
        "tags": m.get("tags", [])[:10],
        "created_at": created,
        "url": f"https://huggingface.co/{model_id}",
    }


def _cross_reference(models, posts):
    """Find related site posts for each model."""
    for model in models:
        related = []
        model_name = model['model_id'].lower()
        author = model['author'].lower()

        for post in posts:
            text = f"{post['title']} {' '.join(post['categories'])}".lower()
            # Check model name or author in post text
            if model_name in text or (author and len(author) > 3 and author in text):
                related.append({"title": post['title'], "url": post['url']})

        model['related_posts'] = related[:2]

    return models


def _pick_model_of_the_day(models, deltas, featured_log):
    """
    Select Model of the Day using weighted score:
      +30 created in last 7 days, +15 created in last 30 days (recency)
      +delta * 2  (momentum: like gain since last run)
      +10 if category not in last 3 featured categories (novelty)
    No repeats within FEATURED_COOLDOWN_DAYS.
    """
    if not models:
        return None

    now = datetime.now(timezone.utc)
    cutoff = (now - timedelta(days=FEATURED_COOLDOWN_DAYS)).strftime("%Y-%m-%d")
    week_ago = (now - timedelta(days=7)).strftime("%Y-%m-%d")
    month_ago = (now - timedelta(days=30)).strftime("%Y-%m-%d")

    # Models featured recently (within cooldown)
    recent_featured = {mid for mid, date in featured_log.items() if date >= cutoff}

    # Last 3 featured categories (for novelty bonus)
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


def publish_models():
    """Main entry point: fetch models, cross-reference, write JSON and page."""
    os.makedirs(DATA_DIR, exist_ok=True)
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # Fetch trending models (by likes, as 'trending' sort is not supported)
    print("Fetching trending models from HuggingFace...")
    trending_raw = _fetch_models(f"{HF_API_BASE}?sort=likes&direction=-1&limit=30")
    trending = [_parse_model(m) for m in trending_raw]
    print(f"Fetched {len(trending)} trending models")

    # Fetch recent models (last 7 days, sorted by likes to find notable ones)
    print("Fetching new releases from HuggingFace...")
    new_raw = _fetch_models(f"{HF_API_BASE}?sort=likes&direction=-1&limit=100")
    seven_days_ago = (datetime.now(timezone.utc) - timedelta(days=7)).strftime("%Y-%m-%d")
    new_releases = []
    for m in new_raw:
        parsed = _parse_model(m)
        if parsed['created_at'] and parsed['created_at'] >= seven_days_ago:
            new_releases.append(parsed)
    # Sort by likes descending
    new_releases.sort(key=lambda x: x['likes'], reverse=True)
    print(f"Found {len(new_releases)} new releases from last 7 days")

    # Cross-reference with AI posts
    posts = get_recent_posts(days=30, niche_filter={'ai'})
    trending = _cross_reference(trending, posts)
    new_releases = _cross_reference(new_releases, posts)

    # Load history, compute deltas (must happen BEFORE writing today's snapshot)
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
