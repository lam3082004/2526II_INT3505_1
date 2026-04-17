from __future__ import annotations

from pathlib import Path

import yaml
from flasgger import Swagger
from flask import Flask, jsonify

try:
    from .routes.product_routes import product_bp
except ImportError:
    from routes.product_routes import product_bp


def create_app() -> Flask:
    app = Flask(__name__)

    openapi_path = Path(__file__).resolve().parent.parent / "openapi.yaml"
    swagger_template = yaml.safe_load(openapi_path.read_text(encoding="utf-8"))

    Swagger(app, template=swagger_template)

    app.register_blueprint(product_bp)

    @app.get("/")
    def home():
        return jsonify({"message": "Week7 Product API is running", "docs": "/apidocs/"}), 200

    @app.get("/health")
    def health():
        return jsonify({"status": "ok"}), 200

    @app.errorhandler(404)
    def not_found(_error):
        return jsonify({"error": "Route not found"}), 404

    @app.errorhandler(Exception)
    def handle_exception(error):
        return jsonify({"error": str(error) or "Internal Server Error"}), 500

    return app