# This script removes specified keys (e.g., language, file, abstract) 
# from all entries in a .bib file and overwrites the original file.

import re

bib_path = '../master-thesis.bib'  # Path to the .bib file
keys_to_remove = {'language', 'file', 'abstract', 'note', 'keywords', 'editor'}
chars_to_remove = {'\u2009'}

with open(bib_path, 'r', encoding='utf-8') as f:
    content = f.read()

for ch in chars_to_remove:
    content = content.replace(ch, '')

def clean(entry: str) -> str:
    for key in keys_to_remove:
        entry = re.sub(rf'\s*{key}\s*=\s*{{.*?}},\n?', '', entry, flags=re.IGNORECASE | re.DOTALL)
    return entry

entries = content.split('@')
cleaned = ['@' + clean(e) for e in entries if e.strip()]

with open(bib_path, 'w', encoding='utf-8') as f:
    f.write(''.join(cleaned))

print(f"Removed keys: {', '.join(keys_to_remove)} from {bib_path}")
