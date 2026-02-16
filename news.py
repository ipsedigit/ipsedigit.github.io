import feedparser
import uuid
import requests
import re
import random
import os
from datetime import datetime, timezone, date
from utils import read_text_file, track_published
from const import (
    NEWS_SOURCES,
    PUBLISHED_NEWS_FILE_NAME,
    MIN_HN_SCORE,
    HIGH_VOLUME_TOPICS,
    HIGH_CTR_PATTERNS,
    PENALTY_PATTERNS,
    TEMPORAL_BONUS,
    WEIGHTS,
    CONTENT_CATEGORIES,
    MAX_POSTS_PER_DAY,
    DAILY_CATEGORIES_FILE,
)
from keywords import KEYWORDS
from bs4 import BeautifulSoup
from tags import generate_tag_pages


def publish_news():
    """
    Pubblica la migliore notizia disponibile.
    Rispetta il limite giornaliero e diversifica le categorie.
    """
    # Controlla quanti post sono stati fatti oggi e in quali categorie
    today_categories = get_today_categories()
    posts_today = len(today_categories)

    if posts_today >= MAX_POSTS_PER_DAY:
        print(f"⏸️ Already published {posts_today}/{MAX_POSTS_PER_DAY} posts today. Skipping.")
        return

    print(f"📊 Posts today: {posts_today}/{MAX_POSTS_PER_DAY}")
    print(f"   Categories used: {today_categories if today_categories else 'None'}")

    # Seleziona news evitando categorie già usate oggi
    news = select_best_news(exclude_categories=today_categories)

    if news is not None:
        # Identifica la categoria del post
        post_category = identify_category(news)

        create_post(news)
        generate_tag_pages()
        track_published(news['link'], PUBLISHED_NEWS_FILE_NAME)
        track_daily_category(post_category)

        print(f"✅ Published: {news['title']}")
        print(f"   Source: {news.get('source', 'Unknown')}")
        print(f"   Category: {post_category}")
        print(f"   Market Score: {news.get('market_score', 0):.1f}")
    else:
        print("❌ No suitable news found from any source")


def get_today_categories():
    """Legge le categorie già pubblicate oggi."""
    try:
        if not os.path.exists(DAILY_CATEGORIES_FILE):
            return []

        with open(DAILY_CATEGORIES_FILE, 'r') as f:
            content = f.read().strip()
            if not content:
                return []

            lines = content.split('\n')
            # Formato: YYYY-MM-DD:category
            today_str = date.today().isoformat()
            today_cats = [line.split(':')[1] for line in lines
                         if line.startswith(today_str) and ':' in line]
            return today_cats
    except Exception:
        return []


def track_daily_category(category):
    """Traccia la categoria pubblicata oggi."""
    today_str = date.today().isoformat()
    with open(DAILY_CATEGORIES_FILE, 'a') as f:
        f.write(f"{today_str}:{category}\n")


def identify_category(news):
    """Identifica la categoria principale di un post basandosi sui tag e titolo."""
    title_lower = news.get('title', '').lower()
    tags_lower = [t.lower() for t in news.get('tags', [])]
    combined = title_lower + ' ' + ' '.join(tags_lower)

    best_category = 'general'
    best_matches = 0

    for cat_key, cat_info in CONTENT_CATEGORIES.items():
        matches = sum(1 for kw in cat_info['keywords'] if kw in combined)
        if matches > best_matches:
            best_matches = matches
            best_category = cat_key

    return best_category


def select_source():
    """
    Seleziona una fonte usando weighted random selection.
    Fonti con weight maggiore hanno più probabilità di essere selezionate.
    """
    sources = list(NEWS_SOURCES.keys())
    weights = [NEWS_SOURCES[s]['weight'] for s in sources]
    return random.choices(sources, weights=weights, k=1)[0]


