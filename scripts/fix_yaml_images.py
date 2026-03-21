import os
import re
from pathlib import Path

# Directory containing blog posts
blog_dir = Path(__file__).parent.parent / "data" / "blog"

# Counter
fixed_count = 0
file_count = 0

# Process all .mdx files
for mdx_file in blog_dir.glob("*.mdx"):
    file_count += 1
    content = mdx_file.read_text(encoding='utf-8')
    original_content = content
    
    # Split into frontmatter and body
    parts = content.split('---', 2)
    if len(parts) >= 3:
        frontmatter = parts[1]
        body = parts[2]
        
        # Fix images field - remove trailing whitespace from image paths
        lines = frontmatter.split('\n')
        new_lines = []
        in_images = False
        
        for line in lines:
            if line.strip().startswith('images:'):
                in_images = True
                new_lines.append(line)
            elif in_images and line.strip().startswith('- '):
                # Remove trailing whitespace from image path
                cleaned_line = line.rstrip()
                new_lines.append(cleaned_line)
                in_images = False
            else:
                new_lines.append(line)
                if line.strip() and not line.startswith(' ') and in_images:
                    in_images = False
        
        new_frontmatter = '\n'.join(new_lines)
        new_content = f"---{new_frontmatter}---{body}"
        
        if new_content != content:
            mdx_file.write_text(new_content, encoding='utf-8')
            fixed_count += 1
            print(f"Fixed: {mdx_file.name}")

print(f"\nProcessed {file_count} files, fixed {fixed_count} files")
