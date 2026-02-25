# Two-Pass Article Selection Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Replace the current score-greedy, single-niche-per-run article selection with a two-pass system that guarantees niche balance, content type diversity, and a tight daily budget of 10-12 posts.

**Architecture:** Each workflow run reads the day's published state, then applies a two-pass algorithm: Pass 1 fills guaranteed niche slots (1 best per niche + 1 creator), Pass 2 fills open slots by score with type diversity constraints. The workflow no longer rotates niches — every run considers all niches.

**Tech Stack:** Python 3, feedparser, requests, bs4 (no new dependencies)

---

### Task 1: Add constants for two-pass selection to `const.py`

**Files:**
- Modify: `const.py:1-9` (publishing strategy section)

**Step 1: Write the failing test**

Create file `tests/test_const.py`:

```python
from const import (
    CONTENT_TYPE_PATTERNS,
    MIN_SCORE,
    MIN_SCORE_FALLBACK,
    DAILY_TARGET,
    DAILY_MINIMUM,
    MAX_PER_TYPE,
    MAX_POSTS_PER_NICHE_PER_DAY,
)


def test_constants_exist_and_are_sane():
    assert MIN_SCORE == 70
    assert MIN_SCORE_FALLBACK == 60
    assert DAILY_TARGET == 12
    assert DAILY_MINIMUM == 8
    assert MAX_PER_TYPE == 4
    assert MAX_POSTS_PER_NICHE_PER_DAY == 3

    assert 'breaking' in CONTENT_TYPE_PATTERNS
    assert 'deep' in CONTENT_TYPE_PATTERNS
    assert 'community' in CONTENT_TYPE_PATTERNS

    # Each content type has a list of regex patterns
    for ctype, patterns in CONTENT_TYPE_PATTERNS.items():
        assert isinstance(patterns, list)
        assert len(patterns) > 0
```

**Step 2: Run test to verify it fails**

Run: `cd /c/repo/ipsedigit.github.io && python -m pytest tests/test_const.py -v`
Expected: FAIL with ImportError (CONTENT_TYPE_PATTERNS not found)

**Step 3: Write minimal implementation**

Add to `const.py` after line 8 (`DAILY_CATEGORIES_FILE`):

```python
# --- Two-pass selection budget ---
MIN_SCORE = 70               # Quality floor (raised from 50)
MIN_SCORE_FALLBACK = 60      # Fallback floor on slow news days
DAILY_TARGET = 12            # Hard cap: max posts per day
DAILY_MINIMUM = 8            # Soft floor: lower quality threshold if below this

MAX_PER_TYPE = 4             # Max posts of one content type per day

# Content type detection patterns (checked in priority order by classify_content_type)
CONTENT_TYPE_PATTERNS = {
    'community': [
        r'show\s+hn',
        r'open.?source',
        r'built\s+a\b',
        r'side\s+project',
    ],
    'breaking': [
        r'(announce|launch|releas|introduc)',
        r'(vulnerab|exploit|breach|CVE-|zero.?day)',
        r'(hack|leak|attack|incident)',
    ],
    'deep': [
        r'(paper|arxiv|research|benchmark)',
        r'(how\s+we|architecture|deep\s+dive)',
        r'(tutorial|guide|case\s+study)',
        r'(system\s+design|scalab|pattern)',
    ],
}
```

**Step 4: Run test to verify it passes**

Run: `cd /c/repo/ipsedigit.github.io && python -m pytest tests/test_const.py -v`
Expected: PASS

**Step 5: Commit**

```bash
git add tests/test_const.py const.py
git commit -m "feat: add two-pass selection constants and content type patterns"
```

---

### Task 2: Implement `classify_content_type()` in `news.py`

**Files:**
- Modify: `news.py` (add new function after `identify_subniche`)
- Create: `tests/test_classify_content_type.py`

**Step 1: Write the failing test**

Create file `tests/test_classify_content_type.py`:

