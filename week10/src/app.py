from __future__ import annotations

import logging
import os
from datetime import datetime, timezone
from prometheus_client import Counter, Histogram, generate_latest
from flask import Flask, jsonify, request

try:
    from .config.logging_config import setup_logging
    from .middleware.rate_limiter import create_rate_limiter
    from .routes.api_routes import api_bp
except ImportError:
    from config.logging_config import setup_logging
    from middleware.rate_limiter import create_rate_limiter
    from routes.api_routes import api_bp

logger = logging.getLogger(__name__)

# Prometheus metrics
REQUEST_COUNT = Counter(
    "http_requests_total",
    "Total HTTP requests",
    ["method", "endpoint", "status"],
)
REQUEST_DURATION = Histogram(
    "http_request_duration_seconds",
    "HTTP request duration",
    ["method", "endpoint"],
)
RATE_LIMIT_EXCEEDED = Counter(
    "rate_limit_exceeded_total",
    "Rate limit exceeded events",
    ["endpoint"],
)


def create_app() -> Flask:
    setup_logging(os.getenv("LOG_LEVEL", "INFO"))

    app = Flask(__name__)

    # Rate limiter
    limiter = create_rate_limiter()
    if limiter:
        limiter.init_app(app)
        app.limiter = limiter
    
    # Register blueprints
    app.register_blueprint(api_bp)

    # Security headers
    @app.after_request
    def add_security_headers(response):
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        if os.getenv("ENVIRONMENT") == "production":
            response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
        return response

    # Request tracking
    @app.before_request
    def before_request():
        request.start_time = datetime.now(timezone.utc)

    @app.after_request
    def after_request(response):
        if hasattr(request, "start_time"):
            duration = (datetime.now(timezone.utc) - request.start_time).total_seconds()
            REQUEST_DURATION.labels(request.method, request.path).observe(duration)
        REQUEST_COUNT.labels(request.method, request.path, response.status_code).inc()
        
        if response.status_code == 429:
            RATE_LIMIT_EXCEEDED.labels(request.path).inc()

        logger.info(
            {
                "method": request.method,
                "path": request.path,
                "status": response.status_code,
                "ip": request.remote_addr,
                "duration_ms": (datetime.now(timezone.utc) - request.start_time).total_seconds() * 1000 if hasattr(request, "start_time") else 0,
            }
        )
        return response

    @app.get("/health")
    def health():
        return (
            jsonify(
                {
                    "status": "ok",
                    "service": "week10-api",
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                }
            ),
            200,
        )

    @app.get("/metrics")
    def metrics():
        return generate_latest(), 200, {"Content-Type": "text/plain; charset=utf-8"}

    @app.errorhandler(429)
    def ratelimit_handler(e):
        logger.warning(f"Rate limit exceeded for {request.remote_addr} on {request.path}")
        return jsonify({"error": "Rate limit exceeded"}), 429

    @app.errorhandler(404)
    def not_found(_error):
        return jsonify({"error": "Route not found"}), 404

    @app.errorhandler(Exception)
    def handle_exception(error):
        logger.error(f"Unexpected error: {str(error)}", exc_info=True)
        return jsonify({"error": "Internal Server Error"}), 500

    if limiter:
        limiter.limit("1000/hour")(health)
        limiter.limit("1000/hour")(metrics)

    return app
