# Production Setup Guide - Week10 API

## 1. Pre-deployment Checklist

- [ ] Environment variables configured (.env)
- [ ] Logs directory writable and monitored
- [ ] Prometheus scrape endpoint accessible
- [ ] Rate limits tuned for expected traffic
- [ ] Circuit breaker thresholds tested
- [ ] Security headers validated
- [ ] Audit logging enabled

## 2. Environment Setup

Production `.env` (example):

```
PORT=5000
FLASK_DEBUG=0
LOG_LEVEL=INFO
RATE_LIMIT_ENABLED=1
RATE_LIMIT_PER_MINUTE=100
CIRCUIT_BREAKER_ENABLED=1
CIRCUIT_BREAKER_FAILURE_THRESHOLD=10
CIRCUIT_BREAKER_RECOVERY_TIMEOUT=120
ENVIRONMENT=production
```

## 3. Logging & Monitoring

**Logs:**
- Application logs: `logs/app.log` (JSON format, rotated daily)
- Audit logs: `logs/audit.log` (all user actions)

**Metrics:**
- Prometheus endpoint: `/metrics`
- Scrape interval: 15s recommended
- Key metrics:
  - `http_requests_total`: request count
  - `http_request_duration_seconds`: latency histogram
  - `rate_limit_exceeded_total`: rate limit violations
  - `circuit_breaker_events_total`: circuit breaker trips

## 4. Rate Limiting Strategy

Default: 60 requests/minute per IP

Per-endpoint tuning:
- `/health`: No limit (internal checks)
- `/metrics`: No limit (monitoring)
- `/api/users`: 60/min
- `/api/users/<id>`: 60/min

## 5. Circuit Breaker Configuration

Threshold: 5 consecutive failures
Recovery timeout: 60 seconds

When circuit opens:
- New requests immediately return 503
- Health check continues
- After timeout, attempts half-open state

## 6. Security Headers

Applied globally:

```
X-Content-Type-Options: nosniff
X-Frame-Options: DENY
X-XSS-Protection: 1; mode=block
Strict-Transport-Security: max-age=31536000; includeSubDomains
```

## 7. Deployment Strategies

### Docker (recommended)

```bash
docker build -f docker/Dockerfile -t week10-api:1.0 .
docker-compose -f docker-compose.yaml up -d
```

### Manual (systemd)

```bash
# /etc/systemd/system/week10-api.service
[Unit]
Description=Week10 API
After=network.target

[Service]
Type=simple
User=apiuser
WorkingDirectory=/opt/week10-api
ExecStart=/opt/week10-api/venv/bin/python src/server.py
Restart=on-failure
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
```

## 8. Health Checks

Endpoint: `GET /health`

Response:
```json
{
  "status": "ok",
  "service": "week10-api",
  "timestamp": "2026-05-15T10:30:45Z"
}
```

## 9. Monitoring Alerts

Prometheus alerts to setup:

- `HighErrorRate`: error_rate > 5% for 5m
- `HighLatency`: p95 latency > 1s
- `RateLimitExceeded`: limit violations > 10/min
- `CircuitBreakerOpen`: circuit breaker trips > 3/hour

## 10. Rollback Plan

1. Previous version tagged in Docker registry
2. `docker-compose pull; docker-compose up -d` to rollback
3. Monitor metrics for recovery

## 11. Scaling Considerations

- Horizontal scaling: use load balancer (nginx, HAProxy)
- Each instance logs to centralized ELK/Splunk
- Prometheus federation for multiple instances
- Redis for distributed rate limiting (future)

## 12. SLA Targets

- Availability: 99.5%
- Error rate: < 1%
- P95 latency: < 500ms
- Rate limit compliance: 100%
