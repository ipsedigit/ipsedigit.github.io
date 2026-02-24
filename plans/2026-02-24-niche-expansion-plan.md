# Niche Expansion Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Expand eof.news from 2 niches (AI, Security) to 5 (+ Cloud, DevTools, Software Engineering), with 15 balanced posts/day and a niche-grouped homepage.

**Architecture:** Add 3 new niche definitions with sub-niches and detection keywords to `const.py`. Expand `keywords.py` for article matching. Generalize `news.py` classification to be data-driven instead of hardcoded. Add 10 new RSS sources. Rebuild homepage as niche-sectioned layout. Adjust workflow schedule.

**Tech Stack:** Python 3, Jekyll/Liquid, GitHub Actions

---

### Task 1: Add new niches and sub-niches to `const.py`

**Files:**
- Modify: `const.py:10-48`

**Step 1: Add cloud, devtools, software-engineering to CONTENT_CATEGORIES**

In `const.py`, replace the `CONTENT_CATEGORIES` dict and `NICHE_CATEGORIES` set with:

```python
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

NICHE_CATEGORIES = {'ai', 'security', 'cloud', 'devtools', 'software-engineering'}
```

**Step 2: Add CLOUD_SUBNICHES, DEVTOOLS_SUBNICHES, SE_SUBNICHES**

After `SECURITY_SUBNICHES`, add:

```python
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
```

**Step 3: Add a mapping dict for subniche lookup**

After the sub-niche dicts, add:

```python
NICHE_SUBNICHES = {
    'ai': AI_SUBNICHES,
    'security': SECURITY_SUBNICHES,
    'cloud': CLOUD_SUBNICHES,
    'devtools': DEVTOOLS_SUBNICHES,
    'software-engineering': SE_SUBNICHES,
}
```

**Step 4: Commit**

```bash
git add const.py
git commit -m "feat: add cloud, devtools, software-engineering niches with sub-niches"
```

---

### Task 2: Add new keywords to `keywords.py`

**Files:**
- Modify: `keywords.py`

**Step 1: Add cloud keywords**

Add after the existing "Cloud, DevOps, Infra" section:

```python
    # ☁️ Cloud platforms & services
    "aws": "AWS",
    "amazon web services": "AWS",
    "gcp": "Google Cloud",
    "google cloud": "Google Cloud",
    "azure": "Azure",
    "cloud-native": "Cloud Native",
    "cloud native": "Cloud Native",
    "eks": "Amazon EKS",
    "ecs": "Amazon ECS",
    "lambda": "AWS Lambda",
    "fargate": "AWS Fargate",
    "s3": "Amazon S3",
    "ec2": "Amazon EC2",
    "cloudformation": "CloudFormation",
    "pulumi": "Pulumi",
    "ansible": "Ansible",
    "helm": "Helm",
    "istio": "Istio",
    "service mesh": "Service Mesh",
    "argocd": "ArgoCD",
    "infrastructure as code": "Infrastructure as Code",
    "load balancer": "Load Balancing",
    "cdn": "CDN",
    "api gateway": "API Gateway",
    "edge computing": "Edge Computing",
    "cloud functions": "Cloud Functions",
```

**Step 2: Add devtools keywords**

```python
    # 🔧 Developer Tools
    "vscode": "VS Code",
    "jetbrains": "JetBrains",
    "intellij": "IntelliJ IDEA",
    "neovim": "Neovim",
    "zed": "Zed Editor",
    "cursor": "Cursor",
    "webpack": "Webpack",
    "vite": "Vite",
    "eslint": "ESLint",
    "prettier": "Prettier",
    "monorepo": "Monorepo",
    "npm": "npm",
    "yarn": "Yarn",
    "pnpm": "pnpm",
    "cargo": "Cargo",
    "poetry": "Poetry",
    "bun": "Bun",
    "deno": "Deno",
    "gradle": "Gradle",
    "maven": "Maven",
    "homebrew": "Homebrew",
    "nix": "Nix",
    "react": "React",
    "next.js": "Next.js",
    "nextjs": "Next.js",
    "vue": "Vue.js",
    "svelte": "Svelte",
    "angular": "Angular",
    "django": "Django",
    "fastapi": "FastAPI",
    "spring": "Spring",
    "rails": "Ruby on Rails",
    "htmx": "htmx",
    "astro": "Astro",
```

**Step 3: Add software engineering keywords**

```python
    # 🏗️ Software Engineering
    "system design": "System Design",
    "technical debt": "Technical Debt",
    "clean code": "Clean Code",
    "refactoring": "Refactoring",
    "code review": "Code Review",
    "tdd": "TDD",
    "test-driven": "TDD",
    "pair programming": "Pair Programming",
    "agile": "Agile",
    "scrum": "Scrum",
    "circuit breaker": "Circuit Breaker",
    "saga pattern": "Saga Pattern",
    "rate limiting": "Rate Limiting",
    "api design": "API Design",
    "rest api": "REST API",
    "openapi": "OpenAPI",
    "swagger": "Swagger",
    "webhook": "Webhooks",
    "websocket": "WebSocket",
    "concurrency": "Concurrency",
    "load testing": "Load Testing",
    "profiling": "Profiling",
    "latency": "Latency",
    "throughput": "Throughput",
```

**Step 4: Commit**

```bash
git add keywords.py
git commit -m "feat: add cloud, devtools, SE keywords for article matching"
```

---

### Task 3: Add new RSS sources to `const.py`

**Files:**
- Modify: `const.py` (NEWS_SOURCES section)