```python
from news import classify_content_type


def test_creator_source_is_community():
    entry = {'title': 'How I Built My Startup', 'source_type': 'creator', 'tags': []}
    assert classify_content_type(entry) == 'community'


def test_show_hn_is_community():
    entry = {'title': 'Show HN: A new terminal emulator', 'source_type': 'aggregator', 'tags': []}
    assert classify_content_type(entry) == 'community'


def test_announcement_is_breaking():
    entry = {'title': 'OpenAI launches GPT-5', 'source_type': 'research_blog', 'tags': []}
    assert classify_content_type(entry) == 'breaking'


def test_vulnerability_is_breaking():
    entry = {'title': 'Critical vulnerability in OpenSSL', 'source_type': 'news', 'tags': []}
    assert classify_content_type(entry) == 'breaking'


def test_cve_is_breaking():
    entry = {'title': 'CVE-2026-1234: Remote code execution', 'source_type': 'security', 'tags': []}
    assert classify_content_type(entry) == 'breaking'


def test_research_paper_is_deep():
    entry = {'title': 'New arxiv paper on attention mechanisms', 'source_type': 'news', 'tags': []}
    assert classify_content_type(entry) == 'deep'


def test_how_we_is_deep():
    entry = {'title': 'How we scaled to 1M websocket connections', 'source_type': 'corporate_blog', 'tags': []}
    assert classify_content_type(entry) == 'deep'


def test_tutorial_is_deep():
    entry = {'title': 'A complete guide to Kubernetes networking', 'source_type': 'news', 'tags': []}
    assert classify_content_type(entry) == 'deep'


def test_research_blog_source_is_deep():
    entry = {'title': 'Improving language model efficiency', 'source_type': 'research_blog', 'tags': []}
    assert classify_content_type(entry) == 'deep'


def test_se_blog_source_is_deep():
    entry = {'title': 'Thoughts on software complexity', 'source_type': 'se_blog', 'tags': []}
    assert classify_content_type(entry) == 'deep'


def test_security_source_with_threat_is_breaking():
    entry = {'title': 'New ransomware campaign targets hospitals', 'source_type': 'security', 'tags': []}
    assert classify_content_type(entry) == 'breaking'


def test_generic_news_defaults_to_breaking():
    entry = {'title': 'Google acquires startup for $2B', 'source_type': 'news', 'tags': []}
    assert classify_content_type(entry) == 'breaking'


def test_built_a_is_community():
    entry = {'title': 'I built a CLI tool for managing dotfiles', 'source_type': 'aggregator', 'tags': []}
    assert classify_content_type(entry) == 'community'
```

**Step 2: Run test to verify it fails**

Run: `cd /c/repo/ipsedigit.github.io && python -m pytest tests/test_classify_content_type.py -v`
Expected: FAIL with ImportError (classify_content_type not found)

**Step 3: Write minimal implementation**

Add to `news.py` after the `identify_subniche` function (after line 319), and add `CONTENT_TYPE_PATTERNS` to the imports from const:

Update import line to include `CONTENT_TYPE_PATTERNS`:
```python
from const import (
    NEWS_SOURCES,
    PUBLISHED_NEWS_FILE_NAME,
    CONTENT_CATEGORIES,
    NICHE_CATEGORIES,
    MAX_POSTS_PER_NICHE_PER_DAY,
    CREATOR_MAX_PER_DAY,
    DAILY_CATEGORIES_FILE,
    TITLE_BONUS,
    TITLE_PENALTY,
    NICHE_SUBNICHES,
    CONTENT_TYPE_PATTERNS,
    MIN_SCORE,
    MIN_SCORE_FALLBACK,
    DAILY_TARGET,
    DAILY_MINIMUM,
    MAX_PER_TYPE,
)
```

Add function:
```python
# Security threat keywords for source_type=='security' detection
_SECURITY_THREAT_RE = re.compile(
    r'(malware|ransomware|trojan|botnet|campaign|apt|breach|hack|attack|incident|exploit)',
    re.IGNORECASE,
)


def classify_content_type(entry):
    """Classify an article as 'breaking', 'deep', or 'community'.

    Priority order:
    1. creator source_type → community
    2. Title matches community patterns → community
    3. Title matches breaking patterns → breaking
    4. Title matches deep patterns → deep
    5. research_blog / se_blog source_type → deep
    6. security source with threat keywords → breaking
    7. Default → breaking
    """
    source_type = entry.get('source_type', '')
    title = entry.get('title', '')

    # 1. Creator sources are always community
    if source_type == 'creator':
        return 'community'

    # 2. Community title patterns
    for pattern in CONTENT_TYPE_PATTERNS['community']:
        if re.search(pattern, title, re.IGNORECASE):
            return 'community'

    # 3. Breaking title patterns
    for pattern in CONTENT_TYPE_PATTERNS['breaking']:
        if re.search(pattern, title, re.IGNORECASE):
            return 'breaking'

    # 4. Deep title patterns
    for pattern in CONTENT_TYPE_PATTERNS['deep']:
        if re.search(pattern, title, re.IGNORECASE):
            return 'deep'

    # 5. Source type fallbacks
    if source_type in ('research_blog', 'se_blog'):
        return 'deep'

    # 6. Security source with threat keywords
    if source_type == 'security' and _SECURITY_THREAT_RE.search(title):
        return 'breaking'

    # 7. Default
    return 'breaking'
```

**Step 4: Run test to verify it passes**

Run: `cd /c/repo/ipsedigit.github.io && python -m pytest tests/test_classify_content_type.py -v`
Expected: all 13 tests PASS

**Step 5: Commit**

```bash
git add tests/test_classify_content_type.py news.py const.py
git commit -m "feat: add classify_content_type() for breaking/deep/community detection"
```

---

### Task 3: Implement `get_daily_state()` helper in `news.py`

**Files:**
- Modify: `news.py` (refactor `get_today_subniches` → `get_daily_state`)
- Create: `tests/test_daily_state.py`

**Step 1: Write the failing test**

Create file `tests/test_daily_state.py`:

