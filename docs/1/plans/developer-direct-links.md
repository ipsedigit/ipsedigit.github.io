# Developer direct links — one section instead of Devs + Creators

## Your goal

- **One header entry** that points to **resources for developers**.
- Developers are **linked directly** (their site, their newsletter URL) — **no aggregation platform intermediation** (we don’t send people to “Substack” or “Medium”, we send them to *them*).
- Developers can **get involved** and **be linked** (discoverable, backlinkable, one clear place to ask to be listed).

So: **delete Devs and Creators**, replace with **one clear section** that does this.

---

## Proposal: one section — “Direct” or “For developers”

### One nav item, one page

- **Nav label examples:** “Direct”, “For developers”, “Developer links”, or “Voices” (you pick).
- **URL:** e.g. `/direct/` or `/for-developers/` or `/links/`.
- **Purpose (visible on the page):**
  - **For readers:** “Developers and newsletters we link to — directly to their site, not to a platform.”
  - **For developers:** “We link to you, not to an aggregator. Want to be listed? [Get in touch](/about/).”

### One list, direct links only

- **Content:** A single directory: **name → direct URL** (and optionally one short line per person/source).
  - Example: “Julia Evans” → https://jvns.ca  
  - “The Pragmatic Engineer” → https://newsletter.pragmaticengineer.com  
  - “Dan Luu” → https://danluu.com  
- **No** “recent posts” block on this page (that’s aggregation; the digest already does that on the home). This page is only: **who we link to**, **where to find them directly**.
- **No** profile subpages (unless you later want a minimal `/direct/<slug>/` that just redirects or shows name + single link; keeps backlink URL stable).

So: one page, one list, every row is “Name — direct link”. No intermediation.

### Data: one source of truth

- **Option 1 — Reuse existing:** Keep `NEWS_SOURCES` entries with `type: 'creator'` (or a new type `direct_link`). Pipeline already has names and URLs. Generate one JSON (e.g. `direct_links.json`) with `name`, `url`, optional `description`. Page reads that. When you add a creator source, they appear here automatically; link is their `url` or derived from `feed_url` (their real site, not feed path).
- **Option 2 — Dedicated list:** New dict in `const.py`, e.g. `DIRECT_LINKS` or `DEVELOPER_DIRECTORY`: people/sources you want to promote with a direct link. Can overlap with who’s in `NEWS_SOURCES` or not (e.g. you can list someone even if you don’t have their feed). One script generates `direct_links.json` from that. Simpler for “we link to you” messaging: this list is *only* “who we want to send people to directly.”

Recommendation: **Option 2** so the list is explicitly “people we link to directly” and isn’t tied to feed logic. You can still sync it with creator sources by hand or with a small script.

### Copy on the page (short)

- **Headline:** e.g. “Direct links” or “For developers”.
- **Subline:** “Developers and newsletters we link to — to their site, not to a platform.”
- **CTA:** “We link to you, not to an aggregator. Publish a tech blog or newsletter? [Get in touch](/about/) to be listed.”

That frames both readers (“here’s who we read, go to them directly”) and developers (“get listed and get direct links”).

---

## What to remove

- **Nav:** Remove “Creators” and “Devs”.
- **Pages:** Remove `/creators/` and `/devs/` (and `/devs/<slug>/` profile pages).
- **Pipeline:** Remove `generate_dev_profiles()` and `update_creator_sources_data()` from the publish flow (or keep `update_creator_sources_data` only if you still need it for something else; otherwise remove).
- **Config:** Remove `FEATURED_DEVS`. Keep `type: 'creator'` in `NEWS_SOURCES` only if you still use it for the **digest** (creator slot, scoring). The new “direct” page doesn’t have to be fed from that; it can be its own list.
- **Data/layouts:** Remove `docs/_data/devs.json`, `docs/_data/creator_sources.json` (or repurpose), `docs/devs/*.md`, `docs/creators.md`, layout `dev.html`. Remove `_includes/freshness-banner.html` from creators if it’s only there.

---

## What to add

- **One page:** e.g. `docs/direct.md` (or `for-developers.md`) with the headline, subline, CTA, and a list from `site.data.direct_links` (or whatever the JSON is called).
- **One data file:** e.g. `docs/_data/direct_links.json` — array of `{ "name", "url", optional "description" }`, generated from a new `DIRECT_LINKS` in `const.py` (or from creator sources if you prefer Option 1).
- **One nav item:** e.g. “Direct” or “For developers” in the header pointing to `/direct/`.
- **Optional:** Small script or step in pipeline that builds `direct_links.json` from `const.py` so the list is still single source of truth.

---

## Summary

- **Delete:** Devs and Creators sections (nav, pages, profiles, their data and layouts).
- **Add:** One section — one nav entry, one page: “Developer direct links”. List of names with direct URLs; short CTA for developers to get listed. One source of truth (e.g. `DIRECT_LINKS` in `const.py` → `direct_links.json`).
- **Result:** One clear place for “resources for developers” where they’re linked directly with no aggregation intermediation, and one clear place for developers to get involved and be linked.

If you tell me the exact nav label and URL you want (e.g. “Direct” → `/direct/`, or “For developers” → `/for-developers/`), I can outline the exact file and config changes next.
