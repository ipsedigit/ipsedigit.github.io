PUBLISHED_NEWS_FILE_NAME = "news/published.txt"

# =============================================================================
# PUBLISHING STRATEGY
# =============================================================================

MAX_POSTS_PER_NICHE_PER_DAY = 3
DAILY_CATEGORIES_FILE = "news/daily_categories.txt"

# --- Two-pass selection budget ---
MIN_SCORE = 70               # Quality floor (raised from 50)
MIN_SCORE_FALLBACK = 60      # Fallback floor on slow news days
DAILY_TARGET = 12            # Hard cap: max posts per day
DAILY_MINIMUM = 8            # Soft floor: lower quality threshold if below this
MAX_PER_TYPE = 4             # Max posts of one content type per day

# --- Niche category weighting (soft preference, not hard filter) ---
NICHE_CATEGORY_BONUS = 15    # Bonus for preferred niches (AI, Security, Cloud, DevTools, SE)
OTHER_CATEGORY_PENALTY = 0   # No penalty for non-preferred categories (open to all topics)

# Content type detection patterns (checked in priority order by classify_content_type)
CONTENT_TYPE_PATTERNS = {
    'community': [
        r'show\s+hn',
        r'open.?source',
        r'built\s+a\b',
        r'side\s+project',
    ],
    'breaking': [
        r'(announce|launch|releas|introduc)',
        r'(vulnerab|exploit|breach|CVE-|zero.?day)',
        r'(hack|leak|attack|incident)',
    ],
    'deep': [
        r'(paper|arxiv|research|benchmark)',
        r'(how\s+we|architecture|deep\s+dive)',
        r'(tutorial|guide|case\s+study)',
        r'(system\s+design|scalab|pattern)',
    ],
}

# Niche focus: 5 niches for topical authority and SEO
CONTENT_CATEGORIES = {
    'ai': ['ai', 'artificial intelligence', 'machine learning', 'llm', 'gpt', 'chatgpt',
           'openai', 'anthropic', 'claude', 'gemini', 'copilot', 'neural', 'deep learning'],
    'security': ['security', 'hack', 'breach', 'vulnerability', 'privacy', 'encryption',
                 'cyber', 'malware', 'ransomware', 'exploit'],
    'cloud': ['aws', 'amazon web services', 'gcp', 'google cloud', 'azure', 'kubernetes',
              'k8s', 'docker', 'container', 'terraform', 'serverless', 'lambda', 'cloud-native',
              'cloud native', 'iaas', 'paas', 'saas', 'devops', 'infrastructure as code'],
    'devtools': ['framework', 'ide', 'vscode', 'jetbrains', 'neovim', 'compiler', 'linter',
                 'package manager', 'npm', 'cargo', 'pip', 'sdk', 'cli tool', 'debugger',
                 'developer tool', 'dev tool', 'developer experience', 'dx', 'monorepo',
                 'webpack', 'vite', 'eslint', 'prettier', 'formatter'],
    'software-engineering': ['architecture', 'design pattern', 'microservice', 'system design',
                             'distributed system', 'event-driven', 'domain driven', 'ddd',
                             'cqrs', 'event sourcing', 'technical debt', 'refactor', 'clean code',
                             'solid principle', 'api design', 'scalability', 'observability',
                             'circuit breaker', 'saga pattern'],
}

# Niche categories — ordered list for scheduling rotation
NICHE_CATEGORIES = ['ai', 'software-engineering', 'devtools', 'cloud', 'security']

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

CLOUD_SUBNICHES = {
    'aws': ['aws', 'amazon web services', 's3', 'ec2', 'lambda', 'ecs', 'eks', 'fargate',
            'cloudformation', 'sagemaker', 'dynamodb', 'iam', 'vpc'],
    'gcp-azure': ['gcp', 'google cloud', 'azure', 'bigquery', 'cloud run', 'cloud functions',
                  'app engine', 'azure devops', 'cosmos db'],
    'kubernetes': ['kubernetes', 'k8s', 'helm', 'istio', 'service mesh', 'kubectl', 'operator',
                   'pod', 'ingress', 'kustomize', 'argocd'],
    'serverless': ['serverless', 'lambda', 'cloud functions', 'edge computing', 'edge function',
                   'vercel', 'netlify', 'cloudflare workers', 'faas'],
    'networking-iaas': ['terraform', 'pulumi', 'ansible', 'vpc', 'load balancer', 'cdn',
                        'dns', 'proxy', 'api gateway', 'infrastructure as code', 'iac'],
}

