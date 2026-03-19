#!/usr/bin/env python3
"""
AI Blog Post Generator using Google Gemini.
Generates MDX blog posts with AI-generated images for a Next.js blog.

Uses a 2-step approach to avoid JSON parsing issues:
  Step 1: Generate metadata (title, summary, tags, image prompts) as JSON
  Step 2: Generate full blog content as plain markdown text
"""

import os
import sys
import json
import time
from datetime import datetime
from pathlib import Path
from slugify import slugify

from google import genai
from google.genai import types
from PIL import Image
import io

MAX_RETRIES = 3
RETRY_DELAY = 5  # seconds


def get_client():
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("Error: GEMINI_API_KEY environment variable is required")
        sys.exit(1)
    return genai.Client(api_key=api_key)


def load_skill():
    """Load the blog writing skill/prompt from skill file."""
    skill_path = Path(__file__).parent / "SKILL.md"
    if skill_path.exists():
        return skill_path.read_text(encoding="utf-8")
    return ""


def sanitize_yaml_string(s: str) -> str:
    """Sanitize a string for safe use in YAML double-quoted scalar."""
    s = s.replace("\\", "\\\\")
    s = s.replace('"', '\\"')
    s = s.replace("\r\n", " ").replace("\r", " ").replace("\n", " ")
    return s.strip()


def retry_api_call(func):
    """Retry an API call with exponential backoff."""
    last_error = None
    for attempt in range(MAX_RETRIES):
        try:
            return func()
        except Exception as e:
            last_error = e
            if attempt == MAX_RETRIES - 1:
                raise
            wait = RETRY_DELAY * (2 ** attempt)
            print(f"  ⚠ API call failed (attempt {attempt + 1}/{MAX_RETRIES}): {e}")
            print(f"  ⏳ Retrying in {wait}s...")
            time.sleep(wait)
    raise last_error  # type: ignore[misc]


def generate_metadata(client, topic: str) -> dict:
    """Step 1: Generate blog metadata as structured JSON (small, safe to parse)."""
    response = retry_api_call(lambda: client.models.generate_content(
        model="gemini-2.5-flash",
        contents=f"Generate blog post metadata for the topic: {topic}",
        config=types.GenerateContentConfig(
            system_instruction="""Return ONLY a JSON object with blog post metadata. 
Do NOT include the blog content itself.

JSON structure:
{
  "title": "A compelling blog post title",
  "summary": "A 1-2 sentence SEO summary (single line, no newlines)",
  "tags": ["tag1", "tag2"],
  "image_prompts": {
    "banner": "Detailed prompt for a banner/thumbnail image",
    "inline": "Detailed prompt for an inline illustration"
  }
}

Rules:
- Write title and summary in the same language as the topic
- Tags should be lowercase English
- image_prompts should describe professional, visually appealing illustrations
- Keep summary under 200 characters
- 1-3 tags maximum""",
            temperature=0.7,
            response_mime_type="application/json",
        ),
    ))

    if not response.text:
        print("Error: Gemini returned empty metadata response")
        sys.exit(1)

    try:
        data = json.loads(response.text)
    except json.JSONDecodeError:
        print("Error: Failed to parse metadata JSON")
        print(f"Raw: {response.text[:500]}")
        sys.exit(1)

    for field in ["title", "summary"]:
        if not data.get(field):
            print(f"Error: Missing required field '{field}'")
            sys.exit(1)

    return data


def generate_content(client, topic: str, title: str, skill_prompt: str) -> str:
    """Step 2: Generate blog content as plain markdown (no JSON wrapping)."""
    response = retry_api_call(lambda: client.models.generate_content(
        model="gemini-2.5-flash",
        contents=f'Write a blog post titled "{title}" about: {topic}',
        config=types.GenerateContentConfig(
            system_instruction=f"""You are a technical blog writer.

{skill_prompt}

Write the blog post content in PLAIN MARKDOWN format.

Rules:
- Write in the same language as the topic
- Do NOT include any frontmatter (no --- block)
- Do NOT wrap in JSON or code fences
- Use ## for main sections and ### for subsections
- Include code examples where relevant (use proper markdown code blocks)
- Place exactly one line containing only <!-- INLINE_IMAGE --> where an illustration would help
- Start directly with the introduction paragraph (no title heading)
- Minimum 800 words""",
            temperature=0.8,
        ),
    ))

    if not response.text:
        print("Error: Gemini returned empty content response")
        sys.exit(1)

    content = response.text.strip()

    # Strip wrapping code fences if Gemini added them
    if content.startswith("```markdown"):
        content = content[len("```markdown"):].strip()
    if content.startswith("```md"):
        content = content[len("```md"):].strip()
    if content.startswith("```"):
        content = content[3:].strip()
    if content.endswith("```"):
        content = content[:-3].strip()

    return content


