import feedparser
import os
import re
import uuid
from datetime import datetime, timezone, timedelta
from utils import read_text_file, track_published
from const import DEVLOGS_SOURCES, PUBLISHED_NEWS_FILE_NAME
from news import fetch_preview, calculate_score, _parse_feed_date
from keywords import KEYWORDS

DEVLOGS_LAST_AUTHOR_FILE = "news/devlogs_last_author.txt"
LOOKBACK_DAYS = 30


def _create_devlog_post(entry):
    """Write a Jekyll document to docs/_devlogs/ (separate collection, never shown on home)."""
    now = datetime.now(timezone.utc)
    post_id = str(uuid.uuid1())
    os.makedirs('docs/_devlogs', exist_ok=True)
    file_name = f"docs/_devlogs/{now.strftime('%Y-%m-%d')}-{post_id}.md"

    safe_title = entry['title'].replace('\\', '').replace('"', "'")
    description = entry.get('preview', '')[:155].replace('"', "'").replace('\n', ' ')
    external_url = entry['link']
    source_name = entry.get('source', '')
    tags = entry.get('tags', [])

    with open(file_name, 'w', encoding='utf-8') as f:
        f.write('---\n')
        f.write(f'title: "{safe_title}"\n')
        f.write(f'date: {now.strftime("%Y-%m-%d %H:%M:%S %z")}\n')
        f.write(f'external_url: {external_url}\n')
        f.write(f'source: {source_name}\n')
        f.write(f'description: "{description}"\n')
        if 'image' in entry:
            f.write(f'image: {entry["image"]}\n')
        f.write('categories:\n')
        for tag in tags:
            f.write(f'  - {tag}\n')
        f.write('---\n')


def _read_last_author():
    try:
        with open(DEVLOGS_LAST_AUTHOR_FILE, encoding='utf-8') as f:
            return f.read().strip()
    except FileNotFoundError:
        return ''


def _write_last_author(author):
    os.makedirs('news', exist_ok=True)
    with open(DEVLOGS_LAST_AUTHOR_FILE, 'w', encoding='utf-8') as f:
        f.write(author)


def _scan_devlogs(published, cutoff):
    """Fetch all creator feeds and return scored candidates."""
    candidates = []

    for source_key, source in DEVLOGS_SOURCES.items():
        print(f"🔍 Fetching {source['name']}...")
        try:
            feed = feedparser.parse(source['feed_url'])

            for raw in feed.entries[:20]:
                title = raw.get('title', '').strip()
                link = raw.get('link', '').strip()
                if not title or not link:
                    continue
                if link in published:
                    continue

                pub_date = _parse_feed_date(raw)
                if pub_date < cutoff:
                    continue

                summary = raw.get('summary', '') or raw.get('description', '') or ''
                combined = f"{title} {summary}".lower()
                tags = [label for kw, label in KEYWORDS.items()
                        if re.search(rf'\b{re.escape(kw)}\b', combined, re.IGNORECASE)]

                rss_summary = re.sub(r'<[^>]+>', '', summary).strip()[:200]

                entry = {
                    'title': title,
                    'link': link,
                    'source': source['name'],
                    'source_type': source['type'],
                    'source_boost': source.get('score_boost', 0),
                    'tags': tags,
                    'community_score': 0,
                    '_category': 'devlogs',
                    'content_type': 'community',
                    '_rss_summary': rss_summary,
                }
                entry['score'] = calculate_score(entry, source)
                candidates.append(entry)

        except Exception as e:
            print(f"   ⚠️ Error fetching {source['name']}: {e}")

    return candidates


def publish_devlogs():
    now = datetime.now(timezone.utc)
    cutoff = now - timedelta(days=LOOKBACK_DAYS)
    published = read_text_file(PUBLISHED_NEWS_FILE_NAME)
    last_author = _read_last_author()

    candidates = _scan_devlogs(published, cutoff)

    if not candidates:
        print("❌ No new devlog posts found")
        return

    candidates.sort(key=lambda x: x['score'], reverse=True)

    # Author rotation: skip last author, fall back if no alternatives
    rotated = [e for e in candidates if e['source'] != last_author]
    pick_from = rotated if rotated else candidates

    entry = pick_from[0]
    rss_summary = entry.pop('_rss_summary', '')

    result = fetch_preview(entry)
    if not result:
        # Fall back to RSS summary — personal blogs often lack OG meta tags
        entry['preview'] = rss_summary
        result = entry

    _create_devlog_post(result)
    track_published(result['link'], PUBLISHED_NEWS_FILE_NAME)
    _write_last_author(result['source'])

    print(f"✅ [devlogs] {result['source']}: {result['title'][:60]}")
