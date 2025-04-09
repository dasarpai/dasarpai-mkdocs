#!/usr/bin/env python3
"""
Script to automatically update the article summaries into index.md file
by scanning the jekyll/collections directory for markdown files.
"""

import os
import re
import yaml
from datetime import datetime
from pathlib import Path

# Configuration
## Define what index to create.
BLOG = "dsblog"

index_content = [
    "# Data Science Blog",
    "",
    "Welcome to my Data Science Blog",
    "",
    "Browse through the summaries below to find insights and key takeaways",
    ""
]

## configuration continue
INPUT_DIR = Path("docs/" + BLOG)
INDEX_FILE = INPUT_DIR / "index.md"
ASSETS_DIR = Path("docs/assets/images/" + BLOG)

def extract_frontmatter(file_path):
    """Extract YAML frontmatter from markdown file."""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Look for frontmatter between --- markers
    match = re.search(r'^---\s*\n(.*?)\n---\s*\n', content, re.DOTALL)
    if match:
        try:
            return yaml.safe_load(match.group(1))
        except yaml.YAMLError:
            return {}
    return {}


def estimate_read_time(file_path):
    """Estimate reading time based on word count (avg 200 words per minute)."""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Remove frontmatter
    content = re.sub(r'^---\s*\n.*?\n---\s*\n', '', content, flags=re.DOTALL)
    
    # Count words
    word_count = len(re.findall(r'\b\w+\b', content))
    
    # Calculate minutes (minimum 5 minutes)
    minutes = max(5, round(word_count / 200))
    
    return minutes

def get_excerpt(frontmatter, file_path, max_length=150):
    """Get excerpt from frontmatter or generate from content."""
    # Try to get excerpt from frontmatter
    if 'excerpt' in frontmatter and frontmatter['excerpt']:
        return frontmatter['excerpt'][:max_length]
    else:
        return "EXCERPT Not Found"

def generate_index():
    """Generate the index.md file with article summaries."""
    # Skip the index.md file itself
    files = [f for f in INPUT_DIR.glob('*.md') if f.name != 'index.md']

    # Collect all article  data first
    index_summaries = []
    
    for file_path in files:
        filename = file_path.stem
        frontmatter = extract_frontmatter(file_path)
        
        # Skip files without proper frontmatter
        if not frontmatter:
            continue
        
        title = frontmatter['title']
        image_path = frontmatter['header']['teaser']
        excerpt = get_excerpt(frontmatter, file_path)
        read_time = estimate_read_time(file_path)
        
        # Store article summary data
        index_summaries.append({
            'title': title,
            'filename': filename,
            'image_path': image_path,
            'excerpt': excerpt,
            'read_time': read_time
        })
    
    # Generate markdown with two columns per row
    index_content.append("")
    
    # Process article summaries in pairs
    for i in range(0, len(index_summaries), 2):
        index_content.append('<div class="grid cards" markdown>')
        index_content.append("")
        
        # First column
        article = index_summaries[i]
        index_content.extend([
            f"- ![{article['title']}]({article['image_path']}){{ width=\"200\" }}",
            "",
            f"    ### [{article['title']}]({article['filename']})",
            "    ",
            f"    **Read time:** {article['read_time']} min",
            "    ",
            f"    {article['excerpt']}",
            ""
        ])
        
        # Second column (if available)
        if i + 1 < len(index_summaries):
            article = index_summaries[i + 1]
            index_content.extend([
                f"- ![{article['title']}]({article['image_path']}){{ width=\"200\" }}",
                "",
                f"    ### [{article['title']}]({article['filename']})",
                "    ",
                f"    **Read time:** {article['read_time']} min",
                "    ",
                f"    {article['excerpt']}",
                ""
            ])
        
        index_content.append("</div>")
        index_content.append("")
    
    # Write to file
    with open(INDEX_FILE, 'w', encoding='utf-8') as f:
        f.write('\n'.join(index_content))

    print(f"Updated {INDEX_FILE} with {len(files)} Articles")

if __name__ == "__main__":
    generate_index()
