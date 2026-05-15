# Inventory Management System API

Django REST API and simple web dashboard for managing inventory items and stock in/out transactions. The project runs with Docker Compose and uses SQLite by default.

## Features

- Health check endpoint for API and database status
- CRUD API for inventory items
- Append-only stock transactions for import/export
- Validation to prevent zero/negative quantities and exporting more than current stock
- Sample inventory data generated on first startup
- Runtime logs in `logs/`
- Dockerized development setup

## Tech Stack

- Python 3.11
- Django 5.1.1
- Django REST Framework 3.17.1
- SQLite
- Docker and Docker Compose

## Quick Start

```bash
docker compose up --build
```

Open:

- Web app: http://localhost:8000
- API root: http://localhost:8000/api/
- Health check: http://localhost:8000/api/health

The container runs migrations and then executes `python manage.py populate_inventory`. Sample data is created only when the database has no items.

## API Endpoints

### Health Check

```bash
curl http://localhost:8000/api/health
```

Example response:

```json
{
  "status": "ok",
  "message": "Inventory System is running",
  "database": "connected",
  "items_in_inventory": 50,
  "timestamp": "2026-05-12T12:50:00.000000+00:00"
}
```

### Items

List items:

```bash
curl http://localhost:8000/api/items/
```

Create item:

```bash
curl -X POST http://localhost:8000/api/items/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "iPhone 15 Pro",
    "sku": "SKU-IPHONE-15",
    "description": "Latest iPhone model",
    "price": "999.99",
    "stock_quantity": 50
  }'
```

Update item:

```bash
curl -X PATCH http://localhost:8000/api/items/1/ \
  -H "Content-Type: application/json" \
  -d '{"stock_quantity": 40}'
```

Delete item:

```bash
curl -X DELETE http://localhost:8000/api/items/1/
```

### Stock Transactions

List transactions:

```bash
curl http://localhost:8000/api/stock-logs/
```

Import stock:

```bash
curl -X POST http://localhost:8000/api/stock-logs/ \
  -H "Content-Type: application/json" \
  -d '{
    "item": 1,
    "transaction_type": "IN",
    "quantity": 50,
    "note": "Purchase from supplier"
  }'
```

Export stock:

```bash
curl -X POST http://localhost:8000/api/stock-logs/ \
  -H "Content-Type: application/json" \
  -d '{
    "item": 1,
    "transaction_type": "OUT",
    "quantity": 10,
    "note": "Sale to customer"
  }'
```

Stock logs are append-only. Updating or deleting a stock transaction is disabled because each transaction changes the current stock level.

## Docker Commands

```bash
docker compose up --build
docker compose up -d
docker compose logs -f web
docker compose exec web python manage.py check
docker compose down
```

## Environment Variables

Docker Compose sets these development defaults:

```env
SECRET_KEY=django-insecure-development-key-change-in-production
DEBUG=True
API_BASE_URL=/api
```

Optional database variables:

```env
DB_ENGINE=django.db.backends.sqlite3
DB_NAME=db.sqlite3
DB_USER=
DB_PASSWORD=
DB_HOST=
DB_PORT=
```

## Project Structure

```text
inventory_project/
├── app/
│   ├── fixtures/sample_data.json
│   ├── management/commands/populate_inventory.py
│   ├── migrations/0001_initial.py
│   ├── templates/inventory/index.html
│   ├── models.py
│   ├── serializers.py
│   ├── urls.py
│   └── views.py
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```

## Troubleshooting

If port 8000 is busy, change the left side of the port mapping in `docker-compose.yml`, for example:

```yaml
ports:
  - "8080:8000"
```

If you want to reset local data:

```bash
docker compose down
```

Then delete `db.sqlite3` and start again with `docker compose up --build`.
# React + TypeScript + Vite

## Lệnh chạy nhanh

### Backend (Django)

```powershell
..\.venv\Scripts\Activate.ps1
python.exe manage.py runserver 8000
```

### Frontend (Vite)

```powershell
cd frontend
npm install
npm run dev
```

## Cấu hình môi trường

Tạo file `.env` trong thư mục `frontend` và khai báo URL backend:

```bash
VITE_API_BASE_URL=http://localhost:8000
```

Mẫu này cung cấp cấu hình tối thiểu để React chạy được với Vite (HMR) và một số quy tắc ESLint.

Hiện tại có 2 plugin chính thức:

- [@vitejs/plugin-react](https://github.com/vitejs/vite-plugin-react/blob/main/packages/plugin-react) sử dụng [Oxc](https://oxc.rs)
- [@vitejs/plugin-react-swc](https://github.com/vitejs/vite-plugin-react/blob/main/packages/plugin-react-swc) sử dụng [SWC](https://swc.rs/)

## React Compiler

React Compiler không được bật sẵn vì ảnh hưởng tới hiệu năng khi dev và build. Nếu cần, xem [hướng dẫn này](https://react.dev/learn/react-compiler/installation).

## Mở rộng cấu hình ESLint

Nếu bạn phát triển ứng dụng production, nên cập nhật cấu hình để bật quy tắc lint có nhận biết kiểu:

```js
export default defineConfig([
  globalIgnores(['dist']),
  {
    files: ['**/*.{ts,tsx}'],
    extends: [
      // Các cấu hình khác...

      // Bỏ tseslint.configs.recommended và thay bằng cấu hình này
      tseslint.configs.recommendedTypeChecked,
      // Hoặc dùng cái này nếu muốn stricter
      tseslint.configs.strictTypeChecked,
      // Tùy chọn: thêm quy tắc style
      tseslint.configs.stylisticTypeChecked,

      // Các cấu hình khác...
    ],
    languageOptions: {
      parserOptions: {
        project: ['./tsconfig.node.json', './tsconfig.app.json'],
        tsconfigRootDir: import.meta.dirname,
      },
      // tùy chọn khác...
    },
  },
])
```

Bạn có thể cài [eslint-plugin-react-x](https://github.com/Rel1cx/eslint-react/tree/main/packages/plugins/eslint-plugin-react-x) và [eslint-plugin-react-dom](https://github.com/Rel1cx/eslint-react/tree/main/packages/plugins/eslint-plugin-react-dom) cho quy tắc lint riêng của React:

```js
// eslint.config.js
import reactX from 'eslint-plugin-react-x'
import reactDom from 'eslint-plugin-react-dom'

export default defineConfig([
  globalIgnores(['dist']),
  {
    files: ['**/*.{ts,tsx}'],
    extends: [
      // Các cấu hình khác...
      // Bật quy tắc lint cho React
      reactX.configs['recommended-typescript'],
      // Bật quy tắc lint cho React DOM
      reactDom.configs.recommended,
    ],
    languageOptions: {
      parserOptions: {
        project: ['./tsconfig.node.json', './tsconfig.app.json'],
        tsconfigRootDir: import.meta.dirname,
      },
      // tùy chọn khác...
    },
  },
])
```