def select_best_news(exclude_categories=None):
    """
    Strategia di selezione multi-source:
    1. Seleziona una fonte primaria (weighted random)
    2. Prova a trovare un buon post da quella fonte
    3. Se fallisce, prova le altre fonti in ordine di authority
    4. Esclude post di categorie già pubblicate oggi
    """
    if exclude_categories is None:
        exclude_categories = []

    published = read_text_file(PUBLISHED_NEWS_FILE_NAME)

    # Seleziona fonte primaria
    primary_source = select_source()
    print(f"🎯 Primary source selected: {NEWS_SOURCES[primary_source]['name']}")

    # Prova la fonte primaria
    result = fetch_and_score_from_source(primary_source, published, exclude_categories)
    if result:
        return result

    # Fallback: prova altre fonti ordinate per authority
    other_sources = sorted(
        [s for s in NEWS_SOURCES.keys() if s != primary_source],
        key=lambda s: NEWS_SOURCES[s]['authority'],
        reverse=True
    )

    for source_key in other_sources:
        print(f"🔄 Trying fallback source: {NEWS_SOURCES[source_key]['name']}")
        result = fetch_and_score_from_source(source_key, published, exclude_categories)
        if result:
            return result

    return None


def fetch_and_score_from_source(source_key, published, exclude_categories=None):
    """Fetch, filtra, score e restituisce il miglior post da una fonte."""
    if exclude_categories is None:
        exclude_categories = []

    source = NEWS_SOURCES[source_key]

    try:
        feed = feedparser.parse(source['feed_url'])
        if not feed.entries:
            print(f"   ⚠️ No entries from {source['name']}")
            return None

        # Estrai entries
        entries = extract_entries(feed, source)

        # Filtra già pubblicati
        unpublished = [e for e in entries if e.get("link") not in published]
        if not unpublished:
            print(f"   ⚠️ All entries already published from {source['name']}")
            return None

        # Filtra categorie già usate oggi
        if exclude_categories:
            filtered = []
            for entry in unpublished:
                entry_cat = identify_category(entry)
                if entry_cat not in exclude_categories:
                    filtered.append(entry)
            unpublished = filtered

            if not unpublished:
                print(f"   ⚠️ All entries from {source['name']} are in already-published categories")
                return None

        # Calcola market score
        scored = calculate_market_score(unpublished, source)
        sorted_entries = sorted(scored, key=lambda x: x.get("market_score", 0), reverse=True)

        # Trova il migliore con preview valida
        result = filter_entries_by_preview(sorted_entries)
        return result

    except Exception as e:
        print(f"   ❌ Error fetching {source['name']}: {e}")
        return None


def extract_entries(feed, source):
    """Estrae e normalizza le entries da un feed RSS."""
    entries = []
    source_type = source.get('type', 'unknown')

    for entry in feed.entries[:50]:  # Limita a 50 per performance
        title = entry.get("title", "")
        link = entry.get("link", "")
        description = entry.get("summary", "") or entry.get("description", "") or ""

        # Estrai tags basati sui keyword
        combined = f"{title} {description}"
        matched_labels = [label for kw, label in KEYWORDS.items() if keyword_in_text(combined, kw)]

        # Salta se non matcha nessun keyword (per mantenere focus tech)
        if not matched_labels:
            continue

        # Estrai score se disponibile (solo HN e Lobsters hanno score nel feed)
        score = 0
        if source_type == 'aggregator':
            score_match = re.search(r'(\d+)\s+points?', description)
            if score_match:
                score = int(score_match.group(1))

        entries.append({
            "title": title,
            "link": link,
            "source": source['name'],
            "source_type": source_type,
            "source_authority": source['authority'],
            "tags": matched_labels,
            "community_score": score,
        })

    return entries


