# 🎨 Retro Minimal Nerd Design - UI/UX Documentation

## Design Philosophy

**Concept:** "Terminal News Feed"  
**Style:** Retro minimal nerd - Unix terminal aesthetic  
**Target:** Personal tech aggregator for engineers  
**No monetization:** Pure content focus

---

## Visual Identity

### Color Palette
```
Background:  #0a0a0a (Deep black)
Surface:     #111111 (Card background)
Border:      #333333 (Subtle borders)
Text:        #e8e8e8 (High contrast white)
Secondary:   #888888 (Muted text)
Accent:      #00ff00 (Terminal green)
Dim:         #666666 (Metadata)
```

### Typography
- **Font:** IBM Plex Mono (Google Fonts)
- **Style:** Monospace throughout (terminal aesthetic)
- **Sizes:** 
  - Base: 14px
  - Hero title: 1.4rem
  - Archive title: 1rem
  - Metadata: 0.75rem

### Iconography
- Minimal use of icons
- ASCII art aesthetic: `→`, `▶`, `$`, `//`
- No images in UI chrome

---

## Layout Structure

### Header
```
┌─────────────────────────────────────────────────┐
│ $ eof.news          [ai] [security] [cloud]...  │
└─────────────────────────────────────────────────┘
```

**Features:**
- Terminal prompt (`$`) prefix
- Monospace nav items
- Border buttons with hover glow
- Green accent on active state

### Hero Post (Featured)
```
┌─▶────────────────────────────────────────────────┐
│  2026-03-06 · [AI] · OpenAI Blog                 │
│                                                   │
│  Large Title Goes Here                           │
│  Description paragraph with more context...      │
│                                                   │
│  "why this was picked" - editorial note          │
│                                                   │
│  [Read article ↗]                                │
└───────────────────────────────────────────────────┘
```

**Features:**
- Left green border (accent)
- Triangle indicator (`▶`)
- Metadata in muted colors
- Bordered pill badges
- CTA button with hover glow

### Archive List
```
// archive
────────────────────────────────────────────

→ Post Title One
  2026-03-06 · [security] · Krebs on Security

→ Post Title Two  
  2026-03-05 · [cloud] · AWS Blog
```

**Features:**
- Section header with `//` comment style
- Arrow (`→`) prefix for items
- Hover: indent + background glow
- Arrow color changes on hover

### Footer
```
────────────────────────────────────────────
Description text...    [about] [sources] [rss]

eof.news // curated by algorithms, consumed by humans
```

---

## Interaction Design

### Hover States
1. **Links:** Underline appears (green)
2. **Nav items:** Border + background glow
3. **Archive items:** Indent left + subtle background
4. **Buttons:** Box shadow glow effect

### Visual Hierarchy
1. Hero post (featured block)
2. Archive list (terminal log style)
3. Metadata (muted, small)
4. Navigation (peripheral, subtle)

### Accessibility
- High contrast (white on black)
- Clear focus states
- Semantic HTML
- No reliance on color alone

---

## Responsive Behavior

### Mobile (< 768px)
- Stack header vertically
- Reduce font sizes (13px base)
- Smaller padding
- Full-width buttons
- Footer grid becomes single column

### Desktop (> 768px)
- Max width: 900px (readable line length)
- Generous padding
- Horizontal nav
- Two-column footer

---

## Design Inspirations

1. **Hacker News** - Brutal minimalism, content-first
2. **Unix Terminal** - Monospace, green accents, prompts
3. **VT100/CRT** - Retro computing aesthetic
4. **Brutalist Web** - Raw HTML, no decorations
5. **Early 2000s Tech Blogs** - Simple, functional

---

## CSS Architecture

### File Structure
```
style.scss (single file)
├── Reset & Base
├── Header (Terminal Prompt)
├── Main Content (Terminal Output)
├── Footer (Terminal End)
└── Responsive
```

### Naming Convention
- BEM-inspired but simplified
- Semantic class names
- No utility classes
- Minimal nesting

### Performance
- Single CSS file
- No frameworks
- Google Fonts (IBM Plex Mono only)
- No JavaScript for styling

---

## Key Features

✅ **No Ads** - Pure content focus  
✅ **No Cookies Banner** - Privacy-first  
✅ **No Newsletter Popup** - Non-intrusive  
✅ **No Social Widgets** - Minimal distractions  
✅ **RSS Feed** - Standard, open format  
✅ **Fast Load** - Minimal assets  
✅ **Readable** - High contrast, good spacing  
✅ **Retro Cool** - Nerd aesthetic  

---

## Future Enhancements

### v2.0 (Optional)
- [ ] Dark/Light toggle (amber/green themes)
- [ ] CRT scanline effect (subtle)
- [ ] ASCII art logo
- [ ] Terminal-style loading states
- [ ] Keyboard shortcuts (vim-style)
- [ ] Matrix rain easter egg

### Content Features
- [ ] Search (grep-style)
- [ ] Filter by niche (tabs)
- [ ] Sort by date/score
- [ ] "Load more" instead of pagination
- [ ] Bookmarks (localStorage)

---

## Design Tokens

```scss
// Colors
$bg-primary: #0a0a0a;
$bg-secondary: #111111;
$border: #333333;
$text-primary: #e8e8e8;
$text-secondary: #888888;
$accent: #00ff00;
$text-muted: #666666;

// Spacing
$space-xs: 0.25rem;
$space-sm: 0.5rem;
$space-md: 1rem;
$space-lg: 1.5rem;
$space-xl: 2rem;

// Typography
$font-mono: 'IBM Plex Mono', 'Courier New', monospace;
$font-size-base: 14px;
$font-size-small: 0.75rem;
$line-height: 1.6;

// Layout
$max-width: 900px;
$border-radius: 0; // Sharp corners
$transition: 0.2s ease;
```

---

## Implementation Notes

### Jekyll Integration
- Uses minima theme as base
- Overrides with custom SCSS
- Maintains Jekyll structure
- Compatible with GitHub Pages

### Browser Support
- Modern browsers (Chrome, Firefox, Safari, Edge)
- No IE support needed
- Progressive enhancement approach
- Graceful degradation for old browsers

### Performance Budget
- CSS: < 20KB
- Fonts: < 50KB (1 family)
- Images: None in chrome
- JavaScript: Minimal (only for analytics)

---

**Created:** 2026-03-06  
**Version:** 1.0  
**Status:** Implemented  
**Maintainer:** Personal project

