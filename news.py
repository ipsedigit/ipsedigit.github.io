import feedparser
import uuid
import requests
import re
import os
from datetime import datetime, timezone, date, timedelta
from utils import read_text_file, track_published
from const import (
    NEWS_SOURCES,
    PUBLISHED_NEWS_FILE_NAME,
    CONTENT_CATEGORIES,
    NICHE_CATEGORIES,
    MAX_POSTS_PER_DAY,
    DAILY_CATEGORIES_FILE,
    RECENCY_BONUS,
    RECENCY_OLD_PENALTY,
    CROSS_SOURCE_BONUS,
    QUALITY_SIGNALS,
    NOISE_SIGNALS,
)
from keywords import KEYWORDS
from bs4 import BeautifulSoup
from tags import generate_tag_pages


# ---------------------------------------------------------------------------
# Main entry point
# ---------------------------------------------------------------------------

def publish_news():
    today_categories = get_today_categories()
    if len(today_categories) >= MAX_POSTS_PER_DAY:
        print(f"⏸️ Limit reached: {len(today_categories)}/{MAX_POSTS_PER_DAY} posts today")
        return

    print(f"📊 Posts today: {len(today_categories)}/{MAX_POSTS_PER_DAY}")

    best_post = find_best_post(exclude_categories=today_categories)

    if best_post:
        create_post(best_post)
        generate_tag_pages()
        track_published(best_post['link'], PUBLISHED_NEWS_FILE_NAME)
        track_daily_category(identify_category(best_post))

        print(f"✅ Published: {best_post['title']}")
        print(f"   Source:    {best_post['source']}")
        print(f"   Category:  {identify_category(best_post)}")
        print(f"   Score:     {best_post['score']}")
    else:
        print("❌ No suitable posts found")


# ---------------------------------------------------------------------------
# Candidate collection
# ---------------------------------------------------------------------------

def find_best_post(exclude_categories=None):
    if exclude_categories is None:
        exclude_categories = []

    published = set(read_text_file(PUBLISHED_NEWS_FILE_NAME))
    all_candidates = []

    for source_key, source in NEWS_SOURCES.items():
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

                if exclude_categories and cat in exclude_categories:
                    continue

                all_candidates.append(entry)

        except Exception as e:
            print(f"   ⚠️ Error: {e}")

    if not all_candidates:
        return None

    # Apply cross-source bonus before final scoring
    _apply_cross_source_bonus(all_candidates)

    # Score and sort
    for entry in all_candidates:
        entry['score'] = calculate_score(entry)

    all_candidates.sort(key=lambda x: x['score'], reverse=True)
    top = all_candidates[:10]

    print("📋 Top candidates:")
    for i, c in enumerate(top[:5]):
        print(f"   {i+1}. [{c['score']}] {c['title'][:60]}")

    # Return first with a fetchable preview
    for candidate in top:
        result = fetch_preview(candidate)
        if result:
            return result

    return None


# ---------------------------------------------------------------------------
# Entry extraction
# ---------------------------------------------------------------------------

def extract_entries(feed, source):
    entries = []

    for entry in feed.entries[:50]:
        title = entry.get("title", "").strip()
        link = entry.get("link", "").strip()
        summary = entry.get("summary", "") or entry.get("description", "") or ""

        if not title or not link:
            continue

        # Match AI/Security keywords
        combined = f"{title} {summary}".lower()
        tags = [label for kw, label in KEYWORDS.items()
                if re.search(rf'\b{re.escape(kw)}\b', combined, re.IGNORECASE)]

        if not tags:
            continue

        # Community score (HN, Lobsters)
        community_score = 0
        score_match = re.search(r'(\d+)\s+points?', summary)
        if score_match:
            community_score = int(score_match.group(1))

        if community_score < source.get('min_score', 0):
            continue

        # Parse published date
        published_dt = _parse_published(entry)

        entries.append({
            'title': title,
            'link': link,
            'source': source['name'],
            'source_key': next(k for k, v in NEWS_SOURCES.items() if v['name'] == source['name']),
            'source_type': source['type'],
            'source_trust': source.get('trust', 0),
            'tags': tags,
            'community_score': community_score,
            'published_dt': published_dt,
            'cross_source_count': 1,  # Will be updated by _apply_cross_source_bonus
        })

    return entries


def _parse_published(entry):
    """Parse the published/updated time from a feedparser entry."""
    for attr in ('published_parsed', 'updated_parsed'):
        t = entry.get(attr)
        if t:
            try:
                return datetime(*t[:6], tzinfo=timezone.utc)
            except Exception:
                pass
    return None


# ---------------------------------------------------------------------------
# Cross-source detection
# ---------------------------------------------------------------------------

def _normalize_title(title):
    """Return a frozenset of significant words for similarity comparison."""
    stopwords = {'a', 'an', 'the', 'in', 'on', 'at', 'to', 'for', 'of',
                 'and', 'or', 'is', 'are', 'was', 'were', 'with', 'by'}
    words = re.findall(r'[a-z0-9]+', title.lower())
    return frozenset(w for w in words if w not in stopwords and len(w) > 2)


