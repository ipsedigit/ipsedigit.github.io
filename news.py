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
    MAX_POSTS_PER_DAY,
    DAILY_CATEGORIES_FILE,
    TITLE_BONUS,
    TITLE_PENALTY,
)
from keywords import KEYWORDS
from bs4 import BeautifulSoup
from tags import generate_tag_pages


def publish_news():
    """Pubblica il miglior post disponibile da tutte le fonti."""

    # Check limite giornaliero
    today_categories = get_today_categories()
    if len(today_categories) >= MAX_POSTS_PER_DAY:
        print(f"⏸️ Limit reached: {len(today_categories)}/{MAX_POSTS_PER_DAY} posts today")
        return

    print(f"📊 Posts today: {len(today_categories)}/{MAX_POSTS_PER_DAY}")

    # Trova il miglior post da TUTTE le fonti
    best_post = find_best_post(exclude_categories=today_categories)

    if best_post:
        create_post(best_post)
        generate_tag_pages()
        track_published(best_post['link'], PUBLISHED_NEWS_FILE_NAME)
        track_daily_category(identify_category(best_post))

        print(f"✅ Published: {best_post['title']}")
        print(f"   Source: {best_post['source']}")
        print(f"   Score: {best_post['score']}")
    else:
        print("❌ No suitable posts found")


def find_best_post(exclude_categories=None):
    """
    Cerca il miglior post da TUTTE le fonti e ritorna quello con score più alto.
    Non fa selezione random - prende sempre il migliore disponibile.
    """
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
                # Skip già pubblicati
                if entry['link'] in published:
                    continue

                # Skip categorie già usate oggi
                if exclude_categories:
                    cat = identify_category(entry)
                    if cat in exclude_categories:
                        continue

                # Calcola score
                entry['score'] = calculate_score(entry, source)

                # Skip se score troppo basso
                if entry['score'] < 50:
                    continue

                all_candidates.append(entry)

        except Exception as e:
            print(f"   ⚠️ Error: {e}")

    if not all_candidates:
        return None

    # Ordina per score e prendi i top 10
    all_candidates.sort(key=lambda x: x['score'], reverse=True)
    top_candidates = all_candidates[:10]

    print(f"📋 Top candidates:")
    for i, c in enumerate(top_candidates[:5]):
        print(f"   {i+1}. [{c['score']}] {c['title'][:50]}...")

    # Trova il primo con preview valida
    for candidate in top_candidates:
        result = fetch_preview(candidate)
        if result:
            return result

    return None


def extract_entries(feed, source):
    """Estrae entries dal feed."""
    entries = []

    for entry in feed.entries[:50]:
        title = entry.get("title", "").strip()
        link = entry.get("link", "").strip()
        summary = entry.get("summary", "") or entry.get("description", "") or ""

        if not title or not link:
            continue

        # Match keywords per i tag
        combined = f"{title} {summary}".lower()
        tags = [label for kw, label in KEYWORDS.items()
                if re.search(rf'\b{re.escape(kw)}\b', combined, re.IGNORECASE)]

        # Skip se non matcha nessun keyword tech
        if not tags:
            continue

        # Estrai community score (per HN, Lobsters)
        community_score = 0
        score_match = re.search(r'(\d+)\s+points?', summary)
        if score_match:
            community_score = int(score_match.group(1))

        # Filtra per min_score della fonte
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
    Calcola score semplice:
    - Base: community score (0-50 normalizzato)
    - Bonus: tipo fonte
    - Bonus: pattern titolo
    - Penalty: contenuti da evitare
    """
    title_lower = entry['title'].lower()
    link_lower = entry['link'].lower()

    # Base score da community (normalizzato 0-50)
    score = min(entry.get('community_score', 0) / 2, 50)

    # Bonus per tipo fonte
    source_type = entry['source_type']
    if source_type == 'corporate_blog':
        score += 30  # Contenuti originali = meno competizione SEO
    elif source_type == 'security':
        score += 25  # Security news = alto engagement
    elif source_type == 'startup':
        score += 20  # Startup news = buon traffico
    elif source_type == 'community':
        score += 10  # Community = variabile

    # Bonus per pattern nel titolo
    for pattern, bonus in TITLE_BONUS.items():
        if re.search(pattern, title_lower):
            score += bonus

    # Penalty
    for pattern, penalty in TITLE_PENALTY.items():
        if re.search(pattern, title_lower) or re.search(pattern, link_lower):
            score += penalty

    # Bonus per titoli di lunghezza ottimale (40-80 char)
    title_len = len(entry['title'])
    if 40 <= title_len <= 80:
        score += 10
    elif title_len > 120:
        score -= 10

    return max(score, 0)


def identify_category(entry):
    """Identifica la categoria del post."""
    text = (entry.get('title', '') + ' ' + ' '.join(entry.get('tags', []))).lower()

    best_cat = 'general'
    best_matches = 0

    for cat, keywords in CONTENT_CATEGORIES.items():
        matches = sum(1 for kw in keywords if kw in text)
        if matches > best_matches:
            best_matches = matches
            best_cat = cat

    return best_cat


def fetch_preview(entry):
    """Fetch preview e immagine dalla pagina."""
    try:
        response = requests.get(entry['link'], timeout=5, headers={
            'User-Agent': 'Mozilla/5.0 (compatible; eofBot/1.0)'
        })
        if response.status_code != 200:
            return None

        soup = BeautifulSoup(response.text, 'html.parser')

        # Get description
        meta_desc = (
            soup.find("meta", property="og:description") or
            soup.find("meta", attrs={"name": "description"})
        )
        if meta_desc and meta_desc.get("content"):
            entry['preview'] = meta_desc["content"].strip()[:200]
        else:
            return None

        # Get image (opzionale)
        meta_img = soup.find("meta", property="og:image")
        if meta_img and meta_img.get("content"):
            entry['image'] = meta_img["content"].strip()

        return entry

    except Exception as e:
        print(f"   ⚠️ Preview fetch failed: {e}")
        return None


def get_today_categories():
    """Legge le categorie già pubblicate oggi."""
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


def track_daily_category(category):
    """Traccia la categoria pubblicata oggi."""
    today_str = date.today().isoformat()
    with open(DAILY_CATEGORIES_FILE, 'a') as f:
        f.write(f"{today_str}:{category}\n")


def keyword_in_text(text, keyword):
    return re.search(rf'\b{re.escape(keyword)}\b', text, re.IGNORECASE)


def create_post(news):
    """Crea il file markdown del post."""
    now = datetime.now(timezone.utc)
    post_id = str(uuid.uuid1())
    file_name = f"docs/_posts/{now.strftime('%Y-%m-%d')}-top-tech-news-{post_id}.md"

    safe_title = news["title"].replace('"', "'")
    description = news.get("preview", "")[:155].replace('"', "'").replace("\n", " ")

    with open(file_name, 'w', encoding='utf-8') as f:
        f.write("---\n")
        f.write("layout: post\n")
        f.write(f'title: "{safe_title}"\n')
        f.write(f'date: {now.strftime("%Y-%m-%d %H:%M:%S %z")}\n')
        f.write(f'external_url: {news["link"]}\n')
        f.write("categories:\n")
        for tag in news['tags']:
            f.write(f"  - {tag}\n")
        f.write(f'description: "{description}"\n')
        if "image" in news:
            f.write(f'image: {news["image"]}\n')
        f.write(f'source: {news.get("source", "Unknown")}\n')
        f.write("---\n\n")
        f.write(f"> {news.get('preview', '')}\n\n")
        if "image" in news:
            f.write(f"![Preview]({news['image']})\n")
