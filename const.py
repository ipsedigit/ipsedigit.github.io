PUBLISHED_NEWS_FILE_NAME = "news/published.txt"

# =============================================================================
# PUBLISHING STRATEGY
# =============================================================================

MAX_POSTS_PER_DAY = 3
DAILY_CATEGORIES_FILE = "news/daily_categories.txt"

# Categorie per diversificare i post giornalieri
CONTENT_CATEGORIES = {
    'ai': ['ai', 'artificial intelligence', 'machine learning', 'llm', 'gpt', 'chatgpt',
           'openai', 'anthropic', 'claude', 'gemini', 'copilot', 'neural', 'deep learning'],
    'dev': ['python', 'rust', 'golang', 'javascript', 'typescript', 'react', 'programming',
            'developer', 'coding', 'software', 'github', 'open source'],
    'infra': ['kubernetes', 'docker', 'aws', 'cloud', 'devops', 'terraform', 'linux',
              'serverless', 'database', 'postgresql', 'redis', 'api'],
    'security': ['security', 'hack', 'breach', 'vulnerability', 'privacy', 'encryption',
                 'cyber', 'malware', 'ransomware', 'exploit'],
    'startup': ['startup', 'funding', 'raised', 'billion', 'acquisition', 'ipo', 'venture',
                'founder', 'layoff', 'valuation'],
}

# =============================================================================
# NEWS SOURCES
# =============================================================================

NEWS_SOURCES = {
    'hackernews': {
        'name': 'Hacker News',
        'feed_url': 'https://hnrss.org/frontpage?count=100',
        'min_score': 100,  # Solo post con almeno 100 punti
        'type': 'aggregator',
    },
    'lobsters': {
        'name': 'Lobste.rs',
        'feed_url': 'https://lobste.rs/rss',
        'min_score': 20,
        'type': 'aggregator',
    },
    'github_blog': {
        'name': 'GitHub Blog',
        'feed_url': 'https://github.blog/feed/',
        'min_score': 0,
        'type': 'corporate_blog',
    },
    'netflix_tech': {
        'name': 'Netflix Tech Blog',
        'feed_url': 'https://netflixtechblog.com/feed',
        'min_score': 0,
        'type': 'corporate_blog',
    },
    'cloudflare_blog': {
        'name': 'Cloudflare Blog',
        'feed_url': 'https://blog.cloudflare.com/rss/',
        'min_score': 0,
        'type': 'corporate_blog',
    },
}

# =============================================================================
# SCORING - Semplificato
# =============================================================================

# Bonus per pattern nel titolo che aumentano i click
TITLE_BONUS = {
    # Numeri nei titoli = +20% CTR
    r'^\d+\s': 20,
    r'\d+\s*(ways|tips|reasons|things)': 25,

    # How-to = alto valore per utenti
    r'how\s+to\s+': 30,
    r'guide|tutorial': 25,

    # Novità/Annunci = urgenza
    r'(announce|launch|releas|introduc)': 30,
    r'show\s+hn': 35,

    # Controversia = viralità
    r'(is\s+dead|killed|quit|fired|layoff)': 35,

    # Security = sempre cliccato
    r'(hack|breach|vulnerab|exploit|leak)': 40,

    # Soldi = interesse
    r'(\$\d|million|billion|raised|funding)': 30,
}

# Penalità per contenuti da evitare
TITLE_PENALTY = {
    r'ask\s+hn': -50,  # Discussioni, non articoli
    r'\[pdf\]': -30,   # PDF = UX peggiore
    r'(nytimes|wsj|bloomberg)\.com': -100,  # Paywall
    r'(rant|opinion|unpopular)': -40,
    r'(years?\s+ago|in\s+20[01]\d)': -50,  # Contenuti vecchi
}