```python
import os
import tempfile
from unittest.mock import patch
from datetime import date


def test_get_daily_state_empty(tmp_path):
    state_file = str(tmp_path / "daily.txt")
    with patch('news.DAILY_CATEGORIES_FILE', state_file):
        from news import get_daily_state
        state = get_daily_state()

    assert state['subniches'] == []
    assert state['niche_counts'] == {}
    assert state['type_counts'] == {'breaking': 0, 'deep': 0, 'community': 0}
    assert state['total'] == 0


def test_get_daily_state_with_entries(tmp_path):
    state_file = str(tmp_path / "daily.txt")
    today = date.today().isoformat()
    with open(state_file, 'w') as f:
        f.write(f"{today}:ai:llm:breaking\n")
        f.write(f"{today}:security:malware:breaking\n")
        f.write(f"{today}:cloud:kubernetes:deep\n")
        f.write("2020-01-01:ai:old:breaking\n")  # old entry, should be ignored

    with patch('news.DAILY_CATEGORIES_FILE', state_file):
        from news import get_daily_state
        state = get_daily_state()

    assert state['total'] == 3
    assert state['niche_counts'] == {'ai': 1, 'security': 1, 'cloud': 1}
    assert state['type_counts'] == {'breaking': 2, 'deep': 1, 'community': 0}
    assert 'ai:llm' in state['subniches']
    assert 'security:malware' in state['subniches']
    assert 'cloud:kubernetes' in state['subniches']


def test_get_daily_state_file_missing(tmp_path):
    with patch('news.DAILY_CATEGORIES_FILE', str(tmp_path / "nonexistent.txt")):
        from news import get_daily_state
        state = get_daily_state()

    assert state['total'] == 0
```

**Step 2: Run test to verify it fails**

Run: `cd /c/repo/ipsedigit.github.io && python -m pytest tests/test_daily_state.py -v`
Expected: FAIL with ImportError (get_daily_state not found)

**Step 3: Write minimal implementation**

Replace `get_today_subniches()` in `news.py` (lines 388-408) with:

```python
def get_daily_state():
    """Read today's published state. Returns dict with subniches, niche_counts, type_counts, total."""
    state = {
        'subniches': [],       # e.g. ['ai:llm', 'security:malware']
        'niche_counts': {},    # e.g. {'ai': 2, 'security': 1}
        'type_counts': {'breaking': 0, 'deep': 0, 'community': 0},
        'total': 0,
    }
    try:
        if not os.path.exists(DAILY_CATEGORIES_FILE):
            return state

        with open(DAILY_CATEGORIES_FILE, 'r') as f:
            lines = f.read().strip().split('\n')

        today_str = date.today().isoformat()
        for line in lines:
            if not line.startswith(today_str):
                continue
            # Format: "2026-02-25:niche:subniche:content_type"
            parts = line[len(today_str) + 1:].split(':')  # skip date prefix
            if len(parts) >= 3:
                niche, subniche, content_type = parts[0], parts[1], parts[2]
                state['subniches'].append(f"{niche}:{subniche}")
                state['niche_counts'][niche] = state['niche_counts'].get(niche, 0) + 1
                if content_type in state['type_counts']:
                    state['type_counts'][content_type] += 1
                state['total'] += 1
            elif len(parts) >= 2:
                # Legacy format: "niche:subniche" (no content_type)
                niche, subniche = parts[0], parts[1]
                state['subniches'].append(f"{niche}:{subniche}")
                state['niche_counts'][niche] = state['niche_counts'].get(niche, 0) + 1
                state['total'] += 1

    except Exception:
        pass

    return state


def get_today_subniches():
    """Legacy wrapper — returns list of sub-niches published today."""
    return get_daily_state()['subniches']
```

**Step 4: Run test to verify it passes**

Run: `cd /c/repo/ipsedigit.github.io && python -m pytest tests/test_daily_state.py -v`
Expected: all 3 tests PASS

**Step 5: Commit**

```bash
git add tests/test_daily_state.py news.py
git commit -m "feat: add get_daily_state() for tracking niche counts and content types"
```

---

### Task 4: Update `track_daily_subniche()` to include content type

**Files:**
- Modify: `news.py` (`track_daily_subniche` function, lines 411-415)

**Step 1: Write the failing test**

Create file `tests/test_track_daily.py`:

```python
import os
from unittest.mock import patch
from datetime import date


def test_track_writes_content_type(tmp_path):
    state_file = str(tmp_path / "daily.txt")
    with patch('news.DAILY_CATEGORIES_FILE', state_file):
        from news import track_daily_subniche
        track_daily_subniche('ai', 'llm', 'breaking')

    with open(state_file) as f:
        content = f.read()

    today = date.today().isoformat()
    assert f"{today}:ai:llm:breaking\n" in content


def test_track_appends_multiple(tmp_path):
    state_file = str(tmp_path / "daily.txt")
    with patch('news.DAILY_CATEGORIES_FILE', state_file):
        from news import track_daily_subniche
        track_daily_subniche('ai', 'llm', 'breaking')
        track_daily_subniche('security', 'malware', 'deep')

    with open(state_file) as f:
        lines = f.read().strip().split('\n')

    assert len(lines) == 2
```

