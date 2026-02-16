import os
import re

posts_dir = 'docs/_posts'
updated = 0

for filename in os.listdir(posts_dir):
    if not filename.endswith('.md'):
        continue
    
    filepath = os.path.join(posts_dir, filename)
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Skip se ha già description nel front matter
    if 'description:' in content[:500]:
        continue
    
    # Estrai description dal blockquote
    desc_match = re.search(r'^>\s*(.+)$', content, re.MULTILINE)
    if not desc_match:
        continue
    description = desc_match.group(1).strip()[:150].replace('"', "'")
    
    # Estrai image
    img_match = re.search(r'!\[.+?\]\((https?://[^\)]+)\)', content)
    image = img_match.group(1) if img_match else None
    
    # Trova il secondo --- e inserisci prima
    first_marker = content.find('---')
    second_marker = content.find('---', first_marker + 3)
    
    if second_marker == -1:
        continue
    
    # Costruisci nuovi campi
    new_fields = f'description: "{description}"\n'
    if image:
        new_fields += f'image: {image}\n'
    
    # Inserisci prima del secondo ---
    new_content = content[:second_marker] + new_fields + content[second_marker:]
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)
    updated += 1

print(f'Updated {updated} posts')

