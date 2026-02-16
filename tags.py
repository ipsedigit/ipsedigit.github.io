import os
import re


def slugify(text):
    """Generate slug matching Jekyll's slugify filter."""
    # Convert to lowercase
    slug = text.lower()
    # Replace non-alphanumeric characters with hyphens
    slug = re.sub(r'[^a-z0-9]+', '-', slug)
    # Remove leading/trailing hyphens
    slug = slug.strip('-')
    return slug


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
        slug = slugify(tag)
        filename = os.path.join(tags_dir, f'{slug}.md')
        with open(filename, 'w', encoding='utf-8') as f:
            f.write('---\n')
            f.write('layout: tag\n')
            f.write(f'tag: "{tag}"\n')
            f.write(f'title: "{tag} - Tech News & Articles | ipsedigit"\n')
            f.write(f'description: "Latest {tag} news, tutorials and insights. Curated tech articles from Hacker News about {tag}."\n')
            f.write(f'permalink: /tags/{slug}/\n')
            f.write('---\n')


if __name__ == "__main__":
    generate_tag_pages()
    print("Tag pages generated!")
