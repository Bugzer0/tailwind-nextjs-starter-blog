# Hướng dẫn triển khai AI Blog Generator — Glucose & Diabetes Health

## Tổng quan

Hệ thống tự động viết bài blog về **glucose, tiểu đường, và sức khỏe chuyển hóa** bằng Gemini AI:
- **Tự động chọn topic**: AI rà soát bài cũ, tự sinh chủ đề mới không trùng lặp
- **Tạo nội dung** (MDX) bằng Gemini 2.0 Flash — viết bằng tiếng Việt
- **Tạo ảnh** banner + inline bằng Gemini 2.0 Flash Image
- Tự động commit và push lên GitHub
- Workflow `pages.yml` hiện tại sẽ tự deploy khi có push vào `main`

### Tính năng chính
- **Không cần file topics.txt** — chỉ cần bấm "Run workflow" là có bài mới
- **Duplicate check** — scan tất cả bài viết hiện có trước khi viết
- **SEO-optimized** — title, summary, tags theo chuẩn SEO
- **Brand voice** — giọng văn thân thiện, giáo dục, đáng tin cậy
- **CTA tự nhiên** — gợi ý app quản lý đường huyết không aggressive

## Cấu trúc file

```
scripts/ai-blog-generator/
├── generate_post.py      # Script chính (auto-topic + duplicate check)
├── SKILL.md              # Brand voice, content strategy, templates
└── requirements.txt      # Python dependencies

.github/workflows/
└── generate-blog-post.yml  # GitHub Action workflow
```

## Bước 1: Lấy Gemini API Key

