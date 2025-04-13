import re
from pathlib import Path

def process_audio_embeds():
    source_dir = Path("docs/samskrutyatra/chanting")
    target_dir = Path("docs/samskrutyatra/chanting1")
    
    target_dir.mkdir(exist_ok=True)
    
    # Simplified pattern with proper group handling
    pattern = re.compile(
        r'(?:\{\%\s*include\s+embed-audio\.html\s+src\s*\=\s*\"([^\"]+\.(?:mp3|mp4|ogg|wav|m4a|aac|flac))\"\s*\%\}|\{\{\s*embed_audio\("([^\"]+\.(?:mp3|mp4|ogg|wav|m4a|aac|flac))"\)\s*\|\s*safe\s*\}\})',
        re.IGNORECASE
    )
    
    processed_files = []
    
    for md_file in source_dir.glob("*.md"):
        with open(md_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Find and replace both formats
        new_content = pattern.sub(
            lambda m: f'<audio controls>\n  <source src="{m.group(1) or m.group(2)}" type="audio/{Path(m.group(1) or m.group(2)).suffix[1:]}">\n  Your browser does not support the audio element.\n</audio>',
            content
        )
        
        if new_content != content:
            target_file = target_dir / md_file.name
            with open(target_file, 'w', encoding='utf-8') as f:
                f.write(new_content)
            processed_files.append(md_file.name)
    
    return processed_files

if __name__ == "__main__":
    processed = process_audio_embeds()
    print("Processed files:")
    for file in processed:
        print(f"- {file}")