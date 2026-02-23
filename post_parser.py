"""
Shared post parsing module.
Provides frontmatter parsing, post retrieval, category extraction, and Jekyll URL generation.
"""
import os
import re
import glob
from datetime import datetime, timezone, timedelta

POSTS_DIR = "docs/_posts"


def parse_frontmatter(path):
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

        in_list_key = None
        list_items = []

        for line in fm.splitlines():
            # YAML list item (e.g. "  - tag1")
            stripped = line.strip()
            if stripped.startswith('- ') and in_list_key:
                list_items.append(stripped[2:].strip().strip('"').strip("'"))
                continue

            # Save accumulated list
            if in_list_key and list_items:
                data[in_list_key] = list_items
                in_list_key = None
                list_items = []

            if ':' in line:
                key, _, value = line.partition(':')
                key = key.strip()
                value = value.strip().strip('"').strip("'")

                # Check for inline YAML list: categories: [a, b, c]
                if value.startswith('[') and value.endswith(']'):
                    data[key] = [v.strip().strip('"').strip("'")
                                 for v in value[1:-1].split(',') if v.strip()]
                elif value == '':
                    # Start of a YAML list block
                    in_list_key = key
                    list_items = []
                else:
                    data[key] = value

        # Save final list if file ends with one
        if in_list_key and list_items:
            data[in_list_key] = list_items

        data['_body'] = body
        data['_path'] = path
    except Exception:
        return None

    return data


def parse_date(date_str):
    """Parse a date string from frontmatter. Returns datetime or None."""
    if not date_str:
        return None
    try:
        return datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S %z")
    except ValueError:
        pass
    try:
        return datetime.strptime(date_str[:10], "%Y-%m-%d").replace(tzinfo=timezone.utc)
    except Exception:
        return None


def jekyll_url_from_path(path):
    """Generate a Jekyll URL from a post file path.
    e.g. docs/_posts/2025-04-20-my-post-title.md -> /2025/04/20/my-post-title.html
    """
    basename = os.path.basename(path)
    name = basename.replace('.md', '')
    # Format: YYYY-MM-DD-slug
    match = re.match(r'(\d{4})-(\d{2})-(\d{2})-(.+)', name)
    if match:
        y, m, d, slug = match.groups()
        return f"/{y}/{m}/{d}/{slug}.html"
    return f"/{name}.html"


def get_all_posts():
    """Return all parsed post dicts with frontmatter and computed fields."""
    posts = []
    for path in glob.glob(os.path.join(POSTS_DIR, "*.md")):
        fm = parse_frontmatter(path)
        if not fm:
            continue

        post_date = parse_date(fm.get('date', ''))

        categories = fm.get('categories', [])
        if isinstance(categories, str):
            categories = [c.strip() for c in categories.split(',') if c.strip()]

        posts.append({
            'title': fm.get('title', 'Untitled'),
            'external_url': fm.get('external_url', ''),
            'description': fm.get('description', ''),
            'source': fm.get('source', ''),
            'score': int(float(fm.get('score', 0) or 0)),
            'niche_category': fm.get('niche_category', ''),
            'niche_subniche': fm.get('niche_subniche', ''),
            'categories': categories,
            'date': post_date,
            'url': jekyll_url_from_path(path),
            '_path': path,
            '_body': fm.get('_body', ''),
        })

    return posts


def get_recent_posts(days=7, niche_filter=None):
    """Return posts published in the last `days` days.
    If niche_filter is provided, only include posts with matching niche_category.
    """
    cutoff = datetime.now(timezone.utc) - timedelta(days=days)
    posts = get_all_posts()

    result = []
    for post in posts:
        if post['date'] is None or post['date'] < cutoff:
            continue
        if niche_filter and post['niche_category'] not in niche_filter:
            continue
        result.append(post)

    return result
