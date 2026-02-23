"""
Weekly AI & Security Digest generator.
Reads posts from the past 7 days, picks top 5 by score, and generates a digest post.
"""
import os
from datetime import datetime, timezone

from post_parser import get_recent_posts

POSTS_DIR = "docs/_posts"


def publish_digest():
    """Generate and write a weekly AI & Security digest post."""
    now = datetime.now(timezone.utc)
    posts = get_recent_posts(days=7, niche_filter={'ai', 'security'})

    if not posts:
        print("⏸️ Digest: no qualifying posts from the past 7 days")
        return

    # Top 5 by score
    top5 = sorted(posts, key=lambda p: p['score'], reverse=True)[:5]

    week_str = now.strftime("%B %d, %Y")
    first_title = top5[0]['title'][:40] if top5 else ""
    meta_desc = f"Top AI and security stories this week: {first_title}..."

    # Build frontmatter
    lines = ["---"]
    lines.append("layout: post")
    lines.append(f'title: "AI & Security Weekly Digest — Week of {week_str}"')
    lines.append(f'date: {now.strftime("%Y-%m-%d %H:%M:%S %z")}')
    lines.append("categories:")
    lines.append("  - digest")
    lines.append("  - ai")
    lines.append("  - security")
    lines.append(f'description: "{meta_desc}"')
    lines.append("niche_category: digest")
    lines.append("---")
    lines.append("")

    # Body
    lines.append("## This Week in AI & Security")
    lines.append("")

    for i, post in enumerate(top5, 1):
        title = post['title']
        url = post['external_url']
        desc = post['description']
        source = post['source']
        lines.append(f"### {i}. [{title}]({url})")
        if desc:
            lines.append("")
            lines.append(desc)
        if source:
            lines.append(f"*Source: {source}*")
        lines.append("")

    lines.append("---")
    lines.append("")
    lines.append("*Curated weekly by [eof.news](https://eof.news)*")
    lines.append("")

    content = "\n".join(lines)

    file_name = os.path.join(
        POSTS_DIR,
        f"{now.strftime('%Y-%m-%d')}-weekly-digest-ai-security.md"
    )
    with open(file_name, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"✅ Weekly digest published: {file_name} ({len(top5)} stories)")
