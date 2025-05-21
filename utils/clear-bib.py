# Remove selected keys from every BibTeX entry and
# convert specific @phdthesis entries to @mastersthesis.

import re

bib_path = '../master-thesis.bib'
keys_to_remove = {'language', 'file', 'abstract', 'note', 'keywords', 'editor'}
chars_to_remove = {'\u2009'}
# phd_to_master = {'culemann_construction_2024', 'huang_construction_2024', 'kruip_design_2024', 'dux_optical_2023'}
phd_to_master = {}

with open(bib_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Remove stray characters first
for ch in chars_to_remove:
    content = content.replace(ch, '')

content = content.replace("!=", "$\neq$")
content = content.replace("{Li6}", "{$^6$Li}")

def clean_and_convert(entry: str) -> str:
    """Remove unwanted fields and convert selected entry types."""
    # Drop specified fields
    for key in keys_to_remove:
        entry = re.sub(
            rf'\s*{key}\s*=\s*{{.*?}},\n?', '',
            entry,
            flags=re.IGNORECASE | re.DOTALL
        )

    # Detect entry type and citekey
    m = re.match(r'\s*(\w+)\s*{\s*([^,]+),', entry)
    if m:
        entry_type, citekey = m.groups()
        if entry_type.lower() == 'phdthesis' and citekey in phd_to_master:
            # Replace only the first occurrence of the entry type
            entry = re.sub(
                r'^\s*phdthesis',
                'mastersthesis',
                entry,
                count=1,
                flags=re.IGNORECASE
            )
    return entry

# Split on '@', process each chunk, then glue back together
entries = content.split('@')
cleaned_entries = ['@' + clean_and_convert(e) for e in entries if e.strip()]

with open(bib_path, 'w', encoding='utf-8') as f:
    f.write(''.join(cleaned_entries))

print(f'Done.')
