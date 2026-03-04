# Redefining Devs and Creators sections

**Status:** Proposal — home, GitHub, CVEs, models are fine; devs and creators need a clear redefinition.

---

## Current state (why it’s confusing)

| Aspect | **Creators** (`/creators/`) | **Devs** (`/devs/`, `/devs/<slug>/`) |
|--------|------------------------------|--------------------------------------|
| **Data source** | Auto: `NEWS_SOURCES` where `type == 'creator'` → `creator_sources.json` | Manual: `FEATURED_DEVS` in `const.py` → `devs.json` + generated `devs/<slug>.md` |
| **Content** | (1) Grid of creator *sources* (name, link), (2) “Recent from creators” (posts with `source_type: creator`) | (1) Grid of *people* (name, bio, link), (2) Per-person profile page with “Posts curated on eof.news” |
| **Purpose (intended)** | “Sources we pull from” + stream of creator posts | “Featured people” with profile pages for backlinks/SEO |
| **Overlap** | Same people as devs (Julia Evans, Dan Luu, Pragmatic Engineer, etc.) | Same people as creators + ByteByteGo (who is `se_blog`, not `creator`) |
| **Fed by** | Pipeline: creator slot + `update_creator_sources_data()` | Pipeline: `generate_dev_profiles()` on every `publish_news()` |

**Problems:**
- Two sections describe almost the same set of people (“indie creators / newsletter authors we feature”).
- Creators = list of *sources*; Devs = list of *people* with profiles. Visitor can’t tell why someone is on one page and not the other.
- Two sources of truth: `NEWS_SOURCES` (creator type) vs `FEATURED_DEVS`. Keeping them in sync is manual (e.g. add to both when adding a new creator).

---

## Option A: One section — “Creators” (merge devs into creators)

**Idea:** Have a single “people/sources we curate from” section.

- **Single page:** `/creators/` (or rename to “People” / “Voices”).
- **Content:**
  - List of creators (name, optional one-line bio, link). Data from one place: e.g. extend `creator_sources.json` with optional `bio` from `const.py` (one config only).
  - “Recent from creators” stays (posts with `source_type == 'creator'`).
- **Profile pages:** Either drop them, or generate them from the same single list (e.g. every creator with a `slug` gets a `/creators/<slug>/` page with bio + “Posts we picked from this creator”). No separate “devs” concept.
- **Data:** One source of truth. Either:
  - **A1:** Only `NEWS_SOURCES` (type `creator`). Add optional `bio` and `slug` to each creator source in `const.py`; generate profile pages only for those with `slug`. No `FEATURED_DEVS`.
  - **A2:** Keep a single list in `const.py` (e.g. `CREATOR_PROFILES` or extended creator entries) that drives both “who we pull from” (feeds) and “who gets a profile” (slug + bio). Pipeline generates one JSON + profile pages from that.

**Pros:** One concept, one nav item, no overlap. **Cons:** Loses a separate “featured” tier unless you model it inside the single list (e.g. “featured” = has profile page).

---

## Option B: Two sections, clear roles

**Idea:** Creators = *sources* (feeds we read). Devs = *people we spotlight* (profiles + curated posts).

### Creators — “Sources we read”

- **Purpose:** “Newsletters and indie blogs we pull from.” Emphasis on *where* content comes from, not on the person’s profile.
- **URL:** `/creators/` (or “Newsletters” / “Indie sources”).
- **Content:**
  - List of sources: name, link (and optional one-line description). **Only** from `NEWS_SOURCES` with `type: 'creator'`. No bios, no profile pages.
  - “Recent from creators”: last N posts with `source_type == 'creator'`.
- **Data:** Only `creator_sources.json` (from pipeline). No `FEATURED_DEVS` for this page.
- **UX:** Lightweight directory + stream. “Subscribe to them / read them; we also surface their best on our digest.”

### Devs — “Featured builders”

- **Purpose:** “People we spotlight” — permanent profile pages for backlinks, SEO, and “who we recommend.” Not tied to “do we have a feed for them.”
- **Content:**
  - Directory: cards (name, short bio, link to profile).
  - Profile page: bio, link to their site, “Posts we’ve curated from them” (if any; `source` match), optional “Featured since” etc.
- **Data:** Single source: `FEATURED_DEVS` in `const.py`. Can include:
  - People who *are* creator sources (Julia Evans, Dan Luu, …) so they get a profile and their creator posts show under “Posts we’ve curated.”
  - People who are *not* in our feeds (e.g. conference speakers, OSS maintainers, book authors) — profile is “spotlight” only, “Posts we’ve curated” may be empty.
- **Separation:** A “creator” (source we pull from) may or may not be a “featured dev” (has profile). A “featured dev” may or may not be a creator source. So: two lists, two purposes. No need to keep them identical.

**Pros:** Clear mental model: creators = input sources, devs = output spotlight. **Cons:** Two nav items and two lists to maintain (by design).

---

## Recommendation

**Option B** is the better fit if you want to keep both sections and make them “decent”:

1. **Creators** = input/sources only: “Who we read” (feeds + recent posts). No profiles, no `FEATURED_DEVS` here. Single source of truth: `NEWS_SOURCES` (type `creator`) → `creator_sources.json`.
2. **Devs** = output/spotlight: “Who we recommend” (directory + profile pages, optional “posts we’ve curated”). Single source of truth: `FEATURED_DEVS`. No need to mirror creator list; can include non-creator people.

Then:

- **Rename / copy:** Consider nav label “Creators” → “Newsletters” or “Indie sources” so it’s clearly “sources we read.” Keep “Devs” as “Featured builders” or “People” so it’s clearly “people we spotlight.”
- **Copy on pages:** On `/creators/`: short line like “Newsletters and indie blogs we pull from. When we feature a piece, it appears on the homepage and below.” On `/devs/`: “People we spotlight — indie developers, authors, and voices we recommend. Each has a profile and, when we’ve curated their work, links to it.”
- **Implementation:** (1) Strip from creators page any notion of “featured” or profile; remove `FEATURED_DEVS` from creator data. (2) Keep devs fully driven by `FEATURED_DEVS`; profile page stays “Posts curated on eof.news” by `source` match. (3) Optionally add a `CREATOR_SOURCE_KEY` or `source_name` in `FEATURED_DEVS` so “Posts we’ve curated” uses the same name as in posts (already done via `source_name`).

---

## Implementation checklist (Option B)

- [ ] **Creators page:** Remove any reference to “featured” or profiles. Keep: source list from `creator_sources.sources`, “Recent from creators” from posts. Optional: add one-line descriptions per source if you add them to `const.py` and to `update_creator_sources_data()`.
- [ ] **Creators nav/label:** Consider “Newsletters” or “Indie sources” and align title/description.
- [ ] **Devs page:** Clarify copy: “Featured builders” / “People we spotlight.” Keep directory + profile pages driven only by `FEATURED_DEVS`.
- [ ] **Devs data:** Keep `FEATURED_DEVS` as the single source; ensure `source_name` matches post `source` for “Posts curated on eof.news.” Optionally add non-creator people (e.g. OSS maintainers) who don’t have a feed.
- [ ] **Pipeline:** No change to `update_creator_sources_data()` (already uses only `NEWS_SOURCES`). Keep `generate_dev_profiles()` for devs. No coupling between the two.
- [ ] **Optional:** Add `docs/plans/` or README note that “Creators = sources we read; Devs = people we spotlight” so future edits stay consistent.

---

If you confirm Option A (merge) or Option B (and any naming preferences), next step is to apply the chosen redefinition to the site and code.