def calculate_market_score(entries, source=None):
    """
    Calcola uno score orientato al mercato per massimizzare traffico organico.

    Formula: market_score = (community + topic + ctr + authority + temporal + penalties)
    """
    today = datetime.now().strftime('%A').lower()
    temporal_bonus = TEMPORAL_BONUS.get(today, 0)

    for entry in entries:
        title = entry.get("title", "")
        title_lower = title.lower()
        link = entry.get("link", "").lower()

        # --- COMPONENTE 1: Community Score (popolarità validata) ---
        community_score = entry.get("community_score", 0)
        # Normalizza su scala 0-100, con cap a 500 punti
        community_component = min(community_score / 5, 100) * WEIGHTS['hn_score']

        # --- COMPONENTE 2: Topic Volume (potenziale SEO) ---
        topic_component = 0
        for topic, value in HIGH_VOLUME_TOPICS.items():
            if topic in title_lower or topic in link:
                topic_component = max(topic_component, value)
        topic_component *= WEIGHTS['topic_volume']

        # --- COMPONENTE 3: CTR Pattern (clickability) ---
        ctr_component = 0
        for pattern, value in HIGH_CTR_PATTERNS:
            if re.search(pattern, title_lower):
                ctr_component += value
        # Cap a 100
        ctr_component = min(ctr_component, 100) * WEIGHTS['ctr_pattern']

        # --- COMPONENTE 4: Source Authority Bonus ---
        # Blog aziendali (GitHub, Netflix, Cloudflare) hanno contenuti originali
        # che Google premia per freshness e unicità
        authority = entry.get("source_authority", 80)
        source_type = entry.get("source_type", "unknown")

        authority_bonus = 0
        if source_type == 'corporate_blog':
            # Contenuti originali = meno competizione SEO
            authority_bonus = 25
        elif source_type == 'news':
            # News mainstream = alto trust ma alta competizione
            authority_bonus = 10
        elif authority >= 90:
            authority_bonus = 15

        # --- COMPONENTE 5: Penalità ---
        penalty = 0
        for pattern, value in PENALTY_PATTERNS:
            if re.search(pattern, title_lower) or re.search(pattern, link):
                penalty += value

        # --- COMPONENTE 6: Bonus temporale ---
        time_bonus = temporal_bonus * 0.5

        # --- SCORE FINALE ---
        market_score = (
            community_component +
            topic_component +
            ctr_component +
            authority_bonus +
            penalty +
            time_bonus
        )

        # Bonus per titoli di lunghezza ottimale (50-70 chars = sweet spot SEO)
        title_len = len(title)
        if 50 <= title_len <= 70:
            market_score += 10
        elif title_len > 100:
            market_score -= 10

        entry["market_score"] = max(market_score, 0)

    return entries



def keyword_in_text(text, keyword):
    return re.search(rf'\b{re.escape(keyword)}\b', text, re.IGNORECASE)


def filter_entries_by_preview(entries):
    """Filtra entries che hanno preview e immagine valide."""
    for entry in entries:
        try:
            response = requests.get(entry["link"], timeout=5)
            if response.status_code != 200:
                continue

            soup = BeautifulSoup(response.text, "html.parser")

            # Get preview text
            meta_desc = (
                soup.find("meta", property="og:description") or
                soup.find("meta", attrs={"name": "twitter:description"}) or
                soup.find("meta", attrs={"name": "description"})
            )

            # Get preview image
            meta_img = (
                soup.find("meta", property="og:image") or
                soup.find("meta", attrs={"name": "twitter:image"})
            )

            if meta_desc and meta_desc.get("content"):
                entry["preview"] = meta_desc["content"].strip()
                if meta_img and meta_img.get("content"):
                    entry["image"] = meta_img["content"].strip()
                    return entry

        except Exception as e:
            print(f"⚠️ Failed to fetch preview for {entry['link']}: {e}")

    return None



def create_post(news):
    now = datetime.now(timezone.utc)
    post_id = str(uuid.uuid1())
    file_name = f"docs/_posts/{now.strftime('%Y-%m-%d')}-top-tech-news-{post_id}.md"

    # Escape double quotes in title to avoid YAML parsing issues
    safe_title = news["title"].replace('"', "'")

    # Clean description for SEO (max 160 chars)
    description = news.get("preview", "")[:155] + "..." if len(news.get("preview", "")) > 155 else news.get("preview", "")
    description = description.replace('"', "'").replace("\n", " ")

    with open(file_name, 'w', encoding='utf-8') as f:
        f.write("---\n")
        f.write("layout: post\n")
        f.write(f'title: "{safe_title}"\n')
        f.write(f'date: {now.strftime("%Y-%m-%d %H:%M:%S %z")}\n')
        f.write(f"categories:\n")
        for tag in news['tags']:
            f.write(f"  - {tag}\n")
        f.write(f'description: "{description}"\n')
        if "image" in news:
            f.write(f'image: {news["image"]}\n')
        f.write(f'keywords: {", ".join(news["tags"]).lower()}, tech news\n')
        f.write(f'source: {news.get("source", "Unknown")}\n')
        f.write(f'author: ipsedigit\n')
        f.write("---\n\n")

        f.write(f"### [{news['title']}]({news['link']})\n\n")
        f.write(f"> {news['preview']}\n")

        if "image" in news:
            f.write(f"![Preview Image]({news['image']})\n\n")


