# eof.news Brand Identity Design
Date: 2026-02-28

## Goal
Replace the ipsedigit placeholder logo with a proper eof.news brand mark, and add a homepage hero banner that establishes the site identity.

## Brand Direction
- Minimal & dark — professional, not gimmicky terminal
- Monospace font (`eof` wordmark)
- Dark `#111` background, white text, muted `.news` in `#888`

## Logo SVG
**File:** `docs/assets/images/logo.svg`

Dark `#111` rounded square, white bold `eof` text in monospace. Used in the site nav at 28×28px. Scales to any size cleanly.

## Favicon
**File:** `docs/assets/images/favicon.svg`

Same mark as logo. Modern browsers support SVG favicons natively. Referenced in `head.html`.

## Homepage Hero
**File:** `docs/index.html`

- Switch `layout: page` → `layout: base` (removes auto-generated `<h1>`)
- Full-width dark band (`#111`) at top of content
- Large `eof` in white + `.news` in muted gray `#888`, monospace, bold
- No tagline, no links — just the brand mark
- Below: existing featured article card, then article list

## Files Changed
| File | Action |
|------|--------|
| `docs/assets/images/logo.svg` | Create |
| `docs/assets/images/favicon.svg` | Create |
| `docs/_includes/header.html` | Modify: `logo.png` → `logo.svg` |
| `docs/_includes/head.html` | Modify: favicon reference → `favicon.svg` |
| `docs/index.html` | Modify: layout + hero section |

## Out of Scope
- Redesigning the nav bar
- Adding tagline or section links to hero
- Changing non-homepage pages
