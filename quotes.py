from datetime import datetime
import json
import random
from dataclasses import dataclass
from datetime import datetime, timezone
import sys


@dataclass
class Quote:
    id: str
    author: str
    en: str


def read_quotes() -> list[Quote]:
    with open('quotes/quotes.json', 'r', encoding='utf-8') as f:
        quotes = json.load(f)
        return [Quote(**quote) for quote in quotes]


def select_quote() -> Quote:
    quotes = read_quotes()
    quote = random.choice(quotes)
    published_ids = load_published()
    if quote.id not in published_ids:
        return quote
    else:
        print("Quote already published. Script terminated.")
        sys.exit(1)


def create_post(quote: Quote):
    now = datetime.now(timezone.utc)
    file_name = f"docs/_posts/{now.strftime("%Y-%m-%d")}-quote-{quote.id}.md"
    with open(file_name, 'w', encoding='utf-8') as f:
        f.write(f"---\n")
        f.write(f"layout: post\n")
        f.write(f"title: {quote.author}\n")
        f.write(f"date: {now.strftime("%Y-%m-%d %H:%M:%S %z")}\n")
        f.write(f"categories: [quotes]\n")
        f.write(f"---\n\n")
        f.write(f"{quote.en}  \n\n")


def track_published(post_id: str):
    with open('quotes/published.txt','a', encoding='utf-8') as f:
        f.write(post_id + '\n')


def load_published() -> set:
    try:
        with open('quotes/published.txt', 'r', encoding='utf-8') as f:
            return set(line.strip() for line in f)
    except FileNotFoundError:
        return set()


def publish_quote():
    quote = select_quote()
    create_post(quote)
    track_published(quote.id)
