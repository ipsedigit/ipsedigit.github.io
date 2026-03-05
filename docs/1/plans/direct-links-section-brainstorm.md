# Direct links section — brainstorm

**Goal:** One section where you link directly to developer resources so (1) they see they’re linked, (2) they’re more likely to link back to you (backlinks, “featured on”, “as seen on eof.news”).

---

## 1. Why they might link back

- **Visibility:** They see their name/URL on your site → they notice you.
- **Direct link:** You send traffic to *their* site (not an aggregator) → they value the referral.
- **Credibility:** “Featured on eof.news” is something they can put in their footer / about / press.
- **Reciprocity:** You gave them a link; many will reciprocate with “as seen on” or “read more at eof.news”.
- **Stable URL:** If each has a permalink (e.g. `/direct/julia-evans`), they can link to “my page on eof.news” and you get a dofollow backlink to a relevant URL.

So the section should: **list them by name with a direct link**, and optionally **give each a stable permalink** they can cite.

---

## 2. Naming (nav + page title)

Options — pick one that fits your tone:

| Label | Vibe | Use when |
|-------|------|----------|
| **Direct** | Short, “no intermediation” | You want minimal, one word |
| **Who we link to** | Explicit | You want “we link to you” front and center |
| **Developer links** | Audience + intent | You want “for developers” and “links” |
| **Voices** | Editorial, human | You want “people, not platforms” |
| **For developers** | CTA / audience | You want it to read like a resource page for devs |
| **Featured** | Classic “we highlight you” | You’re ok with a bit of “curated list” feel |

Recommendation: **“Direct”** or **“Who we link to”** — both say “we link to you” without sounding like a directory. Reserve **“For developers”** for the subline/description if you want that audience in the copy.

---

## 3. What the page shows

**Minimum (must-have):**
- **List:** Name (or publication name) → link to their site (blog, newsletter, etc.). No aggregator URL; their real destination.
- **One line of copy:** “We link to you directly. If we’ve featured your work, you’re here. Want to be listed? [Get in touch](/about/).”

**Nice-to-have:**
- **One-line description per person/source** (e.g. “Writes about systems and debugging”) so the page is useful for readers and shows you care.
- **Stable permalink per entry** (e.g. `/direct/julia-evans`) so they can link to “my page on eof.news” → better backlinks and tracking.
- **“Featured in our digest”** or **“We’ve curated N posts from them”** (if you have that data) so they see concrete value.

**Avoid (for this section):**
- “Recent posts” or “latest from them” — that’s aggregation; keep that on the home/digest. This page is only “who we link to” and “where to find them.”

---

## 4. Data: how you maintain the list

**Option A — Manual list in code**  
- One dict in `const.py`, e.g. `DIRECT_LINKS = { 'julia-evans': { 'name': 'Julia Evans', 'url': 'https://jvns.ca', 'description': '...' }, ... }`.
- A small script (or a step in the pipeline) writes `docs/_data/direct_links.json` and, if you want permalinks, generates `docs/direct/<slug>.md` (minimal page: name, link, description, “We link to you — [link back to eof.news](/)”).
- You add/remove people by editing `const.py`. Full control.

**Option B — Derive from existing sources**  
- Reuse `NEWS_SOURCES` where `type == 'creator'` (or a new type). Build the “direct links” list from that (name, url from feed). No separate list, but the list is “who we pull from” not “who we want to promote for backlinks” — so you can’t easily add someone you don’t have a feed for.

**Option C — Hybrid**  
- “Direct links” = its own list in `const.py` (DIRECT_LINKS). Can overlap with creator sources or not. You can list someone even if you don’t have their feed (e.g. “we recommend them, here’s their link”). Pipeline generates JSON + optional profile pages from this list only.

Recommendation: **Option A or C** — a dedicated list so the section is explicitly “people we link to and want to get link-backs from,” not “everyone in our RSS.”

---

## 5. Maximizing “they link back”

- **Stable URL per person:** e.g. `/direct/julia-evans` so they can put “Featured on [eof.news/direct/julia-evans](https://ipsedigit.github.io/direct/julia-evans)” in their footer/about. One URL = one backlink.
- **Clear CTA on the page:** “We link to you. Link back? Add ‘As seen on [eof.news](/)’ or link to your page here.” (Optional: add a small “link back” badge they can use.)
- **Email them (optional):** When you add someone, a short email: “We added you to our direct links page: [link]. If you’d like to link back, here’s our site / your page.” Increases chance they notice and reciprocate.
- **About/press for them:** On their permalink page, one line: “You’re featured on eof.news. Link to this page from your site: [permalink].” Makes it easy to copy-paste.

---

## 6. Where it lives

- **Nav:** One entry, e.g. “Direct” or “Who we link to” between existing items (e.g. after Models, before Topics/Sources if you have those).
- **URL:** `/direct/` for the list; `/direct/<slug>/` for each person if you add permalinks.
- **Homepage:** Optional short line in the intro or quick-nav: “We link to developers directly → [Direct](/direct/).”

---

## 7. Scope of the list

- **Only people you’ve curated from** (current creator-type sources) — smaller, coherent list.
- **Or broader:** add OSS maintainers, book authors, speakers you don’t have a feed for — “people we recommend,” link to their site, hope they link back when they see it.

Start small (e.g. 5–10 names from your current creator sources), then add more as you want.

---

## 8. Summary: minimal version to ship

1. **One page** at `/direct/`: title “Direct” or “Who we link to”, subline “We link to developers and newsletters directly — to their site, not to a platform.”
2. **List** from data: name → direct URL; optional one-line description.
3. **CTA:** “We link to you. Want to be listed or link back? [Get in touch](/about/).”
4. **Data:** `DIRECT_LINKS` in `const.py` → script or pipeline step writes `docs/_data/direct_links.json`. Jekyll reads it and renders the list.
5. **Nav:** Add “Direct” (or chosen label) in the header.

**Later (if you want more backlinks):** Add per-person permalinks (`/direct/<slug>/`) and a line on each: “Link to this page from your site: [url].”

**Reaching weirdo / indie devs:** See `reaching-weirdo-developers.md` for where they hang out (Handmade Network, IndieWeb, indieblog.page, ooh.directory, Bluesky/Mastodon, etc.) and how to get listed there so they find you.

If you tell me your preferred **nav label** and **URL** (e.g. “Direct” → `/direct/`), I can outline the exact files and code changes next.
