import os

tex_dir = '../parts/'
output_file = 'combined.tex'

with open(output_file, 'w', encoding='utf-8') as out:
    for file in sorted(os.listdir(tex_dir)):
        if file.endswith('.tex'):
            out.write(f'--- {file} ---\n')
            with open(os.path.join(tex_dir, file), 'r', encoding='utf-8') as f:
                out.write(f.read() + '\n\n')
