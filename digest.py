"""
Weekly AI & Security Digest generator.
Reads posts from the past 7 days, picks top 5 by score, and generates a digest post.
"""
import os
import re
import glob
from datetime import datetime, timezone, timedelta


POSTS_DIR = "docs/_posts"


def _parse_frontmatter(path):
    """Parse YAML-style frontmatter from a markdown post file."""
    data = {}
    try:
        with open(path, encoding='utf-8') as f:
            content = f.read()

        if not content.startswith('---'):
            return None

        end = content.index('---', 3)
        fm = content[3:end].strip()
        body = content[end + 3:].strip()

        for line in fm.splitlines():
            if ':' in line:
                key, _, value = line.partition(':')
                data[key.strip()] = value.strip().strip('"').strip("'")

        data['_body'] = body
        data['_path'] = path
    except Exception:
        return None

    return data


def _get_recent_posts(days=7):
    """Return post frontmatter dicts for posts published in the last `days` days."""
    cutoff = datetime.now(timezone.utc) - timedelta(days=days)
    posts = []

    for path in glob.glob(os.path.join(POSTS_DIR, "*.md")):
        fm = _parse_frontmatter(path)
        if not fm:
            continue

        # Only niche posts (ai/security), skip digest posts themselves
        niche = fm.get('niche_category', '')
        if niche not in ('ai', 'security'):
            continue

        # Parse date from frontmatter
        date_str = fm.get('date', '')
        try:
            # Try "%Y-%m-%d %H:%M:%S %z" then "%Y-%m-%d"
            try:
                post_date = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S %z")
            except ValueError:
                post_date = datetime.strptime(date_str[:10], "%Y-%m-%d").replace(tzinfo=timezone.utc)
        except Exception:
            continue

        if post_date < cutoff:
            continue

        posts.append({
            'title': fm.get('title', 'Untitled'),
            'external_url': fm.get('external_url', ''),
            'description': fm.get('description', ''),
            'source': fm.get('source', ''),
            'score': int(fm.get('score', 0)),
            'niche_category': niche,
            'date': post_date,
        })

    return posts


def publish_digest():
    """Generate and write a weekly AI & Security digest post."""
    now = datetime.now(timezone.utc)
    posts = _get_recent_posts(days=7)

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
