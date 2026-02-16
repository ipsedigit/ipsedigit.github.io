PUBLISHED_NEWS_FILE_NAME = "news/published.txt"

# =============================================================================
# PUBLISHING STRATEGY: Quanti post al giorno e come distribuirli
# =============================================================================

# Numero massimo di post al giorno
MAX_POSTS_PER_DAY = 3

# Categorie principali - ogni post giornaliero deve essere di categoria diversa
# Questo evita cannibalizzazione SEO e diversifica l'audience
CONTENT_CATEGORIES = {
    'ai': {
        'name': 'AI & Machine Learning',
        'keywords': ['ai', 'artificial intelligence', 'machine learning', 'llm', 'gpt', 'chatgpt',
                     'openai', 'anthropic', 'claude', 'gemini', 'copilot', 'neural', 'deep learning'],
        'priority': 1,  # Alta priorità - topic trending
    },
    'dev': {
        'name': 'Programming & Development',
        'keywords': ['python', 'rust', 'golang', 'javascript', 'typescript', 'react', 'java',
                     'kotlin', 'programming', 'developer', 'coding', 'software'],
        'priority': 2,
    },
    'infra': {
        'name': 'Infrastructure & DevOps',
        'keywords': ['kubernetes', 'docker', 'aws', 'cloud', 'devops', 'terraform', 'linux',
                     'serverless', 'microservices', 'database', 'postgresql', 'redis'],
        'priority': 2,
    },
    'security': {
        'name': 'Security & Privacy',
        'keywords': ['security', 'hack', 'breach', 'vulnerability', 'privacy', 'encryption',
                     'cyber', 'malware', 'ransomware'],
        'priority': 3,  # Alta viralità
    },
    'startup': {
        'name': 'Startups & Business',
        'keywords': ['startup', 'funding', 'raised', 'billion', 'acquisition', 'ipo', 'venture'],
        'priority': 3,
    },
}

# File per tracciare le categorie già pubblicate oggi
DAILY_CATEGORIES_FILE = "news/daily_categories.txt"

# =============================================================================
# NEWS SOURCES: Sorgenti autorevoli per tech news
# =============================================================================

NEWS_SOURCES = {
    # --- TIER 1: Aggregatori tech (alto volume, validazione community) ---
    'hackernews': {
        'name': 'Hacker News',
        'feed_url': 'https://hnrss.org/frontpage?count=100',
        'weight': 30,  # Probabilità selezione (%)
        'authority': 90,
        'type': 'aggregator',
    },
    'lobsters': {
        'name': 'Lobste.rs',
        'feed_url': 'https://lobste.rs/rss',
        'weight': 15,
        'authority': 85,
        'type': 'aggregator',
    },

    # --- TIER 2: Blog tech aziendali (contenuti originali, alta qualità) ---
    'github_blog': {
        'name': 'GitHub Blog',
        'feed_url': 'https://github.blog/feed/',
        'weight': 10,
        'authority': 95,
        'type': 'corporate_blog',
    },
    'netflix_tech': {
        'name': 'Netflix Tech Blog',
        'feed_url': 'https://netflixtechblog.com/feed',
        'weight': 8,
        'authority': 90,
        'type': 'corporate_blog',
    },
    'cloudflare_blog': {
        'name': 'Cloudflare Blog',
        'feed_url': 'https://blog.cloudflare.com/rss/',
        'weight': 8,
        'authority': 90,
        'type': 'corporate_blog',
    },
    'uber_eng': {
        'name': 'Uber Engineering',
        'feed_url': 'https://eng.uber.com/feed/',
        'weight': 5,
        'authority': 85,
        'type': 'corporate_blog',
    },

    # --- TIER 3: News tech mainstream (alto reach, SEO boost) ---
    'ars_technica': {
        'name': 'Ars Technica',
        'feed_url': 'https://feeds.arstechnica.com/arstechnica/technology-lab',
        'weight': 8,
        'authority': 88,
        'type': 'news',
    },
    'the_verge': {
        'name': 'The Verge',
        'feed_url': 'https://www.theverge.com/rss/index.xml',
        'weight': 6,
        'authority': 85,
        'type': 'news',
    },
    'techcrunch': {
        'name': 'TechCrunch',
        'feed_url': 'https://techcrunch.com/feed/',
        'weight': 5,
        'authority': 85,
        'type': 'news',
    },

    # --- TIER 4: Dev/Programming focused ---
    'dev_to': {
        'name': 'DEV Community',
        'feed_url': 'https://dev.to/feed',
        'weight': 5,
        'authority': 75,
        'type': 'community',
    },
}

