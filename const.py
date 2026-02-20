PUBLISHED_NEWS_FILE_NAME = "news/published.txt"

# =============================================================================
# PUBLISHING STRATEGY
# =============================================================================

MAX_POSTS_PER_DAY = 3
DAILY_CATEGORIES_FILE = "news/daily_categories.txt"

# Niche focus: AI + Security for topical authority and SEO
CONTENT_CATEGORIES = {
    'ai': ['ai', 'artificial intelligence', 'machine learning', 'llm', 'gpt', 'chatgpt',
           'openai', 'anthropic', 'claude', 'gemini', 'copilot', 'neural', 'deep learning'],
    'security': ['security', 'hack', 'breach', 'vulnerability', 'privacy', 'encryption',
                 'cyber', 'malware', 'ransomware', 'exploit'],
}

# Niche categories — only these are accepted for publishing
NICHE_CATEGORIES = {'ai', 'security'}

# Sub-niches for AI
AI_SUBNICHES = {
    'llm': ['llm', 'large language model', 'gpt', 'chatgpt', 'claude', 'gemini', 'mistral',
            'prompt', 'rag', 'fine-tun', 'retrieval augmented', 'instruction tuning',
            'context window', 'token', 'llama'],
    'ai-research': ['paper', 'arxiv', 'research', 'benchmark', 'dataset', 'model architecture',
                    'transformer', 'diffusion', 'deepmind', 'multimodal', 'reasoning',
                    'alignment', 'computer vision', 'nlp'],
    'ai-infrastructure': ['inference', 'training', 'gpu', 'tpu', 'mlops', 'model serving',
                          'vllm', 'triton', 'cuda', 'distributed training', 'embeddings',
                          'vector database', 'feature store', 'quantization'],
    'mlops': ['mlflow', 'kubeflow', 'mlops', 'model registry', 'pipeline', 'drift',
              'deployment', 'production', 'monitoring'],
}

# Sub-niches for Security
SECURITY_SUBNICHES = {
    'appsec': ['xss', 'sql injection', 'csrf', 'owasp', 'web security', 'application security',
               'appsec', 'sast', 'dast', 'pen test', 'bug bounty', 'injection'],
    'threat-intel': ['threat intelligence', 'apt', 'nation state', 'campaign', 'ioc', 'ttps',
                     'mitre', 'attack pattern', 'threat actor', 'espionage'],
    'malware': ['malware', 'ransomware', 'trojan', 'botnet', 'backdoor', 'rootkit', 'spyware',
                'worm', 'virus', 'payload'],
    'cryptography': ['encryption', 'cryptography', 'cipher', 'tls', 'ssl', 'certificate',
                     'pki', 'zero knowledge', 'post quantum', 'key management'],
    'vulnerability': ['cve', 'zero-day', '0day', 'exploit', 'patch', 'disclosure', 'poc',
                      'rce', 'privilege escalation', 'memory corruption'],
}

# =============================================================================
# NEWS SOURCES — Curated primary sources (signal > volume)
# =============================================================================

