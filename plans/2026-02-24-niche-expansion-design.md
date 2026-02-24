# Niche Expansion Design — 5 Categories

**Date:** 2026-02-24
**Status:** Approved

## Goal

Expand eof.news from 2 niches (AI, Security) to 5 niches (AI, Security, Cloud, DevTools, Software Engineering). 15 posts/day balanced across niches. Homepage reorganized around niche sections.

## Niches & Sub-niches

### Existing (unchanged)

- **ai**: `llm`, `ai-research`, `ai-infrastructure`, `mlops`
- **security**: `appsec`, `threat-intel`, `malware`, `cryptography`, `vulnerability`

### New

- **cloud**: `aws`, `gcp-azure`, `kubernetes`, `serverless`, `networking-iaas`
- **devtools**: `frameworks`, `languages`, `ides-editors`, `cicd`, `package-managers`
- **software-engineering**: `architecture`, `design-patterns`, `methodologies`, `api-design`, `performance`

## Changes

### 1. `const.py`

- Add `cloud`, `devtools`, `software-engineering` to `CONTENT_CATEGORIES` with detection keywords
- Add `NICHE_CATEGORIES = {'ai', 'security', 'cloud', 'devtools', 'software-engineering'}`
- Add `CLOUD_SUBNICHES`, `DEVTOOLS_SUBNICHES`, `SE_SUBNICHES` dicts
- `MAX_POSTS_PER_NICHE_PER_DAY` stays at 3 (5x3=15/day)
- Add new RSS sources for cloud/devtools/SE coverage

### 2. `keywords.py`

Add ~40-50 new keywords:
- Cloud: aws, gcp, azure, eks, ecs, lambda, fargate, cloud-native, s3, ec2, iam, vpc, load balancer, cdn, cloudformation, pulumi, ansible
- DevTools: vscode, jetbrains, neovim, webpack, vite, eslint, prettier, npm, pip, cargo, gradle, maven, sdk, cli, debugger, profiler, git, monorepo
- Software Engineering: system design, technical debt, clean code, solid principles, refactoring, code review, tdd, bdd, agile, scrum, sprint, observability pattern, circuit breaker, saga pattern, rate limiting

### 3. `news.py`

- `identify_subniche()`: replace hardcoded if/elif with a dict mapping `{niche: subniche_dict}`
- `generate_why_picked()`: handle new source types
- No changes to `identify_category()` — it already loops over `CONTENT_CATEGORIES`

### 4. New RSS Sources

| Key | Name | Feed URL | Type | Niche focus |
|-----|------|----------|------|-------------|
| `thenewstack` | The New Stack | https://thenewstack.io/feed/ | news | cloud, k8s |
| `devops_com` | DevOps.com | https://devops.com/feed/ | news | cloud, cicd |
| `infoworld` | InfoWorld | https://www.infoworld.com/feed/ | news | devtools, languages |
| `devto` | dev.to | https://dev.to/feed | community | devtools, SE |
| `martinfowler` | Martin Fowler | https://martinfowler.com/feed.atom | blog | architecture |
| `pragmatic_eng` | The Pragmatic Engineer | https://newsletter.pragmaticengineer.com/feed | blog | SE |
| `bytebytego` | ByteByteGo | https://blog.bytebytego.com/feed | blog | system design |
| `hashicorp` | HashiCorp Blog | https://www.hashicorp.com/blog/feed.xml | corporate_blog | terraform, cloud |
| `docker_blog` | Docker Blog | https://www.docker.com/blog/feed/ | corporate_blog | containers |
| `k8s_blog` | Kubernetes Blog | https://kubernetes.io/feed.xml | corporate_blog | k8s |

### 5. Homepage (`docs/index.md`)

Replace flat chronological list with niche-grouped sections:

```
[eof.news header]

[Cloud section — 3 latest posts]
[DevTools section — 3 latest posts]
[Software Engineering section — 3 latest posts]
[AI section — 3 latest posts]
[Security section — 3 latest posts]
```

Each section: heading, 3 post cards (same card style as current), "more" link to tag page.

### 6. Scoring (`const.py`)

Add `TITLE_BONUS` patterns for new niches:
- `r'(kubernetes|k8s|docker|container|cloud)': 25` — cloud signal
- `r'(framework|library|sdk|release|v\d)': 20` — devtools signal
- `r'(architecture|system design|scalab|pattern)': 20` — SE signal