# Calcolo automatico: i pesi devono sommare a 100
_total_weight = sum(s['weight'] for s in NEWS_SOURCES.values())
for source in NEWS_SOURCES.values():
    source['normalized_weight'] = source['weight'] / _total_weight * 100

# =============================================================================
# MARKET STRATEGY: Selezione post per massimizzare traffico organico
# =============================================================================

# Soglia minima HN score - post sotto questa soglia sono ignorati
MIN_HN_SCORE = 50

# -----------------------------------------------------------------------------
# TIER 1: Topic ad alto volume di ricerca (Google Trends + keyword research)
# Questi topic hanno volume di ricerca mensile elevato
# -----------------------------------------------------------------------------
HIGH_VOLUME_TOPICS = {
    # AI/ML - Volume altissimo, competizione alta ma traffico garantito
    'chatgpt': 80,
    'openai': 70,
    'gpt-4': 70,
    'gpt-5': 90,      # Nuove release = picchi di ricerca
    'claude': 60,
    'gemini': 65,
    'llama': 50,
    'copilot': 60,
    'midjourney': 55,
    'stable diffusion': 50,
    'sora': 70,       # Video AI molto cercato

    # Big Tech - Sempre alto interesse
    'apple': 40,
    'google': 40,
    'microsoft': 40,
    'amazon': 35,
    'meta': 35,
    'tesla': 50,
    'nvidia': 60,     # AI hardware = molto cercato

    # Programming trending
    'rust': 45,
    'golang': 40,
    'python': 35,
    'typescript': 35,
    'react': 30,
    'nextjs': 35,
}

# -----------------------------------------------------------------------------
# TIER 2: Pattern titoli ad alta conversione (CTR optimization)
# Basati su analisi di headline che generano più click
# -----------------------------------------------------------------------------
HIGH_CTR_PATTERNS = [
    # Numeri = +30% CTR medio
    (r'^\d+\s', 25),
    (r'\d+\s*(ways|tips|tricks|reasons|things)', 30),

    # How-to = Intent informazionale, alto tempo su pagina
    (r'how\s+to\s+', 35),
    (r'guide\s+to', 30),
    (r'tutorial', 25),

    # Controversy/Drama = Viralità sociale
    (r'(is\s+dead|is\s+dying|killed|will\s+kill)', 40),
    (r'(why\s+i\s+quit|why\s+i\s+left|i\s+quit)', 45),
    (r'(controversy|scandal|fired|lawsuit)', 35),

    # Breaking/News = Urgenza
    (r'(breaking|just\s+announced|announces|launched|releases)', 40),
    (r'(new|introducing|meet\s+the)', 20),

    # Money/Success = Aspirazionale
    (r'(\$\d|million|billion|raised|funding|valuation)', 35),
    (r'(salary|earning|made\s+\$)', 40),

    # Fear/Security = Alto engagement
    (r'(hack|breach|leak|vulnerability|exploit)', 45),
    (r'(warning|danger|risk|threat)', 35),

    # Show HN = Contenuto originale, bassa competizione SEO
    (r'show\s+hn', 50),

    # Comparison = Alto intent commerciale
    (r'\s+vs\.?\s+', 30),
    (r'(compared|comparison|better\s+than|alternative)', 25),
]

# -----------------------------------------------------------------------------
# TIER 3: Penalità - Contenuti da evitare
# -----------------------------------------------------------------------------
PENALTY_PATTERNS = [
    # Contenuti che non generano traffico organico
    (r'ask\s+hn', -30),           # Discussioni senza valore SEO
    (r'(rant|complaint|frustrated)', -25),
    (r'(opinion|unpopular)', -20),

    # Paywall/Inaccessibili
    (r'(nytimes|wsj|bloomberg)\.com', -40),
    (r'\[pdf\]', -20),

    # Troppo di nicchia
    (r'(emacs|vim|neovim)\s', -15),  # Basso volume

    # Vecchio/Datato
    (r'(years?\s+ago|in\s+20[01]\d)', -30),
]

# -----------------------------------------------------------------------------
# TIER 4: Bonus temporali - Cavalcare i trend
# -----------------------------------------------------------------------------
TEMPORAL_BONUS = {
    # Giorni della settimana (lunedì = più traffico)
    'monday': 15,
    'tuesday': 10,
    'wednesday': 5,
    'thursday': 0,
    'friday': -5,
    'saturday': -15,
    'sunday': -10,
}

# Peso dei vari fattori nello score finale
WEIGHTS = {
    'hn_score': 0.25,        # Popolarità HN
    'topic_volume': 0.30,    # Volume ricerca keyword
    'ctr_pattern': 0.25,     # Pattern titolo
    'freshness': 0.10,       # Freschezza contenuto
    'image_bonus': 0.10,     # Ha immagine preview
}

