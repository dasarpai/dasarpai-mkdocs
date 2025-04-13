## python scripts/transfer_from_jekyll.py --blog_type dsblog --output_dir "docs/dsblog"
import os
import shutil
import re
import argparse
from pathlib import Path

def copy_files_without_date_prefix(input_dir, output_dir, blog_type=None):
    """
    Copy files from input_dir to output_dir, removing date prefixes from filenames.
    Date format expected: YYYY-MM-DD- (e.g., 2021-07-14-)
    Also creates:
    - .namemap file mapping input filenames to output filenames
    - .pages file with title and arrange entries for the output files
    
    Args:
        input_dir (str): Input directory path
        output_dir (str): Output directory path
        blog_type (str, optional): Blog type to process (e.g., 'dsblog', 'booksummary')
                                 If provided, will look for _blog_type subdirectory
    """
    # Determine the actual input directory based on blog_type
    if blog_type:
        # Jekyll blogs are typically in _blog_type directories
        actual_input_dir = os.path.join(input_dir, f"_{blog_type}")
        if not os.path.exists(actual_input_dir):
            print(f"Error: Blog directory '{actual_input_dir}' not found.")
            return
    else:
        actual_input_dir = input_dir
    
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Regular expression to match date pattern: YYYY-MM-DD-
    date_pattern = r'^\d{4}-\d{2}-\d{2}-'
    
    # Get list of files in input directory
    try:
        # Get list of files in input directory order by name

        files = sorted(os.listdir(actual_input_dir),reverse=True)
    except FileNotFoundError:
        print(f"Error: Input directory '{actual_input_dir}' not found.")
        return
    
    copied_count = 0
    name_mapping = {}
    output_filenames = []
    
    for filename in files:
        input_path = os.path.join(actual_input_dir, filename)
        
        # Skip directories and non-markdown files
        if os.path.isdir(input_path) or not filename.lower().endswith(('.md', '.markdown')):
            continue
        
        # Remove date prefix from filename
        new_filename = re.sub(date_pattern, '', filename)
        output_path = os.path.join(output_dir, new_filename)
        
        print(f"Copying: {filename} -> {new_filename}")
        
        # Copy the file
        shutil.copy2(input_path, output_path)

        # Read the copied file and replace /assets/ with ../assets/
        with open(output_path, 'r', encoding='utf-8') as f:
            content = f.read()
        content = content.replace('/assets/', '../assets/')

        # Replace layout:.* with empty line using regex
        content = re.sub(r'^layout:.*$', '', content, flags=re.MULTILINE)
        

        # Write the modified content back
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(content)
            
        copied_count += 1
        
        # Add to name mapping
        name_mapping[filename] = new_filename
        
        # Add to output filenames list (without extension for .pages file)
        output_filenames.append(os.path.splitext(new_filename)[0])
    
    print(f"Copied {copied_count} files from {actual_input_dir} to {output_dir} with date prefixes removed.")
    
    # Create .namemap file
    namemap_path = os.path.join(output_dir, ".namemap")
    with open(namemap_path, 'w') as f:
        for input_name, output_name in name_mapping.items():
            f.write(f"{input_name}: {output_name}\n")
    print(f"Created .namemap file at {namemap_path}")
    
    # Create .pages file
    pages_path = os.path.join(output_dir, ".pages")
    # Use blog_type for the title if provided, otherwise use folder name
    title = blog_type.title() if blog_type else os.path.basename(output_dir).title()
    with open(pages_path, 'w') as f:
        f.write(f"title: {title}\n")
        f.write("arrange:\n")
        for filename in output_filenames:
            f.write(f"  - {filename}\n")
    print(f"Created .pages file at {pages_path}")

def main():
    # parser = argparse.ArgumentParser(description='Copy files from Jekyll blog to MkDocs, removing date prefixes from filenames.')
    # parser.add_argument('--input_dir', default="D:\\github-blog\\dasarpai.github.io", 
    #                     help='Input directory containing Jekyll blog files (default: D:\\github-blog\\dasarpai.github.io)')
    # parser.add_argument('--output_dir', required=True, 
    #                     help='Output directory for files with date prefixes removed')
    # parser.add_argument('--blog_type', choices=['dsblog', 'gallary', 'booksummary', 'pmblog', 'pmbok6', 'dsresources', 'management', 'dscourses'],
    #                     help='Type of blog to process (corresponds to _blogtype directory in Jekyll)')
    # args = parser.parse_args()
    
    # # Convert to absolute paths if needed
    # input_dir = os.path.abspath(args.input_dir)
    # output_dir = os.path.abspath(args.output_dir)
    # copy_files_without_date_prefix(input_dir, output_dir, args.blog_type)

    blogs = ["booksummary", "dsblog", "dscourses", "dsresources", "gallery", "gk", "management", "news", 
            "pages", "pmblog", "pmbok6", "pmbok6hi", "projects", "quotations", 
            "samskrutyatra", "wiaposts"]
    blogs = ["quotations"]
    for blog in blogs:

        blog_type = blog
        input_dir = "D:\\github-blog\\dasarpai.github.io\\"
        output_dir = "D:\\github-blog\\dasarpai-mkdocs\\docs\\"+blog
        # input_dir = "D:\\github-blog\\dasarpai-websitetest\\"
        # output_dir = "D:\\github-blog\\dasarpai-mkdocs-test\\docs\\"+blog
        copy_files_without_date_prefix(input_dir, output_dir, blog)

if __name__ == "__main__":
    main()