**Step 2: Run test to verify it fails**

Run: `cd /c/repo/ipsedigit.github.io && python -m pytest tests/test_track_daily.py -v`
Expected: FAIL with TypeError (track_daily_subniche takes 2 args, got 3)

**Step 3: Write minimal implementation**

Replace `track_daily_subniche` in `news.py`:

```python
def track_daily_subniche(niche, subniche, content_type='breaking'):
    """Track the niche:sub-niche:content_type published today."""
    today_str = date.today().isoformat()
    with open(DAILY_CATEGORIES_FILE, 'a') as f:
        f.write(f"{today_str}:{niche}:{subniche}:{content_type}\n")
```

**Step 4: Run test to verify it passes**

Run: `cd /c/repo/ipsedigit.github.io && python -m pytest tests/test_track_daily.py -v`
Expected: all 2 tests PASS

**Step 5: Commit**

```bash
git add tests/test_track_daily.py news.py
git commit -m "feat: track_daily_subniche now includes content_type"
```

---

### Task 5: Build all candidates pool (`_build_candidates`)

**Files:**
- Modify: `news.py` (extract candidate-building from `find_best_post` into `_build_candidates`)
- Create: `tests/test_build_candidates.py`

**Step 1: Write the failing test**

Create file `tests/test_build_candidates.py`:

```python
from unittest.mock import patch, MagicMock
from news import _build_candidates


def _make_entry(title, source_type, score, category, subniche, link):
    return {
        'title': title,
        'source_type': source_type,
        'score': score,
        '_category': category,
        '_subniche': subniche,
        'link': link,
        'tags': ['AI', 'Machine Learning'],
        'community_score': 0,
        'source': 'Test Source',
        'content_type': 'breaking',
    }


def test_build_candidates_filters_published():
    entries = [
        _make_entry('Published article', 'news', 80, 'ai', 'llm', 'http://published.com'),
        _make_entry('New article', 'news', 80, 'ai', 'llm', 'http://new.com'),
    ]

    with patch('news.read_text_file', return_value={'http://published.com'}):
        with patch('news._scan_all_sources', return_value=entries):
            candidates = _build_candidates()

    links = [c['link'] for c in candidates]
    assert 'http://published.com' not in links
    assert 'http://new.com' in links


def test_build_candidates_filters_below_min_score():
    entries = [
        _make_entry('Low score', 'news', 50, 'ai', 'llm', 'http://low.com'),
        _make_entry('High score', 'news', 80, 'ai', 'llm', 'http://high.com'),
    ]

    with patch('news.read_text_file', return_value=set()):
        with patch('news._scan_all_sources', return_value=entries):
            candidates = _build_candidates(min_score=70)

    assert len(candidates) == 1
    assert candidates[0]['link'] == 'http://high.com'


def test_build_candidates_sorted_by_score_desc():
    entries = [
        _make_entry('Mid', 'news', 80, 'ai', 'llm', 'http://mid.com'),
        _make_entry('Top', 'news', 120, 'security', 'malware', 'http://top.com'),
        _make_entry('Low', 'news', 71, 'cloud', 'aws', 'http://low.com'),
    ]

    with patch('news.read_text_file', return_value=set()):
        with patch('news._scan_all_sources', return_value=entries):
            candidates = _build_candidates(min_score=70)

    assert candidates[0]['score'] == 120
    assert candidates[1]['score'] == 80
    assert candidates[2]['score'] == 71
```

**Step 2: Run test to verify it fails**

Run: `cd /c/repo/ipsedigit.github.io && python -m pytest tests/test_build_candidates.py -v`
Expected: FAIL with ImportError (_build_candidates not found)

**Step 3: Write minimal implementation**

Add two new functions to `news.py`:

```python
def _scan_all_sources():
    """Scan all RSS feeds and return scored, categorized candidate entries."""
    all_entries = []

    for source_key, source in NEWS_SOURCES.items():
        try:
            feed = feedparser.parse(source['feed_url'])
            entries = extract_entries(feed, source)

            for entry in entries:
                cat = identify_category(entry)
                if cat not in NICHE_CATEGORIES:
                    continue

                subniche = identify_subniche(entry, cat)
                entry['_category'] = cat
                entry['_subniche'] = subniche
                entry['score'] = calculate_score(entry, source)
                entry['content_type'] = classify_content_type(entry)
                all_entries.append(entry)

        except Exception as e:
            print(f"   ⚠️ Error scanning {source.get('name', source_key)}: {e}")

    return all_entries


def _build_candidates(min_score=None):
    """Build sorted list of publishable candidates (not yet published, above score floor)."""
    if min_score is None:
        min_score = MIN_SCORE

    published = set(read_text_file(PUBLISHED_NEWS_FILE_NAME))
    all_entries = _scan_all_sources()

    candidates = [
        e for e in all_entries
        if e['link'] not in published and e['score'] >= min_score
    ]

    candidates.sort(key=lambda x: x['score'], reverse=True)
    return candidates
```

