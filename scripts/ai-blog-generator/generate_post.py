#!/usr/bin/env python3
"""
AI Blog Post Generator for GlucoAI — Glucose & Diabetes Health Blog.
Generates MDX blog posts with AI-generated images for a Next.js blog.

Flow:
  Step 0: Scan existing blog posts to build context (avoid duplicates)
  Step 1: Auto-generate a unique topic (or use BLOG_TOPIC env if provided)
  Step 2: Generate metadata (title, summary, tags, image prompts) as JSON
  Step 3: Generate full blog content as plain markdown
  Step 4: Generate images
  Step 5: Create MDX file
"""

import os
import sys
import json
import re
import time
from datetime import datetime
from pathlib import Path
from typing import List, Dict
from slugify import slugify

from google import genai
from google.genai import types
from PIL import Image
import io

MAX_RETRIES = 3
RETRY_DELAY = 5  # seconds

# Project root — resolve relative to this script's location
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
BLOG_DIR = PROJECT_ROOT / "data" / "blog"


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


# ---------------------------------------------------------------------------
# Step 0: Scan existing posts
# ---------------------------------------------------------------------------

def scan_existing_posts() -> List[Dict]:
    """Scan all .mdx files in data/blog/ and extract title, tags, summary."""
    posts = []
    if not BLOG_DIR.exists():
        return posts

    for mdx_file in sorted(BLOG_DIR.glob("*.mdx")):
        try:
            text = mdx_file.read_text(encoding="utf-8")
        except Exception:
            continue

        # Extract YAML frontmatter between --- markers
        fm_match = re.match(r"^---\s*\n(.*?)\n---", text, re.DOTALL)
        if not fm_match:
            continue

        fm_text = fm_match.group(1)

        title = ""
        summary = ""
        tags_list = []

        # Parse title
        title_match = re.search(r'^title:\s*["\']?(.*?)["\']?\s*$', fm_text, re.MULTILINE)
        if title_match:
            title = title_match.group(1).strip()

        # Parse summary (handle multiline YAML |)
        summary_match = re.search(r'^summary:\s*\|?\s*\n?\s*(.*?)(?:\n\w|\Z)', fm_text, re.MULTILINE | re.DOTALL)
        if summary_match:
            summary = summary_match.group(1).strip().replace("\n", " ")
        else:
            summary_match = re.search(r'^summary:\s*["\']?(.*?)["\']?\s*$', fm_text, re.MULTILINE)
            if summary_match:
                summary = summary_match.group(1).strip()

        # Parse tags
        tags_match = re.search(r'^tags:\s*(\[.*?\])', fm_text, re.MULTILINE)
        if tags_match:
            try:
                tags_list = json.loads(tags_match.group(1))
            except json.JSONDecodeError:
                tags_list = []

        posts.append({
            "file": mdx_file.name,
            "title": title,
            "summary": summary[:200],
            "tags": tags_list,
        })

    return posts


def build_existing_posts_context(posts: list[dict]) -> str:
    """Build a concise summary of existing posts for the AI to avoid duplicates."""
    if not posts:
        return "No existing blog posts found."

    lines = [f"There are {len(posts)} existing blog posts:"]
    for i, p in enumerate(posts, 1):
        tags_str = ", ".join(p["tags"]) if p["tags"] else "none"
        lines.append(f"{i}. \"{p['title']}\" [tags: {tags_str}]")
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Step 1: Auto-generate topic
# ---------------------------------------------------------------------------

def generate_topic(client, existing_context: str, skill_prompt: str) -> str:
    """Use AI to generate a unique blog topic about glucose/diabetes."""
    response = retry_api_call(lambda: client.models.generate_content(
        model="gemini-2.0-flash",
        contents=f"""Generate ONE new blog post topic for a Vietnamese glucose/diabetes health blog.

{existing_context}

IMPORTANT: The new topic MUST be different from ALL existing posts listed above.
Choose a topic that would attract readers interested in glucose monitoring, diabetes management, metabolic health, CGM technology, or healthy lifestyle for blood sugar control.""",
        config=types.GenerateContentConfig(
            system_instruction=f"""You are a content strategist for a Vietnamese health blog about glucose and diabetes.

Reference the content strategy below to pick topics from the right content pillars:
{skill_prompt}

Return ONLY a JSON object:
{{
  "topic": "A specific blog topic description in Vietnamese (1-2 sentences)",
  "content_type": "how-to|app-review|listicle|myth-busting|case-study|beginners-guide",
  "primary_keyword": "main SEO keyword in Vietnamese",
  "reasoning": "Brief explanation of why this topic is valuable and how it differs from existing posts"
}}

Rules:
- Topic MUST be in Vietnamese
- Topic should be specific enough to write a focused 800-2500 word article
- Pick topics that naturally lead to mentioning glucose monitoring apps
- Vary content types — don't always pick the same type
- Consider seasonal relevance and trending health topics""",
            temperature=0.9,
            response_mime_type="application/json",
        ),
    ))

    if not response.text:
        print("Error: Gemini returned empty topic response")
        sys.exit(1)

    try:
        data = json.loads(response.text)
    except json.JSONDecodeError:
        print("Error: Failed to parse topic JSON")
        print(f"Raw: {response.text[:500]}")
        sys.exit(1)

    topic = data.get("topic", "").strip()
    if not topic:
        print("Error: AI returned empty topic")
        sys.exit(1)

    content_type = data.get("content_type", "unknown")
    keyword = data.get("primary_keyword", "")
    reasoning = data.get("reasoning", "")

    print(f"  ✓ Topic: {topic}")
    print(f"  ✓ Type: {content_type}")
    print(f"  ✓ Keyword: {keyword}")
    if reasoning:
        print(f"  ✓ Reasoning: {reasoning}")

    return topic