NEWS_SOURCES = {
    # --- TIER 1: Aggregators (community-validated signal) ---
    'hackernews': {
        'name': 'Hacker News',
        'feed_url': 'https://hnrss.org/frontpage?count=100',
        'min_score': 150,
        'type': 'aggregator',
    },
    'lobsters': {
        'name': 'Lobste.rs',
        'feed_url': 'https://lobste.rs/rss',
        'min_score': 20,
        'type': 'aggregator',
    },

    # --- TIER 2: Big Tech Engineering Blogs (original, primary-source content) ---
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
    'uber_eng': {
        'name': 'Uber Engineering',
        'feed_url': 'https://www.uber.com/blog/engineering/rss/',
        'min_score': 0,
        'type': 'corporate_blog',
    },
    'stripe_blog': {
        'name': 'Stripe Blog',
        'feed_url': 'https://stripe.com/blog/feed.rss',
        'min_score': 0,
        'type': 'corporate_blog',
    },
    'airbnb_eng': {
        'name': 'Airbnb Engineering',
        'feed_url': 'https://medium.com/feed/airbnb-engineering',
        'min_score': 0,
        'type': 'corporate_blog',
    },
    'spotify_eng': {
        'name': 'Spotify Engineering',
        'feed_url': 'https://engineering.atspotify.com/feed/',
        'min_score': 0,
        'type': 'corporate_blog',
    },
    'linkedin_eng': {
        'name': 'LinkedIn Engineering',
        'feed_url': 'https://engineering.linkedin.com/blog.rss',
        'min_score': 0,
        'type': 'corporate_blog',
    },
    'meta_eng': {
        'name': 'Meta Engineering',
        'feed_url': 'https://engineering.fb.com/feed/',
        'min_score': 0,
        'type': 'corporate_blog',
    },
    'google_dev': {
        'name': 'Google Developers',
        'feed_url': 'https://developers.googleblog.com/feeds/posts/default',
        'min_score': 0,
        'type': 'corporate_blog',
    },
    'aws_blog': {
        'name': 'AWS Blog',
        'feed_url': 'https://aws.amazon.com/blogs/aws/feed/',
        'min_score': 0,
        'type': 'corporate_blog',
    },
    'microsoft_dev': {
        'name': 'Microsoft DevBlogs',
        'feed_url': 'https://devblogs.microsoft.com/feed/',
        'min_score': 0,
        'type': 'corporate_blog',
    },
    'dropbox_tech': {
        'name': 'Dropbox Tech',
        'feed_url': 'https://dropbox.tech/feed',
        'min_score': 0,
        'type': 'corporate_blog',
    },
    'slack_eng': {
        'name': 'Slack Engineering',
        'feed_url': 'https://slack.engineering/feed/',
        'min_score': 0,
        'type': 'corporate_blog',
    },
    'pinterest_eng': {
        'name': 'Pinterest Engineering',
        'feed_url': 'https://medium.com/feed/pinterest-engineering',
        'min_score': 0,
        'type': 'corporate_blog',
    },
    'shopify_eng': {
        'name': 'Shopify Engineering',
        'feed_url': 'https://shopify.engineering/blog.atom',
        'min_score': 0,
        'type': 'corporate_blog',
    },

    # --- TIER 3: Curated Tech Press (technical depth, not consumer news) ---
    'ars_technica': {
        'name': 'Ars Technica',
        'feed_url': 'https://feeds.arstechnica.com/arstechnica/index',
        'min_score': 0,
        'type': 'news',
    },
    'wired': {
        'name': 'Wired',
        'feed_url': 'https://www.wired.com/feed/rss',
        'min_score': 0,
        'type': 'news',
    },
    'mit_tech_review': {
        'name': 'MIT Technology Review',
        'feed_url': 'https://www.technologyreview.com/feed/',
        'min_score': 0,
        'type': 'news',
    },
    'the_register': {
        'name': 'The Register',
        'feed_url': 'https://www.theregister.com/headlines.atom',
        'min_score': 0,
        'type': 'news',
    },
    'infoq': {
        'name': 'InfoQ',
        'feed_url': 'https://www.infoq.com/feed/',
        'min_score': 0,
        'type': 'community',
    },

    # --- TIER 4: AI/ML Research Blogs (primary-source research content) ---
    'openai_blog': {
        'name': 'OpenAI Blog',
        'feed_url': 'https://openai.com/blog/rss/',
        'min_score': 0,
        'type': 'research_blog',
    },
    'google_ai': {
        'name': 'Google AI Blog',
        'feed_url': 'https://ai.googleblog.com/feeds/posts/default',
        'min_score': 0,
        'type': 'research_blog',
    },
    'deepmind': {
        'name': 'DeepMind Blog',
        'feed_url': 'https://deepmind.com/blog/feed/basic/',
        'min_score': 0,
        'type': 'research_blog',
    },
    'huggingface': {
        'name': 'Hugging Face Blog',
        'feed_url': 'https://huggingface.co/blog/feed.xml',
        'min_score': 0,
        'type': 'research_blog',
    },

    # --- TIER 5: Security (specialist, practitioner-focused) ---
    'krebs': {
        'name': 'Krebs on Security',
        'feed_url': 'https://krebsonsecurity.com/feed/',
        'min_score': 0,
        'type': 'security',
    },
    'hacker_news_security': {
        'name': 'The Hacker News',
        'feed_url': 'https://feeds.feedburner.com/TheHackersNews',
        'min_score': 0,
        'type': 'security',
    },
    'schneier': {
        'name': 'Schneier on Security',
        'feed_url': 'https://www.schneier.com/feed/atom/',
        'min_score': 0,
        'type': 'security',
    },
    'dark_reading': {
        'name': 'Dark Reading',
        'feed_url': 'https://www.darkreading.com/rss.xml',
        'min_score': 0,
        'type': 'security',
    },

    # --- TIER 6: Startup/Practitioner Insight ---
    'yc_blog': {
        'name': 'Y Combinator Blog',
        'feed_url': 'https://www.ycombinator.com/blog.rss',
        'min_score': 0,
        'type': 'startup',
    },
    'first_round': {
        'name': 'First Round Review',
        'feed_url': 'https://review.firstround.com/feed.xml',
        'min_score': 0,
        'type': 'startup',
    },
}

# =============================================================================
# SCORING
# =============================================================================

TITLE_BONUS = {
    r'(announce|launch|releas|introduc)': 30,          # Primary announcements
    r'(paper|arxiv|research|benchmark|study)': 20,     # Research signal
    r'how\s+to\s+': 15,                                # Practical guides
    r'guide|tutorial': 15,                             # Tutorials
    r'show\s+hn': 35,                                  # Community-built projects
    r'(hack|breach|vulnerab|exploit|leak)': 40,        # Strong security signal
}

TITLE_PENALTY = {
    r'ask\s+hn': -50,
    r'\[pdf\]': -30,
    r'(nytimes|wsj|bloomberg)\.com': -100,
    r'(rant|opinion|unpopular)': -40,
    r'(years?\s+ago|in\s+20[01]\d)': -50,
    r'\d+\s*(ways|tips|reasons|things)\s': -10,        # Listicle SEO bait
}