**Step 4: Run test to verify it passes**

Run: `cd /c/repo/ipsedigit.github.io && python -m pytest tests/test_build_candidates.py -v`
Expected: all 3 tests PASS

**Step 5: Commit**

```bash
git add tests/test_build_candidates.py news.py
git commit -m "feat: extract _scan_all_sources and _build_candidates from find_best_post"
```

---

### Task 6: Implement two-pass `select_daily_posts()`

**Files:**
- Modify: `news.py` (add `select_daily_posts` function)
- Create: `tests/test_select_daily.py`

**Step 1: Write the failing test**

Create file `tests/test_select_daily.py`:

```python
from unittest.mock import patch
from news import select_daily_posts


def _make(title, score, niche, subniche, ctype, source_type='news', link=None):
    return {
        'title': title,
        'score': score,
        '_category': niche,
        '_subniche': subniche,
        'content_type': ctype,
        'source_type': source_type,
        'source': 'Test',
        'link': link or f'http://example.com/{title.replace(" ", "-").lower()}',
        'tags': ['tag1'],
        'community_score': 0,
    }


def _empty_state():
    return {
        'subniches': [],
        'niche_counts': {},
        'type_counts': {'breaking': 0, 'deep': 0, 'community': 0},
        'total': 0,
    }


def test_pass1_selects_one_per_niche():
    candidates = [
        _make('AI top', 100, 'ai', 'llm', 'breaking'),
        _make('AI second', 90, 'ai', 'ai-research', 'deep'),
        _make('Sec top', 95, 'security', 'malware', 'breaking'),
        _make('Cloud top', 80, 'cloud', 'aws', 'deep'),
        _make('DevTools top', 85, 'devtools', 'frameworks', 'community'),
        _make('SE top', 82, 'software-engineering', 'architecture', 'deep'),
    ]

    with patch('news._build_candidates', return_value=candidates):
        with patch('news.get_daily_state', return_value=_empty_state()):
            selected = select_daily_posts()

    niches = [s['_category'] for s in selected]
    assert 'ai' in niches
    assert 'security' in niches
    assert 'cloud' in niches
    assert 'devtools' in niches
    assert 'software-engineering' in niches


def test_pass1_skips_niche_at_max():
    state = _empty_state()
    state['niche_counts'] = {'ai': 3}  # already at max
    state['subniches'] = ['ai:llm', 'ai:ai-research', 'ai:mlops']
    state['total'] = 3

    candidates = [
        _make('AI extra', 100, 'ai', 'ai-infrastructure', 'breaking'),
        _make('Sec top', 95, 'security', 'malware', 'breaking'),
    ]

    with patch('news._build_candidates', return_value=candidates):
        with patch('news.get_daily_state', return_value=state):
            selected = select_daily_posts()

    niches = [s['_category'] for s in selected]
    assert 'ai' not in niches
    assert 'security' in niches


def test_pass2_fills_open_slots():
    candidates = [
        _make('AI top', 100, 'ai', 'llm', 'breaking'),
        _make('Sec top', 95, 'security', 'malware', 'breaking'),
        _make('Cloud top', 80, 'cloud', 'aws', 'deep'),
        _make('DevTools top', 85, 'devtools', 'frameworks', 'community'),
        _make('SE top', 82, 'software-engineering', 'architecture', 'deep'),
        # Pass 2 candidates (different sub-niches)
        _make('AI bonus', 92, 'ai', 'ai-research', 'deep'),
        _make('Sec bonus', 88, 'security', 'appsec', 'deep'),
        _make('Creator post', 78, 'cloud', 'kubernetes', 'community', source_type='creator'),
    ]

    with patch('news._build_candidates', return_value=candidates):
        with patch('news.get_daily_state', return_value=_empty_state()):
            selected = select_daily_posts()

    # Should have 5 from pass1 + some from pass2
    assert len(selected) >= 5
    assert len(selected) <= 12


def test_pass2_respects_type_cap():
    # 5 breaking articles for pass1, then all pass2 candidates are breaking too
    candidates = [
        _make('AI top', 100, 'ai', 'llm', 'breaking'),
        _make('Sec top', 95, 'security', 'malware', 'breaking'),
        _make('Cloud top', 80, 'cloud', 'aws', 'breaking'),
        _make('DevTools top', 85, 'devtools', 'frameworks', 'breaking'),
        _make('SE top', 82, 'software-engineering', 'architecture', 'breaking'),
        # More breaking — should be capped
        _make('Extra1', 90, 'ai', 'ai-research', 'breaking'),
        _make('Extra2', 88, 'security', 'appsec', 'breaking'),
        # One deep — should get through
        _make('Deep1', 75, 'cloud', 'kubernetes', 'deep'),
    ]

    with patch('news._build_candidates', return_value=candidates):
        with patch('news.get_daily_state', return_value=_empty_state()):
            selected = select_daily_posts()

    type_counts = {}
    for s in selected:
        t = s['content_type']
        type_counts[t] = type_counts.get(t, 0) + 1

    # Breaking should not exceed MAX_PER_TYPE (4) in pass2
    # Pass1 can exceed it (guaranteed slots), but pass2 won't add more
    # With 5 breaking in pass1, pass2 should prefer non-breaking
    deep_selected = [s for s in selected if s['content_type'] == 'deep']
    assert len(deep_selected) >= 1


def test_no_duplicate_subniches():
    candidates = [
        _make('AI first', 100, 'ai', 'llm', 'breaking'),
        _make('AI same sub', 90, 'ai', 'llm', 'deep'),  # same subniche!
        _make('AI diff sub', 85, 'ai', 'ai-research', 'deep'),
    ]

    with patch('news._build_candidates', return_value=candidates):
        with patch('news.get_daily_state', return_value=_empty_state()):
            selected = select_daily_posts()

    ai_posts = [s for s in selected if s['_category'] == 'ai']
    subniches = [s['_subniche'] for s in ai_posts]
    assert len(subniches) == len(set(subniches)), "Duplicate sub-niches selected"
```

