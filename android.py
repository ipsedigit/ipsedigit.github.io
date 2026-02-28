"""
Android Developer Tracker.
Fetches curated news from Android RSS feeds.
Generates docs/_data/android.json and docs/android/index.md.
"""
import json
import os
import re
import feedparser
from datetime import datetime, timezone

DATA_DIR = "docs/_data"
OUTPUT_JSON = os.path.join(DATA_DIR, "android.json")
OUTPUT_DIR = "docs/android"
OUTPUT_PAGE = os.path.join(OUTPUT_DIR, "index.md")
MAX_ARTICLES = 20
MIN_EXCERPT_LENGTH = 40  # articles without a real description are skipped

RSS_SOURCES = [
    {"name": "Android Developers Blog", "url": "https://feeds.feedburner.com/blogspot/hsDu"},
    {"name": "ProAndroidDev",            "url": "https://proandroiddev.com/feed"},
    {"name": "Android Authority",        "url": "https://www.androidauthority.com/feed/"},
    {"name": "Kotlin Blog",              "url": "https://blog.jetbrains.com/kotlin/feed/"},
    {"name": "Android Weekly",           "url": "https://androidweekly.net/issues/rss"},
]


def _fetch_rss_articles():
    """Fetch articles from Android RSS feeds. Only keeps articles with a real excerpt."""
    articles = []
    for source in RSS_SOURCES:
        try:
            feed = feedparser.parse(source["url"])
            for entry in feed.entries[:20]:
                title = (entry.get("title") or "").strip()
                link = (entry.get("link") or "").strip()
                if not title or not link:
                    continue
                summary = (entry.get("summary") or entry.get("description") or "").strip()
                if summary:
                    summary = re.sub(r"<[^>]+>", "", summary).strip()
                    # Collapse whitespace
                    summary = re.sub(r"\s+", " ", summary)[:280]
                # Skip articles with no real description
                if len(summary) < MIN_EXCERPT_LENGTH:
                    continue
                pub = entry.get("published_parsed") or entry.get("updated_parsed")
                if pub and len(pub) >= 6:
                    try:
                        dt = datetime(pub[0], pub[1], pub[2], pub[3], pub[4], pub[5], tzinfo=timezone.utc)
                    except (TypeError, ValueError):
                        dt = datetime.now(timezone.utc)
                else:
                    dt = datetime.now(timezone.utc)
                articles.append({
                    "title": title,
                    "url": link,
                    "source": source["name"],
                    "published": dt.strftime("%Y-%m-%dT%H:%M:%SZ"),
                    "excerpt": summary,
                })
        except Exception as e:
            print(f"  RSS error [{source['name']}]: {e}")

    # Sort by date descending, deduplicate by URL
    seen_urls = set()
    unique = []
    articles.sort(key=lambda a: a["published"], reverse=True)
    for a in articles:
        if a["url"] not in seen_urls:
            seen_urls.add(a["url"])
            unique.append(a)

    print(f"  Articles fetched: {len(unique)} (with excerpt, from {len(RSS_SOURCES)} feeds)")
    return unique[:MAX_ARTICLES]


def _generate_page(articles):
    """Generate the Jekyll markdown page for /android/."""
    lines = [
        "---",
        "layout: page",
        'title: "Android Dev News"',
        'description: "Curated news for Android developers. Kotlin, Jetpack Compose, and the Android ecosystem — updated daily."',
        "permalink: /android/",
        "---",
        "",
        "{% assign articles = site.data.android.articles %}",
        "",
        '<p style="font-size:0.9em; color:#6b7280; margin-bottom:1.5em;">{{ articles.size }} articles &middot; Updated: {{ site.data.android.generated_at }}</p>',
        "",
        "{% for article in articles %}",
        '<div style="margin-bottom:1.25em; padding:0.85em; border:1px solid #e5e7eb; border-radius:8px;">',
        '  <div style="margin-bottom:0.3em;">',
        '    <strong><a href="{{ article.url }}" target="_blank" rel="noopener">{{ article.title }}</a></strong>',
        '  </div>',
        '  <p style="margin:0 0 0.4em 0; font-size:0.88em; color:#374151; line-height:1.5;">{{ article.excerpt }}</p>',
        '  <span style="font-size:0.78em; color:#9ca3af;">{{ article.source }} &middot; {{ article.published | slice: 0, 10 }}</span>',
        "</div>",
        "{% endfor %}",
        "",
    ]
    return "\n".join(lines)


def publish_android():
    """Main entry point: fetch articles, generate outputs."""
    os.makedirs(DATA_DIR, exist_ok=True)
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    print("=== Android Tracker ===")
    articles = _fetch_rss_articles()

    now = datetime.now(timezone.utc)
    output = {
        "generated_at": now.strftime("%Y-%m-%d %H:%M:%S UTC"),
        "total_articles": len(articles),
        "articles": articles,
    }

    with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    print(f"  JSON written: {OUTPUT_JSON}")

    page_content = _generate_page(articles)
    with open(OUTPUT_PAGE, "w", encoding="utf-8") as f:
        f.write(page_content)
    print(f"  Page written: {OUTPUT_PAGE}")
    print("=== Done ===")
