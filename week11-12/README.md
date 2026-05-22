# Week11-12 - API Design Patterns

Buoi 11-12 tap trung vao cach thiet ke API bang nhieu pattern ket hop trong cung mot he thong. Project nay dung Flask de mo phong mot backend ban hang/thong bao nho, trong do:

- Product API minh hoa CRUD, Query va HATEOAS.
- Notification va Order API minh hoa Event-driven.
- Webhook API minh hoa tich hop voi he thong ben ngoai.
- OpenAPI/Swagger giup quan sat va test API truc quan.

## Muc tieu bai hoc

Kien thuc can dat:

- Hieu cac mau thiet ke API: CRUD, Query, HATEOAS, Event-driven, Webhook.
- Biet luc nao nen dung REST, gRPC hoac GraphQL.
- Nhin duoc cac pattern nay trong API thuc te nhu Stripe va GitHub.

Ky nang can lam duoc:

- Thiet ke API dung nhieu pattern ket hop.
- Trien khai webhook de tich hop he thong.
- Tao event khi co hanh dong nghiep vu va gui event ra ngoai qua webhook.
- Viet tai lieu API bang OpenAPI/Swagger.

Thuc hanh trong project:

- Tao product bang CRUD API.
- Loc, tim kiem, sap xep va phan trang product bang Query pattern.
- Tra ve `_links` trong response theo HATEOAS.
- Tao notification/order va ghi event vao event log.
- Dang ky webhook subscription va gui event den URL ben ngoai.
- Doc file `API_PATTERN_ANALYSIS.md` de phan tich Stripe va GitHub.

## Cach chay project

```bash
cd week11-12
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python src/server.py
```

Server mac dinh:

```text
http://127.0.0.1:5013
```

Swagger UI:

```text
http://127.0.0.1:5013/docs
```

OpenAPI JSON:

```text
http://127.0.0.1:5013/openapi.json
```

Luu y khi dung Swagger:

- Phai mo bang dia chi `http://127.0.0.1:5013/docs`, khong mo file HTML truc tiep bang `file://`.
- Neu Swagger bao `Failed to fetch`, kiem tra server Flask con dang chay va `/openapi.json` co tra ve JSON hay khong.
- Swagger UI trong project dung CDN, nen trinh duyet can truy cap duoc `https://unpkg.com`.

## Cau truc thu muc

```text
week11-12/
├── README.md
├── API_PATTERN_ANALYSIS.md
├── requirements.txt
├── docker-compose.yaml
├── .env.example
└── src/
    ├── server.py
    ├── app.py
    ├── openapi.py
    ├── storage.py
    ├── routes/
    │   ├── product_routes.py
    │   ├── notification_routes.py
    │   └── webhook_routes.py
    ├── services/
    │   ├── event_bus.py
    │   └── webhook_service.py
    └── utils/
        └── hateoas.py
```

Vai tro cac file chinh:

- `src/server.py`: entrypoint, load `.env`, chay Flask server.
- `src/app.py`: tao Flask app, dang ky route, noi event bus voi webhook service, them Swagger route.
- `src/openapi.py`: dac ta OpenAPI 3.0 cho Swagger.
- `src/storage.py`: bo nho tam in-memory cho product, notification, order, webhook va event.
- `src/routes/product_routes.py`: CRUD, Query, HATEOAS cho product.
- `src/routes/notification_routes.py`: notification, order va event log.
- `src/routes/webhook_routes.py`: dang ky webhook va xem delivery log.
- `src/services/event_bus.py`: pub/sub event in-memory.
- `src/services/webhook_service.py`: tao subscription, ky HMAC, gui HTTP POST webhook.
- `src/utils/hateoas.py`: helper tao `_links`.

## Tong quan luong he thong

```text
Client
  |
  | REST request
  v
Flask Routes
  |
  | luu du lieu vao storage in-memory
  v
Business action: create notification / create order
  |
  | publish event
  v
Event Bus
  |
  | dispatch event
  v
Webhook Service
  |
  | HTTP POST + X-Webhook-Signature
  v
External system, vi du webhook.site
```

Vi du:

1. Client goi `POST /api/notifications`.
2. Server tao notification va luu vao `NOTIFICATIONS`.
3. Server publish event `notification.created`.
4. Event bus ghi event vao `EVENT_LOG`.
5. Webhook service tim cac subscription dang lang nghe `notification.created`.
6. Server gui HTTP POST den URL da dang ky.
7. Ket qua gui webhook duoc luu vao `WEBHOOK_DELIVERY_LOG`.

