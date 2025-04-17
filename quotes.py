import json
import random
from dataclasses import dataclass
from datetime import datetime, timezone

from const import PUBLISHED_QUOTES_FILE_NAME, QUOTES_FILE_NAME
from utils import read_text_file, is_fresh_resource, track_published
import sys


@dataclass
class Quote:
    id: str
    author: str
    en: str


def read_quotes() -> list[Quote]:
    with open(QUOTES_FILE_NAME, 'r', encoding='utf-8') as f:
        quotes = json.load(f)
        return [Quote(**quote) for quote in quotes]


def select_quote() -> Quote:
    quotes = read_quotes()
    quote = random.choice(quotes)
    published_ids = read_text_file(PUBLISHED_QUOTES_FILE_NAME)
    if is_fresh_resource(quote.id, published_ids):
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


def publish_quote():
    quote = select_quote()
    create_post(quote)
    track_published(quote.id, PUBLISHED_QUOTES_FILE_NAME)
