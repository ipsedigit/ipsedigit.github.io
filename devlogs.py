import feedparser
import json
import os
import re
from datetime import datetime, timezone, timedelta
from utils import read_text_file, track_published
from const import DEVLOGS_SOURCES

DEVLOGS_PUBLISHED_FILE = "news/devlogs_published.txt"
DEVLOGS_LAST_AUTHOR_FILE = "news/devlogs_last_author.txt"
DEVLOGS_DATA_FILE = "docs/_data/devlogs.json"
DAILY_LIMIT = 1
MAX_ITEMS = 6
LOOKBACK_DAYS = 30


def _parse_date(entry):
    for key in ("published_parsed", "updated_parsed"):
        p = entry.get(key)
        if p and len(p) >= 6 and all(x is not None for x in p[:6]):
            try:
                return datetime(p[0], p[1], p[2], p[3], p[4], p[5], tzinfo=timezone.utc)
            except (TypeError, ValueError):
                pass
    return datetime.now(timezone.utc)


def _read_last_author():
    try:
        with open(DEVLOGS_LAST_AUTHOR_FILE, encoding='utf-8') as f:
            return f.read().strip()
    except FileNotFoundError:
        return ''


def _write_last_author(author):
    with open(DEVLOGS_LAST_AUTHOR_FILE, 'w', encoding='utf-8') as f:
        f.write(author)


def _read_existing_items():
    try:
        with open(DEVLOGS_DATA_FILE, encoding='utf-8') as f:
            return json.load(f).get('items', [])
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def publish_devlogs():
    now = datetime.now(timezone.utc)
    cutoff = now - timedelta(days=LOOKBACK_DAYS)
    published = read_text_file(DEVLOGS_PUBLISHED_FILE)
    last_author = _read_last_author()

    candidates = []

    for source_key, source in DEVLOGS_SOURCES.items():
        print(f"🔍 Fetching {source['name']}...")
        try:
            feed = feedparser.parse(source['feed_url'])
            for entry in feed.entries[:15]:
                title = entry.get('title', '').strip()
                link = entry.get('link', '').strip()
                if not title or not link:
                    continue
                if link in published:
                    continue

                date = _parse_date(entry)
                if date < cutoff:
                    continue

                summary = entry.get('summary', '') or entry.get('description', '') or ''
                summary = re.sub(r'<[^>]+>', '', summary).strip()[:200]

                candidates.append({
                    'title': title,
                    'url': link,
                    'author': source['name'],
                    'author_url': source.get('url', ''),
                    'date': date.strftime('%Y-%m-%d'),
                    '_ts': date.timestamp(),
                    'summary': summary,
                })
        except Exception as e:
            print(f"   ⚠️ Error fetching {source['name']}: {e}")

    # Most recent first
    candidates.sort(key=lambda x: x['_ts'], reverse=True)

    # Skip last author to ensure rotation; fall back to any if no other options
    rotated = [c for c in candidates if c['author'] != last_author]
    pick_from = rotated if rotated else candidates

    if not pick_from:
        print("❌ No new posts found")
        return

    picked = {k: v for k, v in pick_from[0].items() if k != '_ts'}

    # Prepend new item, keep last MAX_ITEMS
    existing = _read_existing_items()
    items = [picked] + existing
    items = items[:MAX_ITEMS]

    os.makedirs('news', exist_ok=True)
    os.makedirs('docs/_data', exist_ok=True)

    with open(DEVLOGS_DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump({
            'items': items,
            'generated_at': now.isoformat(),
        }, f, ensure_ascii=False, indent=2)

    track_published(picked['url'], DEVLOGS_PUBLISHED_FILE)
    _write_last_author(picked['author'])

    print(f"✅ {picked['author']}: {picked['title'][:60]}")
    print(f"\n📊 Devlogs now has {len(items)} items")
