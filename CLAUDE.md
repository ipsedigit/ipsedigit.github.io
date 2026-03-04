# CLAUDE.md — eof.news

## What This Project Is

**eof.news** is a personal tech news aggregator and an agentic development learning project.

Two goals, equal priority:
1. **Personal use** — stay informed on AI, security, cloud, devtools, software engineering without noise
2. **Learning** — experiment with agentic Python pipelines, GitHub Actions automation, and iterative AI-assisted development

It is a Jekyll static site on GitHub Pages. A Python pipeline runs on a schedule, fetches RSS from curated sources, scores and selects articles, and publishes them as Jekyll posts. Fully automated, no CMS, no user accounts.

---

## Architecture

```
main.py --action=news [--niche=<niche>]
    └── news.py           # fetch → score → select → publish Jekyll posts
        ├── const.py      # sources, scoring rules, niche config, keywords
        ├── keywords.py   # 176 classification keywords
        ├── tags.py       # generates docs/tags/*.md pages
        ├── post_parser.py
        └── utils.py

tests/                    # pytest suite (test_build_candidates, test_select_daily, etc.)

docs/                     # Jekyll site (GitHub Pages)
  _posts/                 # auto-generated news posts (external_url frontmatter)
  _data/                  # JSON data files for dynamic sections
  _layouts/               # base, home, niche, page, post, tag
  _includes/              # header, footer, head, etc.
  _sass/minima/           # custom styles (custom-styles.scss is the main override)
  niche/                  # 5 niche landing pages
  tags/                   # auto-generated tag pages
  index.html              # homepage (paginated reverse-chron feed)

.github/workflows/
  dailynewspublisher.yml   # runs news pipeline 8x/day on main
  deploy-production.yml    # push to main → Jekyll build → gh-pages root
  deploy-preview.yml       # push to branch xyz → Jekyll build → gh-pages/xyz/
  cleanup-preview.yml      # delete branch xyz → removes gh-pages/xyz/

.claude/skills/
  update-claude-md/       # skill: keep CLAUDE.md current after significant changes
```

## Five Niches

`ai` | `software-engineering` | `devtools` | `cloud` | `security`

Defined in `const.py → NICHE_CATEGORIES`. Each has sub-niches in `NICHE_SUBNICHES`.

---

## Conventions

### Never commit automatically
The user commits manually via their git client. Claude must never run `git commit`, `git push`, or any destructive git command unless explicitly asked.

### No subagent-driven development
Too slow and heavy. Direct edits only.

### No multi-agent review pipelines for straightforward tasks.

### Keep it simple
This is a personal project, not a product. Avoid over-engineering. No abstractions for one-time use. No backwards-compat shims.

### Python style
- No external deps beyond: `feedparser`, `bs4`, `tweepy`, `requests`
- stdlib-first
- Functions over classes unless state is genuinely needed

### Jekyll/Liquid
- Global CSS goes in `docs/_sass/minima/custom-styles.scss`
- Font loaded in `docs/_includes/head.html`
- Nav links in `docs/_includes/header.html`
- Posts use `external_url` frontmatter — clicking goes directly to original source

---

## Current State (post-cleanup, 2026-03-04)

Everything except the core news pipeline has been pruned:
- Removed: Android, iOS, Models, Digest, GitHub Trending, CVEs, Outages sections
- What remains: `news.py` pipeline + Jekyll front-end + daily workflow

The site is back to fundamentals. The next features should be built deliberately, one at a time, with clear purpose.

Branch preview deployments added (2026-03-04): push to any non-main branch → site live at `/branchname/`. GitHub Pages now serves from `gh-pages` branch (manual setup required before first deploy).

---

## Development Philosophy

Since this is also a learning project, prefer:
- **Explicit over implicit** — code should be readable and obvious
- **Small, complete features** — one thing at a time, working end-to-end
- **Brainstorm before building** — use the brainstorming skill before any non-trivial feature
- **Plans before code** — write a plan doc before implementation
- **Verify before claiming done** — run tests or check output before saying something works
