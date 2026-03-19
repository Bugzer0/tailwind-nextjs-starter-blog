#!/usr/bin/env python3
"""
AI Blog Post Generator using Google Gemini.
Generates MDX blog posts with AI-generated images for a Next.js blog.
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
    # Collapse newlines to space (YAML double-quoted strings)
    s = s.replace("\r\n", " ").replace("\r", " ").replace("\n", " ")
    return s.strip()


def retry_api_call(func, *args, **kwargs):
    """Retry an API call with exponential backoff."""
    last_error = None
    for attempt in range(MAX_RETRIES):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            last_error = e
            if attempt == MAX_RETRIES - 1:
                raise
            wait = RETRY_DELAY * (2 ** attempt)
            print(f"  ⚠ API call failed (attempt {attempt + 1}/{MAX_RETRIES}): {e}")
            print(f"  ⏳ Retrying in {wait}s...")
            time.sleep(wait)
    # Should never reach here, but just in case
    raise last_error  # type: ignore[misc]


def generate_blog_content(client, topic: str, skill_prompt: str) -> dict:
    """Generate blog post content using Gemini."""
    system_prompt = f"""You are a technical blog writer. Write high-quality, engaging blog posts.

{skill_prompt}

IMPORTANT: Return your response as valid JSON with this exact structure:
{{
  "title": "The blog post title",
  "summary": "A 1-2 sentence summary for SEO",
  "tags": ["tag1", "tag2"],
  "content": "The full markdown content of the blog post (without frontmatter)",
  "image_prompts": {{
    "banner": "A detailed prompt to generate a banner/thumbnail image for this post. Describe a visually appealing, professional illustration.",
    "inline": "A detailed prompt to generate an inline illustration that complements a key section of the post."
  }}
}}

Rules:
- Write in the same language as the topic provided
- Content should be well-structured with headings (##, ###)
- Include code examples where relevant
- The content field should NOT include frontmatter (no --- block)
- image_prompts should describe images that are relevant to the blog topic
- Banner image should be eye-catching and represent the overall topic
- Inline image should illustrate a specific concept from the post
- Mark where the inline image should be placed by including exactly one line: {{INLINE_IMAGE}} in the content
"""

    def _call():
        return client.models.generate_content(
            model="gemini-2.5-flash",
            contents=f"Write a blog post about: {topic}",
            config=types.GenerateContentConfig(
                system_instruction=system_prompt,
                temperature=0.8,
                response_mime_type="application/json",
            ),
        )

    response = retry_api_call(_call)

    if not response.text:
        print("Error: Gemini returned empty response (possibly blocked by safety filter)")
        sys.exit(1)

    try:
        data = json.loads(response.text)
    except json.JSONDecodeError:
        print("Error: Failed to parse Gemini response as JSON")
        print(f"Raw response: {response.text[:500]}")
        sys.exit(1)

    # Validate required fields
    required = ["title", "summary", "content"]
    for field in required:
        if not data.get(field):
            print(f"Error: Missing required field '{field}' in Gemini response")
            sys.exit(1)

    return data


def generate_image(client, prompt: str, output_path: Path) -> bool:
    """Generate an image using Gemini's image generation."""
    try:
        def _call():
            return client.models.generate_content(
                model="gemini-2.0-flash-exp",
                contents=f"Generate an image: {prompt}",
                config=types.GenerateContentConfig(
                    response_modalities=["IMAGE", "TEXT"],
                ),
            )

        response = retry_api_call(_call)

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


def create_blog_post(blog_data: dict, slug_name: str, images_generated: dict):
    """Create the MDX file with frontmatter and content."""
    today = datetime.now().strftime("%Y-%m-%d")
    image_dir = f"/static/images/{slug_name}"

    # Build images list for frontmatter
    images_list = []
    if images_generated.get("banner"):
        images_list.append(f"{image_dir}/banner.jpg")

    # Process content - replace inline image placeholder
    content = blog_data["content"]
    if images_generated.get("inline") and "{INLINE_IMAGE}" in content:
        inline_img = f"\n![illustration]({image_dir}/inline.jpg)\n"
        content = content.replace("{INLINE_IMAGE}", inline_img)
    elif images_generated.get("inline"):
        # If no placeholder, insert after first ## heading
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

    # Escape title for YAML safety, flatten summary to single line
    safe_title = sanitize_yaml_string(blog_data["title"])
    safe_summary = sanitize_yaml_string(blog_data["summary"])

    # Build tags and images as JSON arrays (valid YAML)
    tags_str = json.dumps(blog_data.get("tags", ["ai-generated"]))
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

    # Step 1: Generate blog content
    print("\n📝 Generating blog content...")
    blog_data = generate_blog_content(client, topic, skill_prompt)
    print(f"  ✓ Title: {blog_data['title']}")
    print(f"  ✓ Tags: {blog_data.get('tags', [])}")

    # Step 2: Create slug from title
    slug_name = slugify(blog_data["title"], max_length=60)
    if not slug_name:
        # Fallback slug from topic or timestamp
        slug_name = slugify(topic, max_length=60) or f"post-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
    print(f"  ✓ Slug: {slug_name}")

    # Step 3: Check for duplicate slug
    mdx_path = Path(f"data/blog/{slug_name}.mdx")
    if mdx_path.exists():
        slug_name = f"{slug_name}-{datetime.now().strftime('%Y%m%d')}"
        print(f"  ⚠ Slug already exists, using: {slug_name}")

    # Step 4: Generate images
    images_generated = {}
    image_prompts = blog_data.get("image_prompts", {})

    if image_prompts.get("banner"):
        print("\n🎨 Generating banner image...")
        image_dir = Path(f"public/static/images/{slug_name}")
        images_generated["banner"] = generate_image(
            client, image_prompts["banner"], image_dir / "banner.jpg"
        )

    if image_prompts.get("inline"):
        print("🎨 Generating inline image...")
        image_dir = Path(f"public/static/images/{slug_name}")
        images_generated["inline"] = generate_image(
            client, image_prompts["inline"], image_dir / "inline.jpg"
        )

    # Step 5: Create MDX file
    print("\n📄 Creating MDX file...")
    created_path = create_blog_post(blog_data, slug_name, images_generated)

    # Output for GitHub Actions
    github_output = os.environ.get("GITHUB_OUTPUT")
    if github_output:
        with open(github_output, "a") as f:
            f.write(f"slug={slug_name}\n")
            # Sanitize title: remove quotes, newlines, limit length
            safe_title = blog_data["title"].replace('"', "").replace("'", "")
            safe_title = safe_title.replace("\n", " ").replace("\r", "")[:80]
            f.write(f"title={safe_title}\n")
            f.write(f"mdx_path={created_path}\n")

    print("\n" + "=" * 60)
    print("✅ Done!")


if __name__ == "__main__":
    main()
