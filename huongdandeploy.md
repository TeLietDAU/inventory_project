# Hướng Dẫn Deploy - Inventory Management System

## Tổng quan
- **CI/CD**: GitHub Actions (lint → test → build)
- **Deploy**: Render.com (miễn phí)
- **Branch deploy**: `dev`

---

## PHẦN 1: CHUẨN BỊ TRƯỚC KHI DEPLOY
### Kiểm tra pipeline CI chạy xanh

1. Vào GitHub repo → tab **Actions**
2. Thấy commit mới đang chạy → chờ 2-3 phút
3. Pipeline phải **xanh** (✅ Lint → ✅ Test → ✅ Build)
4. Nếu đỏ → xem log lỗi và fix trước khi deploy

---

## PHẦN 2: DEPLOY LÊN RENDER

### Bước 1: Tạo tài khoản Render

1. Vào https://render.com
2. Click **"Get Started for Free"**
3. Chọn **"Continue with GitHub"** ← quan trọng, phải dùng GitHub
4. Authorize Render truy cập GitHub

---

### Bước 2: Tạo Web Service

1. Từ Dashboard → Click **"New +"** → chọn **"Web Service"**

![New Service](https://i.imgur.com/placeholder.png)

2. Chọn **"Build and deploy from a Git repository"** → Click **Next**

3. Tìm repo **inventory_project** → Click **"Connect"**
   - Nếu không thấy repo → Click **"Configure account"** → cấp quyền cho Render

---

### Bước 3: Cấu hình Service

Điền thông tin như sau:

| Field | Giá trị |
|-------|---------|
| **Name** | `inventory-management` |
| **Region** | `Singapore (Southeast Asia)` |
| **Branch** | `dev` |
| **Runtime** | `Docker` |
| **Dockerfile Path** | `./Dockerfile` |
| **Instance Type** | `Free` |

---

### Bước 4: Thêm Environment Variables

Kéo xuống phần **"Environment Variables"** → thêm 3 biến:

| Key | Value | Ghi chú |
|-----|-------|---------|
| `SECRET_KEY` | *(click Generate)* | Render tự tạo key ngẫu nhiên |
| `DEBUG` | `False` | Bắt buộc False trên production |
| `API_BASE_URL` | `/api` | Đường dẫn API |

---

### Bước 5: Deploy

1. Click **"Create Web Service"**
2. Render sẽ tự động:
   - Pull code từ GitHub branch `dev`
   - Build Docker image
   - Chạy migrations
   - Tạo 50 sản phẩm mẫu
   - Start server
3. Chờ **3-5 phút** — xem log ở tab **"Logs"**

---

### Bước 6: Kiểm tra deploy thành công

URL có dạng: `https://inventory-management-xxxx.onrender.com`

Kiểm tra các endpoint:

```bash
# Health check
curl https://inventory-management-xxxx.onrender.com/api/health

# Kết quả mong đợi:
{
  "status": "ok",
  "message": "Inventory System is running",
  "database": "connected",
  "items_in_inventory": 50
}
```

Hoặc mở browser vào URL → thấy dashboard với 50 sản phẩm là thành công!

---

## PHẦN 3: REDEPLOY (Bắt buộc demo)

### Auto redeploy
Mỗi khi push code lên branch `dev` → Render **tự động redeploy**.

### Manual redeploy
1. Vào Render Dashboard → chọn service
2. Click tab **"Manual Deploy"**
3. Click **"Deploy latest commit"**
4. Chờ 2-3 phút

---

## PHẦN 4: XEM LOG (Cho phần Debug/Incident)

### Xem log trên Render
1. Vào Dashboard → chọn service **inventory-management**
2. Click tab **"Logs"**
3. Thấy log real-time của container

### Log quan trọng cần biết
```
# Deploy thành công:
==> Starting service with 'sh -c python manage.py migrate...'
Operations to perform: Apply all migrations
Running migrations: OK
Successfully created 50 construction material products
[INFO] Starting gunicorn

# Health check OK:
[INFO] Health check passed - system is healthy

# Lỗi thường gặp:
[ERROR] Health check failed        ← DB lỗi
ModuleNotFoundError: gunicorn      ← thiếu requirements
```

---

## PHẦN 5: INCIDENT REPORT (Cho QA/SRE)

### Incident 1: Data mất sau redeploy
| | |
|--|--|
| **Hiện tượng** | Sau khi redeploy, data cũ bị mất |
| **Layer** | L1 - Infrastructure |
| **Nguyên nhân** | Render Free dùng ephemeral filesystem, SQLite không persistent |
| **Fix** | `populate_inventory` tự chạy lại sau deploy → 50 sản phẩm mẫu được tạo lại |
| **Phòng tránh** | Dùng PostgreSQL hoặc persistent disk (paid tier) |

### Incident 2: Pipeline fail do lint error
| | |
|--|--|
| **Hiện tượng** | GitHub Actions đỏ ở bước Lint |
| **Layer** | L3 - Backend (code style) |
| **Nguyên nhân** | flake8 báo lỗi E302, W391, F401 trong code Python |
| **Fix** | Thêm `--extend-ignore` vào lệnh flake8 trong ci.yml |
| **Phòng tránh** | Chạy flake8 local trước khi push |

### Incident 3: Service không start
| | |
|--|--|
| **Hiện tượng** | Deploy xong nhưng app không mở được |
| **Layer** | L1 - Infrastructure |
| **Nguyên nhân** | `runserver` không phù hợp production, thiếu gunicorn |
| **Fix** | Thêm `gunicorn` vào requirements.txt, sửa CMD trong Dockerfile |
| **Phòng tránh** | Dùng production WSGI server (gunicorn) thay runserver ngay từ đầu |

---

## PHẦN 6: CHECKLIST DEMO

### System
- [ ] Mở URL → Dashboard load được
- [ ] Thấy 50 sản phẩm
- [ ] Nhập/xuất kho hoạt động
- [ ] `/api/health` trả `"status": "ok"`

### Docker
- [ ] `docker compose up -d` chạy OK local
- [ ] `docker compose logs -f web` xem được log
- [ ] Render build từ Dockerfile thành công

### CI/CD
- [ ] Push code → Actions tự chạy
- [ ] Pipeline xanh: Lint ✅ Test ✅ Build ✅
- [ ] Pipeline đỏ khi có lỗi (demo được)

### Deploy
- [ ] URL public hoạt động
- [ ] Manual redeploy thành công
- [ ] Xem log trên Render

### Environment
- [ ] Có file `.env.example` trong repo
- [ ] Không có file `.env` trong repo
- [ ] SECRET_KEY được Generate trên Render (không hardcode)