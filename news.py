import feedparser
import json
import uuid
import requests
import re
import os
from datetime import datetime, timezone, date
from urllib.parse import urlparse
from utils import read_text_file, track_published
from const import (
    NEWS_SOURCES,
    PUBLISHED_NEWS_FILE_NAME,
    CONTENT_CATEGORIES,
    NICHE_CATEGORIES,
    MAX_POSTS_PER_NICHE_PER_DAY,
    DAILY_CATEGORIES_FILE,
    DIRECT_LINKS,
    TITLE_BONUS,
    TITLE_PENALTY,
    NICHE_SUBNICHES,
    CONTENT_TYPE_PATTERNS,
    MIN_SCORE,
    MIN_SCORE_FALLBACK,
    DAILY_TARGET,
    DAILY_MINIMUM,
    MAX_PER_TYPE,
)
from keywords import KEYWORDS
from bs4 import BeautifulSoup
from tags import generate_tag_pages

DIRECT_LINKS_DATA_PATH = "docs/_data/direct_links.json"


def update_direct_links_data():
    """Write docs/_data/direct_links.json from DIRECT_LINKS for the /direct/ page."""
    data = {
        "links": list(DIRECT_LINKS),
        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    }
    os.makedirs(os.path.dirname(DIRECT_LINKS_DATA_PATH), exist_ok=True)
    with open(DIRECT_LINKS_DATA_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
    print(f"Updated {DIRECT_LINKS_DATA_PATH} ({len(DIRECT_LINKS)} links)")


def publish_news(target_niche=None):
    """Publish articles using two-pass selection.

    If target_niche is given, falls back to single-niche mode (legacy workflow compat).
    Otherwise, uses full two-pass selection across all niches.
    """
    update_direct_links_data()
    if target_niche:
        _publish_single_niche(target_niche)
        return

    selected = select_daily_posts()
    if not selected:
        print("❌ No posts selected this run")
        return

    published_count = 0
    for entry in selected:
        result = fetch_preview(entry)
        if not result:
            print(f"   ⚠️ Preview fetch failed, skipping: {entry['title'][:50]}")
            continue

        result['why_picked'] = generate_why_picked(result)
        create_post(result)
        generate_tag_pages()
        track_published(result['link'], PUBLISHED_NEWS_FILE_NAME)
        sub_key = result.get('_subniche') or result.get('_category', 'unknown')
        ctype = result.get('content_type', 'breaking')
        track_daily_subniche(result['_category'], sub_key, ctype)
        published_count += 1

        print(f"✅ [{result['_category']}] [{ctype}] Published: {result['title'][:60]}")
        print(f"   Score: {result['score']} | Source: {result['source']}")

    print(f"\n📊 Published {published_count} articles this run")


def _publish_single_niche(target_niche):
    """Legacy single-niche publish for backward compatibility with niche-rotation workflow."""
    today_entries = get_today_subniches()

    niche_entries = [e for e in today_entries if e.startswith(f"{target_niche}:") or e == target_niche]
    niche_count = len(niche_entries)

    if niche_count >= MAX_POSTS_PER_NICHE_PER_DAY:
        print(f"⏸️ [{target_niche}] Daily limit reached: {niche_count}/{MAX_POSTS_PER_NICHE_PER_DAY}")
        return

    best_post = find_best_post(exclude_subniches=today_entries, target_niche=target_niche)
    if best_post:
        create_post(best_post)
        generate_tag_pages()
        track_published(best_post['link'], PUBLISHED_NEWS_FILE_NAME)
        sub_key = best_post.get('_subniche') or best_post.get('_category', 'unknown')
        ctype = best_post.get('content_type', classify_content_type(best_post))
        track_daily_subniche(target_niche, sub_key, ctype)
        print(f"✅ [{target_niche}] Published: {best_post['title']}")
    else:
        print(f"❌ [{target_niche}] No suitable posts found")


def find_best_post(exclude_subniches=None, target_niche=None, source_type_filter=None):
    """
    Find the best post across all sources by score.
    Requires 2+ keyword matches and niche category (AI, Security, Cloud, DevTools, or Software Engineering).
    Skips sub-niches already covered today to ensure diversity.
    If target_niche is set, only considers posts from that niche.
    If source_type_filter is set (e.g. 'creator'), only considers posts from sources of that type.
    """
    if exclude_subniches is None:
        exclude_subniches = []

    published = set(read_text_file(PUBLISHED_NEWS_FILE_NAME))
    all_candidates = []

    for source_key, source in NEWS_SOURCES.items():
        if source_type_filter and source.get("type") != source_type_filter:
            continue
        print(f"🔍 Scanning {source['name']}...")

        try:
            feed = feedparser.parse(source['feed_url'])
            entries = extract_entries(feed, source)

            for entry in entries:
                if entry['link'] in published:
                    continue

                cat = identify_category(entry)
                if cat not in NICHE_CATEGORIES:
                    continue

                if target_niche and cat != target_niche:
                    continue

                subniche = identify_subniche(entry, cat)
                entry['_category'] = cat
                entry['_subniche'] = subniche

                # Skip sub-niches already covered today (format: "niche:subniche" or "creator:SourceName")
                sub_key = f"{cat}:{subniche}" if subniche else cat
                if source_type_filter == "creator":
                    sub_key = f"creator:{source.get('name', source_key)}"
                if sub_key in exclude_subniches:
                    continue

                entry['score'] = calculate_score(entry, source)
                entry['content_type'] = classify_content_type(entry)

                if entry['score'] < MIN_SCORE:
                    continue

                all_candidates.append(entry)

        except Exception as e:
            print(f"   ⚠️ Error: {e}")

    if not all_candidates:
        return None

    all_candidates.sort(key=lambda x: x['score'], reverse=True)
    top_candidates = all_candidates[:10]

    print(f"📋 Top candidates:")
    for i, c in enumerate(top_candidates[:5]):
        cat_label = f"{c.get('_category')}/{c.get('_subniche') or '—'}"
        print(f"   {i+1}. [{c['score']}] [{cat_label}] {c['title'][:50]}...")

    for candidate in top_candidates:
        result = fetch_preview(candidate)
        if result:
            result['why_picked'] = generate_why_picked(result)
            return result

    return None


def extract_entries(feed, source):
    """Extract and keyword-filter entries from a feed. Requires 2+ keyword matches."""
    entries = []

    for entry in feed.entries[:50]:
        title = entry.get("title", "").strip()
        link = entry.get("link", "").strip()
        summary = entry.get("summary", "") or entry.get("description", "") or ""

        if not title or not link:
            continue

        combined = f"{title} {summary}".lower()
        tags = [label for kw, label in KEYWORDS.items()
                if re.search(rf'\b{re.escape(kw)}\b', combined, re.IGNORECASE)]

        # Require at least 2 keyword matches for topical depth
        if len(tags) < 2:
            continue

        community_score = 0
        score_match = re.search(r'(\d+)\s+points?', summary)
        if score_match:
            community_score = int(score_match.group(1))

        if community_score < source.get('min_score', 0):
            continue

        entries.append({
            'title': title,
            'link': link,
            'source': source['name'],
            'source_type': source['type'],
            'tags': tags,
            'community_score': community_score,
        })

    return entries


def calculate_score(entry, source):
    """
    Score based on:
    - Community signal (aggregators)
    - Source authority: research_blog > security > corporate_blog > startup > community > news
    - Niche relevance bonus
    - Title quality signals
    """
    title_lower = entry['title'].lower()
    link_lower = entry['link'].lower()

    # Base score from community signal (normalized 0-50)
    score = min(entry.get('community_score', 0) / 2, 50)

    # Source type bonus
    source_type = entry['source_type']
    if source_type == 'research_blog':
        score += 45   # Primary AI/ML research — highest signal
    elif source_type == 'security':
        score += 35   # Specialist security practitioner content
    elif source_type == 'corporate_blog':
        score += 30   # Original engineering content
    elif source_type == 'startup':
        score += 20
    elif source_type == 'cloud_news':
        score += 30   # Cloud/infrastructure specialist content
    elif source_type == 'se_blog':
        score += 35   # Software engineering thought leaders
    elif source_type == 'creator':
        score += 28   # Indie creators, newsletters (Substack, etc.) — strong signal for individual reach
    elif source_type == 'community':
        score += 10
    # 'news' and 'aggregator' types: rely on community score or title patterns

    # Niche bonus
    cat = entry.get('_category') or identify_category(entry)
    if cat in NICHE_CATEGORIES:
        score += 10

    # Title pattern bonuses/penalties
    for pattern, bonus in TITLE_BONUS.items():
        if re.search(pattern, title_lower):
            score += bonus

    for pattern, penalty in TITLE_PENALTY.items():
        if re.search(pattern, title_lower) or re.search(pattern, link_lower):
            score += penalty

    # Optimal title length (40-80 chars)
    title_len = len(entry['title'])
    if 40 <= title_len <= 80:
        score += 10
    elif title_len > 120:
        score -= 10

    return max(score, 0)


def identify_category(entry):
    """Identify the main niche category (ai or security)."""
    text = (entry.get('title', '') + ' ' + ' '.join(entry.get('tags', []))).lower()

    best_cat = 'general'
    best_matches = 0

    for cat, keywords in CONTENT_CATEGORIES.items():
        matches = sum(1 for kw in keywords if kw in text)
        if matches > best_matches:
            best_matches = matches
            best_cat = cat

    return best_cat


def identify_subniche(entry, main_cat):
    """Identify the sub-niche within any niche category."""
    text = (entry.get('title', '') + ' ' + ' '.join(entry.get('tags', []))).lower()

    subniches = NICHE_SUBNICHES.get(main_cat)
    if not subniches:
        return None

    best_sub = None
    best_matches = 0

    for sub, keywords in subniches.items():
        matches = sum(1 for kw in keywords if kw in text)
        if matches > best_matches:
            best_matches = matches
            best_sub = sub

    return best_sub


# Security threat keywords for source_type=='security' detection
_SECURITY_THREAT_RE = re.compile(
    r'(malware|ransomware|trojan|botnet|campaign|apt|breach|hack|attack|incident|exploit)',
    re.IGNORECASE,
)


def classify_content_type(entry):
    """Classify an article as 'breaking', 'deep', or 'community'.

    Priority order:
    1. creator source_type -> community
    2. Title matches community patterns -> community
    3. Title matches breaking patterns -> breaking
    4. Title matches deep patterns -> deep
    5. research_blog / se_blog source_type -> deep
    6. security source with threat keywords -> breaking
    7. Default -> breaking
    """
    source_type = entry.get('source_type', '')
    title = entry.get('title', '')

    if source_type == 'creator':
        return 'community'

    for pattern in CONTENT_TYPE_PATTERNS['community']:
        if re.search(pattern, title, re.IGNORECASE):
            return 'community'

    for pattern in CONTENT_TYPE_PATTERNS['breaking']:
        if re.search(pattern, title, re.IGNORECASE):
            return 'breaking'

    for pattern in CONTENT_TYPE_PATTERNS['deep']:
        if re.search(pattern, title, re.IGNORECASE):
            return 'deep'

    if source_type in ('research_blog', 'se_blog'):
        return 'deep'

    if source_type == 'security' and _SECURITY_THREAT_RE.search(title):
        return 'breaking'

    return 'breaking'


def _scan_all_sources():
    """Scan all RSS feeds and return scored, categorized candidate entries."""
    all_entries = []

    for source_key, source in NEWS_SOURCES.items():
        try:
            feed = feedparser.parse(source['feed_url'])
            entries = extract_entries(feed, source)

            for entry in entries:
                cat = identify_category(entry)
                if cat not in NICHE_CATEGORIES:
                    continue

                subniche = identify_subniche(entry, cat)
                entry['_category'] = cat
                entry['_subniche'] = subniche
                entry['score'] = calculate_score(entry, source)
                entry['content_type'] = classify_content_type(entry)
                all_entries.append(entry)

        except Exception as e:
            print(f"   ⚠️ Error scanning {source.get('name', source_key)}: {e}")

    return all_entries


def _build_candidates(min_score=None):
    """Build sorted list of publishable candidates (not yet published, above score floor)."""
    if min_score is None:
        min_score = MIN_SCORE

    published = set(read_text_file(PUBLISHED_NEWS_FILE_NAME))
    all_entries = _scan_all_sources()

    candidates = [
        e for e in all_entries
        if e['link'] not in published and e['score'] >= min_score
    ]

    candidates.sort(key=lambda x: x['score'], reverse=True)
    return candidates


def select_daily_posts():
    """Two-pass article selection. Returns list of selected entries (not yet published/fetched).

    Pass 1: Best article per niche (5 guaranteed slots) + best creator.
    Pass 2: Fill remaining slots by score, respecting type diversity and niche caps.
    """
    state = get_daily_state()

    if state['total'] >= DAILY_TARGET:
        print(f"⏸️ Daily target reached ({state['total']}/{DAILY_TARGET})")
        return []

    candidates = _build_candidates(min_score=MIN_SCORE)
    if not candidates:
        return []

    selected = []
    used_links = set()
    used_subniches = set(state['subniches'])
    niche_counts = dict(state['niche_counts'])
    type_counts = dict(state['type_counts'])
    total = state['total']

    def _can_select(entry):
        if entry['link'] in used_links:
            return False
        niche = entry['_category']
        subniche = entry.get('_subniche')
        sub_key = f"{niche}:{subniche}" if subniche else niche
        if sub_key in used_subniches:
            return False
        if niche_counts.get(niche, 0) >= MAX_POSTS_PER_NICHE_PER_DAY:
            return False
        return True

    def _select(entry):
        nonlocal total
        selected.append(entry)
        used_links.add(entry['link'])
        niche = entry['_category']
        subniche = entry.get('_subniche')
        sub_key = f"{niche}:{subniche}" if subniche else niche
        used_subniches.add(sub_key)
        niche_counts[niche] = niche_counts.get(niche, 0) + 1
        ctype = entry.get('content_type', 'breaking')
        type_counts[ctype] = type_counts.get(ctype, 0) + 1
        total += 1

    # Pass 1: Guaranteed niche slots
    for niche in NICHE_CATEGORIES:
        if niche_counts.get(niche, 0) >= MAX_POSTS_PER_NICHE_PER_DAY:
            continue
        for c in candidates:
            if c['_category'] == niche and _can_select(c):
                _select(c)
                break

    # Pass 2: Open competition
    remaining_slots = DAILY_TARGET - total
    for c in candidates:
        if remaining_slots <= 0:
            break
        if not _can_select(c):
            continue
        ctype = c.get('content_type', 'breaking')
        if type_counts.get(ctype, 0) >= MAX_PER_TYPE:
            continue
        _select(c)
        remaining_slots -= 1

    return selected


def generate_why_picked(entry):
    """Generate a brief editorial note explaining why this article was selected."""
    parts = []
    source_name = entry.get('source', '')
    source_type = entry.get('source_type', '')
    community_score = entry.get('community_score', 0)
    subniche = entry.get('_subniche', '')
    score = entry.get('score', 0)

    if source_type == 'research_blog':
        parts.append(f"primary research from {source_name}")
    elif source_type == 'corporate_blog':
        parts.append(f"original engineering content from {source_name}")
    elif source_type == 'security':
        parts.append(f"specialist source: {source_name}")
    elif source_type == 'cloud_news':
        parts.append(f"cloud infrastructure source: {source_name}")
    elif source_type == 'se_blog':
        parts.append(f"software engineering thought leader: {source_name}")
    elif source_type == 'creator':
        parts.append(f"creator & newsletter: {source_name}")
    elif source_type == 'aggregator' and community_score > 0:
        parts.append(f"{community_score} community points on {source_name}")
    else:
        parts.append(source_name)

    if subniche:
        parts.append(f"{subniche} focus")

    if score >= 90:
        parts.append("top relevance score")

    return " · ".join(parts)


def fetch_preview(entry):
    """Fetch OG description and image from the article URL."""
    try:
        response = requests.get(entry['link'], timeout=5, headers={
            'User-Agent': 'Mozilla/5.0 (compatible; eofBot/1.0)'
        })
        if response.status_code != 200:
            return None

        soup = BeautifulSoup(response.text, 'html.parser')

        meta_desc = (
            soup.find("meta", property="og:description") or
            soup.find("meta", attrs={"name": "description"})
        )
        if meta_desc and meta_desc.get("content"):
            entry['preview'] = meta_desc["content"].strip()[:200]
        else:
            return None

        meta_img = soup.find("meta", property="og:image")
        if meta_img and meta_img.get("content"):
            entry['image'] = meta_img["content"].strip()

        return entry

    except Exception as e:
        print(f"   ⚠️ Preview fetch failed: {e}")
        return None


def get_daily_state():
    """Read today's published state. Returns dict with subniches, niche_counts, type_counts, total."""
    state = {
        'subniches': [],
        'niche_counts': {},
        'type_counts': {'breaking': 0, 'deep': 0, 'community': 0},
        'total': 0,
    }
    try:
        if not os.path.exists(DAILY_CATEGORIES_FILE):
            return state

        with open(DAILY_CATEGORIES_FILE, 'r') as f:
            lines = f.read().strip().split('\n')

        today_str = date.today().isoformat()
        for line in lines:
            if not line.startswith(today_str):
                continue
            parts = line[len(today_str) + 1:].split(':')
            if len(parts) >= 3:
                niche, subniche, content_type = parts[0], parts[1], parts[2]
                state['subniches'].append(f"{niche}:{subniche}")
                state['niche_counts'][niche] = state['niche_counts'].get(niche, 0) + 1
                if content_type in state['type_counts']:
                    state['type_counts'][content_type] += 1
                state['total'] += 1
            elif len(parts) >= 2:
                niche, subniche = parts[0], parts[1]
                state['subniches'].append(f"{niche}:{subniche}")
                state['niche_counts'][niche] = state['niche_counts'].get(niche, 0) + 1
                state['total'] += 1
    except Exception:
        pass

    return state


def get_today_subniches():
    """Legacy wrapper - returns list of sub-niches published today."""
    return get_daily_state()['subniches']


def track_daily_subniche(niche, subniche, content_type='breaking'):
    """Track the niche:sub-niche:content_type published today."""
    today_str = date.today().isoformat()
    with open(DAILY_CATEGORIES_FILE, 'a') as f:
        f.write(f"{today_str}:{niche}:{subniche}:{content_type}\n")


def keyword_in_text(text, keyword):
    return re.search(rf'\b{re.escape(keyword)}\b', text, re.IGNORECASE)


def _seo_title(title, year):
    """Append year to title if not present and within SEO length range."""
    if str(year) not in title and str(year - 1) not in title:
        candidate = f"{title} ({year})"
        if len(candidate) <= 70:
            return candidate
    return title[:70] if len(title) > 70 else title


def create_post(news):
    """Create the Jekyll markdown post file."""
    now = datetime.now(timezone.utc)
    post_id = str(uuid.uuid1())
    category = news.get('_category') or identify_category(news)
    subniche = news.get('_subniche', '')
    file_name = f"docs/_posts/{now.strftime('%Y-%m-%d')}-top-tech-news-{post_id}.md"

    raw_title = news["title"]
    seo_title = _seo_title(raw_title, now.year)
    safe_title = seo_title.replace('"', "'")
    description = news.get("preview", "")[:155].replace('"', "'").replace("\n", " ")
    why_picked = news.get("why_picked", "")

    word_count = len(news.get("preview", "").split())
    reading_time = max(1, round(word_count / 200))

    source_name = news.get("source", "Unknown")
    external_url = news["link"]
    date_str = now.strftime("%B %d, %Y")
    tags = news.get("tags", [])

    with open(file_name, 'w', encoding='utf-8') as f:
        f.write("---\n")
        f.write("layout: post\n")
        f.write(f'title: "{safe_title}"\n')
        f.write(f'date: {now.strftime("%Y-%m-%d %H:%M:%S %z")}\n')
        f.write(f'external_url: {external_url}\n')
        f.write("categories:\n")
        for tag in tags:
            f.write(f"  - {tag}\n")
        f.write(f'description: "{description}"\n')
        if "image" in news:
            f.write(f'image: {news["image"]}\n')
        f.write(f'source: {source_name}\n')
        f.write(f'source_type: {news.get("source_type", "news")}\n')
        f.write(f'reading_time: {reading_time}\n')
        f.write(f'niche_category: {category}\n')
        if subniche:
            f.write(f'niche_subniche: {subniche}\n')
        content_type = news.get('content_type', 'breaking')
        f.write(f'content_type: {content_type}\n')
        if why_picked:
            f.write(f'why_picked: "{why_picked}"\n')
        f.write(f'score: {news.get("score", 0)}\n')
        f.write("---\n\n")
        f.write(f"> {news.get('preview', '')}\n\n")
        if "image" in news:
            f.write(f"![Preview]({news['image']})\n\n")

        category_label = category
        if subniche:
            category_label = f"{category} / {subniche}"

        f.write(f"**Source:** [{source_name}]({external_url}) | "
                f"**Category:** {category_label} | **Published:** {date_str}\n\n")
        f.write("---\n\n")
        f.write("*This article was curated by eof.news — signal for engineers who build.*\n")

    if os.environ.get("TWITTER_ENABLED", "").lower() == "true":
        try:
            from twitter_post import post_tweet
            post_tweet(news, category, file_name)
        except Exception as e:
            print(f"   ⚠️ Twitter post failed: {e}")
