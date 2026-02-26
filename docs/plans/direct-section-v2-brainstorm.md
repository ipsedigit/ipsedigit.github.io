# Direct section v2 — match site pattern + “find out who link”

## What you said

1. **Pattern:** Other sections present a **list of resources** that link to posts or to an aggregator platform. Direct should follow the **same pattern** — not a one-off layout.
2. **Direct to the user:** You want resources that link **directly to the user** (their site), so they know you’re linking and can link back.
3. **“You are in charge to find out who link”:** You want **someone/something** (the system) to be responsible for **finding who links [back]** to eof.news — and to show that.

---

## 1. Match the site pattern

**Current pattern (Sources, Topics, Home):**
- **Layout:** `base` (same as Sources, Topics).
- **Structure:** Page title (h1) + short intro + **list/grid of items**; each item = card with title (link), optional description, optional meta/badge.
- **Styling:** Same family — e.g. `.source-item` / `.topic-card`: `background: #fafafa`, `border: 1px solid #e5e5e5`, `border-radius: 6px`, hover `border-color: #999`. Grid: `grid-template-columns: repeat(auto-fill, minmax(250px, 1fr))`.

**So for Direct:**
- Use **layout: base** (like Sources, Topics).
- Use the **same structure** as Sources: one “category” block, then a **source-list**-style grid of **source-item**-style cards. Reuse the same class names (e.g. `sources-page` → `direct-page` but with **identical CSS** for the list and items so it looks like Sources).
- Each card: **name** (link to their site) + short **description** + optional badge (“Direct” or “We link to you”). Link goes **directly to their URL** (no aggregator).

So: **Direct = same page shape as Sources, same card look; only the copy and the link target differ** (we link to the person’s site so they see it and can link back).

---

## 2. Link directly to the user

- Every entry in the list: **one link = their site** (blog, newsletter homepage, etc.). No link to Substack/Medium as a platform — to *their* URL.
- Copy on the page: “We link to you directly — to your site, not to a platform — so you see we’re linking and can link back if you want.”
- Data stays **DIRECT_LINKS** (name, url, description); url = their real destination.

No change to the data model; only the page layout and wording make the “direct to you” and “so you know we’re linking” explicit.

---

## 3. “Find out who link” — we are in charge of discovering who links back

**Meaning:** The system (pipeline / script / you) is responsible for **finding who links [back]** to eof.news, and the Direct page should **show** that.

**Proposal: two blocks on the same page**

| Block | Purpose | Data |
|-------|--------|------|
| **We link to you** | List of people we link to (direct to their site). | `DIRECT_LINKS` → `direct_links.json` (existing). |
| **Who links to us** | List of people/sites that link back to eof.news. | New: `LINKS_BACK` or `docs/_data/links_back.json` (see below). |

So the page becomes: same pattern as other sections (list of resources), but with **two lists**: (1) we link to you, (2) who links to us. Both use the same card style.

**How we “find out who link” (options):**

- **A) Manual list (start here)**  
  You (or a maintainer) add someone to a “links back” list when you notice they linked (email, tweet, manual check). Data: e.g. `LINKS_BACK` in `const.py` or a JSON file. Pipeline writes `docs/_data/links_back.json`; the page shows it. “We are in charge” = we maintain this list and keep it up to date.

- **B) Google Search Console (later)**  
  Use GSC API (or export) to get “linking sites” or “referring pages.” A script runs periodically, maps referrers to known Direct names where possible, and updates `links_back.json`. Fully automated “find out who link.”

- **C) Notify-us flow**  
  On the Direct page: “If you link to eof.news, [tell us](/about/ or form) and we’ll add you to ‘Who links to us’.” So we discover by them telling us; we’re still “in charge” of curating and displaying the list.

- **D) Crawl / backlink check (later)**  
  For each URL in DIRECT_LINKS, periodically fetch their page and check for a link to eof.news/ipsedigit.github.io; if found, add to links_back. More work and politeness considerations (rate limit, robots.txt).

**Recommendation:** Start with **A (manual list)** so the section and the “who links to us” block exist and follow the same pattern. Add **C** in the copy (“Tell us if you link back”). Later, add **B** or **D** if you want automation.

**Data shape for “Who links to us”:** Same as direct links: e.g. `{ "name", "url" }` (their site that links to us). Optional: `referrer_url` (the page that contains the link). So we can reuse the same card component: name + link to their site.

---

## 4. Concrete changes (summary)

1. **Direct page**
   - Use **layout: base**.
   - Reuse the **same structure and CSS** as Sources: intro + grid of cards (same classes or same styles). Each card: name (link to their site), description, optional badge.
   - **Two sections:**  
     - **“We link to you”** — from `direct_links.json` (unchanged).  
     - **“Who links to us”** — from `links_back.json` (new).
   - Copy: “We link to you directly so you know we’re linking; link back if you like. We track who links to us and list them below.”

2. **Backend**
   - Add **LINKS_BACK** (list of `{ name, url }`) in `const.py`, or a separate data file that the pipeline can write.
   - Add **update_links_back_data()** (or similar) that writes `docs/_data/links_back.json` from LINKS_BACK (or from GSC/crawl later). Call it from the same place that updates direct_links (e.g. `publish_news` or `main.py --action direct`).
   - “Find out who link” = we maintain and display this list; later we can add GSC/crawl/notify to fill it.

3. **Single source of truth**
   - **We link to you:** `DIRECT_LINKS` in const → `direct_links.json`.  
   - **Who links to us:** `LINKS_BACK` in const (or JSON) → `links_back.json`.  
   - Same card UI for both; only the section title and data source differ.

This keeps the section consistent with the rest of the site (list of resources, same pattern), makes “direct to the user” and “so they know we’re linking” explicit, and puts “find out who link” in our hands (list + display, with room to add discovery later).