**Step 2: Run test to verify it fails**

Run: `cd /c/repo/ipsedigit.github.io && python -m pytest tests/test_select_daily.py -v`
Expected: FAIL with ImportError (select_daily_posts not found)

**Step 3: Write minimal implementation**

Add to `news.py`:

```python
def select_daily_posts():
    """Two-pass article selection. Returns list of selected entries (not yet published/fetched).

    Pass 1: Best article per niche (5 guaranteed slots) + best creator.
    Pass 2: Fill remaining slots by score, respecting type diversity and niche caps.
    """
    state = get_daily_state()

    if state['total'] >= DAILY_TARGET:
        print(f"⏸️ Daily target reached ({state['total']}/{DAILY_TARGET})")
        return []

    candidates = _build_candidates(min_score=MIN_SCORE)
    if not candidates:
        return []

    selected = []
    used_links = set()
    used_subniches = set(state['subniches'])
    niche_counts = dict(state['niche_counts'])
    type_counts = dict(state['type_counts'])
    total = state['total']

    def _can_select(entry):
        """Check if entry can be selected given current state."""
        link = entry['link']
        if link in used_links:
            return False
        niche = entry['_category']
        subniche = entry.get('_subniche')
        sub_key = f"{niche}:{subniche}" if subniche else niche
        if sub_key in used_subniches:
            return False
        if niche_counts.get(niche, 0) >= MAX_POSTS_PER_NICHE_PER_DAY:
            return False
        return True

    def _select(entry):
        """Mark entry as selected, update state."""
        selected.append(entry)
        used_links.add(entry['link'])
        niche = entry['_category']
        subniche = entry.get('_subniche')
        sub_key = f"{niche}:{subniche}" if subniche else niche
        used_subniches.add(sub_key)
        niche_counts[niche] = niche_counts.get(niche, 0) + 1
        ctype = entry.get('content_type', 'breaking')
        type_counts[ctype] = type_counts.get(ctype, 0) + 1
        nonlocal total
        total += 1

    # ── Pass 1: Guaranteed niche slots ──
    for niche in NICHE_CATEGORIES:
        if niche_counts.get(niche, 0) >= MAX_POSTS_PER_NICHE_PER_DAY:
            continue
        for c in candidates:
            if c['_category'] == niche and _can_select(c):
                _select(c)
                break

    # Pass 1b: Creator slot
    for c in candidates:
        if c['source_type'] == 'creator' and _can_select(c):
            _select(c)
            break

    # ── Pass 2: Open competition ──
    remaining_slots = DAILY_TARGET - total
    for c in candidates:
        if remaining_slots <= 0:
            break
        if not _can_select(c):
            continue
        ctype = c.get('content_type', 'breaking')
        if type_counts.get(ctype, 0) >= MAX_PER_TYPE:
            continue
        _select(c)
        remaining_slots -= 1

    return selected
```

**Step 4: Run test to verify it passes**

Run: `cd /c/repo/ipsedigit.github.io && python -m pytest tests/test_select_daily.py -v`
Expected: all 5 tests PASS

**Step 5: Commit**

```bash
git add tests/test_select_daily.py news.py
git commit -m "feat: implement two-pass select_daily_posts() algorithm"
```

---

### Task 7: Rewrite `publish_news()` to use two-pass selection

**Files:**
- Modify: `news.py` (`publish_news` function, lines 51-111)
- Modify: `news.py` (`create_post` function — add `content_type` to frontmatter)

**Step 1: Write the failing test**

Create file `tests/test_publish_news.py`:

