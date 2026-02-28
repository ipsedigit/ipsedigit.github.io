# Layout Consistency Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Apply a shared layout grammar (stats bar → featured → heading → list → footer) across all tracker pages.

**Architecture:** 4 targeted edits. Android and iOS changes go in their Python `_generate_page()` functions (they regenerate the page). Models and Outages are static Liquid files edited directly.

**Tech Stack:** Python string templates (android.py, ios.py, outages.py), Jekyll Liquid (docs/ai/models.md)

---

### Task 1: Android — add section heading + footer

**Files:**
- Modify: `android.py` — `_generate_page()` function

**Step 1: Add `## Latest News` heading before the article list**

In `android.py`, in `_generate_page`, change the line:
```python
        "{% for article in articles offset:1 %}",
```
to:
```python
        "## Latest News",
        "",
        "{% for article in articles offset:1 %}",
```

**Step 2: Add footer after `{% endfor %}`**

After `"{% endfor %}"`, add:
```python
        "---",
        "",
        '<p style="font-size:0.8em; color:#9ca3af;">Sources: Android Developers Blog, Kotlin Blog, ProAndroidDev &middot; Updated: {{ site.data.android.generated_at }}</p>',
        "",
```

**Step 3: Regenerate the page**

```bash
python -c "from android import publish_android; publish_android()"
```

Expected: `Page written: docs/android\index.md`

**Step 4: Verify heading and footer are present**

```bash
python -c "
content = open('docs/android/index.md').read()
assert '## Latest News' in content, 'Missing heading'
assert 'Updated:' in content, 'Missing footer'
print('OK')
"
```

Expected: `OK`

**Step 5: Commit**

```bash
git add android.py docs/android/index.md docs/_data/android.json
git commit -m "style(android): add section heading and footer for layout consistency"
```

---

### Task 2: iOS — add section heading + footer

**Files:**
- Modify: `ios.py` — `_generate_page()` function

**Step 1: Add `## Latest News` heading before the article list**

In `ios.py`, in `_generate_page`, change:
```python
        "{% for article in articles offset:1 %}",
```
to:
```python
        "## Latest News",
        "",
        "{% for article in articles offset:1 %}",
```

**Step 2: Add footer after `{% endfor %}`**

After `"{% endfor %}"`, add:
```python
        "---",
        "",
        '<p style="font-size:0.8em; color:#9ca3af;">Sources: Apple Developer News, Swift Blog, NSHipster &middot; Updated: {{ site.data.ios.generated_at }}</p>',
        "",
```

**Step 3: Regenerate the page**

```bash
python -c "from ios import publish_ios; publish_ios()"
```

Expected: `Page written: docs/ios\index.md`

**Step 4: Verify**

```bash
python -c "
content = open('docs/ios/index.md').read()
assert '## Latest News' in content, 'Missing heading'
assert 'Updated:' in content, 'Missing footer'
print('OK')
"
```

Expected: `OK`

**Step 5: Commit**

```bash
git add ios.py docs/ios/index.md docs/_data/ios.json
git commit -m "style(ios): add section heading and footer for layout consistency"
```

---

### Task 3: Models — normalize new releases card style

**Files:**
- Modify: `docs/ai/models.md:73`

**Step 1: Find the new releases card div**

Current (line 73):
```html
<div style="margin-bottom:1em; padding:0.5em 0; border-bottom:1px solid #e5e7eb;">
```

**Step 2: Replace with full border style**

Change to:
```html
<div style="margin-bottom:1em; padding:0.75em; border:1px solid #e5e7eb; border-radius:8px;">
```

**Step 3: Verify Jekyll build won't break**

```bash
python -c "
content = open('docs/ai/models.md').read()
assert 'border-bottom:1px solid' not in content, 'Old style still present'
assert 'border:1px solid #e5e7eb; border-radius:8px' in content
print('OK')
"
```

Expected: `OK`

**Step 4: Commit**

```bash
git add docs/ai/models.md
git commit -m "style(models): normalize new-releases card to full border"
```

---

### Task 4: Outages — add `---` divider before footer

**Files:**
- Modify: `outages.py` — `_generate_page()` function

**Step 1: Find the footer lines in `_generate_page`**

Current (near end of `_generate_page`):
```python
    lines += [
        "---",
        "",
        f'<p style="font-size:0.8em; color:#9ca3af;">Updated: {generated_at} &middot; Checks every 30 minutes</p>',
        "",
    ]
```

The `---` is already there. Verify the wording matches the design system standard (source attribution + updated).

**Step 2: Normalize footer wording to match other pages**

Change:
```python
        f'<p style="font-size:0.8em; color:#9ca3af;">Updated: {generated_at} &middot; Checks every 30 minutes</p>',
```
to:
```python
        f'<p style="font-size:0.8em; color:#9ca3af;">Data from statuspage.io APIs &middot; Updated: {generated_at}</p>',
```

**Step 3: Regenerate outages page**

```bash
python -c "from outages import publish_outages; publish_outages()"
```

Expected: `Page written: docs/outages\index.md`

**Step 4: Verify**

```bash
python -c "
content = open('docs/outages/index.md').read()
assert 'Data from statuspage.io' in content
assert '---' in content
print('OK')
"
```

Expected: `OK`

**Step 5: Commit**

```bash
git add outages.py docs/outages/index.md docs/_data/outages.json
git commit -m "style(outages): normalize footer wording for layout consistency"
```

---

### Task 5: Full test run

**Step 1: Run all tests**

```bash
python -m pytest tests/ -v
```

Expected: all tests pass (no test covers page template content directly, so this is a smoke check that nothing in python logic broke).

**Step 2: Verify all pages have consistent structure**

```bash
python -c "
import os
checks = [
    ('docs/android/index.md', ['## Latest News', '---', 'Updated:']),
    ('docs/ios/index.md',     ['## Latest News', '---', 'Updated:']),
    ('docs/ai/models.md',     ['---', 'Updated:', 'border:1px solid #e5e7eb; border-radius:8px']),
    ('docs/outages/index.md', ['---', 'Data from statuspage.io']),
]
for path, tokens in checks:
    content = open(path).read()
    for t in tokens:
        assert t in content, f'{path}: missing {t!r}'
print('All checks passed')
"
```

Expected: `All checks passed`