## Cac API endpoint

| Method | Endpoint | Pattern | Muc dich |
| --- | --- | --- | --- |
| GET | `/` | HATEOAS | Xem thong tin service va link den cac resource |
| GET | `/docs` | Documentation | Mo Swagger UI |
| GET | `/openapi.json` | Documentation | Lay OpenAPI JSON |
| POST | `/api/products` | CRUD | Tao product |
| GET | `/api/products` | Query | Lay danh sach product, loc, tim kiem, sap xep, phan trang |
| GET | `/api/products/{product_id}` | CRUD + HATEOAS | Lay chi tiet product |
| PUT | `/api/products/{product_id}` | CRUD | Cap nhat product |
| DELETE | `/api/products/{product_id}` | CRUD | Xoa product |
| POST | `/api/notifications` | Event-driven | Tao notification va publish `notification.created` |
| GET | `/api/notifications` | CRUD/List | Lay danh sach notification |
| GET | `/api/notifications/{notification_id}` | CRUD + HATEOAS | Lay chi tiet notification |
| POST | `/api/orders` | Event-driven | Tao order va publish `order.created` |
| GET | `/api/events` | Event-driven | Xem event log |
| POST | `/api/webhooks/subscriptions` | Webhook | Dang ky webhook endpoint |
| GET | `/api/webhooks/subscriptions` | Webhook | Xem danh sach webhook subscription |
| DELETE | `/api/webhooks/subscriptions/{subscription_id}` | Webhook | Xoa webhook subscription |
| GET | `/api/webhooks/deliveries` | Webhook | Xem lich su gui webhook |

## Pattern 1: CRUD

CRUD la pattern co ban nhat khi API lam viec voi resource. Trong project nay, resource chinh la `product`.

Mapping HTTP method:

- `POST /api/products`: Create - tao product moi.
- `GET /api/products/{id}`: Read - doc chi tiet product.
- `PUT /api/products/{id}`: Update - cap nhat product.
- `DELETE /api/products/{id}`: Delete - xoa product.

Tao product:

```bash
curl -X POST http://127.0.0.1:5013/api/products \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Python API Patterns",
    "category": "book",
    "price": 35
  }'
```

Response mau:

```json
{
  "id": "uuid",
  "name": "Python API Patterns",
  "category": "book",
  "price": 35.0,
  "created_at": "2026-05-22T00:00:00+00:00",
  "updated_at": "2026-05-22T00:00:00+00:00",
  "_links": {
    "self": { "href": "/api/products/uuid", "method": "GET" },
    "update": { "href": "/api/products/uuid", "method": "PUT" },
    "delete": { "href": "/api/products/uuid", "method": "DELETE" },
    "collection": { "href": "/api/products", "method": "GET" }
  }
}
```

Cap nhat product:

```bash
curl -X PUT http://127.0.0.1:5013/api/products/PRODUCT_ID \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Advanced Python API Patterns",
    "category": "book",
    "price": 42
  }'
```

Xoa product:

```bash
curl -X DELETE http://127.0.0.1:5013/api/products/PRODUCT_ID
```

## Pattern 2: Query

Query pattern dung khi client can lay danh sach resource theo dieu kien. Thay vi tao nhieu endpoint nhu `/books`, `/cheap-products`, `/search-products`, API dung query parameters tren cung mot endpoint.

Endpoint:

```text
GET /api/products
```

Query parameters duoc ho tro:

| Parameter | Kieu | Y nghia |
| --- | --- | --- |
| `category` | string | Loc theo category |
| `search` | string | Tim kiem theo ten product |
| `min_price` | number | Gia nho nhat |
| `max_price` | number | Gia lon nhat |
| `sort` | string | Sap xep theo `name`, `price`, `created_at`, `updated_at`; them dau `-` de sort giam dan |
| `page` | integer | Trang hien tai |
| `limit` | integer | So item moi trang, toi da 100 |

Vi du:

```bash
curl 'http://127.0.0.1:5013/api/products?category=book&search=python&min_price=10&max_price=50&sort=-price&page=1&limit=10'
```

Response co dang:

```json
{
  "data": [],
  "pagination": {
    "page": 1,
    "limit": 10,
    "total_items": 0,
    "total_pages": 1
  },
  "_links": {
    "self": { "href": "/api/products?page=1&limit=10", "method": "GET" },
    "first": { "href": "/api/products?page=1&limit=10", "method": "GET" },
    "last": { "href": "/api/products?page=1&limit=10", "method": "GET" }
  }
}
```

## Pattern 3: HATEOAS

HATEOAS la viet tat cua Hypermedia As The Engine Of Application State. Y tuong chinh: response khong chi tra ve data, ma con tra ve cac link cho biet client co the lam gi tiep theo.

Trong project nay, cac response chinh co field `_links`.

Vi du khi lay product:

```json
{
  "id": "uuid",
  "name": "Python API Patterns",
  "_links": {
    "self": { "href": "/api/products/uuid", "method": "GET" },
    "update": { "href": "/api/products/uuid", "method": "PUT" },
    "delete": { "href": "/api/products/uuid", "method": "DELETE" },
    "collection": { "href": "/api/products", "method": "GET" }
  }
}
```

Loi ich:

- Client co the discover endpoint tiep theo tu response.
- Giam viec hardcode URL o client.
- API tu mo ta hanh dong hop le tren resource.

## Pattern 4: Event-driven

Event-driven pattern tach hanh dong nghiep vu khoi cac xu ly phu. Khi co mot hanh dong quan trong, server publish event. Cac thanh phan khac co the subscribe va xu ly event do.

Trong project:

- `POST /api/notifications` tao notification va publish `notification.created`.
- `POST /api/orders` tao order va publish `order.created`.
- `GET /api/events` cho xem event log.

Tao notification:

```bash
curl -X POST http://127.0.0.1:5013/api/notifications \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Order paid",
    "recipient": "user_01",
    "channel": "email"
  }'
```

Tao order:

```bash
curl -X POST http://127.0.0.1:5013/api/orders \
  -H "Content-Type: application/json" \
  -d '{
    "customer_id": "user_01",
    "amount": 99.5
  }'
```

Xem event log:

```bash
curl http://127.0.0.1:5013/api/events
```

Response mau:

```json
{
  "count": 1,
  "data": [
    {
      "type": "notification.created",
      "timestamp": "2026-05-22T00:00:00+00:00",
      "data": {
        "id": "uuid",
        "message": "Order paid",
        "recipient": "user_01",
        "channel": "email",
        "status": "queued"
      }
    }
  ]
}
```

Loi ich:

- Route tao notification/order khong can biet cu the webhook duoc gui nhu the nao.
- De mo rong: sau nay co the them email service, audit log, analytics consumer.
- Phu hop voi he thong bat dong bo va microservices.

## Pattern 5: Webhook

Webhook la cach mot he thong chu dong goi HTTP request den he thong khac khi co event. Khac voi polling, client khong can lien tuc goi API de hoi co thay doi hay khong.

Trong project:

- Client dang ky URL nhan webhook bang `POST /api/webhooks/subscriptions`.
- Khi co event `notification.created` hoac `order.created`, server gui HTTP POST den URL da dang ky.
- Moi request webhook co header `X-Event-Type` va `X-Webhook-Signature`.
- Ket qua gui webhook duoc luu tai `GET /api/webhooks/deliveries`.

Dang ky webhook bang webhook.site:

1. Vao `https://webhook.site`.
2. Copy URL duoc cap, vi du `https://webhook.site/abc-123`.
3. Goi API dang ky:

```bash
curl -X POST http://127.0.0.1:5013/api/webhooks/subscriptions \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://webhook.site/YOUR_ID",
    "events": ["notification.created", "order.created"],
    "secret": "demo-secret"
  }'
```

Sau do trigger event:

```bash
curl -X POST http://127.0.0.1:5013/api/notifications \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Welcome",
    "recipient": "user_01",
    "channel": "email"
  }'
```

Kiem tra delivery log:

```bash
curl http://127.0.0.1:5013/api/webhooks/deliveries
```

Response delivery co the thanh cong:

```json
{
  "count": 1,
  "data": [
    {
      "subscription_id": "uuid",
      "target_url": "https://webhook.site/YOUR_ID",
      "event": "notification.created",
      "delivered_at": "2026-05-22T00:00:00+00:00",
      "status": "success",
      "http_status": 200
    }
  ]
}
```

Neu URL khong ton tai hoac service dich khong nghe, delivery co `status: failed` va field `error`.

## Webhook signature

Webhook service tao chu ky nhu sau:

