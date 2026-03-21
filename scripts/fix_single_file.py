from pathlib import Path

file_path = Path("data/blog/optimizing-glucose-during-intermittent-fasting.mdx")
content = file_path.read_text(encoding='utf-8')

# Remove the line with just a space (line 30)
lines = content.split('\n')
new_lines = []
for i, line in enumerate(lines):
    # Skip lines that are just whitespace between paragraph and image
    if i > 0 and i < len(lines) - 1:
        prev_line = lines[i-1]
        next_line = lines[i+1]
        # If current line is just whitespace, prev is text, next is empty or image
        if line.strip() == '' and prev_line.strip() == '' and next_line.startswith('!'):
            continue  # Skip this extra blank line
    new_lines.append(line)

file_path.write_text('\n'.join(new_lines), encoding='utf-8', newline='\n')
print(f"Fixed {file_path}")
