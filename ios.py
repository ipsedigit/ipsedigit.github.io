"""
iOS Developer Tracker.
Fetches curated news from iOS/Apple RSS feeds.
Generates docs/_data/ios.json and docs/ios/index.md.
"""
import json
import os
import re
import feedparser
from datetime import datetime, timezone

DATA_DIR = "docs/_data"
OUTPUT_JSON = os.path.join(DATA_DIR, "ios.json")
OUTPUT_DIR = "docs/ios"
OUTPUT_PAGE = os.path.join(OUTPUT_DIR, "index.md")
MAX_ARTICLES = 20
MIN_EXCERPT_LENGTH = 40

RSS_SOURCES = [
    {"name": "Apple Developer News",  "url": "https://developer.apple.com/news/rss/news.rss"},
    {"name": "Swift Blog",            "url": "https://www.swift.org/atom.xml"},
    {"name": "NSHipster",             "url": "https://nshipster.com/feed.xml"},
    {"name": "Hacking with Swift",    "url": "https://www.hackingwithswift.com/articles/rss"},
    {"name": "Swift by Sundell",      "url": "https://swiftbysundell.com/feed.rss"},
    {"name": "iOS Dev Weekly",        "url": "https://iosdevweekly.com/issues.rss"},
]


def _fetch_rss_articles():
    """Fetch articles from iOS RSS feeds. Only keeps articles with a real excerpt."""
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
                    summary = re.sub(r"\s+", " ", summary)[:280]
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
    """Generate the Jekyll markdown page for /ios/."""
    lines = [
        "---",
        "layout: page",
        'title: "iOS Dev News"',
        'description: "Curated news for iOS developers. Swift, SwiftUI, Xcode, and the Apple dev ecosystem — updated daily."',
        "permalink: /ios/",
        "---",
        "",
        "{% assign articles = site.data.ios.articles %}",
        "{% assign featured = articles | first %}",
        "",
        # Stats bar
        '<div style="display:flex; gap:1em; flex-wrap:wrap; margin-bottom:1.5em;">',
        '  <span style="padding:4px 12px; border-radius:12px; background:#dbeafe; color:#1e40af; font-weight:bold;">🍎 iOS</span>',
        '  <span style="padding:4px 12px; border-radius:12px; background:#f3f4f6; color:#374151; font-weight:bold;">{{ articles.size }} articles</span>',
        '</div>',
        "",
        # Featured article card
        "{% if featured %}",
        '<div style="margin-bottom:2em; padding:1.25em; border:2px solid #0071e3; border-radius:8px; background:#f0f7ff;">',
        '  <div style="display:flex; align-items:center; gap:0.5em; flex-wrap:wrap; margin-bottom:0.6em;">',
        '    <span style="padding:3px 10px; border-radius:12px; font-size:0.78em; font-weight:bold; background:#0071e3; color:#fff;">&#9733; Latest</span>',
        '    <span style="font-size:0.78em; color:#6b7280;">{{ featured.source }} &middot; {{ featured.published | slice: 0, 10 }}</span>',
        '  </div>',
        '  <div style="font-weight:700; font-size:1.1em; margin-bottom:0.4em;">',
        '    <a href="{{ featured.url }}" target="_blank" rel="noopener" style="color:#0071e3; text-decoration:none;">{{ featured.title }}</a>',
        '  </div>',
        '  <p style="margin:0; font-size:0.88em; color:#374151; line-height:1.5;">{{ featured.excerpt }}</p>',
        '</div>',
        "{% endif %}",
        "",
        # Article list (skip first — already featured)
        "## Latest News",
        "",
        "{% for article in articles offset:1 %}",
        '<div style="margin-bottom:1.25em; padding:0.85em; border:1px solid #e5e7eb; border-left:3px solid #93c5fd; border-radius:8px;">',
        '  <div style="margin-bottom:0.3em;">',
        '    <strong><a href="{{ article.url }}" target="_blank" rel="noopener">{{ article.title }}</a></strong>',
        '  </div>',
        '  <p style="margin:0 0 0.4em 0; font-size:0.88em; color:#374151; line-height:1.5;">{{ article.excerpt }}</p>',
        '  <span style="font-size:0.78em; color:#9ca3af;">{{ article.source }} &middot; {{ article.published | slice: 0, 10 }}</span>',
        "</div>",
        "{% endfor %}",
        "",
        "---",
        "",
        '<p style="font-size:0.8em; color:#9ca3af;">Sources: Apple Developer News, Swift Blog, NSHipster &middot; Updated: {{ site.data.ios.generated_at }}</p>',
        "",
    ]
    return "\n".join(lines)


def publish_ios():
    """Main entry point: fetch articles, generate outputs."""
    os.makedirs(DATA_DIR, exist_ok=True)
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    print("=== iOS Tracker ===")
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