1. Truy cập [Google AI Studio](https://aistudio.google.com/apikey)
2. Đăng nhập bằng tài khoản Google
3. Click **"Create API Key"**
4. Chọn project hoặc tạo mới
5. Copy API key (dạng `AIza...`)

> **Lưu ý**: Gemini API miễn phí với giới hạn:
> - 2.5 Flash: 500 requests/ngày (free tier)
> - 2.0 Flash (image): 10 images/phút (free tier)
>
> Xem chi tiết tại [Gemini API Pricing](https://ai.google.dev/pricing)

## Bước 2: Thêm Secret vào GitHub Repository

1. Vào GitHub repo → **Settings** → **Secrets and variables** → **Actions**
2. Click **"New repository secret"**
3. Điền:
   - **Name**: `GEMINI_API_KEY`
   - **Secret**: paste API key từ bước 1
4. Click **"Add secret"**

![Settings → Secrets → Actions](https://docs.github.com/assets/cb-29441/mw-1440/images/help/actions/actions-secret-new.webp)

## Bước 3: Kiểm tra Workflow Permissions

1. Vào GitHub repo → **Settings** → **Actions** → **General**
2. Cuộn xuống phần **"Workflow permissions"**
3. Chọn **"Read and write permissions"**
4. Click **"Save"**

> Bước này cần thiết để workflow có quyền push commit lên repo.

## Bước 4: Push code lên GitHub

Commit và push tất cả file mới:

```bash
git add scripts/ai-blog-generator/ .github/workflows/generate-blog-post.yml
git commit -m "feat: add AI blog generator with GitHub Actions"
git push origin main
```

## Bước 5: Chạy thử (Manual)

1. Vào GitHub repo → tab **"Actions"**
2. Sidebar trái → chọn **"Generate AI Blog Post — Glucose & Diabetes Health"**
3. Click **"Run workflow"**
4. Có 2 cách:
   - **Để trống topic** → AI tự động chọn chủ đề mới (không trùng bài cũ)
   - **Nhập topic cụ thể**, ví dụ:
     ```
     Hướng dẫn đọc hiểu chỉ số A1C cho người mới
     ```
5. Click **"Run workflow"** (nút xanh)
6. Đợi workflow chạy xong (~2-5 phút)
7. Kiểm tra kết quả:
   - Tab **Actions** → click vào workflow run → xem logs
   - Tab **Code** → kiểm tra file mới trong `data/blog/` và `public/static/images/`

## Bước 6: Cấu hình chạy tự động (Schedule)

Mặc định workflow chạy tự động **mỗi thứ 2 lúc 8h sáng (UTC+7)**.

### Thay đổi lịch chạy

Sửa cron trong `.github/workflows/generate-blog-post.yml`:

```yaml
schedule:
  - cron: '0 1 * * 1'  # Thứ 2, 8h sáng UTC+7
```

Một số ví dụ cron:

| Cron | Mô tả |
|------|--------|
| `0 1 * * 1` | Thứ 2 hàng tuần, 8h sáng UTC+7 |
| `0 1 * * 1,4` | Thứ 2 và thứ 5, 8h sáng UTC+7 |
| `0 1 1 * *` | Ngày 1 hàng tháng, 8h sáng UTC+7 |
| `0 1 * * *` | Mỗi ngày, 8h sáng UTC+7 |

> **Lưu ý**: GitHub Actions dùng UTC. UTC+7 = UTC - 7 giờ, nên 8h sáng VN = 1h UTC.

### Tắt chạy tự động

Xóa hoặc comment block `schedule` trong workflow:

```yaml
on:
  workflow_dispatch:
    inputs:
      topic:
        description: 'Chủ đề bài viết'
        required: true
        type: string
  # schedule:
  #   - cron: '0 1 * * 1'
```

### Chế độ tự động (không cần topics.txt)

Khi chạy theo schedule hoặc không nhập topic, AI sẽ:
1. **Scan** tất cả bài viết hiện có trong `data/blog/`
2. **Phân tích** title, tags, summary của từng bài
3. **Tự sinh** chủ đề mới về glucose/tiểu đường không trùng lặp
4. **Chọn content type** phù hợp (how-to, review, listicle, myth-busting, case study, beginner's guide)

Không cần quản lý file chủ đề thủ công.

## Bước 7: Tùy chỉnh phong cách viết (SKILL.md)

File `scripts/ai-blog-generator/SKILL.md` chứa toàn bộ chiến lược nội dung:

- **Brand Voice**: The Guide + The Friend — thân thiện, giáo dục, đáng tin cậy
- **Content Pillars**: Educational (40%), Practical (30%), Inspirational (20%), Promotional (10%)
- **CTA Strategy**: Problem→Solution→Tool, Personal Experience, Comparison
- **Content Types**: How-To, App Review, Listicle, Myth Busting, Case Study, Beginner's Guide
- **SEO Guidelines**: keyword placement, title length, summary format
- **Tags**: glucose, diabetes, cgm, a1c, insulin, blood-sugar, nutrition, app-review, etc.

Tất cả nội dung viết bằng **tiếng Việt**, tập trung vào glucose monitoring và diabetes management.

## Luồng hoạt động chi tiết

```
┌──────────────────────────────────────────────────────────┐
│                    GitHub Actions                         │
│                                                           │
│  1. Trigger (manual hoặc schedule)                        │
│         │                                                 │
│         ▼                                                 │
│  2. generate_post.py                                      │
│     ├─ Step 0: Scan data/blog/*.mdx → lấy title/tags     │
│     ├─ Step 1: AI tự chọn topic mới (nếu không nhập)     │
│     ├─ Step 2: Gemini → metadata (title, summary, tags)   │
│     ├─ Step 3: Gemini → nội dung tiếng Việt (markdown)    │
│     ├─ Step 4: Gemini → banner.jpg + inline.jpg           │
│     └─ Step 5: Tạo file MDX với frontmatter + content     │
│         │                                                 │
│         ▼                                                 │
│  3. Git commit + push                                     │
│         │                                                 │
│         ▼                                                 │
│  4. Trigger pages.yml → build & deploy                    │
│                                                           │
└──────────────────────────────────────────────────────────┘
```

## Output

Mỗi lần chạy sẽ tạo:

```
data/blog/<slug>.mdx                        # Bài viết MDX
public/static/images/<slug>/banner.jpg       # Ảnh thumbnail
public/static/images/<slug>/inline.jpg       # Ảnh minh họa trong bài
```

File MDX có format:

```yaml
---
title: "Tiêu đề bài viết"
summary: |
  Mô tả ngắn cho SEO
tags: ["tag1", "tag2"]
date: 2026-03-19
draft: false
images: ["/static/images/slug/banner.jpg"]
---

Nội dung bài viết...

![illustration](/static/images/slug/inline.jpg)

Tiếp tục nội dung...
```

## Xử lý lỗi

| Lỗi | Nguyên nhân | Cách fix |
|-----|-------------|----------|
| `GEMINI_API_KEY not found` | Chưa thêm secret | Xem Bước 2 |
| `Permission denied` khi push | Workflow permissions | Xem Bước 3 |
| `Image generation failed` | Gemini safety filter block ảnh | Sửa image prompt trong SKILL.md cho phù hợp hơn |
| `Failed to parse JSON` | Gemini trả response không đúng format | Chạy lại, hoặc sửa system prompt |
| `AI returned empty topic` | Gemini không sinh được topic | Chạy lại, hoặc set BLOG_TOPIC thủ công |
| Workflow timeout (>10 phút) | API quá chậm hoặc treo | Kiểm tra Gemini API status |

## Giới hạn và lưu ý

- Gemini free tier có rate limit — không nên chạy quá 5 lần/ngày
- Ảnh do AI tạo có thể không hoàn hảo — review trước khi merge nếu cần
- Nếu muốn review trước khi publish, đổi `draft: false` thành `draft: true` trong `generate_post.py`
- Script có retry logic (3 lần, exponential backoff) cho API calls
- Slug trùng sẽ tự động append ngày (VD: `my-post-20260319`)
