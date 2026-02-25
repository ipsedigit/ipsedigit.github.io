# Two-Pass Article Selection Design

**Date:** 2026-02-25
**Goal:** Balanced, interesting, on-point content — 10-12 posts/day with guaranteed niche coverage and content type diversity.

## Problem

Current system is score-greedy: picks the single highest-scoring article per run. Result: AI (50 posts) and GitHub (46) dominate, Cloud (3) starved. No content type diversity enforcement.

## Design: Two-Pass Selection

### Content Type Classification

Every article gets one of 3 types, detected from title patterns + source type:

| Type | Signal |
|---|---|
| **breaking** | Announcements, releases, CVEs, vulnerabilities, launches |
| **deep** | Research, architecture, benchmarks, tutorials, case studies |
| **community** | Show HN, GitHub trending, creator posts, open source projects |

Detection priority:
1. `source_type == 'creator'` → community
2. Title matches `(show\s+hn|open.?source|built\s+a|side\s+project)` → community
3. Title matches `(announce|launch|releas|introduc|vulnerab|exploit|breach|CVE-)` → breaking
4. Title matches `(paper|arxiv|research|benchmark|how\s+we|architecture|deep\s+dive|tutorial|guide|case\s+study)` → deep
5. Source type `research_blog` or `se_blog` → deep
6. Source type `security` + title matches threat keywords → breaking
7. Default → breaking

### Pass 1 — Guaranteed Slots (5-6 posts)

| Slot | Rule |
|---|---|
| 1 best AI article | Highest score in `ai` niche, score >= 70 |
| 1 best Security article | Highest score in `security` niche, score >= 70 |
| 1 best Cloud article | Highest score in `cloud` niche, score >= 70 |
| 1 best DevTools article | Highest score in `devtools` niche, score >= 70 |
| 1 best Software Engineering article | Highest score in `software-engineering` niche, score >= 70 |
| 1 best Creator article | Highest score from `source_type == 'creator'`, any niche |

If a niche has no article scoring >= 70, slot is skipped.

### Pass 2 — Open Competition (4-6 posts)

From remaining candidates, sorted by score descending:
1. Score >= 70
2. Max 3 total posts per niche per day (Pass 1 + Pass 2)
3. Type diversity: if one type already has 4+ posts, skip that type
4. No duplicate sub-niches (existing rule)
5. Stop at 12 total

### Edge Cases

- Slow day (total < 8): lower floor to 60, run Pass 2 again. Minimum target: 8.
- Big news day: hard cap at 12.

### Scoring Changes

- Quality floor raised: 50 → 70
- New frontmatter field: `content_type: "breaking|deep|community"`
- `why_picked` enriched with pass info
- All existing scoring (source bonuses, title patterns, community signal) unchanged

### Daily State Tracking

`news/daily_categories.txt` format expands:
```
2026-02-25:ai:llm:breaking
2026-02-25:security:malware:breaking
2026-02-25:cloud:kubernetes:deep
```

### Files to Modify

| File | Change |
|---|---|
| `const.py` | `CONTENT_TYPE_PATTERNS`, `MIN_SCORE=70`, `MIN_SCORE_FALLBACK=60`, `DAILY_TARGET=12`, `DAILY_MINIMUM=8`, `MAX_PER_TYPE=4` |
| `news.py` | `classify_content_type()`, refactor `find_best_post()` → `select_daily_posts()` (two-pass), add `content_type` to frontmatter |
| `main.py` | Update `--action=news` to call new selection logic with daily state awareness |

### Files NOT Changing

- `keywords.py`, `trends.py`, `models.py`, `cves.py`, `github_trending.py`
- Jekyll templates/layouts
- GitHub Actions workflows