def generate_image(client, prompt: str, output_path: Path) -> bool:
    """Generate an image using Gemini's image generation."""
    try:
        response = retry_api_call(lambda: client.models.generate_content(
            model="gemini-2.0-flash-exp",
            contents=f"Generate an image: {prompt}",
            config=types.GenerateContentConfig(
                response_modalities=["IMAGE", "TEXT"],
            ),
        ))

        if not response.candidates:
            print("  ✗ No candidates in response (safety filter?)")
            return False

        content = response.candidates[0].content
        if not content or not content.parts:
            print("  ✗ Response has no content parts")
            return False

        for part in content.parts:
            if part.inline_data and part.inline_data.mime_type.startswith("image/"):
                image_data = part.inline_data.data
                image = Image.open(io.BytesIO(image_data))
                if image.mode in ("RGBA", "P"):
                    image = image.convert("RGB")
                output_path.parent.mkdir(parents=True, exist_ok=True)
                image.save(str(output_path), "JPEG", quality=85)
                print(f"  ✓ Image saved: {output_path}")
                return True

        print(f"  ✗ No image data in response for: {prompt[:80]}...")
        return False

    except Exception as e:
        print(f"  ✗ Image generation failed: {e}")
        return False


def create_blog_post(metadata: dict, content: str, slug_name: str, images_generated: dict):
    """Create the MDX file with frontmatter and content."""
    today = datetime.now().strftime("%Y-%m-%d")
    image_dir = f"/static/images/{slug_name}"

    # Build images list for frontmatter
    images_list = []
    if images_generated.get("banner"):
        images_list.append(f"{image_dir}/banner.jpg")

    # Process content - replace inline image placeholder
    if images_generated.get("inline") and "<!-- INLINE_IMAGE -->" in content:
        inline_img = f"\n![illustration]({image_dir}/inline.jpg)\n"
        content = content.replace("<!-- INLINE_IMAGE -->", inline_img)
    elif images_generated.get("inline"):
        lines = content.split("\n")
        inserted = False
        for i, line in enumerate(lines):
            if line.startswith("## ") and i > 0:
                inline_img = f"\n![illustration]({image_dir}/inline.jpg)\n"
                lines.insert(i + 1, inline_img)
                inserted = True
                break
        if inserted:
            content = "\n".join(lines)

    # Always remove any leftover placeholders to prevent MDX/JSX parse errors
    content = content.replace("<!-- INLINE_IMAGE -->", "")
    content = content.replace("{INLINE_IMAGE}", "")

    safe_title = sanitize_yaml_string(metadata["title"])
    safe_summary = sanitize_yaml_string(metadata["summary"])
    tags_str = json.dumps(metadata.get("tags", ["ai-generated"]))
    images_str = json.dumps(images_list)

    frontmatter = f'''---
title: "{safe_title}"
summary: |
  {safe_summary}
tags: {tags_str}
date: {today}
draft: false
images: {images_str}
---'''

    mdx_content = f"{frontmatter}\n\n{content}\n"

    mdx_path = Path(f"data/blog/{slug_name}.mdx")
    mdx_path.write_text(mdx_content, encoding="utf-8")
    print(f"✓ Blog post created: {mdx_path}")
    return mdx_path


def main():
    topic = os.environ.get("BLOG_TOPIC", "").strip()
    if not topic:
        print("Error: BLOG_TOPIC environment variable is required")
        sys.exit(1)

    print(f"🚀 Generating blog post about: {topic}")
    print("=" * 60)

    client = get_client()
    skill_prompt = load_skill()

    # Step 1: Generate metadata (JSON - small, safe to parse)
    print("\n📋 Generating metadata...")
    metadata = generate_metadata(client, topic)
    print(f"  ✓ Title: {metadata['title']}")
    print(f"  ✓ Tags: {metadata.get('tags', [])}")

    # Step 2: Generate content (plain markdown - no JSON parsing needed)
    print("\n📝 Generating content...")
    content = generate_content(client, topic, metadata["title"], skill_prompt)
    word_count = len(content.split())
    print(f"  ✓ Content generated ({word_count} words)")

    # Step 3: Create slug
    slug_name = slugify(metadata["title"], max_length=60)
    if not slug_name:
        slug_name = slugify(topic, max_length=60) or f"post-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
    print(f"  ✓ Slug: {slug_name}")

    # Step 4: Check for duplicate slug
    mdx_path = Path(f"data/blog/{slug_name}.mdx")
    if mdx_path.exists():
        slug_name = f"{slug_name}-{datetime.now().strftime('%Y%m%d')}"
        print(f"  ⚠ Slug already exists, using: {slug_name}")

    # Step 5: Generate images
    images_generated = {}
    image_prompts = metadata.get("image_prompts", {})
    image_dir = Path(f"public/static/images/{slug_name}")

    if image_prompts.get("banner"):
        print("\n🎨 Generating banner image...")
        images_generated["banner"] = generate_image(
            client, image_prompts["banner"], image_dir / "banner.jpg"
        )

    if image_prompts.get("inline"):
        print("🎨 Generating inline image...")
        images_generated["inline"] = generate_image(
            client, image_prompts["inline"], image_dir / "inline.jpg"
        )

    # Step 6: Create MDX file
    print("\n📄 Creating MDX file...")
    created_path = create_blog_post(metadata, content, slug_name, images_generated)

    # Output for GitHub Actions
    github_output = os.environ.get("GITHUB_OUTPUT")
    if github_output:
        with open(github_output, "a") as f:
            f.write(f"slug={slug_name}\n")
            safe_title = metadata["title"].replace('"', "").replace("'", "")
            safe_title = safe_title.replace("\n", " ").replace("\r", "")[:80]
            f.write(f"title={safe_title}\n")
            f.write(f"mdx_path={created_path}\n")

    print("\n" + "=" * 60)
    print("✅ Done!")


if __name__ == "__main__":
    main()