**Step 1: Add cloud/devtools/SE sources**

Add after the existing TIER 6 section:

```python
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
    },
    'bytebytego': {
        'name': 'ByteByteGo',
        'feed_url': 'https://blog.bytebytego.com/feed',
        'min_score': 0,
        'type': 'se_blog',
    },
```

**Step 2: Add scoring bonus for new source types and title patterns**

In `TITLE_BONUS`, add:

```python
    r'(kubernetes|k8s|docker|container|cloud)': 25,
    r'(framework|library|sdk|release|v\d)': 20,
    r'(architecture|system design|scalab|pattern)': 20,
```

**Step 3: Commit**

```bash
git add const.py
git commit -m "feat: add 10 RSS sources for cloud, devtools, SE niches"
```

---

### Task 4: Generalize `news.py` classification

**Files:**
- Modify: `news.py:1-19` (imports)
- Modify: `news.py:240-260` (`identify_subniche`)
- Modify: `news.py:172-221` (`calculate_score`)
- Modify: `news.py:263-289` (`generate_why_picked`)

**Step 1: Update imports**

Replace the import of individual subniche dicts with the mapping:

```python
from const import (
    NEWS_SOURCES,
    PUBLISHED_NEWS_FILE_NAME,
    CONTENT_CATEGORIES,
    NICHE_CATEGORIES,
    MAX_POSTS_PER_NICHE_PER_DAY,
    DAILY_CATEGORIES_FILE,
    TITLE_BONUS,
    TITLE_PENALTY,
    NICHE_SUBNICHES,
)
```

**Step 2: Replace `identify_subniche` with data-driven version**

```python
def identify_subniche(entry, main_cat):
    """Identify the sub-niche within any niche category."""
    text = (entry.get('title', '') + ' ' + ' '.join(entry.get('tags', []))).lower()

    subniches = NICHE_SUBNICHES.get(main_cat)
    if not subniches:
        return None

    best_sub = None
    best_matches = 0

    for sub, keywords in subniches.items():
        matches = sum(1 for kw in keywords if kw in text)
        if matches > best_matches:
            best_matches = matches
            best_sub = sub

    return best_sub
```

**Step 3: Update `calculate_score` to handle new source types**

Add scoring for `cloud_news` and `se_blog` types in the source type bonus section:

```python
    elif source_type == 'cloud_news':
        score += 30
    elif source_type == 'se_blog':
        score += 35
```

**Step 4: Update `generate_why_picked` for new source types**

Add cases:

```python
    elif source_type == 'cloud_news':
        parts.append(f"cloud infrastructure source: {source_name}")
    elif source_type == 'se_blog':
        parts.append(f"software engineering thought leader: {source_name}")
```

**Step 5: Commit**

```bash
git add news.py
git commit -m "feat: generalize classification for 5 niches"
```

---

### Task 5: Rebuild homepage with niche sections

**Files:**
- Modify: `docs/index.md`

**Step 1: Replace the post loop with niche-grouped sections**

Keep the existing CSS and header. Replace the `{% for post in site.posts %}` loop with niche sections. Each section shows the niche name as heading, iterates posts filtered by `niche_category`, shows up to 3 per section, using the same card markup.

The Liquid template groups posts by `niche_category` front matter field:

```liquid
{% assign niche_order = "cloud,devtools,software-engineering,ai,security" | split: "," %}
{% assign niche_labels = "Cloud & Infrastructure,Developer Tools,Software Engineering,Artificial Intelligence,Security" | split: "," %}

{% for i in (0..4) %}
  {% assign niche = niche_order[i] %}
  {% assign label = niche_labels[i] %}
  {% assign niche_posts = site.posts | where: "niche_category", niche %}

  {% if niche_posts.size > 0 %}
  <section class="niche-section">
    <h2 class="niche-heading">{{ label }}</h2>
    {% assign count = 0 %}
    {% for post in niche_posts %}
      {% if count >= 3 %}{% break %}{% endif %}
      <article class="post-item">
        <!-- same card markup as current -->
      </article>
      {% assign count = count | plus: 1 %}
    {% endfor %}
  </section>
  {% endif %}
{% endfor %}
```

Add CSS for `.niche-section` and `.niche-heading`.

**Step 2: Commit**

```bash
git add docs/index.md
git commit -m "feat: homepage with niche-grouped sections"
```

---

### Task 6: Adjust workflow schedule

**Files:**
- Modify: `.github/workflows/dailynewspublisher.yml`

**Step 1: Reduce to 3 runs/day**

With 5 niches x 1 post per niche per run, 3 runs reaches the 15 post cap:

```yaml
on:
  schedule:
    - cron: '0 7 * * *'    # 08:00 Rome - Morning
    - cron: '0 13 * * *'   # 14:00 Rome - Afternoon
    - cron: '0 19 * * *'   # 20:00 Rome - Evening
  workflow_dispatch:
```

**Step 2: Commit**

```bash
git add .github/workflows/dailynewspublisher.yml
git commit -m "chore: adjust schedule to 3 runs/day for 5 niches"
```

---

### Task 7: Update footer tagline

**Files:**
- Modify: `news.py:420`

**Step 1: Update the curated-by line**

Change:
```python
f.write("*This article was curated by eof.news — signal for AI engineers and security practitioners.*\n")
```
To:
```python
f.write("*This article was curated by eof.news — signal for engineers who build.*\n")
```

**Step 2: Commit**

```bash
git add news.py
git commit -m "chore: update tagline for broader niche coverage"
```
