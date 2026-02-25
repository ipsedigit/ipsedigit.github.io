"""
Weekly Tech Digest generator.
Reads posts from the past 7 days across all niches, picks top stories, and generates a digest post.
"""
import os
from datetime import datetime, timezone

from post_parser import get_recent_posts
from const import NICHE_CATEGORIES

POSTS_DIR = "docs/_posts"

NICHE_LABELS = {
    'ai': 'AI',
    'software-engineering': 'Software Engineering',
    'devtools': 'Developer Tools',
    'cloud': 'Cloud & Infrastructure',
    'security': 'Security',
}


def publish_digest():
    """Generate and write a weekly digest post covering all niches."""
    now = datetime.now(timezone.utc)
    posts = get_recent_posts(days=7, niche_filter=set(NICHE_CATEGORIES))

    if not posts:
        print("⏸️ Digest: no qualifying posts from the past 7 days")
        return

    # Top 2 per niche (10 total max), then fill remaining slots from overall top
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

    # Fill up to 10 from remaining top-scored posts
    remaining = sorted(
        [p for p in posts if p['external_url'] not in featured_urls],
        key=lambda p: p['score'], reverse=True
    )
    for p in remaining:
        if len(featured) >= 10:
            break
        featured.append(p)
        featured_urls.add(p['external_url'])

    week_str = now.strftime("%B %d, %Y")
    first_title = featured[0]['title'][:40] if featured else ""
    meta_desc = f"Top tech stories this week: {first_title}..."

    # Build frontmatter
    lines = ["---"]
    lines.append("layout: post")
    lines.append(f'title: "Weekly Tech Digest — Week of {week_str}"')
    lines.append(f'date: {now.strftime("%Y-%m-%d %H:%M:%S %z")}')
    lines.append("categories:")
    lines.append("  - digest")
    for niche in NICHE_CATEGORIES:
        lines.append(f"  - {niche}")
    lines.append(f'description: "{meta_desc}"')
    lines.append("niche_category: digest")
    lines.append("---")
    lines.append("")

    # Body — group by niche
    lines.append("## This Week in Tech")
    lines.append("")

    for niche in NICHE_CATEGORIES:
        niche_stories = [p for p in featured if p['niche_category'] == niche]
        if not niche_stories:
            continue
        label = NICHE_LABELS.get(niche, niche)
        lines.append(f"### {label}")
        lines.append("")
        for post in niche_stories:
            title = post['title']
            url = post['external_url']
            desc = post['description']
            source = post['source']
            lines.append(f"**[{title}]({url})**")
            if desc:
                lines.append(f"  {desc}")
            if source:
                lines.append(f"  *Source: {source}*")
            lines.append("")

    lines.append("---")
    lines.append("")
    lines.append("*Curated weekly by [eof.news](https://ipsedigit.github.io) — signal for engineers who build.*")
    lines.append("")

    content = "\n".join(lines)

    file_name = os.path.join(
        POSTS_DIR,
        f"{now.strftime('%Y-%m-%d')}-weekly-tech-digest.md"
    )
    with open(file_name, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"✅ Weekly digest published: {file_name} ({len(featured)} stories)")
