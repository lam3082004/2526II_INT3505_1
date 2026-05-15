# Week10 - Production-Ready API: Observability, Monitoring, Rate Limiting

Tuần 10 tập trung vào deploy API lên production với:

- Logging và structured logs (JSON)
- Prometheus metrics (request count, latency, errors)
- Rate limiting (requests/minute)
- Circuit breaker (prevent cascading failures)
- Security headers (CORS, CSP, X-Frame-Options)
- Audit logs (ai, khi, cái gì)
- Docker support

## Cấu trúc

- `src/server.py`: entrypoint
- `src/app.py`: Flask app setup
- `src/config/logging_config.py`: logging setup
- `src/middleware/rate_limiter.py`: rate limit middleware
- `src/middleware/circuit_breaker.py`: circuit breaker decorator
- `src/routes/api_routes.py`: demo endpoints
- `docker/Dockerfile`: container image
- `docker-compose.yaml`: orchestration
- `PRODUCTION_SETUP.md`: deployment guide

## Chạy local

```bash
cd week10
python -m pip install -r requirements.txt
cp .env.example .env
python src/server.py
```

Server mặc định: `http://127.0.0.1:5012`

## Endpoints

- `GET /health`: health check
- `GET /metrics`: Prometheus metrics
- `GET /api/users`: list users (rate limited)
- `POST /api/users`: create user (rate limited + circuit breaker demo)
- `GET /api/users/<id>`: get user

## Monitoring

- Logs: `logs/app.log` (JSON format)
- Metrics: http://127.0.0.1:5012/metrics
- Audit logs: `logs/audit.log`

## Docker deploy

```bash
docker-compose up -d
```

## Test rate limiting

```bash
# Loop 65 times - should hit limit
for i in {1..65}; do
  curl http://127.0.0.1:5012/api/users
done
```

## Test circuit breaker

```bash
# Repeat failed create requests to trigger circuit breaker
for i in {1..6}; do
  curl -X POST http://127.0.0.1:5012/api/users \
    -H "Content-Type: application/json" \
    -d '{}'
done
```
