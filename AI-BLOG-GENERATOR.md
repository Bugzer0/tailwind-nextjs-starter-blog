# Hướng dẫn triển khai AI Blog Generator với GitHub Actions

## Tổng quan

Hệ thống tự động viết bài blog bằng Gemini AI, bao gồm:
- Tạo nội dung bài viết (MDX) bằng Gemini 2.5 Flash
- Tạo ảnh banner + ảnh inline bằng Gemini 2.0 Flash
- Tự động commit và push lên GitHub
- Workflow `pages.yml` hiện tại sẽ tự deploy khi có push vào `main`

## Cấu trúc file

```
scripts/ai-blog-generator/
├── generate_post.py      # Script chính
├── SKILL.md              # Hướng dẫn phong cách viết cho AI
├── topics.txt            # Danh sách chủ đề cho chế độ tự động
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
2. Sidebar trái → chọn **"Generate AI Blog Post"**
3. Click **"Run workflow"**
4. Nhập chủ đề bài viết, ví dụ:
   ```
   Hướng dẫn sử dụng Docker Compose cho dự án Next.js
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

### Quản lý danh sách chủ đề tự động

Khi chạy theo schedule, workflow sẽ random 1 chủ đề từ `scripts/ai-blog-generator/topics.txt`.

Sửa file này để thêm/bớt chủ đề:

```
Hướng dẫn sử dụng Docker Compose cho dự án Next.js
So sánh Bun vs Node.js - Khi nào nên dùng cái nào
Tối ưu performance cho React Server Components
```

Mỗi dòng là 1 chủ đề. Dòng trống sẽ bị bỏ qua.

## Bước 7: Tùy chỉnh phong cách viết (SKILL.md)

File `scripts/ai-blog-generator/SKILL.md` là "skill" hướng dẫn AI cách viết bài.

Bạn có thể tùy chỉnh:
- Phong cách viết (formal/casual, ngôn ngữ)
- Cấu trúc bài viết (số heading, độ dài)
- Quy tắc nội dung (có code example không, tags nào)
- Yêu cầu đặc biệt (luôn viết tiếng Việt, thêm emoji, v.v.)

Ví dụ thêm rule viết tiếng Việt:

```markdown
## Language
- Always write in Vietnamese
- Use Vietnamese technical terms where possible, keep English for code/library names
```

## Luồng hoạt động chi tiết

```
┌─────────────────────────────────────────────────────┐
│                  GitHub Actions                      │
│                                                      │
│  1. Trigger (manual hoặc schedule)                   │
│         │                                            │
│         ▼                                            │
│  2. Resolve topic                                    │
│     ├─ Manual: dùng input từ user                    │
│     └─ Schedule: random từ topics.txt                │
│         │                                            │
│         ▼                                            │
│  3. generate_post.py                                 │
│     ├─ Gọi Gemini 2.5 Flash → viết nội dung (JSON)  │
│     ├─ Gọi Gemini 2.0 Flash → tạo banner.jpg        │
│     ├─ Gọi Gemini 2.0 Flash → tạo inline.jpg        │
│     └─ Tạo file MDX với frontmatter + content        │
│         │                                            │
│         ▼                                            │
│  4. Git commit + push                                │
│         │                                            │
│         ▼                                            │
│  5. Trigger pages.yml → build & deploy               │
│                                                      │
└─────────────────────────────────────────────────────┘
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
| `No topic provided` | Schedule chạy nhưng topics.txt trống | Thêm chủ đề vào topics.txt |
| Workflow timeout (>10 phút) | API quá chậm hoặc treo | Kiểm tra Gemini API status |

## Giới hạn và lưu ý

- Gemini free tier có rate limit — không nên chạy quá 5 lần/ngày
- Ảnh do AI tạo có thể không hoàn hảo — review trước khi merge nếu cần
- Nếu muốn review trước khi publish, đổi `draft: false` thành `draft: true` trong `generate_post.py`
- Script có retry logic (3 lần, exponential backoff) cho API calls
- Slug trùng sẽ tự động append ngày (VD: `my-post-20260319`)
