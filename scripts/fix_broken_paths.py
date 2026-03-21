import re
from pathlib import Path

blog_dir = Path(__file__).parent.parent / "data" / "blog"

fixed_count = 0
file_count = 0

for mdx_file in blog_dir.glob("*.mdx"):
    file_count += 1
    
    # Read as binary to handle line endings properly
    content = mdx_file.read_bytes().decode('utf-8')
    original_content = content
    
    # Fix broken image paths in YAML frontmatter
    # Pattern: "  - /static/images/..." that might be broken across lines
    # Replace any newline within the path
    def fix_yaml_images(match):
        yaml_block = match.group(0)
        # Remove line breaks within image paths
        fixed = re.sub(r'(/static/images/[^\n]*?)\r?\n\s*([^\n]+\.jpg)', r'\1\2', yaml_block)
        return fixed
    
    # Find and fix the images section in frontmatter
    content = re.sub(
        r'images:\s*\n\s*- /static/images/.*?\.jpg',
        fix_yaml_images,
        content,
        flags=re.DOTALL
    )
    
    # Also normalize line endings to LF
    content = content.replace('\r\n', '\n').replace('\r', '\n')
    
    if content != original_content:
        mdx_file.write_text(content, encoding='utf-8', newline='\n')
        fixed_count += 1
        print(f"Fixed: {mdx_file.name}")

print(f"\nProcessed {file_count} files, fixed {fixed_count} files")