```python
import os
from unittest.mock import patch, MagicMock
from news import publish_news


def _make_selected(title, score, niche, subniche, ctype, source_type='news'):
    return {
        'title': title,
        'score': score,
        '_category': niche,
        '_subniche': subniche,
        'content_type': ctype,
        'source_type': source_type,
        'source': 'Test Source',
        'link': f'http://example.com/{title.replace(" ", "-").lower()}',
        'tags': ['AI'],
        'community_score': 0,
        'preview': 'A test preview description for the article.',
        'why_picked': 'test pick',
    }


def test_publish_news_calls_create_post_for_each_selected(tmp_path):
    entries = [
        _make_selected('Article 1', 100, 'ai', 'llm', 'breaking'),
        _make_selected('Article 2', 90, 'security', 'malware', 'deep'),
    ]

    state_file = str(tmp_path / "daily.txt")
    published_file = str(tmp_path / "published.txt")

    with patch('news.select_daily_posts', return_value=entries):
        with patch('news.fetch_preview', side_effect=lambda e: e):
            with patch('news.create_post') as mock_create:
                with patch('news.track_published'):
                    with patch('news.track_daily_subniche'):
                        with patch('news.generate_tag_pages'):
                            publish_news()

    assert mock_create.call_count == 2


def test_publish_news_skips_entries_without_preview(tmp_path):
    entries = [
        _make_selected('No preview', 100, 'ai', 'llm', 'breaking'),
        _make_selected('Has preview', 90, 'security', 'malware', 'deep'),
    ]

    def fake_preview(e):
        if 'No preview' in e['title']:
            return None
        return e

    with patch('news.select_daily_posts', return_value=entries):
        with patch('news.fetch_preview', side_effect=fake_preview):
            with patch('news.create_post') as mock_create:
                with patch('news.track_published'):
                    with patch('news.track_daily_subniche'):
                        with patch('news.generate_tag_pages'):
                            publish_news()

    assert mock_create.call_count == 1
```

**Step 2: Run test to verify it fails**

Run: `cd /c/repo/ipsedigit.github.io && python -m pytest tests/test_publish_news.py -v`
Expected: FAIL (publish_news still uses old signature/logic)

**Step 3: Write minimal implementation**

Replace `publish_news` in `news.py` with:

```python
def publish_news(target_niche=None):
    """Publish articles using two-pass selection.

    If target_niche is given, falls back to single-niche mode (legacy workflow compat).
    Otherwise, uses full two-pass selection across all niches.
    """
    update_creator_sources_data()

    if target_niche:
        # Legacy single-niche mode for backward compat with workflow
        _publish_single_niche(target_niche)
        return

    selected = select_daily_posts()
    if not selected:
        print("❌ No posts selected this run")
        return

    published_count = 0
    for entry in selected:
        result = fetch_preview(entry)
        if not result:
            print(f"   ⚠️ Preview fetch failed, skipping: {entry['title'][:50]}")
            continue

        result['why_picked'] = generate_why_picked(result)
        create_post(result)
        generate_tag_pages()
        track_published(result['link'], PUBLISHED_NEWS_FILE_NAME)
        sub_key = result.get('_subniche') or result.get('_category', 'unknown')
        ctype = result.get('content_type', 'breaking')
        track_daily_subniche(result['_category'], sub_key, ctype)
        published_count += 1

        print(f"✅ [{result['_category']}] [{ctype}] Published: {result['title'][:60]}")
        print(f"   Score: {result['score']} | Source: {result['source']}")

    print(f"\n📊 Published {published_count} articles this run")


def _publish_single_niche(target_niche):
    """Legacy single-niche publish for backward compatibility with niche-rotation workflow."""
    today_entries = get_today_subniches()

    niche_entries = [e for e in today_entries if e.startswith(f"{target_niche}:") or e == target_niche]
    niche_count = len(niche_entries)

    if niche_count >= MAX_POSTS_PER_NICHE_PER_DAY:
        print(f"⏸️ [{target_niche}] Daily limit reached: {niche_count}/{MAX_POSTS_PER_NICHE_PER_DAY}")
        return

    best_post = find_best_post(exclude_subniches=today_entries, target_niche=target_niche)
    if best_post:
        create_post(best_post)
        generate_tag_pages()
        track_published(best_post['link'], PUBLISHED_NEWS_FILE_NAME)
        sub_key = best_post.get('_subniche') or best_post.get('_category', 'unknown')
        ctype = best_post.get('content_type', classify_content_type(best_post))
        track_daily_subniche(target_niche, sub_key, ctype)
        print(f"✅ [{target_niche}] Published: {best_post['title']}")
    else:
        print(f"❌ [{target_niche}] No suitable posts found")
```

Also update `create_post` in `news.py` to add `content_type` to frontmatter. After the `niche_subniche` line (line 469-470 area), add:

```python
        content_type = news.get('content_type', 'breaking')
        f.write(f'content_type: {content_type}\n')
```

**Step 4: Run test to verify it passes**

Run: `cd /c/repo/ipsedigit.github.io && python -m pytest tests/test_publish_news.py -v`
Expected: all 2 tests PASS

**Step 5: Run all tests**

Run: `cd /c/repo/ipsedigit.github.io && python -m pytest tests/ -v`
Expected: all tests PASS

