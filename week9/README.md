# Week9 - API Versioning va Lifecycle Management (Python)

Buoi 9 tap trung vao 3 chien luoc versioning va cach xu ly breaking changes/deprecation cho API thanh toan.

## Muc tieu dat duoc

- Versioning theo URL: `/api/v1/payments`, `/api/v2/payments`
- Versioning theo Header: `/api/payments` + `X-API-Version: 1|2`
- Versioning theo Query Param: `/api/payments?version=1|2`
- Xu ly breaking change v1 -> v2
- Gui thong bao deprecation cho v1
- Co migration plan cho developers

## Cau truc

- `src/server.py`: entrypoint chay Flask app
- `src/app.py`: tao app va route root
- `src/routes/payments.py`: payment endpoints va versioning logic
- `MIGRATION_PLAN.md`: ke hoach nang cap tu v1 sang v2
- `DEPRECATION_NOTICE.md`: thong bao deprecation gui dev

## Chay local

```bash
cd week9
python -m pip install -r requirements.txt
cp .env.example .env
python src/server.py
```

Server mac dinh: `http://127.0.0.1:5011`

## Swagger UI

Mo: `http://127.0.0.1:5011/apidocs/`

## Test nhanh

### URL versioning

```bash
curl -X POST http://127.0.0.1:5011/api/v1/payments \
  -H "Content-Type: application/json" \
  -d '{"user_id":"u01","amount":12.5,"payment_method":"card"}'
```

```bash
curl -X POST http://127.0.0.1:5011/api/v2/payments \
  -H "Content-Type: application/json" \
  -d '{"customer_id":"c01","amount_cents":1250,"currency":"USD","method":{"type":"card"}}'
```

### Header versioning

```bash
curl -X GET http://127.0.0.1:5011/api/payments -H "X-API-Version: 2"
```

### Query param versioning

```bash
curl -X GET "http://127.0.0.1:5011/api/payments?version=1"
```

## Cac payload example

### V1 payload

```json
{
  "user_id": "u01",
  "amount": 12.5,
  "payment_method": "card"
}
```

### V2 payload

```json
{
  "customer_id": "c01",
  "amount_cents": 1250,
  "currency": "USD",
  "method": {
    "type": "card"
  }
}
```