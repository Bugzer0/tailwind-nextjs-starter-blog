import os
import re
from pathlib import Path

# Directory containing blog posts
blog_dir = Path(__file__).parent.parent / "data" / "blog"

# Pattern to find double newlines before images
pattern = re.compile(r'\n\n\n(!\[.*?\]\(/static/images/.*?\))', re.MULTILINE)

# Counter
fixed_count = 0
file_count = 0

# Process all .mdx files
for mdx_file in blog_dir.glob("*.mdx"):
    file_count += 1
    content = mdx_file.read_text(encoding='utf-8')
    original_content = content
    
    # Replace triple newlines before images with double newlines
    content = pattern.sub(r'\n\n\1', content)
    
    if content != original_content:
        mdx_file.write_text(content, encoding='utf-8')
        fixed_count += 1
        print(f"Fixed: {mdx_file.name}")

print(f"\nProcessed {file_count} files, fixed {fixed_count} files")
