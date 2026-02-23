"""
Trend Dashboard generator.
Analyzes post tags/categories to compute rising/falling topics, active sources, and top stories.
Outputs docs/_data/trends.json and docs/trends.md.
"""
import json
import os
from collections import Counter
from datetime import datetime, timezone, timedelta

from post_parser import get_all_posts

DATA_DIR = "docs/_data"
OUTPUT_JSON = os.path.join(DATA_DIR, "trends.json")
OUTPUT_PAGE = "docs/trends.md"


def _compute_trends():
    """Compute trend data from all posts."""
    now = datetime.now(timezone.utc)
    week_ago = now - timedelta(days=7)
    two_weeks_ago = now - timedelta(days=14)

    all_posts = get_all_posts()

    # Split into this week vs previous week
    this_week = [p for p in all_posts if p['date'] and p['date'] >= week_ago]
    prev_week = [p for p in all_posts
                 if p['date'] and two_weeks_ago <= p['date'] < week_ago]

    # --- Tag/category velocity ---
    tags_this = Counter()
    tags_prev = Counter()

    for p in this_week:
        for tag in p['categories']:
            tags_this[tag.lower()] += 1
        if p['niche_subniche']:
            tags_this[p['niche_subniche'].lower()] += 1

    for p in prev_week:
        for tag in p['categories']:
            tags_prev[tag.lower()] += 1
        if p['niche_subniche']:
            tags_prev[p['niche_subniche'].lower()] += 1

    all_tags = set(tags_this.keys()) | set(tags_prev.keys())
    topic_trends = []
    for tag in all_tags:
        curr = tags_this.get(tag, 0)
        prev = tags_prev.get(tag, 0)
        if curr == 0 and prev == 0:
            continue
        if prev == 0 and curr > 0:
            velocity = "rising"
            change = curr
        elif curr == 0 and prev > 0:
            velocity = "falling"
            change = -prev
        elif curr > prev:
            velocity = "rising"
            change = curr - prev
        elif curr < prev:
            velocity = "falling"
            change = curr - prev
        else:
            velocity = "stable"
            change = 0

        topic_trends.append({
            "topic": tag,
            "count_this_week": curr,
            "count_prev_week": prev,
            "change": change,
            "velocity": velocity,
        })

    # Sort: rising first (by change desc), then falling (by change asc)
    rising = sorted([t for t in topic_trends if t['velocity'] == 'rising'],
                    key=lambda x: x['change'], reverse=True)[:15]
    falling = sorted([t for t in topic_trends if t['velocity'] == 'falling'],
                     key=lambda x: x['change'])[:10]
    stable = sorted([t for t in topic_trends if t['velocity'] == 'stable'],
                    key=lambda x: x['count_this_week'], reverse=True)[:5]

    # --- Most active sources ---
    source_counter = Counter()
    for p in this_week:
        src = p['source']
        if src:
            source_counter[src] += 1

    active_sources = [{"source": s, "count": c}
                      for s, c in source_counter.most_common(10)]

    # --- Top stories this week ---
    top_stories = sorted(this_week, key=lambda p: p['score'], reverse=True)[:10]
    top_stories_data = []
    for p in top_stories:
        top_stories_data.append({
            "title": p['title'],
            "url": p['url'],
            "external_url": p['external_url'],
            "score": p['score'],
            "source": p['source'],
            "date": p['date'].strftime("%Y-%m-%d") if p['date'] else "",
            "niche_category": p['niche_category'],
        })

    return {
        "generated_at": now.strftime("%Y-%m-%d %H:%M:%S UTC"),
        "period": f"{week_ago.strftime('%Y-%m-%d')} to {now.strftime('%Y-%m-%d')}",
        "rising_topics": rising,
        "falling_topics": falling,
        "stable_topics": stable,
        "active_sources": active_sources,
        "top_stories": top_stories_data,
        "total_posts_this_week": len(this_week),
        "total_posts_prev_week": len(prev_week),
    }


