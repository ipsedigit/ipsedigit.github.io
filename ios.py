"""
iOS Developer Tracker.
Fetches Apple Developer, Swift Blog, and iOS community RSS feeds.
Generates docs/_data/ios.json and docs/ios/index.md.
"""
import json
import os
import re
import time as _time
from datetime import datetime, timezone, timedelta

import feedparser

DATA_DIR = "docs/_data"
OUTPUT_JSON = os.path.join(DATA_DIR, "ios.json")
OUTPUT_DIR = "docs/ios"
OUTPUT_PAGE = os.path.join(OUTPUT_DIR, "index.md")

MAX_ITEMS_PER_FEED = 8
MAX_AGE_DAYS = 90

FEEDS = [
    {
        "key": "swift_blog",
        "name": "Swift Blog",
        "url": "https://www.swift.org/atom.xml",
        "section": "apple_official",
        "is_spotlight_candidate": True,
    },
    {
        "key": "apple_dev",
        "name": "Apple Developer News",
        "url": "https://developer.apple.com/news/rss/news.rss",
        "section": "apple_official",
        "is_spotlight_candidate": True,
    },
    {
        "key": "nshipster",
        "name": "NSHipster",
        "url": "https://nshipster.com/feed.xml",
        "section": "community",
        "is_spotlight_candidate": False,
    },
    {
        "key": "hackingwithswift",
        "name": "Hacking with Swift",
        "url": "https://www.hackingwithswift.com/articles/rss",
        "section": "community",
        "is_spotlight_candidate": False,
    },
    {
        "key": "swiftbysundell",
        "name": "Swift by Sundell",
        "url": "https://swiftbysundell.com/feed.rss",
        "section": "community",
        "is_spotlight_candidate": False,
    },
    {
        "key": "iosdevweekly",
        "name": "iOS Dev Weekly",
        "url": "https://iosdevweekly.com/issues.rss",
        "section": "community",
        "is_spotlight_candidate": False,
    },
]

SPOTLIGHT_KEYWORDS = [
    'swift 6', 'swift 7', 'swift 8',
    'xcode 16', 'xcode 17', 'xcode 18',
    'ios 18', 'ios 19', 'ios 20',
    'wwdc',
    'swiftui',
]


def _parse_date(entry):
    """Parse published date from feedparser entry. Returns datetime or None."""
    for attr in ("published_parsed", "updated_parsed"):
        val = getattr(entry, attr, None)
        if val:
            try:
                return datetime.fromtimestamp(_time.mktime(val), tz=timezone.utc)
            except Exception:
                pass
    return None


def _clean_summary(text):
    """Strip HTML tags and truncate summary."""
    text = re.sub(r"<[^>]+>", "", text)
    text = text.strip()
    return text[:200] + "\u2026" if len(text) > 200 else text


def _fetch_feed(feed_config):
    """Fetch and parse an RSS feed. Returns list of normalized items."""
    name = feed_config["name"]
    url = feed_config["url"]
    print(f"  Fetching {name}...")
    try:
        parsed = feedparser.parse(url)
        items = []
        cutoff = datetime.now(timezone.utc) - timedelta(days=MAX_AGE_DAYS)
        for entry in parsed.entries[:MAX_ITEMS_PER_FEED]:
            pub = _parse_date(entry)
            if pub and pub < cutoff:
                continue
            items.append({
                "title": entry.get("title", "").strip(),
                "url": entry.get("link", ""),
                "published": pub.isoformat() if pub else "",
                "summary": _clean_summary(entry.get("summary", "")),
                "source": name,
                "source_key": feed_config["key"],
            })
        print(f"    {len(items)} items")
        return items
    except Exception as e:
        print(f"    Error: {e}")
        return []


def _pick_spotlight(items):
    """Pick the most relevant item as spotlight from apple_official items.

    Prefers items whose title contains a SPOTLIGHT_KEYWORDS match.
    Falls back to most recent item.
    """
    if not items:
        return None
    for kw in SPOTLIGHT_KEYWORDS:
        for item in items:
            if kw in item["title"].lower():
                return item
    return items[0]


def _format_date(iso_str):
    if not iso_str:
        return ""
    try:
        dt = datetime.fromisoformat(iso_str)
        return dt.strftime("%b %d, %Y")
    except (ValueError, AttributeError):
        return iso_str[:10]


