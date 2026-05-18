# Week11-12 - API Design Patterns

Muc tieu:
- Ket hop nhieu API design patterns trong cung he thong
- Trien khai webhook de tich hop he thong thong bao
- Phan tich pattern cua Stripe, GitHub

## Patterns da trien khai

1. CRUD Pattern
- Product API: tao, doc, cap nhat, xoa
- Endpoints:
  - POST /api/products
  - GET /api/products/{id}
  - PUT /api/products/{id}
  - DELETE /api/products/{id}

2. Query Pattern
- Tim kiem/loc/sap xep/phan trang:
  - GET /api/products?category=book&search=python&min_price=10&max_price=50&sort=-price&page=1&limit=10

3. HATEOAS Pattern
- Moi response chinh deu tra ve _links
- Giup client discover endpoint tiep theo ma khong hardcode URL

4. Event-driven Pattern
- Tao notification -> publish event notification.created
- Tao order -> publish event order.created
- Event log endpoint: GET /api/events

5. Webhook Pattern
- Dang ky subscription: POST /api/webhooks/subscriptions
- Khi co event, he thong goi HTTP POST den URL da dang ky
- Theo doi ket qua gui webhook: GET /api/webhooks/deliveries

## REST vs gRPC vs GraphQL

Khi dung REST:
- Public API, de debug, de cache, web-friendly
- CRUD + HTTP semantics ro rang

Khi dung gRPC:
- Service-to-service, can latency thap, payload nho, typing chat
- Streaming realtime giua microservices

Khi dung GraphQL:
- Client can query linh hoat, tranh over-fetch/under-fetch
- Frontend co nhu cau layout du lieu thay doi nhanh

## Cau truc thu muc

- src/server.py: entrypoint
- src/app.py: app factory + register routes + event wiring
- src/routes/product_routes.py: CRUD + Query + HATEOAS
- src/routes/notification_routes.py: Notification + Order + Event log
- src/routes/webhook_routes.py: Webhook subscriptions + delivery log
- src/services/event_bus.py: event pub/sub in-memory
- src/services/webhook_service.py: dispatch webhook + signature
- src/utils/hateoas.py: helper _links
- src/storage.py: in-memory storage

## Chay local

```bash
cd week11-12
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python src/server.py
```

Server: http://127.0.0.1:5013

## Thu nghiem nhanh

### 1) Dang ky webhook (dung webhook.site URL)

```bash
curl -X POST http://127.0.0.1:5013/api/webhooks/subscriptions \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://webhook.site/YOUR_ID",
    "events": ["notification.created", "order.created"],
    "secret": "demo-secret"
  }'
```

### 2) Tao notification -> trigger webhook

```bash
curl -X POST http://127.0.0.1:5013/api/notifications \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Order paid",
    "recipient": "user_01",
    "channel": "email"
  }'
```

### 3) Kiem tra lich su deliver webhook

```bash
curl http://127.0.0.1:5013/api/webhooks/deliveries
```

## Endpoints tong hop

- GET /
- POST /api/products
- GET /api/products
- GET /api/products/{id}
- PUT /api/products/{id}
- DELETE /api/products/{id}
- POST /api/notifications
- GET /api/notifications
- GET /api/notifications/{id}
- POST /api/orders
- GET /api/events
- POST /api/webhooks/subscriptions
- GET /api/webhooks/subscriptions
- DELETE /api/webhooks/subscriptions/{id}
- GET /api/webhooks/deliveries
