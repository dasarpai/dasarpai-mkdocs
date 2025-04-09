#!/usr/bin/env python3
"""
Script to automatically update the book summaries index.md file
by scanning the booksummary directory for markdown files.
"""

import os
import re
import yaml
from datetime import datetime
from pathlib import Path

# Configuration
BOOKSUMMARY_DIR = Path("docs/booksummary")
INDEX_FILE = BOOKSUMMARY_DIR / "index.md"
ASSETS_DIR = Path("docs/assets/images/booksummary")

# Categories mapping - add new categories here as needed
CATEGORIES = {
    "leadership": "Leadership & Self-Improvement",
    "self-improvement": "Leadership & Self-Improvement",
    "literature": "Literature & Philosophy",
    "philosophy": "Literature & Philosophy",
    "economics": "Economics & Business",
    "business": "Economics & Business",
    "interview": "Interviews & Discussions",
    "discussion": "Interviews & Discussions",
    "documentary": "Interviews & Discussions",
    "panel": "Interviews & Discussions",
}

# Default category if none is found
DEFAULT_CATEGORY = "Literature & Philosophy"

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

def determine_category(frontmatter, filename):
    """Determine the category based on frontmatter or filename."""
    # Check tags in frontmatter
    if 'tags' in frontmatter and frontmatter['tags']:
        for tag in frontmatter['tags']:
            tag_lower = tag.lower()
            for key, category in CATEGORIES.items():
                if key in tag_lower:
                    return category
    
    # Check title or filename for category hints
    title = frontmatter.get('title', filename)
    for key, category in CATEGORIES.items():
        if key in title.lower() or key in filename.lower():
            return category
            
    # Special case handling
    if any(x in filename.lower() for x in ['interview', 'talk', 'discussion', 'documentary', 'panel', 'ama']):
        return "Interviews & Discussions"
    
    if any(x in filename.lower() for x in ['economics', 'capital', 'wealth', 'money', 'investor']):
        return "Economics & Business"
        
    if any(x in filename.lower() for x in ['leader', 'discipline', 'focus', 'listen', 'intention']):
        return "Leadership & Self-Improvement"
        
    # Default category
    return DEFAULT_CATEGORY

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
    
    # Generate excerpt from content
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Remove frontmatter
    content = re.sub(r'^---\s*\n.*?\n---\s*\n', '', content, flags=re.DOTALL)
    
    # Remove markdown formatting
    content = re.sub(r'#.*?\n', '', content)
    content = re.sub(r'!\[.*?\]\(.*?\)', '', content)
    content = re.sub(r'\[.*?\]\(.*?\)', r'\1', content)
    content = re.sub(r'[*_]{1,2}(.*?)[*_]{1,2}', r'\1', content)
    
    # Get first paragraph with meaningful content
    paragraphs = content.split('\n\n')
    for p in paragraphs:
        p = p.strip()
        if p and len(p) > 50:  # Ensure paragraph has enough content
            return p[:max_length] + ('...' if len(p) > max_length else '')
    
    # Fallback
    return "A summary of the book's key ideas and insights."

def generate_index():
    """Generate the index.md file with book summaries organized by category."""
    # Skip the index.md file itself
    files = [f for f in BOOKSUMMARY_DIR.glob('*.md') if f.name != 'index.md']
    
    # Organize files by category
    categories = {}
    
    for file_path in files:
        filename = file_path.stem
        frontmatter = extract_frontmatter(file_path)
        
        # Skip files without proper frontmatter
        if not frontmatter:
            continue
            
        category = determine_category(frontmatter, filename)
        
        if category not in categories:
            categories[category] = []
        
        # Get title from frontmatter or filename
        title = frontmatter.get('title', '')
        if not title:
            title = ' '.join(filename.split('-'))
        
        # Clean up title if it starts with "Book Summary:"
        title = re.sub(r'^Book Summary:\s*', '', title)
        
        # Get image path
        image_path = f"../assets/images/booksummary/{filename}.jpg"
        
        # Get read time
        read_time = estimate_read_time(file_path)
        
        # Get excerpt
        excerpt = get_excerpt(frontmatter, file_path)
        
        categories[category].append({
            'filename': filename,
            'title': title,
            'image': image_path,
            'read_time': read_time,
            'excerpt': excerpt
        })
    
    # Sort categories
    sorted_categories = sorted(categories.items(), key=lambda x: [
        "Leadership & Self-Improvement",
        "Literature & Philosophy",
        "Economics & Business",
        "Interviews & Discussions"
    ].index(x[0]) if x[0] in [
        "Leadership & Self-Improvement",
        "Literature & Philosophy",
        "Economics & Business",
        "Interviews & Discussions"
    ] else 999)
    
    # Generate markdown
    index_content = [
        "# Book Summaries",
        "",
        "Welcome to my collection of book summaries. Here you'll find summaries of various books I've read, including classics, self-help books, economics texts, and interviews with notable figures.",
        "",
        "Browse through the summaries below to find insights and key takeaways from each book.",
        ""
    ]
    
    for category, books in sorted_categories:
        index_content.append(f"## {category}")
        index_content.append("")
        index_content.append('<div class="grid cards" markdown>')
        index_content.append("")
        
        for book in books:
            index_content.extend([
                f"- ![{book['title']}]({book['image']}){{ width=\"200\" }}",
                "",
                f"    ### [{book['title']}]({book['filename']}.md)",
                "    ",
                f"    **Read time:** {book['read_time']} min",
                "    ",
                f"    {book['excerpt']}",
                ""
            ])
        
        index_content.append("</div>")
        index_content.append("")
    
    # Write to file
    with open(INDEX_FILE, 'w', encoding='utf-8') as f:
        f.write('\n'.join(index_content))
    
    print(f"Updated {INDEX_FILE} with {sum(len(books) for _, books in categories.items())} book summaries in {len(categories)} categories.")

if __name__ == "__main__":
    generate_index()
