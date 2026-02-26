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
        'type': 'creator',
    },
    'bytebytego': {
        'name': 'ByteByteGo',
        'feed_url': 'https://blog.bytebytego.com/feed',
        'min_score': 0,
        'type': 'se_blog',
    },

    # --- TIER 9: Creators & newsletters (indie, Substack, Buttondown — reach individuals) ---
    'softwarearchitectureweekly': {
        'name': 'Software Architecture Weekly',
        'feed_url': 'https://softwarearchitectureweekly.substack.com/feed',
        'min_score': 0,
        'type': 'creator',
    },
    # Indie: personal blogs and small/solo Substacks
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
    'strlen': {
        'name': "Schopenhauer's Kubernetes cluster",
        'feed_url': 'https://strlen.substack.com/feed',
        'url': 'https://strlen.substack.com',
        'min_score': 0,
        'type': 'creator',
    },
    'indiedeveloperdiaries': {
        'name': 'Indie Developer Diaries',
        'feed_url': 'https://indiedeveloperdiaries.substack.com/feed',
        'min_score': 0,
        'type': 'creator',
    },
    'howtech': {
        'name': 'How Tech',
        'feed_url': 'https://howtech.substack.com/feed',
        'min_score': 0,
        'type': 'creator',
    },
}

# =============================================================================
# REFERENCE LIST — One resource per developer (blog homepage)
# =============================================================================
# Source: outcoldman/hackernews-personal-blogs (list.opml). Refresh: run
#   python refresh_direct_from_hn_opml.py
# then paste output here. Update site: python main.py --action direct

