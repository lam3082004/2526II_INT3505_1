# Deprecation Notice - Payment API v1

## Subject

Deprecation notice: Payment API v1 will be sunset in 90 days

## Message

Payment API v1 da duoc deprecate va se sunset sau 90 ngay ke tu ngay thong bao.

### Deprecated endpoints

- `POST /api/v1/payments`
- `GET /api/v1/payments`
- `GET /api/v1/payments/{paymentId}`
- `PUT /api/v1/payments/{paymentId}`

### New endpoints

- `POST /api/v2/payments`
- `GET /api/v2/payments`
- `GET /api/v2/payments/{paymentId}`
- `PUT /api/v2/payments/{paymentId}`

### Required actions

- Migrate payload tu v1 sang v2 theo file `MIGRATION_PLAN.md`
- Hoan thanh regression test truoc ngay sunset

### Runtime signal

Khi goi v1, server tra cac header:

- `Deprecation: true`
- `Sunset: Wed, 31 Jul 2026 23:59:59 GMT`
- `Link: </MIGRATION_PLAN.md>; rel="deprecation"`