def _apply_cross_source_bonus(candidates):
    """
    Detect stories covered by multiple sources (overlap in title keywords).
    Increments cross_source_count for each matching pair.
    """
    for i, a in enumerate(candidates):
        words_a = _normalize_title(a['title'])
        for b in candidates[i+1:]:
            if a['source'] == b['source']:
                continue
            words_b = _normalize_title(b['title'])
            overlap = words_a & words_b
            if len(overlap) >= 4:  # Meaningful title overlap
                a['cross_source_count'] = a.get('cross_source_count', 1) + 1
                b['cross_source_count'] = b.get('cross_source_count', 1) + 1


# ---------------------------------------------------------------------------
# Scoring
# ---------------------------------------------------------------------------

def calculate_score(entry):
    score = 0

    # 1. Source trust (intrinsic source quality)
    score += entry.get('source_trust', 0)

    # 2. Community validation (for HN — normalized 0-50)
    score += min(entry.get('community_score', 0) / 6, 50)

    # 3. Recency (fresher = more valuable, especially for security)
    dt = entry.get('published_dt')
    if dt:
        age_hours = (datetime.now(timezone.utc) - dt).total_seconds() / 3600
        bonus = RECENCY_OLD_PENALTY
        for threshold, b in RECENCY_BONUS:
            if age_hours < threshold:
                bonus = b
                break
        score += bonus

    # 4. Cross-source validation (same story in multiple outlets)
    count = entry.get('cross_source_count', 1)
    score += CROSS_SOURCE_BONUS.get(min(count, 3), 0)

    # 5. Quality signals in title
    title_lower = entry['title'].lower()
    for pattern, bonus in QUALITY_SIGNALS.items():
        if re.search(pattern, title_lower):
            score += bonus

    # 6. Noise penalties in title and link
    link_lower = entry['link'].lower()
    for pattern, penalty in NOISE_SIGNALS.items():
        if re.search(pattern, title_lower) or re.search(pattern, link_lower):
            score += penalty

    # 7. Title length sweet spot (40-80 chars)
    title_len = len(entry['title'])
    if 40 <= title_len <= 80:
        score += 10
    elif title_len > 120:
        score -= 10

    return max(score, 0)


# ---------------------------------------------------------------------------
# Category identification
# ---------------------------------------------------------------------------

def identify_category(entry):
    text = (entry.get('title', '') + ' ' + ' '.join(entry.get('tags', []))).lower()

    best_cat = 'general'
    best_matches = 0

    for cat, keywords in CONTENT_CATEGORIES.items():
        matches = sum(1 for kw in keywords if kw in text)
        if matches > best_matches:
            best_matches = matches
            best_cat = cat

    return best_cat


# ---------------------------------------------------------------------------
# Preview fetching
# ---------------------------------------------------------------------------

def fetch_preview(entry):
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


# ---------------------------------------------------------------------------
# Daily category tracking
# ---------------------------------------------------------------------------

def get_today_categories():
    try:
        if not os.path.exists(DAILY_CATEGORIES_FILE):
            return []
        with open(DAILY_CATEGORIES_FILE, 'r') as f:
            lines = f.read().strip().split('\n')
        today_str = date.today().isoformat()
        return [line.split(':')[1] for line in lines
                if line.startswith(today_str) and ':' in line]
    except Exception:
        return []


def track_daily_category(category):
    today_str = date.today().isoformat()
    with open(DAILY_CATEGORIES_FILE, 'a') as f:
        f.write(f"{today_str}:{category}\n")


# ---------------------------------------------------------------------------
# Post creation
# ---------------------------------------------------------------------------

def _seo_title(title, year):
    """Append year if not present and result fits SEO length."""
    if str(year) not in title and str(year - 1) not in title:
        candidate = f"{title} ({year})"
        if len(candidate) <= 70:
            return candidate
    return title[:70] if len(title) > 70 else title


def create_post(news):
    now = datetime.now(timezone.utc)
    post_id = str(uuid.uuid1())
    category = identify_category(news)
    file_name = f"docs/_posts/{now.strftime('%Y-%m-%d')}-top-tech-news-{post_id}.md"

    seo_title = _seo_title(news["title"], now.year)
    safe_title = seo_title.replace('"', "'")
    description = news.get("preview", "")[:155].replace('"', "'").replace("\n", " ")

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
        f.write(f'reading_time: {reading_time}\n')
        f.write(f'niche_category: {category}\n')
        f.write(f'score: {news.get("score", 0)}\n')
        f.write("---\n\n")
        f.write(f"> {news.get('preview', '')}\n\n")
        if "image" in news:
            f.write(f"![Preview]({news['image']})\n\n")
        f.write(f"**Source:** [{source_name}]({external_url}) | "
                f"**Category:** {category} | **Published:** {date_str}\n\n")
        f.write("---\n\n")
        f.write("*This article was curated by eof.news — daily AI and security intelligence.*\n")

    # Post to Twitter/X if enabled
    if os.environ.get("TWITTER_ENABLED", "").lower() == "true":
        try:
            from twitter_post import post_tweet
            post_tweet(news, category, file_name)
        except Exception as e:
            print(f"   ⚠️ Twitter post failed: {e}")