DIRECT_REFERENCE_LIST = [
    {'name': 'jgrahamc', 'url': 'https://blog.jgc.org', 'description': 'Personal blog (HN).'},
    {'name': 'jseliger', 'url': 'https://jakeseliger.com', 'description': 'Personal blog (HN).'},
    {'name': 'mooreds', 'url': 'https://letterstoanewdeveloper.com', 'description': 'Personal blog (HN).'},
    {'name': 'stavros', 'url': 'https://feeds.feedburner.com/stavrosstuff', 'description': 'Personal blog (HN).'},
    {'name': 'bookofjoe', 'url': 'https://www.bookofjoe.com', 'description': 'Personal blog (HN).'},
    {'name': 'fogus', 'url': 'https://blog.fogus.me', 'description': 'Personal blog (HN).'},
    {'name': 'lisper', 'url': 'https://blog.rongarret.info', 'description': 'Personal blog (HN).'},
    {'name': 'mpweiher', 'url': 'https://blog.metaobject.com', 'description': 'Personal blog (HN).'},
    {'name': 'feross', 'url': 'https://feross.org', 'description': 'Personal blog (HN).'},
    {'name': 'giuliomagnifico', 'url': 'http://giuliomagnifico.blog', 'description': 'Personal blog (HN).'},
    {'name': 'ksec', 'url': 'https://nicheless.blog', 'description': 'Personal blog (HN).'},
    {'name': 'Brajeshwar', 'url': 'https://brajeshwar.com', 'description': 'Personal blog (HN).'},
    {'name': 'ekianjo', 'url': 'https://boilingsteam.com', 'description': 'Personal blog (HN).'},
    {'name': 'bryanrasmussen', 'url': 'https://medium.com/feed/luminasticity', 'description': 'Personal blog (HN).'},
    {'name': 'toyg', 'url': 'http://blog.pythonaro.com', 'description': 'Personal blog (HN).'},
    {'name': 'craigkerstiens', 'url': 'https://www.craigkerstiens.com', 'description': 'Personal blog (HN).'},
    {'name': 'fanf2', 'url': 'https://dotat.at/@/blog.atom', 'description': 'Personal blog (HN).'},
    {'name': 'woodruffw', 'url': 'https://blog.yossarian.net', 'description': 'Personal blog (HN).'},
    {'name': 'ComputerGuru', 'url': 'https://neosmart.net', 'description': 'Personal blog (HN).'},
    {'name': 'dijit', 'url': 'http://blog.dijit.sh', 'description': 'Personal blog (HN).'},
    {'name': 'edent', 'url': 'https://shkspr.mobi', 'description': 'Personal blog (HN).'},
    {'name': 'ChrisMarshallNY', 'url': 'https://littlegreenviper.com', 'description': 'Personal blog (HN).'},
    {'name': 'imgabe', 'url': 'https://tiltingatwindmills.dev', 'description': 'Personal blog (HN).'},
    {'name': 'sneak', 'url': 'https://sneak.berlin', 'description': 'Personal blog (HN).'},
    {'name': 'grecy', 'url': 'http://theroadchoseme.com', 'description': 'Personal blog (HN).'},
    {'name': 'jefftk', 'url': 'https://www.jefftk.com', 'description': 'Personal blog (HN).'},
    {'name': 'rcarmo', 'url': 'https://taoofmac.com', 'description': 'Personal blog (HN).'},
    {'name': 'azhenley', 'url': 'https://austinhenley.com/blog', 'description': 'Personal blog (HN).'},
    {'name': 'eatonphil', 'url': 'https://notes.eatonphil.com', 'description': 'Personal blog (HN).'},
    {'name': 'sschueller', 'url': 'https://sschueller.github.io', 'description': 'Personal blog (HN).'},
    {'name': 'prepend', 'url': 'http://prepend.com', 'description': 'Personal blog (HN).'},
    {'name': 'geerlingguy', 'url': 'https://www.jeffgeerling.com', 'description': 'Personal blog (HN).'},
    {'name': 'Pxtl', 'url': 'https://Pxtl.ca', 'description': 'Personal blog (HN).'},
    {'name': 'marginalia_nu', 'url': 'https://www.marginalia.nu/log', 'description': 'Personal blog (HN).'},
    {'name': 'swyx', 'url': 'https://www.swyx.io', 'description': 'Personal blog (HN).'},
    {'name': 'susam', 'url': 'https://susam.net/blog', 'description': 'Personal blog (HN).'},
    {'name': 'orf', 'url': 'https://tomforb.es', 'description': 'Personal blog (HN).'},
    {'name': 'riffraff', 'url': 'https://riffraff.info', 'description': 'Personal blog (HN).'},
    {'name': 'komali2', 'url': 'https://blog.calebjay.com', 'description': 'Personal blog (HN).'},
    {'name': 'csomar', 'url': 'https://omarabid.com', 'description': 'Personal blog (HN).'},
    {'name': 'nindalf', 'url': 'https://blog.nindalf.com', 'description': 'Personal blog (HN).'},
    {'name': 'danpalmer', 'url': 'https://danpalmer.me', 'description': 'Personal blog (HN).'},
    {'name': 'janvdberg', 'url': 'https://j11g.com', 'description': 'Personal blog (HN).'},
    {'name': 'brightball', 'url': 'https://www.brightball.com', 'description': 'Personal blog (HN).'},
    {'name': 'donatj', 'url': 'https://donatstudios.com', 'description': 'Personal blog (HN).'},
    {'name': 'Aissen', 'url': 'https://anisse.astier.eu', 'description': 'Personal blog (HN).'},
    {'name': 'kstrauser', 'url': 'https://honeypot.net', 'description': 'Personal blog (HN).'},
    {'name': 'andyjohnson0', 'url': 'https://andyjohnson.uk', 'description': 'Personal blog (HN).'},
    {'name': 'jl6', 'url': 'https://www.lab6.com', 'description': 'Personal blog (HN).'},
    {'name': 'akkartik', 'url': 'http://feeds.akkartik.name/kartiks-scrapbook', 'description': 'Personal blog (HN).'},
    {'name': 'jakelazaroff', 'url': 'https://jakelazaroff.com', 'description': 'Personal blog (HN).'},
    {'name': 'dewey', 'url': 'https://annoying.technology', 'description': 'Personal blog (HN).'},
    {'name': 'JacobAldridge', 'url': 'https://jacobaldridge.com', 'description': 'Personal blog (HN).'},
    {'name': 'nickjj', 'url': 'https://nickjanetakis.com', 'description': 'Personal blog (HN).'},
    {'name': 'caseysoftware', 'url': 'https://caseysoftware.com', 'description': 'Personal blog (HN).'},
    {'name': 'fredley', 'url': 'https://healthydev.substack.com', 'description': 'Personal blog (HN).'},
    {'name': 'codeulike', 'url': 'https://www.codeulike.com', 'description': 'Personal blog (HN).'},
    {'name': 'fragmede', 'url': 'https://blog.onepatchdown.net', 'description': 'Personal blog (HN).'},
    {'name': 'bhouston', 'url': 'https://benhouston3d.com', 'description': 'Personal blog (HN).'},
    {'name': 'coldcode', 'url': 'https://thecodist.com', 'description': 'Personal blog (HN).'},
    {'name': 'DocFeind', 'url': 'https://maninthedot.com', 'description': 'Personal blog (HN).'},
    {'name': 'mintplant', 'url': 'https://spindas.dreamwidth.org/data', 'description': 'Personal blog (HN).'},
    {'name': 'tedivm', 'url': 'https://blog.tedivm.com', 'description': 'Personal blog (HN).'},
    {'name': 'philip1209', 'url': 'https://www.philipithomas.com', 'description': 'Personal blog (HN).'},
    {'name': 'themodelplumber', 'url': 'https://www.friendlyskies.net', 'description': 'Personal blog (HN).'},
    {'name': 'BeetleB', 'url': 'https://blog.nawaz.org', 'description': 'Personal blog (HN).'},
    {'name': 'PStamatiou', 'url': 'https://paulstamatiou.com', 'description': 'Personal blog (HN).'},
    {'name': 'yellowapple', 'url': 'https://yellowapple.us', 'description': 'Personal blog (HN).'},
    {'name': 'kevincox', 'url': 'https://kevincox.ca', 'description': 'Personal blog (HN).'},
    {'name': 'pclmulqdq', 'url': 'https://specbranch.com', 'description': 'Personal blog (HN).'},
    {'name': 'agentultra', 'url': 'https://agentultra.com', 'description': 'Personal blog (HN).'},
    {'name': 'softwaredoug', 'url': 'http://softwaredoug.com', 'description': 'Personal blog (HN).'},
    {'name': 'cratermoon', 'url': 'https://cmdev.com/blog', 'description': 'Personal blog (HN).'},
    {'name': 'jvanderbot', 'url': 'https://jodavaho.io', 'description': 'Personal blog (HN).'},
    {'name': 'bayindirh', 'url': 'https://blog.bayindirh.io', 'description': 'Personal blog (HN).'},
    {'name': 'captn3m0', 'url': 'https://captnemo.in', 'description': 'Personal blog (HN).'},
    {'name': 'stevekemp', 'url': 'https://blog.steve.fi', 'description': 'Personal blog (HN).'},
    {'name': 'zrail', 'url': 'https://www.petekeen.net', 'description': 'Personal blog (HN).'},
    {'name': 'diego', 'url': 'https://iamnotarobot.substack.com', 'description': 'Personal blog (HN).'},
    {'name': 'paraschopra', 'url': 'https://invertedpassion.com', 'description': 'Personal blog (HN).'},
    {'name': 'mikewarot', 'url': 'https://mikewarot.blogspot.com', 'description': 'Personal blog (HN).'},
    {'name': 'asicsp', 'url': 'https://learnbyexample.github.io', 'description': 'Personal blog (HN).'},
    {'name': 'indymike', 'url': 'https://mikeseidle.com', 'description': 'Personal blog (HN).'},
    {'name': 'zimpenfish', 'url': 'https://rjp.is/blogging', 'description': 'Personal blog (HN).'},
    {'name': 'Hamuko', 'url': 'https://burakku.com', 'description': 'Personal blog (HN).'},
    {'name': 'bergie', 'url': 'https://bergie.iki.fi/blog', 'description': 'Personal blog (HN).'},
    {'name': 'boyter', 'url': 'https://boyter.org', 'description': 'Personal blog (HN).'},
    {'name': 'anderspitman', 'url': 'https://apitman.com', 'description': 'Personal blog (HN).'},
    {'name': 'acconrad', 'url': 'https://www.adamconrad.dev', 'description': 'Personal blog (HN).'},
    {'name': 'ZeljkoS', 'url': 'https://svedic.org', 'description': 'Personal blog (HN).'},
    {'name': 'geocrasher', 'url': 'https://miscdotgeek.com', 'description': 'Personal blog (HN).'},
    {'name': 'jasonlotito', 'url': 'https://blog.damnscout.com', 'description': 'Personal blog (HN).'},
    {'name': 'est', 'url': 'https://feeds.feedburner.com/initiative', 'description': 'Personal blog (HN).'},
    {'name': 'seanwilson', 'url': 'https://www.seanw.org', 'description': 'Personal blog (HN).'},
    {'name': 'bovermyer', 'url': 'https://www.benovermyer.com', 'description': 'Personal blog (HN).'},
    {'name': 'DeusExMachina', 'url': 'https://matteomanferdini.com', 'description': 'Personal blog (HN).'},
    {'name': 'smcleod', 'url': 'https://smcleod.net', 'description': 'Personal blog (HN).'},
    {'name': 'Maro', 'url': 'https://bytepawn.com', 'description': 'Personal blog (HN).'},
    {'name': 'stargrave', 'url': 'http://blog.stargrave.org/russian', 'description': 'Personal blog (HN).'},
    {'name': 'megous', 'url': 'https://xnux.eu/log', 'description': 'Personal blog (HN).'},
    {'name': 'allenleein', 'url': 'https://blog.allen0s.com', 'description': 'Personal blog (HN).'},
    {'name': 'slyall', 'url': 'https://blog.darkmere.gen.nz', 'description': 'Personal blog (HN).'},
    {'name': 'orlp', 'url': 'https://orlp.net/blog', 'description': 'Personal blog (HN).'},
    {'name': 'amadeuspagel', 'url': 'https://amadeuspagel.com', 'description': 'Personal blog (HN).'},
    {'name': 'mgh2', 'url': 'https://medium.com/feed/@trendguardian', 'description': 'Personal blog (HN).'},
    {'name': 'DamnInteresting', 'url': 'https://feeds.feedburner.com/damninteresting/all', 'description': 'Personal blog (HN).'},
    {'name': 'senko', 'url': 'https://blog.senko.net', 'description': 'Personal blog (HN).'},
    {'name': 'benhoyt', 'url': 'https://benhoyt.com/writings', 'description': 'Personal blog (HN).'},
    {'name': 'pera', 'url': 'https://blog.peramid.es', 'description': 'Personal blog (HN).'},
    {'name': 'steve_adams_86', 'url': 'https://steve-adams.me', 'description': 'Personal blog (HN).'},
    {'name': '__david__', 'url': 'https://porkrind.org/missives', 'description': 'Personal blog (HN).'},
    {'name': 'ryanSrich', 'url': 'https://rrich.io', 'description': 'Personal blog (HN).'},
    {'name': 'IvyMike', 'url': 'https://ivymike.dev', 'description': 'Personal blog (HN).'},
    {'name': 'unmole', 'url': 'https://www.anmolsarma.in', 'description': 'Personal blog (HN).'},
    {'name': 'mkeeter', 'url': 'https://mattkeeter.com', 'description': 'Personal blog (HN).'},
    {'name': 'bredren', 'url': 'https://banagale.com', 'description': 'Personal blog (HN).'},
    {'name': 'llimllib', 'url': 'https://notes.billmill.org', 'description': 'Personal blog (HN).'},
    {'name': 'dom96', 'url': 'https://blog.picheta.me', 'description': 'Personal blog (HN).'},
    {'name': 'slimsag', 'url': 'https://devlog.hexops.com', 'description': 'Personal blog (HN).'},
    {'name': 'dash2', 'url': 'https://wyclif.substack.com', 'description': 'Personal blog (HN).'},
]


# Direct page and pipeline use this; keep in sync with DIRECT_REFERENCE_LIST.
DIRECT_LINKS = list(DIRECT_REFERENCE_LIST)

# =============================================================================
# LINKS BACK — Who links to eof.news (we discover and list them)
# =============================================================================
# Add when you find someone linking back; run pipeline or `python main.py --action direct` to update docs/_data/links_back.json.

LINKS_BACK = [
    # Example: {'name': 'Example Dev', 'url': 'https://exampledev.com'},
]

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
