from __future__ import annotations

from pathlib import Path

import yaml
from flasgger import Swagger
from flask import Flask, jsonify

try:
    from .routes.payments import payment_bp
except ImportError:
    from routes.payments import payment_bp


def create_app() -> Flask:
    app = Flask(__name__)

    openapi_path = Path(__file__).resolve().parent.parent / "openapi.yaml"
    if openapi_path.exists():
        swagger_template = yaml.safe_load(openapi_path.read_text(encoding="utf-8"))
        Swagger(app, template=swagger_template)

    app.register_blueprint(payment_bp)

    @app.get("/")
    def home():
        return (
            jsonify(
                {
                    "message": "Week9 Payment API is running",
                    "docs": "/apidocs/",
                    "available_strategies": ["url", "header", "query_param"],
                    "sample": {
                        "url": ["/api/v1/payments", "/api/v2/payments"],
                        "header": "GET /api/payments + X-API-Version: 2",
                        "query": "GET /api/payments?version=2",
                    },
                }
            ),
            200,
        )

    @app.get("/health")
    def health():
        return jsonify({"status": "ok"}), 200

    @app.errorhandler(404)
    def not_found(_error):
        return jsonify({"error": "Route not found"}), 404

    @app.errorhandler(Exception)
    def unexpected_error(error):
        return jsonify({"error": str(error) or "Internal Server Error"}), 500

    return app