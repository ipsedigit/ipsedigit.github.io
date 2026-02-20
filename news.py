import feedparser
import uuid
import requests
import re
import os
from datetime import datetime, timezone, date
from utils import read_text_file, track_published
from const import (
    NEWS_SOURCES,
    PUBLISHED_NEWS_FILE_NAME,
    CONTENT_CATEGORIES,
    NICHE_CATEGORIES,
    MAX_POSTS_PER_DAY,
    DAILY_CATEGORIES_FILE,
    TITLE_BONUS,
    TITLE_PENALTY,
    AI_SUBNICHES,
    SECURITY_SUBNICHES,
)
from keywords import KEYWORDS
from bs4 import BeautifulSoup
from tags import generate_tag_pages


def publish_news():
    """Publish the best available post for an un-covered sub-niche today."""
    today_subniches = get_today_subniches()

    if len(today_subniches) >= MAX_POSTS_PER_DAY:
        print(f"⏸️ Daily limit reached: {len(today_subniches)}/{MAX_POSTS_PER_DAY} posts today")
        return

    print(f"📊 Posts today: {len(today_subniches)}/{MAX_POSTS_PER_DAY}")
    print(f"   Sub-niches covered: {today_subniches or 'none yet'}")

    best_post = find_best_post(exclude_subniches=today_subniches)

    if best_post:
        create_post(best_post)
        generate_tag_pages()
        track_published(best_post['link'], PUBLISHED_NEWS_FILE_NAME)
        sub_key = best_post.get('_subniche') or best_post.get('_category', 'unknown')
        track_daily_subniche(sub_key)

        print(f"✅ Published: {best_post['title']}")
        print(f"   Source: {best_post['source']}")
        print(f"   Score: {best_post['score']}")
        print(f"   Category: {best_post.get('_category')} / {best_post.get('_subniche')}")
    else:
        print("❌ No suitable posts found for uncovered sub-niches")


def find_best_post(exclude_subniches=None):
    """
    Find the best post across all sources by score.
    Requires 2+ keyword matches and niche category (AI or Security).
    Skips sub-niches already covered today to ensure diversity.
    """
    if exclude_subniches is None:
        exclude_subniches = []

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

                subniche = identify_subniche(entry, cat)
                entry['_category'] = cat
                entry['_subniche'] = subniche

                # Skip sub-niches (or categories) already covered today
                sub_key = subniche or cat
                if sub_key in exclude_subniches:
                    continue

                entry['score'] = calculate_score(entry, source)

                if entry['score'] < 50:
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
    """Identify the sub-niche within AI or Security."""
    text = (entry.get('title', '') + ' ' + ' '.join(entry.get('tags', []))).lower()

    if main_cat == 'ai':
        subniches = AI_SUBNICHES
    elif main_cat == 'security':
        subniches = SECURITY_SUBNICHES
    else:
        return None

    best_sub = None
    best_matches = 0

    for sub, keywords in subniches.items():
        matches = sum(1 for kw in keywords if kw in text)
        if matches > best_matches:
            best_matches = matches
            best_sub = sub

    return best_sub


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


def get_today_subniches():
    """Read sub-niches already published today."""
    try:
        if not os.path.exists(DAILY_CATEGORIES_FILE):
            return []

        with open(DAILY_CATEGORIES_FILE, 'r') as f:
            lines = f.read().strip().split('\n')

        today_str = date.today().isoformat()
        return [line.split(':')[1] for line in lines
                if line.startswith(today_str) and ':' in line]
    except:
        return []


def track_daily_subniche(subniche):
    """Track the sub-niche published today."""
    today_str = date.today().isoformat()
    with open(DAILY_CATEGORIES_FILE, 'a') as f:
        f.write(f"{today_str}:{subniche}\n")


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
        f.write(f'reading_time: {reading_time}\n')
        f.write(f'niche_category: {category}\n')
        if subniche:
            f.write(f'niche_subniche: {subniche}\n')
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
        f.write("*This article was curated by eof.news — signal for AI engineers and security practitioners.*\n")

    if os.environ.get("TWITTER_ENABLED", "").lower() == "true":
        try:
            from twitter_post import post_tweet
            post_tweet(news, category, file_name)
        except Exception as e:
            print(f"   ⚠️ Twitter post failed: {e}")
