import feedparser
import uuid
import requests
import re
from datetime import datetime, timezone
from utils import read_text_file, track_published
from const import HACKERNEWS_FEED_URL, PUBLISHED_NEWS_FILE_NAME, MIN_HN_SCORE, VIRAL_PATTERNS
from keywords import KEYWORDS
from bs4 import BeautifulSoup
from tags import generate_tag_pages


def publish_news():
    news = select_hackernews_news()
    if news is not None:
        create_post(news)
        generate_tag_pages()
        track_published(news['link'], PUBLISHED_NEWS_FILE_NAME)


def select_hackernews_news():
    feed = feedparser.parse(HACKERNEWS_FEED_URL)
    if not feed.entries:
        return None

    # Step 1: Filtra per keyword
    interesting_entries = filter_entries_by_keywords(feed)

    # Step 2: Rimuovi già pubblicati
    published = read_text_file(PUBLISHED_NEWS_FILE_NAME)
    unpublished_entries = [e for e in interesting_entries if e.get("link") not in published]

    # Step 3: Calcola score viralità e ordina
    scored_entries = calculate_viral_score(unpublished_entries)
    sorted_entries = sorted(scored_entries, key=lambda x: x.get("viral_score", 0), reverse=True)

    # Step 4: Prendi il migliore con preview valida
    top_entry = filter_entries_by_preview(sorted_entries)
    return top_entry


def calculate_viral_score(entries):
    """Calcola uno score di viralità per ogni entry."""
    for entry in entries:
        score = 0
        title = entry.get("title", "").lower()

        # Score da HN (se disponibile)
        hn_score = entry.get("hn_score", 0)
        if hn_score >= MIN_HN_SCORE:
            score += 50  # Bonus per post popolari
        score += min(hn_score // 10, 30)  # Max 30 punti da HN score

        # Bonus per pattern virali nel titolo
        for pattern in VIRAL_PATTERNS:
            if re.search(pattern, title, re.IGNORECASE):
                score += 15
                break  # Solo un bonus per pattern

        # Bonus per titoli corti e incisivi (più clickabili)
        if len(entry.get("title", "")) < 60:
            score += 10

        # Bonus per più tag (più audience potenziale)
        score += len(entry.get("tags", [])) * 5

        entry["viral_score"] = score

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
        f.write(f"categories: [{', '.join(news['tags'])}]\n")
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


