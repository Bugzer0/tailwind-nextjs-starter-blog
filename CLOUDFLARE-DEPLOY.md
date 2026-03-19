# 🚀 Hướng Dẫn Triển Khai Lên Cloudflare Pages

## 📋 Điều kiện tiên quyết

- ✅ Tài khoản GitHub (miễn phí)
- ✅ Tài khoản Cloudflare (miễn phí)
- ✅ Dự án đã được push lên GitHub repository

---

## 🔧 Bước 1: Chuẩn bị Repository GitHub

### 1.1. Khởi tạo Git (nếu chưa có)

```bash
# Khởi tạo git repository
git init

# Thêm tất cả files
git add .

# Commit đầu tiên
git commit -m "Initial commit"
```

### 1.2. Tạo repository trên GitHub

1. Truy cập [https://github.com/new](https://github.com/new)
2. Điền thông tin:
   - **Repository name**: `my-blog` (hoặc tên bạn muốn)
   - **Visibility**: Public hoặc Private (cả hai đều được)
3. **KHÔNG** chọn "Initialize with README"
4. Click **"Create repository"**

### 1.3. Push code lên GitHub

```bash
# Thêm remote repository
git remote add origin https://github.com/USERNAME/REPO_NAME.git

# Push code
git branch -M main
git push -u origin main
```

**Thay thế:**

- `USERNAME`: Tên GitHub của bạn
- `REPO_NAME`: Tên repository vừa tạo

---

## ☁️ Bước 2: Tạo Tài Khoản Cloudflare

### 2.1. Đăng ký Cloudflare (nếu chưa có)

1. Truy cập [https://dash.cloudflare.com/sign-up](https://dash.cloudflare.com/sign-up)
2. Điền email và mật khẩu
3. Xác nhận email
4. **Miễn phí 100%** - không cần thẻ tín dụng

### 2.2. Truy cập Cloudflare Pages

1. Đăng nhập vào [https://dash.cloudflare.com](https://dash.cloudflare.com)
2. Chọn **"Workers & Pages"** từ sidebar bên trái
3. Click tab **"Pages"**
4. Click nút **"Create application"**
5. Chọn **"Connect to Git"**

---

## 🔗 Bước 3: Kết Nối GitHub với Cloudflare

### 3.1. Authorize Cloudflare

1. Click **"Connect GitHub"**
2. Đăng nhập GitHub (nếu chưa đăng nhập)
3. Click **"Authorize Cloudflare Pages"**
4. Chọn repository access:
   - **All repositories**: Cho phép tất cả repos
   - **Only select repositories**: Chọn repo cụ thể (khuyến nghị)

### 3.2. Chọn Repository

1. Tìm và chọn repository blog của bạn
2. Click **"Begin setup"**

---

## ⚙️ Bước 4: Cấu Hình Build Settings

### 4.1. Project Settings

**Project name:**

```
my-blog
```

_Tên này sẽ là subdomain: `my-blog.pages.dev`_

**Production branch:**

```
main
```

### 4.2. Build Configuration

**Framework preset:**

```
Next.js (Static HTML Export)
```

**Build command:**

```bash
yarn build
```

**Build output directory:**

```
out
```

**Root directory (optional):**

```
/
```

_Để trống nếu project ở root_

### 4.3. Environment Variables

Click **"Add variable"** và thêm:

| Variable name  | Value |
| -------------- | ----- |
| `EXPORT`       | `1`   |
| `UNOPTIMIZED`  | `1`   |
| `NODE_VERSION` | `20`  |

**Giải thích:**

- `EXPORT=1`: Bật static export mode
- `UNOPTIMIZED=1`: Tắt image optimization (Cloudflare có CDN riêng)
- `NODE_VERSION=20`: Sử dụng Node.js 20

### 4.4. Hoàn tất setup

1. Kiểm tra lại tất cả settings
2. Click **"Save and Deploy"**

---

## 🎯 Bước 5: Theo Dõi Quá Trình Build

### 5.1. Build Process

Cloudflare sẽ tự động:

1. ✅ Clone repository từ GitHub
2. ✅ Install dependencies (`yarn install`)
3. ✅ Run build command (`yarn build`)
4. ✅ Deploy static files từ folder `out`

**Thời gian build:** ~2-3 phút

### 5.2. Xem Build Logs

1. Click vào deployment đang chạy
2. Xem **"Build log"** để theo dõi tiến trình
3. Nếu có lỗi, logs sẽ hiển thị chi tiết

### 5.3. Build thành công

Khi build xong, bạn sẽ thấy:

- ✅ **Status**: "Success"
- 🌐 **URL**: `https://my-blog.pages.dev`
- 📊 **Build time**: ~2 phút
- 📦 **Assets deployed**: số lượng files

---

## 🌐 Bước 6: Truy Cập Website

### 6.1. URL mặc định

```
https://YOUR-PROJECT-NAME.pages.dev
```

**Ví dụ:**

```
https://my-blog.pages.dev
```

### 6.2. Kiểm tra website

1. Click vào URL hoặc copy vào browser
2. Kiểm tra:
   - ✅ Trang chủ hiển thị đúng
   - ✅ Blog posts load được
   - ✅ Navigation hoạt động
   - ✅ Images hiển thị
   - ✅ Responsive design

---

## 🔄 Bước 7: Tự Động Deploy Khi Push Code

### 7.1. Workflow tự động

Từ giờ, mỗi khi bạn push code:

```bash
# Sửa code
git add .
git commit -m "Update blog post"
git push origin main
```

Cloudflare sẽ **tự động**:

1. 🔍 Phát hiện commit mới
2. 🔨 Build lại project
3. 🚀 Deploy version mới
4. 📧 Gửi email thông báo (nếu bật)

**Thời gian:** ~2-3 phút từ push đến live

### 7.2. Preview Deployments

Nếu push lên branch khác (không phải `main`):

- Cloudflare tạo **preview URL** riêng
- Test được trước khi merge vào main
- URL dạng: `https://abc123.my-blog.pages.dev`

---

## 🎨 Bước 8: Cấu Hình Custom Domain (Tùy chọn)

### 8.1. Thêm Custom Domain

1. Vào **Pages project** → **Custom domains**
2. Click **"Set up a custom domain"**
3. Nhập domain của bạn: `blog.example.com`
4. Click **"Continue"**

### 8.2. Cấu hình DNS

**Nếu domain đã dùng Cloudflare:**

- ✅ Tự động thêm DNS record
- ✅ SSL certificate tự động

**Nếu domain ở nhà cung cấp khác:**

Thêm CNAME record:

```
Type: CNAME
Name: blog (hoặc @ cho root domain)
Value: YOUR-PROJECT-NAME.pages.dev
```

### 8.3. Chờ DNS propagate

- ⏱️ Thời gian: 5-30 phút
- 🔒 SSL certificate: Tự động sau 24h

---

## 📊 Bước 9: Quản Lý Deployments

### 9.1. Xem lịch sử deployments

1. Vào **Pages project**
2. Tab **"Deployments"**
3. Xem tất cả builds (thành công/thất bại)

### 9.2. Rollback version cũ

1. Click vào deployment cũ
2. Click **"Rollback to this deployment"**
3. Confirm → Website quay về version cũ

### 9.3. Xóa deployment

1. Click vào deployment
2. Click **"..."** → **"Delete deployment"**

---

## 🔧 Troubleshooting

### ❌ Build Failed

**Lỗi thường gặp:**

**1. Dependencies install failed**

```bash
# Kiểm tra package.json
# Đảm bảo yarn.lock có trong repo
git add yarn.lock
git commit -m "Add yarn.lock"
git push
```

**2. Build command failed**

```bash
# Test build locally trước
yarn build

# Nếu lỗi, sửa và push lại
```

**3. Out of memory**

```bash
# Thêm environment variable
NODE_OPTIONS=--max-old-space-size=4096
```

### ❌ Website không hiển thị đúng

**1. 404 errors**

- Kiểm tra `output` directory = `out`
- Kiểm tra `EXPORT=1` trong env variables

**2. Images không load**

- Kiểm tra images trong `public/` folder
- Đảm bảo `UNOPTIMIZED=1` được set

**3. CSS không apply**

- Clear browser cache (Ctrl+Shift+R)
- Kiểm tra build logs

### ❌ Auto-deploy không hoạt động

1. Vào **Settings** → **Builds & deployments**
2. Kiểm tra **"Automatic deployments"** = Enabled
3. Kiểm tra branch name đúng (`main`)

---

## 📈 Monitoring & Analytics

### 1. Web Analytics (Miễn phí)

1. Vào **Pages project** → **Analytics**
2. Click **"Enable Web Analytics"**
3. Xem:
   - 📊 Page views
   - 👥 Unique visitors
   - 🌍 Geographic data
   - 📱 Device types

### 2. Performance Metrics

- ⚡ **Core Web Vitals**
- 🚀 **Load times**
- 📊 **Bandwidth usage**

---

## 🎯 Best Practices

### 1. Branch Strategy

```bash
main          # Production (auto-deploy)
├── develop   # Staging (preview deploy)
└── feature/* # Features (preview deploy)
```

### 2. Environment Variables

- ❌ **KHÔNG** commit `.env` files
- ✅ Set trong Cloudflare Pages dashboard
- ✅ Dùng `NEXT_PUBLIC_*` cho client-side vars

### 3. Build Optimization

```bash
# Kiểm tra bundle size trước khi deploy
yarn analyze

# Optimize images
# Minify code
# Remove unused dependencies
```

---

## 📚 Resources

### Official Docs

- [Cloudflare Pages Docs](https://developers.cloudflare.com/pages/)
- [Next.js Static Export](https://nextjs.org/docs/app/building-your-application/deploying/static-exports)

### Support

- [Cloudflare Community](https://community.cloudflare.com/)
- [Discord](https://discord.cloudflare.com/)

---

## ✅ Checklist Triển Khai

- [ ] Repository đã push lên GitHub
- [ ] Tài khoản Cloudflare đã tạo
- [ ] GitHub đã authorize Cloudflare
- [ ] Build settings đã cấu hình đúng
- [ ] Environment variables đã thêm
- [ ] Build thành công
- [ ] Website truy cập được
- [ ] Auto-deploy hoạt động
- [ ] Custom domain đã setup (nếu có)
- [ ] Analytics đã enable

---

## 🎉 Hoàn Thành!

Website của bạn đã live tại:

```
https://YOUR-PROJECT-NAME.pages.dev
```

**Từ giờ:**

- ✅ Mỗi lần push code → Tự động deploy
- ✅ Global CDN → Tốc độ nhanh toàn cầu
- ✅ SSL miễn phí → Bảo mật
- ✅ Unlimited requests → Không giới hạn

**Next steps:**

1. Viết blog posts mới trong `data/blog/`
2. Customize theme và colors
3. Thêm custom domain
4. Enable analytics
5. Share với bạn bè! 🚀
