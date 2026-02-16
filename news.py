import feedparser
import uuid
import requests
import re
from datetime import datetime, timezone
from utils import read_text_file, track_published
from const import (
    HACKERNEWS_FEED_URL,
    PUBLISHED_NEWS_FILE_NAME,
    MIN_HN_SCORE,
    HIGH_VOLUME_TOPICS,
    HIGH_CTR_PATTERNS,
    PENALTY_PATTERNS,
    TEMPORAL_BONUS,
    WEIGHTS
)
from keywords import KEYWORDS
from bs4 import BeautifulSoup
from tags import generate_tag_pages


def publish_news():
    news = select_hackernews_news()
    if news is not None:
        create_post(news)
        generate_tag_pages()
        track_published(news['link'], PUBLISHED_NEWS_FILE_NAME)
        print(f"✅ Published: {news['title']}")
        print(f"   Market Score: {news.get('market_score', 0):.1f}")
        print(f"   HN Score: {news.get('hn_score', 0)}")
    else:
        print("❌ No suitable news found")


def select_hackernews_news():
    feed = feedparser.parse(HACKERNEWS_FEED_URL)
    if not feed.entries:
        return None

    # Step 1: Estrai e filtra per keyword
    interesting_entries = filter_entries_by_keywords(feed)

    # Step 2: Rimuovi già pubblicati
    published = read_text_file(PUBLISHED_NEWS_FILE_NAME)
    unpublished_entries = [e for e in interesting_entries if e.get("link") not in published]

    # Step 3: Filtra per HN score minimo
    qualified_entries = [e for e in unpublished_entries if e.get("hn_score", 0) >= MIN_HN_SCORE]

    # Se nessuno passa il filtro, abbassa la soglia
    if not qualified_entries:
        qualified_entries = unpublished_entries

    # Step 4: Calcola market score e ordina
    scored_entries = calculate_market_score(qualified_entries)
    sorted_entries = sorted(scored_entries, key=lambda x: x.get("market_score", 0), reverse=True)

    # Step 5: Prendi il migliore con preview valida
    top_entry = filter_entries_by_preview(sorted_entries)
    return top_entry


def calculate_market_score(entries):
    """
    Calcola uno score orientato al mercato per massimizzare traffico organico.

    Formula: market_score = (hn_component + topic_component + ctr_component + penalties + temporal) * image_multiplier
    """
    today = datetime.now().strftime('%A').lower()
    temporal_bonus = TEMPORAL_BONUS.get(today, 0)

    for entry in entries:
        title = entry.get("title", "")
        title_lower = title.lower()
        link = entry.get("link", "").lower()

        # --- COMPONENTE 1: HN Score (popolarità validata) ---
        hn_score = entry.get("hn_score", 0)
        # Normalizza su scala 0-100, con cap a 500 punti HN
        hn_component = min(hn_score / 5, 100) * WEIGHTS['hn_score']

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

        # --- COMPONENTE 4: Penalità ---
        penalty = 0
        for pattern, value in PENALTY_PATTERNS:
            if re.search(pattern, title_lower) or re.search(pattern, link):
                penalty += value

        # --- COMPONENTE 5: Bonus temporale ---
        time_bonus = temporal_bonus * 0.5

        # --- SCORE FINALE ---
        market_score = hn_component + topic_component + ctr_component + penalty + time_bonus

        # Bonus per titoli di lunghezza ottimale (50-70 chars = sweet spot SEO)
        title_len = len(title)
        if 50 <= title_len <= 70:
            market_score += 10
        elif title_len > 100:
            market_score -= 10

        entry["market_score"] = max(market_score, 0)

        # Debug info
        entry["_debug"] = {
            "hn": round(hn_component, 1),
            "topic": round(topic_component, 1),
            "ctr": round(ctr_component, 1),
            "penalty": penalty,
            "temporal": time_bonus
        }

    return entries


def filter_entries_by_keywords(entries):
    matched = []

    for entry in entries["entries"]:
        title = entry.get("title", "")
        description = entry.get("summary", "") or ""
        combined = f"{title} {description}"
        matched_labels = [label for kw, label in KEYWORDS.items() if keyword_in_text(combined, kw)]

        if matched_labels:
            # Estrai score HN dal summary (hnrss include "X points")
            hn_score = 0
            score_match = re.search(r'(\d+)\s+points?', description)
            if score_match:
                hn_score = int(score_match.group(1))

            matched.append({
                "title": title,
                "link": entry.get("link", ""),
                "source": "Hacker News",
                "tags": matched_labels,
                "hn_score": hn_score
            })

    return matched


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
        f.write(f'keywords: {", ".join(news["tags"]).lower()}, tech news, hacker news\n')
        f.write(f'author: ipsedigit\n')
        f.write("---\n\n")

        f.write(f"### [{news['title']}]({news['link']})\n\n")
        f.write(f"> {news['preview']}\n")

        if "image" in news:
            f.write(f"![Preview Image]({news['image']})\n\n")


