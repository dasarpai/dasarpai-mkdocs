#!/usr/bin/env python3
"""
Script to automatically update the article summaries into index.md file
by scanning the jekyll/collections directory for markdown files.
"""

import os
import re
import yaml
import json
from datetime import datetime
from pathlib import Path



def load_collection_intro(COLLECTION_INTRO_FILE):
    """Load collection intro content from JSON file."""
    try:
        with open(COLLECTION_INTRO_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading collection intro file: {e}")
        return {}

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

def get_image_path(frontmatter, blog):
    """Get image path from frontmatter with error handling."""
    try:
        if frontmatter and 'header' in frontmatter and frontmatter['header'] and 'teaser' in frontmatter['header']:
            return frontmatter['header']['teaser']
        else:
            # Return a default image path if header or teaser is missing
            return f"../assets/images/{blog}/default.jpg"
    except (TypeError, KeyError):
        # Handle any other errors
        return f"../assets/images/{blog}/default.jpg"

def generate_index(blog, index_content):
    """Generate the index.md file with article summaries."""
    # Set the input directory and index file for the current blog
    input_dir = Path("docs/" + blog)
    index_file = input_dir / "index.md"
    
    # read file name from .namemap file 
    namemap_file = input_dir / ".namemap"
    with open(namemap_file, 'r', encoding='utf-8') as f:
        namemap = f.read()

    # for each line in .namemap file get the pair
    namemap = namemap.split('\n')
    
    namemap = [line.split(':') for line in namemap]

    namemap_dict = {line[0]: line[1] for line in namemap if len(line) == 2}
    

    # Collect all article  data first
    index_summaries = []
    
    for _, mkdcosfilename in namemap_dict.items():
        try:
            file_path = input_dir.joinpath(mkdcosfilename.strip()) 

            frontmatter = extract_frontmatter(file_path)
            
            # Skip files without proper frontmatter
            if not frontmatter:
                print(f"Skipping {file_path} - No frontmatter found")
                continue
            
            # Get title with fallback
            title = frontmatter.get('title', mkdcosfilename)
            # print(file_path)
            
            # Get image path with error handling
            image_path = get_image_path(frontmatter, blog)
            
            excerpt = get_excerpt(frontmatter, file_path)
            read_time = estimate_read_time(file_path)
            
            # Store article summary data
            index_summaries.append({
                'title': title,
                'filename': file_path,
                'image_path': image_path,
                'excerpt': excerpt,
                'read_time': read_time,
                'mkdocsfile' : mkdcosfilename.strip()
            })

        except Exception as e:
            print(f"Error processing {file_path}: {e}")
            continue
    
    # Generate markdown with two columns per row
    index_content_lines = index_content.split('\n')
    index_content_lines.append("")
    
    # Process article summaries in pairs
    for i in range(0, len(index_summaries), 2):
        index_content_lines.append('<div class="grid cards" markdown>')
        index_content_lines.append("")
        
        # First column
        article = index_summaries[i]
        index_content_lines.extend([
            "\n",
            f"- ![{article['title']}]({article['image_path']}){{ width=\"200\" }}",
            "",
            f"    ### [{article['title']}]({article['mkdocsfile']})",
            "    ",
            f"    **Read time:** {article['read_time']} min",
            "    ",
            f"    {article['excerpt']}"
            ""
        ])
        
        # Second column (if available)
        if i + 1 < len(index_summaries):
            article = index_summaries[i + 1]
            index_content_lines.extend([
                "\n",
                f"- ![{article['title']}]({article['image_path']}){{ width=\"200\" }}",
                "",
                f"    ### [{article['title']}]({article['mkdocsfile']})",
                "    ",
                f"    **Read time:** {article['read_time']} min",
                "    ",
                f"    {article['excerpt']}",
                "    "
            ])
        
        index_content_lines.append("</div>")
        index_content_lines.append("")
    
    # Write to file
    with open(index_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(index_content_lines))

    print(f"Updated {index_file} with {len(index_summaries)} Articles")

if __name__ == "__main__":
    # Define what index to create.
    blogs = ["booksummary", "dsblog", "dscourses", "dsresources", "gallery", "gk", "management", "news", 
            "pages", "pmblog", "pmbok6", "pmbok6hi", "projects", "quotations", 
            "samskrutyatra", "wiaposts"]
    
    # Load collection intro content
    blogs = ["quotations"]
    COLLECTION_INTRO_FILE = Path("scripts/0-collection_intro.json")
    collection_intro = load_collection_intro(COLLECTION_INTRO_FILE)
    
    for blog in blogs:
        try:
            # Get the intro content for this blog from the JSON file
            if blog in collection_intro:
                index_content = collection_intro[blog]
            else:
                # Default content if blog not found in JSON
                index_content = f"# {blog.capitalize()}\n\nWelcome to {blog.capitalize()} page."
            # Generate the index for this blog
            generate_index(blog, index_content)
        except Exception as e:
            print(f"Error generating index for {blog}: {e}")
            continue