```text
signature = HMAC_SHA256(secret, json_payload_sorted_by_key)
```

Signature duoc gui qua header:

```text
X-Webhook-Signature: <signature>
```

Y nghia:

- He thong nhan webhook co the kiem tra request co dung tu server cua minh gui den khong.
- Neu payload bi sua giua duong, signature se khong khop.
- Day la pattern quan trong trong cac API nhu Stripe va GitHub.

## REST vs gRPC vs GraphQL

### Khi dung REST

Nen dung REST khi:

- API public cho web/mobile/third-party developer.
- Resource ro rang nhu product, order, user, notification.
- Can de debug bang browser, curl, Postman, Swagger.
- Muon tan dung HTTP method, status code, cache.
- He thong can webhook tich hop ben ngoai.

Trong project nay, REST phu hop vi cac resource va thao tac deu ro rang:

```text
GET /api/products
POST /api/products
GET /api/products/{id}
```

### Khi dung gRPC

Nen dung gRPC khi:

- Giao tiep service-to-service trong noi bo backend.
- Can latency thap, payload nho, contract chat bang protobuf.
- Can streaming 2 chieu hoac realtime giua microservices.
- Hai dau client/server do minh kiem soat.

Khong qua phu hop cho demo nay vi API can de test bang Swagger/curl va co webhook public.

### Khi dung GraphQL

Nen dung GraphQL khi:

- Frontend can lay du lieu linh hoat theo man hinh.
- Can tranh over-fetching hoac under-fetching.
- Mot man hinh can gom data tu nhieu resource.
- Client muon tu quyet dinh shape cua response.

Vi du frontend can product, seller, reviews trong mot request thi GraphQL co the phu hop hon REST.

## Phan tich Stripe va GitHub

Chi tiet nam trong file `API_PATTERN_ANALYSIS.md`.

Tom tat:

### Stripe

- Resource-oriented REST: `/customers`, `/payment_intents`, `/subscriptions`.
- CRUD semantics ro rang qua HTTP method.
- Idempotency key cho POST de tranh tao duplicate khi retry thanh toan.
- Event-driven va webhook la core integration model.
- Verify webhook signature qua `Stripe-Signature`.
- Query/expand pattern nhu `expand[]` de lay nested object.

### GitHub

- REST endpoint theo resource: repository, issue, pull request.
- Query/search pattern rat manh.
- Pagination qua `Link` header.
- Webhook cho cac event nhu `push`, `pull_request`, `issues`.
- Signature verification qua `X-Hub-Signature-256`.
- Rate limit qua response headers.

## Thu tu demo tren lop

1. Chay server:

```bash
python src/server.py
```

2. Mo Swagger:

```text
http://127.0.0.1:5013/docs
```

3. Goi `GET /` de xem `_links` va danh sach pattern.

4. Tao product bang `POST /api/products`.

5. Lay danh sach product bang `GET /api/products` voi query:

```text
category=book
search=python
min_price=10
max_price=50
sort=-price
page=1
limit=10
```

6. Lay chi tiet product va chi ra `_links` trong response.

7. Dang ky webhook bang webhook.site.

8. Tao notification bang `POST /api/notifications`.

9. Xem `GET /api/events` de thay event `notification.created`.

10. Xem webhook.site va `GET /api/webhooks/deliveries` de thay delivery result.

11. Tao order bang `POST /api/orders` de trigger event `order.created`.

12. Lien he voi Stripe/GitHub:

- Stripe dung webhook cho payment events.
- GitHub dung webhook cho repository events.
- Ca hai deu dung signature de verify webhook.

## Bien moi truong

File `.env.example`:

```env
PORT=5013
FLASK_DEBUG=0
WEBHOOK_TIMEOUT_SECONDS=3
```

Y nghia:

- `PORT`: cong chay Flask server.
- `FLASK_DEBUG`: `1` de bat debug mode, `0` de tat.
- `WEBHOOK_TIMEOUT_SECONDS`: timeout khi gui webhook ra ngoai.

## Luu y gioi han cua demo

- Du lieu luu in-memory, restart server la mat du lieu.
- Chua co database that.
- Chua co retry queue cho webhook failed.
- Chua co auth cho API.
- Signature moi duoc tao khi gui webhook, project chua co endpoint receiver de verify nguoc lai.

Nhung cac gioi han nay giup project gon va tap trung vao muc tieu chinh cua buoi hoc: hieu API design patterns va cach chung ket hop voi nhau.
