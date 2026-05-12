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
