import re
from pathlib import Path

# Configuration
CHANT_DIR = Path("docs/samskrutyatra/test")
PATTERN = r'\{%\s*include\s+embed-audio\.html\s+src\s*=\s*"(.*?)"\s*%\}'
REPLACEMENT = r'{{ embed_audio("\1") | safe }}'

for md_file in CHANT_DIR.glob("**/*.md"):
    content = md_file.read_text(encoding="utf-8")
    new_content = re.sub(PATTERN, REPLACEMENT, content)
    
    if new_content != content:
        md_file.write_text(new_content, encoding="utf-8")
        print(f"Updated: {md_file}")