def _generate_page():
    """Generate the Jekyll markdown page for trends."""
    lines = [
        "---",
        "layout: page",
        'title: "Trend Dashboard"',
        'description: "Rising and falling tech topics, most active sources, and top stories this week on eof.news"',
        "permalink: /trends/",
        "---",
        "",
        "## Rising Topics",
        "",
        "{% if site.data.trends.rising_topics.size > 0 %}",
        '<div class="trends-list">',
        "{% for topic in site.data.trends.rising_topics %}",
        '<div class="trend-item trend-rising">',
        '  <span class="trend-arrow" style="color: #22c55e;">&#9650;</span>',
        '  <span class="trend-topic"><strong>{{ topic.topic }}</strong></span>',
        '  <span class="trend-count">{{ topic.count_this_week }} posts</span>',
        '  <span class="trend-change" style="color: #22c55e;">+{{ topic.change }}</span>',
        '  <span class="trend-bar" style="display:inline-block; background:#22c55e; height:8px; width:{{ topic.count_this_week | times: 8 }}px; border-radius:4px;"></span>',
        "</div>",
        "{% endfor %}",
        "</div>",
        "{% else %}",
        "<p>No rising topics this week.</p>",
        "{% endif %}",
        "",
        "## Falling Topics",
        "",
        "{% if site.data.trends.falling_topics.size > 0 %}",
        '<div class="trends-list">',
        "{% for topic in site.data.trends.falling_topics %}",
        '<div class="trend-item trend-falling">',
        '  <span class="trend-arrow" style="color: #ef4444;">&#9660;</span>',
        '  <span class="trend-topic"><strong>{{ topic.topic }}</strong></span>',
        '  <span class="trend-count">{{ topic.count_this_week }} posts</span>',
        '  <span class="trend-change" style="color: #ef4444;">{{ topic.change }}</span>',
        "</div>",
        "{% endfor %}",
        "</div>",
        "{% else %}",
        "<p>No falling topics this week.</p>",
        "{% endif %}",
        "",
        "## Most Active Sources",
        "",
        "{% if site.data.trends.active_sources.size > 0 %}",
        "| Source | Posts This Week |",
        "|--------|----------------|",
        "{% for src in site.data.trends.active_sources %}",
        "| {{ src.source }} | {{ src.count }} |",
        "{% endfor %}",
        "{% else %}",
        "<p>No source data available.</p>",
        "{% endif %}",
        "",
        "## Top Stories This Week",
        "",
        "{% if site.data.trends.top_stories.size > 0 %}",
        "{% for story in site.data.trends.top_stories %}",
        '<div class="top-story" style="margin-bottom: 1em; padding: 0.5em 0; border-bottom: 1px solid #e5e7eb;">',
        '  <strong><a href="{{ story.external_url }}">{{ story.title }}</a></strong>',
        '  <br>',
        '  <span style="display:inline-block; padding:2px 8px; border-radius:12px; font-size:0.8em; background:#dbeafe; color:#1e40af;">score: {{ story.score }}</span>',
        '  <span style="font-size:0.85em; color:#6b7280;">{{ story.source }} &middot; {{ story.date }}</span>',
        "</div>",
        "{% endfor %}",
        "{% else %}",
        "<p>No stories this week.</p>",
        "{% endif %}",
        "",
        "---",
        "",
        '<p style="font-size:0.8em; color:#9ca3af;">',
        "Updated: {{ site.data.trends.generated_at }} &middot; ",
        "{{ site.data.trends.total_posts_this_week }} posts this week vs {{ site.data.trends.total_posts_prev_week }} last week",
        "</p>",
        "",
    ]
    return "\n".join(lines)


def publish_trends():
    """Main entry point: compute trends, write JSON and page."""
    os.makedirs(DATA_DIR, exist_ok=True)

    data = _compute_trends()

    with open(OUTPUT_JSON, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"✅ Trends JSON written: {OUTPUT_JSON}")

    page_content = _generate_page()
    with open(OUTPUT_PAGE, 'w', encoding='utf-8') as f:
        f.write(page_content)
    print(f"✅ Trends page written: {OUTPUT_PAGE}")
