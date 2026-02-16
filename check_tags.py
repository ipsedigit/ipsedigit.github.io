import os
import re

# Raccogli tutti i tag dai post
tags_in_posts = set()
posts_dir = 'docs/_posts'
for filename in os.listdir(posts_dir):
    if filename.endswith('.md'):
        with open(os.path.join(posts_dir, filename), 'r', encoding='utf-8') as f:
            content = f.read()
            match = re.search(r'categories:\s*(.+)', content)
            if match:
                line = match.group(1).strip().replace('[', '').replace(']', '')
                for c in line.split(','):
                    tag = c.strip()
                    if tag:
                        tags_in_posts.add(tag)

# Raccogli tutti i tag disponibili (file nella cartella tags)
tags_available = set()
tags_dir = 'docs/tags'
for filename in os.listdir(tags_dir):
    if filename.endswith('.md'):
        slug = filename.replace('.md', '')
        tags_available.add(slug)

# Funzione slugify (come Jekyll)
def slugify(text):
    slug = text.lower()
    slug = re.sub(r'[^a-z0-9]+', '-', slug)
    slug = slug.strip('-')
    return slug

# Verifica
missing = []
ok = []
for tag in sorted(tags_in_posts):
    slug = slugify(tag)
    if slug in tags_available:
        ok.append((tag, slug))
    else:
        missing.append((tag, slug))

print("=== MISSING TAG PAGES ===")
for tag, slug in missing:
    print(f"  {tag} -> /tags/{slug}/")

print(f"\n=== OK: {len(ok)} tags ===")

print("\n=== ORPHAN TAG FILES ===")
used_slugs = {slugify(t) for t in tags_in_posts}
for slug in sorted(tags_available):
    if slug not in used_slugs:
        print(f"  {slug}")