**Step 6: Commit**

```bash
git add tests/test_publish_news.py news.py
git commit -m "feat: rewrite publish_news to use two-pass selection with legacy fallback"
```

---

### Task 8: Update workflow to use two-pass mode

**Files:**
- Modify: `.github/workflows/dailynewspublisher.yml`

**Step 1: Review current workflow**

The current workflow runs 15 times/day (hourly 06-20 UTC) with niche rotation.
The new workflow should:
- Run fewer times (e.g., 3-4 times/day) since each run publishes multiple articles
- Call `python main.py --action=news` WITHOUT `--niche` to trigger two-pass mode
- Keep `workflow_dispatch` with optional `--niche` for manual single-niche runs

**Step 2: Update the workflow**

Replace `.github/workflows/dailynewspublisher.yml` with:

```yaml
name: Daily News Publisher

on:
  schedule:
    # Run 4 times/day: morning, midday, afternoon, evening (UTC)
    - cron: '0 7 * * *'
    - cron: '0 11 * * *'
    - cron: '0 15 * * *'
    - cron: '0 19 * * *'
  workflow_dispatch:
    inputs:
      niche:
        description: 'Target niche (leave empty for two-pass auto-selection)'
        required: false
        default: ''

jobs:
  publish-news:
    runs-on: ubuntu-latest

    steps:
    - name: Checkout main branch
      uses: actions/checkout@v4
      with:
        ref: main

    - name: Configure Git
      run: |
        git config user.name "github-actions[bot]"
        git config user.email "github-actions[bot]@users.noreply.github.com"

    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.x'

    - name: Install Dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt

    - name: Run news publisher
      env:
        TWITTER_API_KEY: ${{ secrets.TWITTER_API_KEY }}
        TWITTER_API_SECRET: ${{ secrets.TWITTER_API_SECRET }}
        TWITTER_ACCESS_TOKEN: ${{ secrets.TWITTER_ACCESS_TOKEN }}
        TWITTER_ACCESS_SECRET: ${{ secrets.TWITTER_ACCESS_SECRET }}
        TWITTER_ENABLED: "true"
      run: |
        if [ -n "${{ github.event.inputs.niche }}" ]; then
          python main.py --action=news --niche=${{ github.event.inputs.niche }}
        else
          python main.py --action=news
        fi

    - name: Commit and Push changes
      run: |
        find . -type d -name "__pycache__" -exec rm -r {} +
        find . -name "*.pyc" -delete
        git add .
        TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')
        git commit -m "Auto: news update at ${TIMESTAMP}" || echo "No changes to commit"
        git push origin main
```

**Step 3: Commit**

```bash
git add .github/workflows/dailynewspublisher.yml
git commit -m "feat: update workflow to use two-pass selection (4 runs/day)"
```

---

### Task 9: Update `find_best_post` score threshold and add content_type

**Files:**
- Modify: `news.py` (`find_best_post` function — update score threshold from 50 to `MIN_SCORE`, add `content_type`)

**Step 1: Update `find_best_post`**

In `find_best_post`, change line `if entry['score'] < 50:` to:

```python
                entry['content_type'] = classify_content_type(entry)

                if entry['score'] < MIN_SCORE:
                    continue
```

This ensures the legacy single-niche path also uses the raised quality floor and tags content types.

**Step 2: Run all tests**

Run: `cd /c/repo/ipsedigit.github.io && python -m pytest tests/ -v`
Expected: all tests PASS

**Step 3: Commit**

```bash
git add news.py
git commit -m "feat: update find_best_post to use MIN_SCORE and classify content type"
```

---

### Task 10: Add `tests/__init__.py` and verify full test suite

**Files:**
- Create: `tests/__init__.py` (empty, for Python package)

**Step 1: Create init file**

```python
# tests package
```

**Step 2: Run full test suite**

Run: `cd /c/repo/ipsedigit.github.io && python -m pytest tests/ -v --tb=short`
Expected: all tests PASS (should be ~28 tests across 6 files)

**Step 3: Commit**

```bash
git add tests/__init__.py
git commit -m "chore: add tests package init"
```

---

## Summary

| Task | What | Files |
|------|------|-------|
| 1 | Constants for two-pass | `const.py`, `tests/test_const.py` |
| 2 | `classify_content_type()` | `news.py`, `tests/test_classify_content_type.py` |
| 3 | `get_daily_state()` | `news.py`, `tests/test_daily_state.py` |
| 4 | Update `track_daily_subniche()` | `news.py`, `tests/test_track_daily.py` |
| 5 | `_build_candidates()` | `news.py`, `tests/test_build_candidates.py` |
| 6 | `select_daily_posts()` | `news.py`, `tests/test_select_daily.py` |
| 7 | Rewrite `publish_news()` | `news.py`, `tests/test_publish_news.py` |
| 8 | Update workflow | `.github/workflows/dailynewspublisher.yml` |
| 9 | Update `find_best_post` threshold | `news.py` |
| 10 | Test package init + full suite | `tests/__init__.py` |