# ---------------------------------------------------------------------------
# Step 2: Generate metadata
# ---------------------------------------------------------------------------

def generate_metadata(client, topic: str, existing_context: str) -> dict:
    """Generate blog metadata as structured JSON."""
    response = retry_api_call(lambda: client.models.generate_content(
        model="gemini-2.0-flash",
        contents=f"Generate blog post metadata for the topic: {topic}",
        config=types.GenerateContentConfig(
            system_instruction=f"""Return ONLY a JSON object with blog post metadata.
Do NOT include the blog content itself.

JSON structure:
{{
  "title": "A compelling blog post title in Vietnamese",
  "summary": "A 1-2 sentence SEO summary in Vietnamese (single line, no newlines)",
  "tags": ["tag1", "tag2"],
  "image_prompts": {{
    "banner": "Detailed prompt for a banner/thumbnail image about glucose/health",
    "inline1": "Detailed prompt for first inline illustration (appears after first section)",
    "inline2": "Detailed prompt for second inline illustration (appears mid-article)"
  }}
}}

{existing_context}

Rules:
- Title and summary MUST be in Vietnamese
- Title should contain the primary SEO keyword, under 60 characters
- Tags should be lowercase English from this list: glucose, diabetes, cgm, a1c, insulin, blood-sugar, nutrition, diet, app-review, tips, health, metabolic-health, freestyle-libre, dexcom, type-1, type-2, prediabetes
- image_prompts: MUST include banner, inline1, and inline2 (3 images total)
- All image prompts should describe clean, modern, health-themed illustrations (no text in images, no faces)
- inline1: illustration for early in article (after first main section)
- inline2: illustration for mid-article (around 50-60% through content)
- Keep summary under 200 characters
- 1-3 tags maximum
- Title MUST be different from all existing posts""",
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


# ---------------------------------------------------------------------------
# Step 3: Generate content
# ---------------------------------------------------------------------------

def generate_content(client, topic: str, title: str, skill_prompt: str, existing_context: str) -> str:
    """Generate blog content as plain markdown."""
    response = retry_api_call(lambda: client.models.generate_content(
        model="gemini-2.0-flash",
        contents=f'Write a blog post titled "{title}" about: {topic}',
        config=types.GenerateContentConfig(
            system_instruction=f"""You are a Vietnamese health blog writer specializing in glucose monitoring and diabetes management.

{skill_prompt}

{existing_context}
If any existing posts are related, you may reference them with relative links like [bài viết liên quan](/blog/slug-name) to build internal linking.

Write the blog post content in PLAIN MARKDOWN format.

Rules:
- Write ENTIRELY in Vietnamese
- Do NOT include any frontmatter (no --- block)
- Do NOT wrap in JSON or code fences
- Use ## for main sections and ### for subsections
- MUST include `<!-- INLINE_IMAGE_1 -->` placeholder after the first main section
- MUST include `<!-- INLINE_IMAGE_2 -->` placeholder around 50-60% through the article
- Start directly with the introduction paragraph (no title heading)
- Minimum 800 words, maximum 2500 words
- Follow the CTA strategy: naturally mention relevant apps when solving a problem
- End with a "Tóm Lại" or "Kết Luận" section with key takeaways
- Include a natural call-to-action at the end""",
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


# ---------------------------------------------------------------------------
# Step 4: Generate images
# ---------------------------------------------------------------------------

def generate_image(client, prompt: str, output_path: Path) -> bool:
    """Generate an image using Gemini's image generation model."""
    try:
        response = retry_api_call(lambda: client.models.generate_content(
            model="gemini-2.0-flash-exp-image-generation",
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


# ---------------------------------------------------------------------------
# Step 5: Create MDX file
# ---------------------------------------------------------------------------

def create_blog_post(metadata: dict, content: str, slug_name: str, images_generated: dict):
    """Create the MDX file with frontmatter and content."""
    today = datetime.now().strftime("%Y-%m-%d")
    image_dir = f"/static/images/{slug_name}"

    # Build images list for frontmatter
    images_list = []
    if images_generated.get("banner"):
        images_list.append(f"{image_dir}/banner.jpg")

    # Process content - replace inline image placeholders
    if images_generated.get("inline1"):
        if "<!-- INLINE_IMAGE_1 -->" in content:
            inline1_img = f"\n![illustration]({image_dir}/inline1.jpg)\n"
            content = content.replace("<!-- INLINE_IMAGE_1 -->", inline1_img)
        else:
            # Fallback: insert after first ## section
            lines = content.split("\n")
            for i, line in enumerate(lines):
                if line.startswith("## ") and i > 0:
                    inline1_img = f"\n![illustration]({image_dir}/inline1.jpg)\n"
                    lines.insert(i + 1, inline1_img)
                    break
            content = "\n".join(lines)

    if images_generated.get("inline2"):
        if "<!-- INLINE_IMAGE_2 -->" in content:
            inline2_img = f"\n![illustration]({image_dir}/inline2.jpg)\n"
            content = content.replace("<!-- INLINE_IMAGE_2 -->", inline2_img)
        else:
            # Fallback: insert at middle of content
            lines = content.split("\n")
            mid_point = len(lines) // 2
            inserted = False
            for i in range(mid_point, len(lines)):
                if lines[i].startswith("## "):
                    inline2_img = f"\n![illustration]({image_dir}/inline2.jpg)\n"
                    lines.insert(i + 1, inline2_img)
                    inserted = True
                    break
            if inserted:
                content = "\n".join(lines)

    # Always remove any leftover placeholders to prevent MDX/JSX parse errors
    content = content.replace("<!-- INLINE_IMAGE_1 -->", "")
    content = content.replace("<!-- INLINE_IMAGE_2 -->", "")
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

    mdx_path = BLOG_DIR / f"{slug_name}.mdx"
    mdx_path.parent.mkdir(parents=True, exist_ok=True)
    mdx_path.write_text(mdx_content, encoding="utf-8")
    print(f"✓ Blog post created: {mdx_path}")
    return mdx_path


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    print("🩺 GlucoAI Blog Generator — Glucose & Diabetes Health")
    print("=" * 60)

    client = get_client()
    skill_prompt = load_skill()

    # Step 0: Scan existing posts
    print("\n🔍 Scanning existing blog posts...")
    existing_posts = scan_existing_posts()
    existing_context = build_existing_posts_context(existing_posts)
    print(f"  ✓ Found {len(existing_posts)} existing posts")
    for p in existing_posts:
        print(f"    • {p['title']}")

    # Step 1: Get or generate topic
    topic = os.environ.get("BLOG_TOPIC", "").strip()
    if topic:
        print(f"\n📌 Using provided topic: {topic}")
    else:
        print("\n🧠 Auto-generating a new unique topic...")
        topic = generate_topic(client, existing_context, skill_prompt)

    # Step 2: Generate metadata
    print("\n📋 Generating metadata...")
    metadata = generate_metadata(client, topic, existing_context)
    print(f"  ✓ Title: {metadata['title']}")
    print(f"  ✓ Summary: {metadata['summary'][:100]}...")
    print(f"  ✓ Tags: {metadata.get('tags', [])}")

    # Step 3: Generate content
    print("\n📝 Generating content...")
    content = generate_content(client, topic, metadata["title"], skill_prompt, existing_context)
    word_count = len(content.split())
    print(f"  ✓ Content generated ({word_count} words)")

    # Step 4: Create slug & check duplicates
    slug_name = slugify(metadata["title"], max_length=60)
    if not slug_name:
        slug_name = slugify(topic, max_length=60) or f"post-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
    print(f"  ✓ Slug: {slug_name}")

    mdx_path = BLOG_DIR / f"{slug_name}.mdx"
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

    if image_prompts.get("inline1"):
        print("🎨 Generating inline image 1...")
        images_generated["inline1"] = generate_image(
            client, image_prompts["inline1"], image_dir / "inline1.jpg"
        )

    if image_prompts.get("inline2"):
        print("🎨 Generating inline image 2...")
        images_generated["inline2"] = generate_image(
            client, image_prompts["inline2"], image_dir / "inline2.jpg"
        )

    # Validate: warn if missing inline images
    inline_count = sum([bool(images_generated.get("inline1")), bool(images_generated.get("inline2"))])
    if inline_count < 2:
        print(f"  ⚠ Warning: Only {inline_count}/2 inline images generated successfully")

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
    print("✅ Done! New glucose/diabetes blog post created successfully.")


if __name__ == "__main__":
    main()
