PUBLISHED_NEWS_FILE_NAME = "news/published.txt"

# =============================================================================
# PUBLISHING STRATEGY
# =============================================================================

MAX_POSTS_PER_DAY = 1          # One great story per day, not three mediocre ones
DAILY_CATEGORIES_FILE = "news/daily_categories.txt"

# Niche focus: AI + Security for topical authority
CONTENT_CATEGORIES = {
    'ai': [
        'ai', 'artificial intelligence', 'machine learning', 'llm', 'gpt', 'chatgpt',
        'openai', 'anthropic', 'claude', 'gemini', 'copilot', 'neural', 'deep learning',
        'language model', 'foundation model', 'diffusion', 'transformer', 'hugging face',
        'mistral', 'deepmind', 'generative ai', 'agi',
    ],
    'security': [
        'security', 'hack', 'breach', 'vulnerability', 'privacy', 'encryption',
        'cyber', 'malware', 'ransomware', 'exploit', 'cve', 'zero-day', 'zero day',
        'phishing', 'backdoor', 'botnet', 'infosec', 'threat', 'attack', 'intrusion',
    ],
}

# Only these categories are accepted for publishing
NICHE_CATEGORIES = {'ai', 'security'}

# =============================================================================
# NEWS SOURCES — 12 Elite Sources
#
# Principle: every source must be capable of producing a story
# worth reading on its own. No noise, no padding.
#
# 'trust' = base score added to every story from this source.
# Higher = we trust this source more intrinsically.
# =============================================================================

NEWS_SOURCES = {

    # --- AI PRIMARY SOURCES ---
    # These are the authoritative voices. Every post they publish is relevant.

    'openai_blog': {
        'name': 'OpenAI Blog',
        'feed_url': 'https://openai.com/blog/rss/',
        'min_score': 0,
        'type': 'ai_primary',
        'trust': 50,
    },
    'anthropic_blog': {
        'name': 'Anthropic Blog',
        'feed_url': 'https://www.anthropic.com/rss.xml',
        'min_score': 0,
        'type': 'ai_primary',
        'trust': 50,
    },
    'google_ai': {
        'name': 'Google AI Blog',
        'feed_url': 'https://ai.googleblog.com/feeds/posts/default',
        'min_score': 0,
        'type': 'ai_primary',
        'trust': 48,
    },
    'deepmind': {
        'name': 'DeepMind Blog',
        'feed_url': 'https://deepmind.com/blog/feed/basic/',
        'min_score': 0,
        'type': 'ai_primary',
        'trust': 48,
    },
    'huggingface': {
        'name': 'Hugging Face Blog',
        'feed_url': 'https://huggingface.co/blog/feed.xml',
        'min_score': 0,
        'type': 'ai_primary',
        'trust': 40,
    },

    # --- SECURITY PRIMARY SOURCES ---
    # Krebs and Schneier: gold standard. They publish rarely, always signal.

    'krebs': {
        'name': 'Krebs on Security',
        'feed_url': 'https://krebsonsecurity.com/feed/',
        'min_score': 0,
        'type': 'security_primary',
        'trust': 60,
    },
    'schneier': {
        'name': 'Schneier on Security',
        'feed_url': 'https://www.schneier.com/feed/atom/',
        'min_score': 0,
        'type': 'security_primary',
        'trust': 55,
    },
    'hacker_news_security': {
        'name': 'The Hacker News',
        'feed_url': 'https://feeds.feedburner.com/TheHackersNews',
        'min_score': 0,
        'type': 'security',
        'trust': 30,
    },
    'dark_reading': {
        'name': 'Dark Reading',
        'feed_url': 'https://www.darkreading.com/rss.xml',
        'min_score': 0,
        'type': 'security',
        'trust': 25,
    },

    # --- CROSS-NICHE JOURNALISM ---
    # These cover both AI and Security with real editorial standards.

    'mit_tech_review': {
        'name': 'MIT Technology Review',
        'feed_url': 'https://www.technologyreview.com/feed/',
        'min_score': 0,
        'type': 'journalism',
        'trust': 42,
    },
    'ars_technica': {
        'name': 'Ars Technica',
        'feed_url': 'https://feeds.arstechnica.com/arstechnica/index',
        'min_score': 0,
        'type': 'journalism',
        'trust': 35,
    },

    # --- COMMUNITY AGGREGATOR ---
    # Only viral stories (score >= 300) — the community has already filtered for quality.

    'hackernews': {
        'name': 'Hacker News',
        'feed_url': 'https://hnrss.org/frontpage?count=100',
        'min_score': 300,
        'type': 'aggregator',
        'trust': 0,    # Trust comes from community score, not the source itself
    },
}

# =============================================================================
# SCORING SIGNALS
# =============================================================================

# Recency bonus (hours since published)
RECENCY_BONUS = [
    (6,   30),   # < 6h  → +30
    (24,  15),   # < 24h → +15
    (48,   0),   # < 48h → +0
]
RECENCY_OLD_PENALTY = -20   # > 48h

# Cross-source bonus: same story appears in multiple elite sources
CROSS_SOURCE_BONUS = {
    2: 40,   # 2 sources → +40
    3: 60,   # 3+ sources → +60
}

# Signals that raise quality confidence
QUALITY_SIGNALS = {
    r'(breach|exploit|cve|vulnerab|ransomware|zero.?day|malware)': 30,   # Active threat
    r'(announce|launch|releas|introduc|new model|new version)': 20,       # Launch news
    r'(research|paper|study|experiment|benchmark)': 15,                   # Research
    r'show\s+hn': 20,                                                      # HN Show post
}

# Signals that indicate marketing/noise — penalize hard
NOISE_SIGNALS = {
    r'(webinar|whitepaper|e.?book|case.?study)': -60,
    r'(partner|sponsor|announces.partnership)': -50,
    r'(hiring|job.opening|we.re.looking|join.our.team)': -50,
    r'(free.trial|sign.up.now|register.now|limited.time)': -60,
    r'ask\s+hn': -50,
    r'\[pdf\]': -30,
    r'(rant|opinion|unpopular)': -40,
    r'(years?\s+ago|in\s+20[01]\d)': -40,   # Old content
}
