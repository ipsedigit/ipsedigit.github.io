import os
import re


def generate_tag_pages():
    """Generate a page for each unique tag found in posts."""
    tags = set()
    posts_dir = 'docs/_posts'

    for filename in os.listdir(posts_dir):
        if filename.endswith('.md'):
            filepath = os.path.join(posts_dir, filename)
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
                match = re.search(r'categories:\s*(.+)', content)
                if match:
                    line = match.group(1).strip()
                    line = line.replace('[', '').replace(']', '')
                    cats = line.split(',')
                    for c in cats:
                        tag = c.strip()
                        if tag:
                            tags.add(tag)

    tags_dir = 'docs/tags'
    os.makedirs(tags_dir, exist_ok=True)

    for tag in tags:
        slug = tag.lower().replace(' ', '-').replace('(', '').replace(')', '')
        filename = os.path.join(tags_dir, f'{slug}.md')
        if not os.path.exists(filename):
            with open(filename, 'w', encoding='utf-8') as f:
                f.write('---\n')
                f.write('layout: tag\n')
                f.write(f'tag: "{tag}"\n')
                f.write(f'permalink: /tags/{slug}/\n')
                f.write('---\n')