DEVTOOLS_SUBNICHES = {
    'frameworks': ['react', 'next.js', 'vue', 'svelte', 'angular', 'django', 'flask', 'fastapi',
                   'spring', 'rails', 'express', 'nest.js', 'htmx', 'astro'],
    'languages': ['python', 'rust', 'go', 'typescript', 'kotlin', 'swift', 'zig', 'elixir',
                  'java', 'c++', 'c#', 'ruby', 'scala', 'haskell'],
    'ides-editors': ['vscode', 'jetbrains', 'intellij', 'neovim', 'vim', 'emacs', 'zed',
                     'cursor', 'sublime', 'helix'],
    'cicd': ['ci/cd', 'github actions', 'gitlab ci', 'jenkins', 'circleci', 'buildkite',
             'drone', 'tekton', 'pipeline', 'continuous integration', 'continuous delivery'],
    'package-managers': ['npm', 'yarn', 'pnpm', 'pip', 'poetry', 'cargo', 'gradle', 'maven',
                         'bun', 'deno', 'homebrew', 'apt', 'nix'],
}

SE_SUBNICHES = {
    'architecture': ['architecture', 'microservice', 'monolith', 'event-driven', 'hexagonal',
                     'clean architecture', 'layered', 'modular', 'domain driven', 'ddd'],
    'design-patterns': ['design pattern', 'factory', 'singleton', 'observer', 'strategy',
                        'adapter', 'decorator', 'repository pattern', 'cqrs', 'event sourcing',
                        'saga pattern', 'circuit breaker'],
    'methodologies': ['agile', 'scrum', 'kanban', 'tdd', 'bdd', 'extreme programming', 'xp',
                      'pair programming', 'mob programming', 'code review', 'sprint'],
    'api-design': ['api design', 'rest', 'graphql', 'grpc', 'openapi', 'swagger', 'webhook',
                   'websocket', 'api gateway', 'rate limiting', 'pagination', 'versioning'],
    'performance': ['performance', 'scalability', 'caching', 'load testing', 'profiling',
                    'latency', 'throughput', 'optimization', 'benchmark', 'concurrency'],
}

