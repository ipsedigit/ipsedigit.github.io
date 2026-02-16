PUBLISHED_NEWS_FILE_NAME = "news/published.txt"
PUBLISHED_QUOTES_FILE_NAME = "quotes/published.txt"
QUOTES_FILE_NAME = "quotes/quotes.json"

# Fetch più post per avere più scelta
HACKERNEWS_FEED_URL = "https://hnrss.org/frontpage?count=100"

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

