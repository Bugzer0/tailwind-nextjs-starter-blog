# 🚀 Hướng Dẫn Chạy Dự Án Tailwind Next.js Starter Blog

## 📋 Yêu cầu hệ thống

- **Node.js**: 18.17+ hoặc 20+
- **npm/yarn**: Latest version
- **OS**: Windows 10/11, macOS, Linux

---

## ⚡ Quick Start (Nhanh nhất)

### 1. Cài đặt dependencies

```bash
# Sử dụng yarn (khuyến nghị)
yarn install

# Hoặc npm
npm install
```

### 2. Chạy development server

```bash
# Development mode với hot reload
yarn dev

# Hoặc
npm run dev
```


### 3. Mở trình duyệt

👉 [http://localhost:3000](http://localhost:3000)

---

## 📝 Các lệnh hữu ích

```bash
# Development
yarn dev              # Chạy server development (port 3000)
yarn build            # Build cho production
yarn start            # Chạy production server
yarn lint             # Kiểm tra và sửa lỗi code
yarn analyze          # Phân tích bundle size

# Development nâng cao
yarn dev:debug        # Debug mode
yarn build:debug      # Build với debug info
```

---

1. Chạy TypeScript Check

npx tsc --noEmit

Khuyến nghị: Chạy yarn build trước khi push lên Cloudflare Pages để đảm bảo không có lỗi build.
yarn build

## 🔧 Cấu hình ban đầu

### 1. Cấu hình site metadata

File: `data/siteMetadata.js`

```javascript
export const siteMetadata = {
  title: 'Tên Blog Của Bạn',
  author: 'Tên Tác Giả',
  description: 'Mô tả ngắn về blog',
  siteUrl: 'https://ten-blog-cua-ban.vercel.app',
  // ... các cấu hình khác
}
```

### 2. Cấu hình navigation

File: `data/headerNavLinks.js`

```javascript
const headerNavLinks = [
  { title: 'Blog', href: '/blog' },
  { title: 'Tags', href: '/tags' },
  { title: 'About', href: '/about' },
  { title: 'Projects', href: '/projects' },
]
```

### 3. Cấu hình tác giả

File: `data/authors/default.md`

```markdown
---
name: Tên Của Bạn
avatar: /static/images/avatar.png
occupation: 'Frontend Developer'
company: 'Tên Công Ty'
email: 'email@example.com'
twitter: 'https://twitter.com/username'
linkedin: 'https://linkedin.com/in/username'
github: 'https://github.com/username'
---
```

---

## 📁 Cấu trúc thư mục quan trọng

```
├── app/                    # Next.js App Router
│   ├── layout.tsx         # Root layout
│   ├── page.tsx           # Trang chủ
│   ├── blog/              # Blog routes
│   └── tags/              # Tag pages
├── components/             # React components
├── data/                  # Dữ liệu tĩnh
│   ├── siteMetadata.js    # Site config
│   ├── authors/           # Thông tin tác giả
│   └── blog/              # Blog posts (.md files)
├── layouts/               # Layout templates
├── public/                # Static assets
└── styles/                # CSS files
```

---

## 📝 Viết bài blog mới

### 1. Tạo file markdown mới

File: `data/blog/ten-bai-viet.md`

````markdown
---
title: 'Tiêu Đề Bài Viết'
date: '2024-03-19'
tags: ['nextjs', 'tailwind', 'tutorial']
draft: false
summary: 'Mô tả ngắn về bài viết'
images: ['/static/images/preview.jpg']
authors: ['default']
layout: PostLayout
---

Nội dung bài viết của bạn ở đây...

## Cú pháp Markdown hỗ trợ

- **Bold text**
- _Italic text_
- `Inline code`

```javascript
// Code block với syntax highlighting
const hello = 'world'
```
````

> Quote block

- [Link](/blog/other-post)
- ![Image](/static/images/image.jpg)

````

### 2. Frontmatter fields hỗ trợ

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `title` | string | ✅ | Tiêu đề bài viết |
| `date` | string | ✅ | Ngày đăng (YYYY-MM-DD) |
| `tags` | array | ❌ | Tags bài viết |
| `draft` | boolean | ❌ | Draft mode (default: false) |
| `summary` | string | ❌ | Mô tả ngắn |
| `images` | array | ❌ | URLs hình ảnh |
| `authors` | array | ❌ | Tác giả (default: ['default']) |
| `layout` | string | ❌ | Layout template |

---

## 🎨 Tùy chỉnh giao diện

### 1. Thay đổi màu chủ đạo
File: `tailwind.config.js`
```javascript
theme: {
  extend: {
    colors: {
      primary: '#your-color',
    },
  },
},
````

### 2. Tùy chỉnh CSS

File: `styles/globals.css`

```css
/* Custom styles here */
.custom-class {
  /* your styles */
}
```

---

## 🔍 Tìm kiếm và SEO

### 1. Tìm kiếm (Kbar)

- Tự động index tất cả blog posts
- Sử dụng `Ctrl+K` hoặc `Cmd+K` để mở

### 2. SEO optimization

- Tự động tạo sitemap: `/sitemap.xml`
- Tự động tạo RSS feed: `/feed.xml`
- Robots.txt: `/robots.txt`

---

## 📱 Testing

### 1. Lighthouse score

```bash
# Build và kiểm tra performance
yarn build
yarn start

# Mở Chrome DevTools → Lighthouse tab
```

### 2. Responsive testing

- Test trên các kích thước màn hình khác nhau
- Kiểm tra mobile view

---

## 🚀 Deploy

### 1. Cloudflare Pages (Khuyến nghị - Miễn phí & Nhanh)

**Ưu điểm:**

- ✅ Global CDN (200+ locations)
- ✅ Tự động deploy khi push GitHub
- ✅ Unlimited requests
- ✅ SSL miễn phí
- ✅ 100GB bandwidth/tháng

**Quick Setup:**

1. Push code lên GitHub
2. Kết nối repo với Cloudflare Pages
3. Cấu hình build:
   - Build command: `yarn build`
   - Output directory: `out`
   - Environment variables: `EXPORT=1`, `UNOPTIMIZED=1`

📖 **[Xem hướng dẫn chi tiết](./CLOUDFLARE-DEPLOY.md)**

### 2. Vercel

```bash
# Install Vercel CLI
npm i -g vercel

# Deploy
vercel

# Deploy production
vercel --prod
```

### 3. GitHub Pages

```bash
# Build static
EXPORT=1 UNOPTIMIZED=1 yarn build

# Deploy folder `out`
```

### 4. Netlify

- Connect repo trên Netlify
- Build command: `yarn build`
- Publish directory: `.next`

---

## 🔧 Troubleshooting

### Common Issues

**1. Port 3000 đang được sử dụng**

```bash
# Sử dụng port khác
yarn dev -p 3001
```

**2. Lỗi TypeScript**

```bash
# Kiểm tra types
yarn build

# Sửa lỗi tự động
yarn lint --fix
```

**3. Build lỗi trên Windows**

```bash
# Set environment variable
$env:PWD = $(Get-Location).Path
yarn build
```

**4. Images không hiển thị**

- Kiểm tra path trong `public/` folder
- Đảm bảo file tồn tại

---

## 📊 Performance Optimization

### 1. Image optimization

```javascript
// Sử dụng next/image với đúng props
<Image
  src="/path/to/image.jpg"
  alt="Description"
  width={800}
  height={400}
  sizes="100vw"
  priority={true} // Cho LCP images
/>
```

### 2. Bundle analysis

```bash
# Phân tích bundle size
yarn analyze
```

---

## 🛠️ Development Tips

### 1. Hot reload

- Tự động reload khi save file
- CSS changes update instantly
- Component changes require refresh

### 2. Debug mode

```bash
# Debug Next.js
DEBUG=* yarn dev

# Debug build
yarn build:debug
```

### 3. Environment variables

File: `.env.local`

```env
NEXT_PUBLIC_SITE_URL=https://your-site.com
NEXT_PUBLIC_ANALYTICS_ID=your-id
```

---

## 📚 Resources hữu ích

- [Next.js Documentation](https://nextjs.org/docs)
- [Tailwind CSS Docs](https://tailwindcss.com/docs)
- [MDX Documentation](https://mdxjs.com/)
- [Contentlayer](https://www.contentlayer.dev/)

---

## 🆘 Help & Support

1. **Check logs**: Terminal output cho error messages
2. **Browser console**: F12 → Console tab
3. **Network tab**: Kiểm tra failed requests
4. **Issues**: GitHub issues của template

---

## ✅ Checklist trước khi deploy

- [ ] Cấu hình `siteMetadata.js`
- [ ] Thay đổi author info
- [ ] Thêm blog posts
- [ ] Kiểm tra navigation links
- [ ] Test responsive design
- [ ] Run `yarn build` thành công
- [ ] Test production build locally

---

🎉 **Chúc mừng! Blog của bạn đã sẵn sàng!**

Nếu có vấn đề, hãy kiểm tra terminal output và browser console để tìm chi tiết lỗi.
