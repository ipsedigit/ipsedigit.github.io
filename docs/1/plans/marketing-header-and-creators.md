# Marketing: Header proposition & creators section

## 1. Header / value proposition — how to review it

**Current (index):**  
- H1: "eof.news"  
- Subline: "Currated tech news from 50+ sources"

**Issues:**  
- Subline is feature-led (“50+ sources”) not benefit-led.  
- “Curated” is table stakes; it doesn’t say *why* your curation is different.  
- No hint of “trending” or “what’s hot,” so it doesn’t pull in trend-seeking visitors.

**Principles for the new proposition:**

1. **Lead with outcome, not input**  
   “What I get” (save time, stay ahead, ship better) > “where it comes from” (50+ sources).

2. **Signal “trending / today”**  
   One short phrase that says “daily, fresh, what matters now” (e.g. “Today’s signal”, “What’s moving tech today”).

3. **Differentiate in one phrase**  
   e.g. “for builders”, “for engineers who ship”, “no fluff” — so it’s clear who it’s for and what to expect.

4. **Keep it scannable**  
   One line for promise, one optional line for proof/differentiator. Avoid long sentences.

---

## 2. Copy options (pick one or mix)

**Option A — Trend + audience**  
- **H1:** eof.news  
- **Subline:** Today’s tech signal for engineers who build.  
- **Optional 2nd line:** Curated from 50+ sources — AI, security, cloud, devtools.

**Option B — Outcome first**  
- **H1:** eof.news  
- **Subline:** The tech that matters. One digest, no noise.  
- **Optional 2nd line:** Daily picks from research, engineering blogs, and top newsletters.

**Option C — “Trending” explicit**  
- **H1:** eof.news  
- **Subline:** Trending tech that matters — curated daily for builders.  
- **Optional 2nd line:** AI, security, cloud, devtools & software engineering.

**Option D — Short and sharp**  
- **H1:** eof.news  
- **Subline:** Daily tech signal. No noise.  
- **Quick nav:** “Trending”, “By topic”, “From creators”, “RSS”.

**Recommendation:** Start with **Option A** or **C** if you want “trending” and “interesting” to be obvious; use **Option D** if you prefer minimal and let “From creators” + topics do the work.

---

## 3. SEO / meta alignment

Keep the **page title** and **meta description** aligned with the chosen subline:

- If you use “Today’s tech signal for engineers who build” →  
  **Title:** eof.news — Today’s tech signal for engineers who build  
  **Description:** Daily curated tech signal: AI, security, cloud, devtools. For engineers who build. No noise.

Update both in `index.html` (front matter) and in `_config.yml` where relevant so search results match the proposition.

---

## 4. “Creators” section — why it helps reach individuals

**Why non-corporate content helps:**

- **Substack / Buttondown / indie blogs** = individual creators with their own audience. When you feature them, their readers discover you (backlinks, shares, “featured on eof.news”).
- **Algorithmic reach:** Content from people (byline, face, newsletter) often gets more engagement and shares than “Company Blog” — so a dedicated “From creators” stream can perform better on social and search.
- **Trust:** “Engineers like me” trust other practitioners; a clear “creators & newsletters” bucket positions you as the place that surfaces *people*, not only corporate comms.

**How it can work:**

1. **New source type: `creator`**  
   In `const.py`, add a tier for “Creators & newsletters”: Substack/Buttondown/indie RSS feeds. Give them a scoring bonus so they appear in the main feed but are also filterable.

2. **Dedicated section on site:**  
   - **“From creators”** (or “Indie voices” / “Newsletters”) in the main nav and in the homepage quick-nav.  
   - Links to a **/creators/** page that:  
     - Lists the creator sources (name, one line, link to their Substack/newsletter).  
     - Optionally shows “Recent from creators” (posts where `source_type == 'creator'`).

3. **Reach mechanics:**  
   - When you feature a creator’s post, they’re more likely to share or link back.  
   - You can (with permission) list them on the Creators page → they link to eof.news from their newsletter or bio → you get referral traffic and backlinks.  
   - Over time you can add “Subscribe” or “Featured in” badges to encourage cross-promotion.

**Naming options:**

- **“From creators”** — clear, works for Substack/YouTube/indie blogs.  
- **“Newsletters & indie”** — very explicit for Substack/Buttondown.  
- **“Indie voices”** — distinct from “corporate,” a bit more editorial.

Recommendation: **“From creators”** in the UI; in code use `creator` or `newsletter` as `source_type`.

---

## 5. Implementation checklist

- [ ] Choose one header option (A–D) and set it in the homepage header and, if desired, in `_config.yml` (tagline/description).
- [ ] Align `index.html` title and meta description with the new proposition.
- [ ] Add `creator` (or `newsletter`) source type in `const.py` and scoring in `news.py`.
- [ ] Add 3–5 creator/newsletter RSS feeds to `NEWS_SOURCES` (e.g. Pragmatic Engineer already present; add more Substack/Buttondown).
- [ ] Create `/creators/` page: intro + list of creator sources + optional “Recent from creators” block.
- [ ] Add “From creators” (or chosen label) to site nav and to the homepage quick-nav.
- [ ] Optionally add a niche badge or filter for creator-sourced posts in the main feed.

After that, you can A/B test header copy and measure: time on site, clicks to creator posts, and referral traffic from creator sites.