NICHE_SUBNICHES = {
    'ai': AI_SUBNICHES,
    'security': SECURITY_SUBNICHES,
    'cloud': CLOUD_SUBNICHES,
    'devtools': DEVTOOLS_SUBNICHES,
    'software-engineering': SE_SUBNICHES,
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
    'techcrunch': {
        'name': 'TechCrunch',
        'feed_url': 'https://techcrunch.com/feed/',
        'min_score': 0,
        'type': 'news',
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
    'threatpost': {
        'name': 'Threatpost',
        'feed_url': 'https://threatpost.com/feed/',
        'min_score': 0,
        'type': 'security',
    },
    'bleepingcomputer': {
        'name': 'BleepingComputer',
        'feed_url': 'https://www.bleepingcomputer.com/feed/',
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

    # --- TIER 7: Cloud & Infrastructure ---
    'thenewstack': {
        'name': 'The New Stack',
        'feed_url': 'https://thenewstack.io/feed/',
        'min_score': 0,
        'type': 'cloud_news',
    },
    'devops_com': {
        'name': 'DevOps.com',
        'feed_url': 'https://devops.com/feed/',
        'min_score': 0,
        'type': 'cloud_news',
    },
    'hashicorp': {
        'name': 'HashiCorp Blog',
        'feed_url': 'https://www.hashicorp.com/blog/feed.xml',
        'min_score': 0,
        'type': 'corporate_blog',
    },
    'docker_blog': {
        'name': 'Docker Blog',
        'feed_url': 'https://www.docker.com/blog/feed/',
        'min_score': 0,
        'type': 'corporate_blog',
    },
    'k8s_blog': {
        'name': 'Kubernetes Blog',
        'feed_url': 'https://kubernetes.io/feed.xml',
        'min_score': 0,
        'type': 'corporate_blog',
    },
    'datadoghq_blog': {
        'name': 'Datadog Blog',
        'feed_url': 'https://www.datadoghq.com/blog/feed/',
        'min_score': 0,
        'type': 'corporate_blog',
    },
    'vercel_blog': {
        'name': 'Vercel Blog',
        'feed_url': 'https://vercel.com/blog/feed',
        'min_score': 0,
        'type': 'corporate_blog',
    },
    'planetscale_blog': {
        'name': 'PlanetScale Blog',
        'feed_url': 'https://planetscale.com/blog/feed',
        'min_score': 0,
        'type': 'corporate_blog',
    },
    'tailscale_blog': {
        'name': 'Tailscale Blog',
        'feed_url': 'https://tailscale.com/blog/feed/',
        'min_score': 0,
        'type': 'corporate_blog',
    },
    'flyio_blog': {
        'name': 'Fly.io Blog',
        'feed_url': 'https://fly.io/blog/feed',
        'min_score': 0,
        'type': 'corporate_blog',
    },

    # --- TIER 8: DevTools & Software Engineering ---
    'infoworld': {
        'name': 'InfoWorld',
        'feed_url': 'https://www.infoworld.com/feed/',
        'min_score': 0,
        'type': 'news',
    },
    'devto': {
        'name': 'dev.to',
        'feed_url': 'https://dev.to/feed',
        'min_score': 0,
        'type': 'community',
    },
    'martinfowler': {
        'name': 'Martin Fowler',
        'feed_url': 'https://martinfowler.com/feed.atom',
        'min_score': 0,
        'type': 'se_blog',
    },
    'pragmatic_eng': {
        'name': 'The Pragmatic Engineer',
        'feed_url': 'https://newsletter.pragmaticengineer.com/feed',
        'min_score': 0,
        'type': 'se_blog',
        'score_boost': 20,
    },

    # --- TIER 9: Devs — personal blogs by individual developers ---
    'juliaevans': {
        'name': 'Julia Evans',
        'feed_url': 'https://jvns.ca/atom.xml',
        'url': 'https://jvns.ca/blog',
        'min_score': 0,
        'type': 'creator',
    },
    'danluu': {
        'name': 'Dan Luu',
        'feed_url': 'https://danluu.com/atom.xml',
        'url': 'https://danluu.com',
        'min_score': 0,
        'type': 'creator',
    },
    'computerenhance': {
        'name': 'Computer, Enhance!',
        'feed_url': 'https://computerenhance.com/feed',
        'url': 'https://computerenhance.com',
        'min_score': 0,
        'type': 'creator',
    },
    'seangoedecke': {
        'name': 'Sean Goedecke',
        'feed_url': 'https://seangoedecke.com/rss.xml',
        'url': 'https://seangoedecke.com',
        'min_score': 0,
        'type': 'creator',
    },
    'marcbrooker': {
        'name': 'Marc Brooker',
        'feed_url': 'https://brooker.co.za/blog/rss.xml',
        'url': 'https://brooker.co.za/blog',
        'min_score': 0,
        'type': 'creator',
    },
    'rachelbythebay': {
        'name': 'Rachel by the Bay',
        'feed_url': 'https://rachelbythebay.com/w/feed/',
        'url': 'https://rachelbythebay.com/w',
        'min_score': 0,
        'type': 'creator',
    },
    'nullprogram': {
        'name': 'Chris Wellons',
        'feed_url': 'https://nullprogram.com/feed/',
        'url': 'https://nullprogram.com',
        'min_score': 0,
        'type': 'creator',
    },
    'arminronacher': {
        'name': 'Armin Ronacher',
        'feed_url': 'https://lucumr.pocoo.org/feed.atom',
        'url': 'https://lucumr.pocoo.org',
        'min_score': 0,
        'type': 'creator',
    },
    'mitchellhashimoto': {
        'name': 'Mitchell Hashimoto',
        'feed_url': 'https://mitchellh.com/feed.xml',
        'url': 'https://mitchellh.com',
        'min_score': 0,
        'type': 'creator',
    },
    'drewdevault': {
        'name': 'Drew DeVault',
        'feed_url': 'https://drewdevault.com/blog/index.xml',
        'url': 'https://drewdevault.com',
        'min_score': 0,
        'type': 'creator',
    },
    'antirez': {
        'name': 'Antirez',
        'feed_url': 'https://antirez.com/rss',
        'url': 'https://antirez.com',
        'min_score': 0,
        'type': 'creator',
    },
    'cryptographyengineering': {
        'name': 'Matthew Green',
        'feed_url': 'https://blog.cryptographyengineering.com/feed/',
        'url': 'https://blog.cryptographyengineering.com',
        'min_score': 0,
        'type': 'creator',
    },
    'jessfraz': {
        'name': 'Jessie Frazelle',
        'feed_url': 'https://blog.jessfraz.com/index.xml',
        'url': 'https://blog.jessfraz.com',
        'min_score': 0,
        'type': 'creator',
    },
    'kenshire': {
        'name': 'Ken Shirriff',
        'feed_url': 'https://www.righto.com/feeds/posts/default',
        'url': 'https://righto.com',
        'min_score': 0,
        'type': 'creator',
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
    r'(kubernetes|k8s|docker|container|cloud)': 25,    # Cloud & infrastructure
    r'(framework|library|sdk|release|v\d)': 20,        # DevTools signal
    r'(architecture|system design|scalab|pattern)': 20, # Software engineering
}

TITLE_PENALTY = {
    r'ask\s+hn': -50,
    r'\[pdf\]': -30,
    r'(nytimes|wsj|bloomberg)\.com': -100,
    r'(rant|opinion|unpopular)': -40,
    r'(years?\s+ago|in\s+20[01]\d)': -50,
    r'\d+\s*(ways|tips|reasons|things)\s': -10,        # Listicle SEO bait
}