def _generate_page(data):
    """Generate Jekyll markdown page for /ios/."""
    spotlight = data.get("spotlight")
    official = data.get("apple_official", [])
    community = data.get("community", [])
    generated_at = data.get("generated_at", "")

    lines = [
        "---",
        "layout: page",
        'title: "iOS Developer"',
        'description: "Curated news and resources for iOS developers. Swift, SwiftUI, Xcode, WWDC, App Store, and the Apple dev community."',
        "permalink: /ios/",
        "---",
        "",
    ]

    # Spotlight card
    if spotlight:
        pub_str = _format_date(spotlight.get("published", ""))
        date_span = f'<span style="font-size:0.82em; color:#6b7280;">{pub_str}</span>' if pub_str else ""
        summary_p = f'<p style="margin:0; color:#374151; font-size:0.9em;">{spotlight["summary"]}</p>' if spotlight.get("summary") else ""
        lines += [
            "## Spotlight",
            "",
            '<div style="margin-bottom:1.5em; padding:1em; border:2px solid #0071e3; border-radius:12px; background:#f0f7ff;">',
            '  <div style="display:flex; align-items:center; gap:0.5em; margin-bottom:0.5em; flex-wrap:wrap;">',
            '    <span style="padding:2px 10px; border-radius:12px; font-size:0.8em; background:#0071e3; color:#fff; font-weight:bold;">&#9733; Apple</span>',
            f'    <span style="font-size:0.82em; color:#6b7280;">{spotlight["source"]}</span>',
            f'    {date_span}',
            "  </div>",
            '  <div style="font-weight:700; font-size:1.1em; margin-bottom:0.4em;">',
            f'    <a href="{spotlight["url"]}" target="_blank" rel="noopener" style="color:#0071e3; text-decoration:none;">{spotlight["title"]}</a>',
            "  </div>",
            f"  {summary_p}",
            "</div>",
            "",
        ]

    # Apple Official section
    non_spotlight = [i for i in official if not spotlight or i["url"] != spotlight.get("url")]
    if non_spotlight:
        lines += ["## Apple Official", ""]
        for item in non_spotlight[:6]:
            pub_str = _format_date(item.get("published", ""))
            date_part = f' <span style="font-size:0.8em; color:#9ca3af;">\u2014 {pub_str}</span>' if pub_str else ""
            lines.append(
                f'- **[{item["title"]}]({item["url"]})**{date_part}  '
                f'<span style="font-size:0.78em; color:#6b7280;">{item["source"]}</span>'
            )
        lines.append("")

    # Community section
    if community:
        lines += ["## Community", ""]
        for item in community[:12]:
            pub_str = _format_date(item.get("published", ""))
            date_part = f' <span style="font-size:0.8em; color:#9ca3af;">\u2014 {pub_str}</span>' if pub_str else ""
            lines.append(
                f'- **[{item["title"]}]({item["url"]})**{date_part}  '
                f'<span style="font-size:0.78em; color:#6b7280;">{item["source"]}</span>'
            )
        lines.append("")

    lines += [
        "---",
        "",
        f'<p style="font-size:0.8em; color:#9ca3af;">Updated: {generated_at}</p>',
        "",
    ]

    return "\n".join(lines)


def publish_ios():
    """Main entry point."""
    os.makedirs(DATA_DIR, exist_ok=True)
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    print("Fetching iOS feeds...")
    all_items = []
    for feed_config in FEEDS:
        items = _fetch_feed(feed_config)
        for item in items:
            item["section"] = feed_config["section"]
            item["is_spotlight_candidate"] = feed_config["is_spotlight_candidate"]
        all_items.extend(items)

    all_items.sort(key=lambda i: i.get("published", ""), reverse=True)

    official_items = [i for i in all_items if i["section"] == "apple_official"]
    community_items = [i for i in all_items if i["section"] == "community"]
    spotlight_candidates = [i for i in all_items if i["is_spotlight_candidate"]]
    spotlight = _pick_spotlight(spotlight_candidates)

    now_str = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")

    data = {
        "generated_at": now_str,
        "spotlight": spotlight,
        "apple_official": official_items,
        "community": community_items,
    }

    with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"  JSON written: {OUTPUT_JSON}")

    page = _generate_page(data)
    with open(OUTPUT_PAGE, "w", encoding="utf-8") as f:
        f.write(page)
    print(f"  Page written: {OUTPUT_PAGE}")
