"""
Weekly Tech Digest generator.
Reads posts from the past 7 days, picks top stories per niche,
writes docs/_data/digest.json, updates digest_archive.json,
and generates docs/digest/index.md.
No longer writes to docs/_posts/.
"""
import json
import os
from datetime import datetime, timezone

from post_parser import get_recent_posts
from const import NICHE_CATEGORIES

DATA_DIR = "docs/_data"
OUTPUT_JSON = os.path.join(DATA_DIR, "digest.json")
ARCHIVE_JSON = os.path.join(DATA_DIR, "digest_archive.json")
OUTPUT_DIR = "docs/digest"
OUTPUT_PAGE = os.path.join(OUTPUT_DIR, "index.md")
ARCHIVE_KEEP_WEEKS = 12

NICHE_LABELS = {
    'ai': 'AI',
    'software-engineering': 'Software Engineering',
    'devtools': 'Developer Tools',
    'cloud': 'Cloud & Infrastructure',
    'security': 'Security',
}

NICHE_COLORS = {
    'ai': '#7c3aed',
    'software-engineering': '#d97706',
    'devtools': '#059669',
    'cloud': '#0284c7',
    'security': '#dc2626',
}


def _pick_featured(posts):
    """Top 2 per niche (up to 10 total), filled from overall top-scored remainder."""
    featured = []
    featured_urls = set()

    for niche in NICHE_CATEGORIES:
        niche_posts = sorted(
            [p for p in posts if p['niche_category'] == niche],
            key=lambda p: p['score'], reverse=True
        )[:2]
        for p in niche_posts:
            if p['external_url'] not in featured_urls:
                featured.append(p)
                featured_urls.add(p['external_url'])

    remaining = sorted(
        [p for p in posts if p['external_url'] not in featured_urls],
        key=lambda p: p['score'], reverse=True
    )
    for p in remaining:
        if len(featured) >= 10:
            break
        featured.append(p)
        featured_urls.add(p['external_url'])

    return featured


def _stories_to_dicts(featured):
    """Convert post dicts to serializable story dicts."""
    return [
        {
            'title': p['title'],
            'url': p['external_url'],
            'description': p.get('description', ''),
            'source': p.get('source', ''),
            'niche': p.get('niche_category', ''),
            'niche_label': NICHE_LABELS.get(p.get('niche_category', ''), ''),
            'score': p.get('score', 0),
        }
        for p in featured
    ]


def _load_archive():
    """Load archive. Returns list of past week dicts."""
    if os.path.exists(ARCHIVE_JSON):
        try:
            with open(ARCHIVE_JSON, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            pass
    return []


def _save_archive(archive, current_week):
    """Prepend current week to archive, keep last ARCHIVE_KEEP_WEEKS."""
    archive = [w for w in archive if w.get('week_of') != current_week['week_of']]
    archive.insert(0, current_week)
    archive = archive[:ARCHIVE_KEEP_WEEKS]
    with open(ARCHIVE_JSON, 'w', encoding='utf-8') as f:
        json.dump(archive, f, indent=2, ensure_ascii=False)
    print(f"  Archive written: {ARCHIVE_JSON} ({len(archive)} weeks)")


def _write_json(stories, week_of, generated_at):
    """Write current week to digest.json."""
    output = {
        'generated_at': generated_at,
        'week_of': week_of,
        'story_count': len(stories),
        'stories': stories,
    }
    with open(OUTPUT_JSON, 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    print(f"  JSON written: {OUTPUT_JSON}")


def _render_story(story):
    """Render a single story as HTML lines."""
    niche = story.get('niche', '')
    color = NICHE_COLORS.get(niche, '#6b7280')
    label = story.get('niche_label', '')
    lines = [
        '<div style="margin-bottom:1em; padding:0.75em 1em; border:1px solid #e5e7eb; border-radius:8px; background:#fafafa;">',
        '  <div style="display:flex; align-items:center; gap:0.5em; flex-wrap:wrap; margin-bottom:0.4em;">',
    ]
    if label:
        lines.append(f'    <span style="padding:2px 8px; border-radius:12px; font-size:0.72em; font-weight:600; background:{color}; color:#fff;">{label}</span>')
    if story.get('source'):
        lines.append(f'    <span style="font-size:0.78em; color:#9ca3af;">{story["source"]}</span>')
    lines += [
        '  </div>',
        '  <div style="font-weight:600; font-size:1em; margin-bottom:0.3em;">',
        f'    <a href="{story["url"]}" target="_blank" rel="noopener" style="color:#111;">{story["title"]}</a>',
        '  </div>',
    ]
    if story.get('description'):
        desc = story['description'][:180]
        lines.append(f'  <p style="margin:0; font-size:0.88em; color:#374151;">{desc}</p>')
    lines.append('</div>')
    return lines


def _generate_page(stories, week_of, archive, generated_at):
    """Generate the /digest/ Jekyll page."""
    lines = [
        '---',
        'layout: page',
        'title: "Weekly Digest"',
        'description: "Top tech stories of the week, curated across AI, security, cloud, devtools and software engineering."',
        'permalink: /digest/',
        '---',
        '',
        f'## Week of {week_of}',
        '',
        f'<p style="font-size:0.85em; color:#6b7280; margin-bottom:1.5em;">{len(stories)} stories across {len(set(s["niche"] for s in stories))} topics</p>',
        '',
    ]

    if not stories:
        lines += [
            '<p style="color:#9ca3af;">No stories this week yet — check back Sunday.</p>',
            '',
        ]
    else:
        for story in stories:
            lines += _render_story(story)
            lines.append('')

    past_weeks = [w for w in archive if w.get('week_of') != week_of]
    if past_weeks:
        lines += [
            '---',
            '',
            '## Past Weeks',
            '',
        ]
        for week in past_weeks:
            w_stories = week.get('stories', [])
            w_label = week.get('week_of', '')
            lines += [
                '<details style="margin-bottom:1em;">',
                f'<summary style="cursor:pointer; font-weight:600; padding:0.5em 0;">Week of {w_label} <span style="font-size:0.82em; color:#9ca3af; font-weight:400;">({len(w_stories)} stories)</span></summary>',
                '<div style="margin-top:0.75em;">',
            ]
            for story in w_stories:
                lines += _render_story(story)
            lines += [
                '</div>',
                '</details>',
                '',
            ]

    lines += [
        '---',
        '',
        f'<p style="font-size:0.8em; color:#9ca3af;">Generated: {generated_at}</p>',
        '',
    ]

    return '\n'.join(lines)


def publish_digest():
    """Main entry point."""
    os.makedirs(DATA_DIR, exist_ok=True)
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    now = datetime.now(timezone.utc)
    generated_at = now.strftime('%Y-%m-%d %H:%M:%S UTC')
    week_of = now.strftime('%B %d, %Y')

    posts = get_recent_posts(days=7, niche_filter=set(NICHE_CATEGORIES))

    if not posts:
        print('Digest: no qualifying posts from the past 7 days')
        return

    featured = _pick_featured(posts)
    stories = _stories_to_dicts(featured)
    print(f'Digest: {len(stories)} stories selected')

    _write_json(stories, week_of, generated_at)

    archive = _load_archive()
    current_week = {'week_of': week_of, 'generated_at': generated_at, 'stories': stories}
    _save_archive(archive, current_week)

    page = _generate_page(stories, week_of, archive, generated_at)
    with open(OUTPUT_PAGE, 'w', encoding='utf-8') as f:
        f.write(page)
    print(f'  Page written: {OUTPUT_PAGE}')
