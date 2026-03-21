# Cloudflare Functions

Thư mục này chứa Cloudflare Functions (serverless functions) cho các tính năng backend.

## 📁 Cấu trúc

```
functions/
├── api/
│   └── newsletter.ts      # Newsletter subscription endpoint
├── tsconfig.json          # TypeScript config
└── README.md             # File này
```

## 🚀 Endpoints

### POST /api/newsletter

**Mô tả:** Đăng ký newsletter với BeeHiiv

**Request:**
```json
{
  "email": "user@example.com"
}
```

**Response thành công (201):**
```json
{
  "message": "Successfully subscribed to the newsletter"
}
```

**Response lỗi (400/500):**
```json
{
  "error": "Error message"
}
```

## 🔧 Development

### Local Testing

```bash
# Install Wrangler CLI
npm install -g wrangler

# Test function locally
wrangler pages dev out \
  --compatibility-date=2024-01-01 \
  --binding BEEHIIV_API_KEY=your_key \
  --binding BEEHIIV_PUBLICATION_ID=your_id
```

### Environment Variables

Cần thiết lập trong Cloudflare Dashboard:

| Variable | Mô tả | Required |
|----------|-------|----------|
| `BEEHIIV_API_KEY` | API key từ BeeHiiv | ✅ |
| `BEEHIIV_PUBLICATION_ID` | Publication ID từ BeeHiiv | ✅ |
| `ALLOWED_ORIGINS` | Danh sách origins cho CORS (phân cách bằng dấu phẩy) | ❌ |

**Ví dụ ALLOWED_ORIGINS:**
```
https://glucoai.app,https://www.glucoai.app,https://glucoai.pages.dev
```

## 🔒 Bảo mật

- ✅ Email validation với regex RFC 5322
- ✅ Input sanitization
- ✅ CORS với whitelist origins
- ✅ Error messages không expose sensitive data
- ✅ Email masking trong logs
- ✅ Request body validation

## 📝 Lưu ý

1. **CORS:** Default cho phép `glucoai.app` và `*.pages.dev`. Tùy chỉnh qua `ALLOWED_ORIGINS`
2. **Rate Limiting:** Cloudflare tự động áp dụng
3. **Logs:** Truy cập tại Cloudflare Dashboard → Functions → Logs
4. **Errors:** Lỗi internal không expose chi tiết cho client

## 🐛 Debugging

### Xem logs real-time

1. Cloudflare Dashboard → Project
2. Tab **Logs** → **Functions**
3. Filter by function name

### Common Issues

**404 Not Found**
- Kiểm tra file tồn tại trong `functions/api/`
- Kiểm tra deployment logs

**500 Server Error**
- Kiểm tra environment variables
- Xem function logs trong Cloudflare

**CORS Error**
- Thêm origin vào `ALLOWED_ORIGINS`
- Kiểm tra origin header trong request
