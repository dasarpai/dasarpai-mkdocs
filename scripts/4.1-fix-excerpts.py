import re
from pathlib import Path

def process_excerpts():
    source_dir = Path(r"D:\github-blog\dasarpai.github.io\_samskrutyatra")
    target_dir = Path(r"D:\github-blog\dasarpai.github.io\_samskrutyatra2")
    
    print(f"Looking for markdown files in: {source_dir}")
    print(f"Files found: {list(source_dir.rglob('*.md'))}")
    
    # Ensure target directory exists
    target_dir.mkdir(parents=True, exist_ok=True)
    
    # Pattern to match YAML front matter with excerpt
    front_matter_pattern = re.compile(r'^---\s*\n(.*?)\n---\s*\n', re.DOTALL)
    excerpt_pattern = re.compile(r'^excerpt:\s*(.*?)(?:\n|$)', re.MULTILINE)
    header_pattern = re.compile(r'^#+\s+(.*?)$', re.MULTILINE)
    
    processed_files = []
    
    # Process all markdown files
    for md_file in source_dir.glob('**/*.md'):
        print(f'\n=== Processing: {md_file} ===')
        with open(md_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        needs_excerpt = False
        new_content = content
        
        # Check for front matter
        front_matter_match = front_matter_pattern.match(content)
        if not front_matter_match:
            print('No front matter found - skipping')
            continue
            
        front_matter = front_matter_match.group(1)
        body_content = content[front_matter_match.end():]
        
        # Check excerpt line
        excerpt_lines = [line for line in front_matter.split('\n') if line.startswith('excerpt:')]
        
        if len(excerpt_lines) == 0:
            print('Excerpt line missing - will add after layout line')
            needs_excerpt = True
        else:
            excerpt_line = excerpt_lines[0]
            excerpt_parts = excerpt_line.split(':', 1)
            
            if len(excerpt_parts) == 1 or not excerpt_parts[1].strip():
                print('Excerpt empty - will regenerate')
                needs_excerpt = True
            else:
                print('Excerpt exists - skipping')
                continue
        
        if needs_excerpt:
            # Check for audio tags first
            audio_end = body_content.find('</audio>')
            if audio_end > 0:
                excerpt_start = audio_end + len('</audio>')
                excerpt_text = body_content[excerpt_start:]
            else:
                # Otherwise use first header
                header_match = header_pattern.search(body_content)
                if header_match:
                    excerpt_start = body_content.find('\n', header_match.end()) + 1
                    excerpt_text = body_content[excerpt_start:]
                else:
                    excerpt_text = body_content
            
            # Take first 40 words
            excerpt_text = ' '.join(excerpt_text.split()[:40])
            excerpt_text = excerpt_text.replace('"', '"')
            print(f'Generated excerpt: "{excerpt_text}"')
            
            # Update or add excerpt
            if len(excerpt_lines) > 0:
                # Replace existing excerpt
                new_front_matter = front_matter.replace(excerpt_lines[0], f'excerpt: "{excerpt_text}"')
            else:
                # Ensure layout line exists and add excerpt after it
                if 'layout:' not in front_matter:
                    front_matter += '\nlayout: amskrut-layout\n'
                layout_line = [line for line in front_matter.split('\n') if line.strip().startswith('layout:')][0]
                new_front_matter = front_matter.replace(layout_line, f'{layout_line}\nexcerpt: "{excerpt_text}"')
            
            # Reconstruct content
            new_content = f'---\n{new_front_matter}\n---\n{body_content}'
            
            # Write to target file
            target_file = target_dir / md_file.relative_to(source_dir)
            target_file.parent.mkdir(parents=True, exist_ok=True)
            with open(target_file, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f'Processed {target_file}')
        else:
            print('No header found - skipping excerpt generation')
        
    return processed_files

if __name__ == "__main__":
    processed = process_excerpts()
    print("Processed files:")
    for file in processed:
        print(f"- {file}")
