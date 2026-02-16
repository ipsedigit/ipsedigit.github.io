PUBLISHED_NEWS_FILE_NAME = "news/published.txt"

# =============================================================================
# PUBLISHING STRATEGY
# =============================================================================

MAX_POSTS_PER_DAY = 5
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
# NEWS SOURCES - 50 Authoritative Tech Sources
# =============================================================================

NEWS_SOURCES = {
    # --- TIER 1: Aggregators (community-validated) ---
    'hackernews': {
        'name': 'Hacker News',
        'feed_url': 'https://hnrss.org/frontpage?count=100',
        'min_score': 100,
        'type': 'aggregator',
    },
    'lobsters': {
        'name': 'Lobste.rs',
        'feed_url': 'https://lobste.rs/rss',
        'min_score': 20,
        'type': 'aggregator',
    },
    'slashdot': {
        'name': 'Slashdot',
        'feed_url': 'https://rss.slashdot.org/Slashdot/slashdotMain',
        'min_score': 0,
        'type': 'aggregator',
    },

    # --- TIER 2: Big Tech Engineering Blogs (original content) ---
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

    # --- TIER 3: Tech News (mainstream, high reach) ---
    'ars_technica': {
        'name': 'Ars Technica',
        'feed_url': 'https://feeds.arstechnica.com/arstechnica/index',
        'min_score': 0,
        'type': 'news',
    },
    'the_verge': {
        'name': 'The Verge',
        'feed_url': 'https://www.theverge.com/rss/index.xml',
        'min_score': 0,
        'type': 'news',
    },
    'techcrunch': {
        'name': 'TechCrunch',
        'feed_url': 'https://techcrunch.com/feed/',
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
    'zdnet': {
        'name': 'ZDNet',
        'feed_url': 'https://www.zdnet.com/news/rss.xml',
        'min_score': 0,
        'type': 'news',
    },
    'venturebeat': {
        'name': 'VentureBeat',
        'feed_url': 'https://venturebeat.com/feed/',
        'min_score': 0,
        'type': 'news',
    },
    'the_register': {
        'name': 'The Register',
        'feed_url': 'https://www.theregister.com/headlines.atom',
        'min_score': 0,
        'type': 'news',
    },
    'engadget': {
        'name': 'Engadget',
        'feed_url': 'https://www.engadget.com/rss.xml',
        'min_score': 0,
        'type': 'news',
    },

    # --- TIER 4: AI/ML Specific ---
    'openai_blog': {
        'name': 'OpenAI Blog',
        'feed_url': 'https://openai.com/blog/rss/',
        'min_score': 0,
        'type': 'corporate_blog',
    },
    'google_ai': {
        'name': 'Google AI Blog',
        'feed_url': 'https://ai.googleblog.com/feeds/posts/default',
        'min_score': 0,
        'type': 'corporate_blog',
    },
    'deepmind': {
        'name': 'DeepMind Blog',
        'feed_url': 'https://deepmind.com/blog/feed/basic/',
        'min_score': 0,
        'type': 'corporate_blog',
    },
    'huggingface': {
        'name': 'Hugging Face Blog',
        'feed_url': 'https://huggingface.co/blog/feed.xml',
        'min_score': 0,
        'type': 'corporate_blog',
    },

    # --- TIER 5: Developer/Programming ---
    'dev_to': {
        'name': 'DEV Community',
        'feed_url': 'https://dev.to/feed',
        'min_score': 0,
        'type': 'community',
    },
    'freecodecamp': {
        'name': 'freeCodeCamp',
        'feed_url': 'https://www.freecodecamp.org/news/rss/',
        'min_score': 0,
        'type': 'community',
    },
    'css_tricks': {
        'name': 'CSS-Tricks',
        'feed_url': 'https://css-tricks.com/feed/',
        'min_score': 0,
        'type': 'community',
    },
    'smashing_mag': {
        'name': 'Smashing Magazine',
        'feed_url': 'https://www.smashingmagazine.com/feed/',
        'min_score': 0,
        'type': 'community',
    },
    'infoq': {
        'name': 'InfoQ',
        'feed_url': 'https://www.infoq.com/feed/',
        'min_score': 0,
        'type': 'community',
    },

    # --- TIER 6: Security ---
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

    # --- TIER 7: Startup/Business ---
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

# Bonus per pattern nel titolo
TITLE_BONUS = {
    r'^\d+\s': 20,
    r'\d+\s*(ways|tips|reasons|things)': 25,
    r'how\s+to\s+': 30,
    r'guide|tutorial': 25,
    r'(announce|launch|releas|introduc)': 30,
    r'show\s+hn': 35,
    r'(is\s+dead|killed|quit|fired|layoff)': 35,
    r'(hack|breach|vulnerab|exploit|leak)': 40,
    r'(\$\d|million|billion|raised|funding)': 30,
}

# Penalità
TITLE_PENALTY = {
    r'ask\s+hn': -50,
    r'\[pdf\]': -30,
    r'(nytimes|wsj|bloomberg)\.com': -100,
    r'(rant|opinion|unpopular)': -40,
    r'(years?\s+ago|in\s+20[01]\d)': -50,
}
