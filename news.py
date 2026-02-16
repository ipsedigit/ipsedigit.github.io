import feedparser
import uuid
import requests
import re
from datetime import datetime, timezone
from utils import read_text_file, is_fresh_resource, track_published
from const import HACKERNEWS_FEED_URL, PUBLISHED_NEWS_FILE_NAME
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
    interesting_entries = filter_entries_by_keywords(feed)
    unpublished_entries = filter_already_published_entries(read_text_file(PUBLISHED_NEWS_FILE_NAME), interesting_entries)
    top_entry = filter_entries_by_preview(unpublished_entries)
    return top_entry


def filter_entries_by_keywords(entries):
    matched = []

    for entry in entries["entries"]:
        title = entry["title"]
        description = entry["summary"] or ""
        combined = f"{title} {description}"
        matched_labels = [label for kw, label in KEYWORDS.items() if keyword_in_text(combined, kw)]

        if matched_labels:
            matched.append({
                "title": entry["title"],
                "link": entry["link"],
                "source": "Hacker News",
                "tags": matched_labels
            })

    return matched


def keyword_in_text(text, keyword):
    return re.search(rf'\b{re.escape(keyword)}\b', text, re.IGNORECASE)


def filter_entries_by_preview(entries):
    for entry in entries:
        try:
            response = requests.get(entry["link"], timeout=5)
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


def filter_already_published_entries(published_links: set, entries: list[dict]) -> list[dict]:
    return [
        entry for entry in entries
        if entry.get("link") not in published_links
    ]


def create_post(news):
    now = datetime.now(timezone.utc)
    post_id = str(uuid.uuid1())
    file_name = f"docs/_posts/{now.strftime('%Y-%m-%d')}-top-tech-news-{post_id}.md"

    # Escape double quotes in title to avoid YAML parsing issues
    safe_title = news["title"].replace('"', "'")

    with open(file_name, 'w', encoding='utf-8') as f:
        f.write("---\n")
        f.write("layout: post\n")
        f.write(f'title: "{safe_title}"\n')
        f.write(f'date: {now.strftime("%Y-%m-%d %H:%M:%S %z")}\n')
        f.write(f"categories: {', '.join(news['tags'])}\n")
        f.write("---\n\n")

        f.write(f"### [{news['title']}]({news['link']})\n\n")
        f.write(f"> {news['preview']}\n")

        if "image" in news:
            f.write(f"![Preview Image]({news['image']})\n\n")


