# 🔧 Fix Newsletter Signup trên Cloudflare Pages

## ❌ Vấn đề

Newsletter signup form không hoạt động trên production (Cloudflare Pages) nhưng chạy bình thường trên localhost.

**Nguyên nhân:** Next.js static export (`EXPORT=1`) **KHÔNG hỗ trợ API routes**

- **Localhost:** `next dev` chạy Node.js server → API routes (`/api/newsletter`) hoạt động ✅
- **Production:** Static export chỉ tạo HTML/CSS/JS tĩnh → API routes bị loại bỏ ❌

## ✅ Giải pháp

Sử dụng **Cloudflare Functions** để thay thế Next.js API routes.

Cloudflare Functions là serverless functions chạy trên Cloudflare's edge network, tương tự như Vercel Edge Functions hoặc AWS Lambda.

## 📁 Cấu trúc đã tạo

```
functions/
├── api/
│   └── newsletter.ts      # Cloudflare Function xử lý newsletter
└── tsconfig.json          # TypeScript config cho Functions
```

## 🚀 Hướng dẫn Deploy

### Bước 1: Push code lên GitHub

```bash
git add functions/
git commit -m "Add Cloudflare Function for newsletter"
git push origin main
```

### Bước 2: Thêm Environment Variables trên Cloudflare

1. Đăng nhập [Cloudflare Dashboard](https://dash.cloudflare.com)
2. Vào **Workers & Pages** → Chọn project của bạn
3. Vào tab **Settings** → **Environment variables**
4. Thêm các biến sau cho **Production**:

| Variable name             | Value                                      |
| ------------------------- | ------------------------------------------ |
| `BEEHIIV_API_KEY`         | `hCALn3tqhESLnN1WwIav2FaclNrovYrcYKDpxqN5u5D6zGS4ssTpzvztKSx6Wa8w` |
| `BEEHIIV_PUBLICATION_ID`  | `pub_705cffb7-dc72-47e6-909a-5c196dbba1ca` |

**Lưu ý:** 
- ✅ Đảm bảo thêm vào **Production** environment
- ✅ Preview environments cũng nên thêm nếu muốn test

5. Click **"Save"**

### Bước 3: Redeploy

Cloudflare sẽ tự động redeploy khi bạn push code mới. Nếu không tự động:

1. Vào tab **Deployments**
2. Click **"Retry deployment"** trên deployment mới nhất

### Bước 4: Kiểm tra

1. Truy cập website production: `https://your-site.pages.dev`
2. Thử đăng ký newsletter với email test
3. Kiểm tra console logs:
   - Cloudflare Dashboard → Project → **Logs** → **Functions**

## 🔍 Cách hoạt động

### Trước (không hoạt động)

```
Browser → /api/newsletter (Next.js API Route)
                ↓
           ❌ 404 Not Found (không tồn tại trong static export)
```

### Sau (hoạt động)

```
Browser → /api/newsletter (Cloudflare Function)
                ↓
     ✅ Cloudflare Function xử lý request
                ↓
          Beehiiv API → Subscribe email
```

## 📝 Chi tiết kỹ thuật

### URL Mapping

Cloudflare Pages tự động map files trong `functions/` thành endpoints:

```
functions/api/newsletter.ts → https://your-site.pages.dev/api/newsletter
```

### Function Structure

```typescript
// functions/api/newsletter.ts
export async function onRequestPost(context) {
  const { request, env } = context
  // env.BEEHIIV_API_KEY - Lấy từ environment variables
  // env.BEEHIIV_PUBLICATION_ID
  // Xử lý request và gọi Beehiiv API
}
```

### Environment Variables

- **Development (localhost):** Dùng `.env.local`
- **Production (Cloudflare):** Dùng Cloudflare Environment Variables

## 🧪 Test Locally (Optional)

Để test Cloudflare Functions local:

```bash
# Install Wrangler CLI
npm install -g wrangler

# Run local dev server với Functions
wrangler pages dev out --compatibility-date=2024-01-01 \
  --binding BEEHIIV_API_KEY=your_key \
  --binding BEEHIIV_PUBLICATION_ID=your_id
```

## ⚠️ Lưu ý

1. **API Keys bảo mật:**
   - ❌ KHÔNG commit `.env.local` vào Git
   - ✅ Chỉ lưu API keys trong Cloudflare Dashboard

2. **CORS:**
   - Cloudflare Function đã config CORS headers
   - Cho phép requests từ mọi origin (`*`)
   - Production có thể giới hạn origin cụ thể

3. **Rate Limiting:**
   - Cloudflare tự động có rate limiting
   - Beehiiv cũng có rate limits riêng

## 🐛 Troubleshooting

### Lỗi: 404 Not Found

**Nguyên nhân:** Functions chưa được deploy hoặc URL sai

**Giải pháp:**
- Kiểm tra folder `functions/` đã được push lên GitHub
- Kiểm tra logs: Cloudflare Dashboard → Logs → Functions

### Lỗi: 500 Server configuration error

**Nguyên nhân:** Environment variables chưa được set

**Giải pháp:**
- Kiểm tra lại Environment variables trong Cloudflare Dashboard
- Đảm bảo đã thêm vào **Production** environment
- Redeploy sau khi thêm env vars

### Lỗi: Failed to subscribe

**Nguyên nhân:** Beehiiv API key hoặc publication ID không đúng

**Giải pháp:**
- Kiểm tra API key tại [Beehiiv API Settings](https://app.beehiiv.com/settings/integrations)
- Kiểm tra Publication ID tại URL: `https://app.beehiiv.com/publications/{PUBLICATION_ID}`

### Email không nhận được

**Nguyên nhân:** Email đã tồn tại hoặc bị spam filter

**Giải pháp:**
- Kiểm tra inbox và spam folder
- Kiểm tra Beehiiv dashboard → Subscribers
- Thử email khác

## 📊 Monitoring

### Xem Logs

1. Cloudflare Dashboard → Project
2. Tab **Logs** → **Functions**
3. Xem real-time logs của newsletter function

### Analytics

1. Cloudflare Dashboard → Project
2. Tab **Analytics**
3. Xem:
   - Request count
   - Success/error rates
   - Response times

## ✅ Checklist

- [ ] Đã tạo `functions/api/newsletter.ts`
- [ ] Đã push code lên GitHub
- [ ] Đã thêm `BEEHIIV_API_KEY` vào Cloudflare env vars
- [ ] Đã thêm `BEEHIIV_PUBLICATION_ID` vào Cloudflare env vars
- [ ] Deployment thành công
- [ ] Test newsletter signup trên production
- [ ] Kiểm tra email nhận được

## 🎉 Hoàn thành!

Newsletter signup giờ hoạt động trên production với Cloudflare Functions!

**Lợi ích:**
- ✅ Chạy trên edge network (nhanh toàn cầu)
- ✅ Serverless (không cần quản lý server)
- ✅ Free tier của Cloudflare rất generous
- ✅ Auto-scaling (tự động scale theo traffic)
