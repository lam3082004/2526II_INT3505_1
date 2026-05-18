from __future__ import annotations

from flask import Flask, jsonify

try:
    from .routes.notification_routes import notification_bp
    from .routes.product_routes import product_bp
    from .routes.webhook_routes import webhook_bp
    from .services.event_bus import EVENT_BUS
    from .services.webhook_service import dispatch_event
except ImportError:
    from routes.notification_routes import notification_bp
    from routes.product_routes import product_bp
    from routes.webhook_routes import webhook_bp
    from services.event_bus import EVENT_BUS
    from services.webhook_service import dispatch_event


def _webhook_handler(event: dict) -> None:
    dispatch_event(event)


def create_app() -> Flask:
    app = Flask(__name__)

    app.register_blueprint(product_bp)
    app.register_blueprint(notification_bp)
    app.register_blueprint(webhook_bp)

    EVENT_BUS.subscribe("notification.created", _webhook_handler)
    EVENT_BUS.subscribe("order.created", _webhook_handler)

    @app.get("/")
    def root():
        return (
            jsonify(
                {
                    "service": "week11-12-api-design-patterns",
                    "patterns": [
                        "CRUD",
                        "Query",
                        "HATEOAS",
                        "Event-driven",
                        "Webhook",
                    ],
                    "_links": {
                        "products": {"href": "/api/products", "method": "GET"},
                        "notifications": {
                            "href": "/api/notifications",
                            "method": "GET",
                        },
                        "webhooks": {
                            "href": "/api/webhooks/subscriptions",
                            "method": "GET",
                        },
                        "events": {"href": "/api/events", "method": "GET"},
                    },
                }
            ),
            200,
        )

    @app.errorhandler(404)
    def not_found(_error):
        return jsonify({"error": "Route not found"}), 404

    @app.errorhandler(Exception)
    def internal_error(error):
        return jsonify({"error": str(error)}), 500

    return app
