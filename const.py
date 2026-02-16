PUBLISHED_NEWS_FILE_NAME = "news/published.txt"
PUBLISHED_QUOTES_FILE_NAME = "quotes/published.txt"
QUOTES_FILE_NAME = "quotes/quotes.json"
HACKERNEWS_FEED_URL = "https://hnrss.org/frontpage?count=50"

# Viralità - punteggio minimo HN
MIN_HN_SCORE = 100

# Pattern titoli virali (regex)
VIRAL_PATTERNS = [
    r'^\d+\s',                    # Inizia con numero: "10 reasons..."
    r'how\s+(i|we|to)\s',         # "How I...", "How to..."
    r'why\s+(i|we)\s',            # "Why I quit...", "Why we..."
    r'show\s+hn',                 # Show HN (progetti nuovi)
    r'ask\s+hn',                  # Ask HN (discussioni)
    r'(is\s+dead|is\s+dying)',    # Controversia
    r'(startup|founded|raised)',  # Startup news
    r'(open.?source|free|free)',  # Open source, gratis
    r'(ai|gpt|llm|chatgpt|copilot)',  # AI hype
]
