from __future__ import annotations

from flask import Blueprint, jsonify, request

try:
    from ..services.webhook_service import (
        create_subscription,
        delete_subscription,
        list_subscriptions,
    )
    from ..storage import WEBHOOK_DELIVERY_LOG
except ImportError:
    from services.webhook_service import (
        create_subscription,
        delete_subscription,
        list_subscriptions,
    )
    from storage import WEBHOOK_DELIVERY_LOG


webhook_bp = Blueprint("webhooks", __name__, url_prefix="/api/webhooks")


@webhook_bp.post("/subscriptions")
def register_webhook():
    payload = request.get_json(silent=True) or {}
    url = (payload.get("url") or "").strip()
    events = payload.get("events") or []
    secret = (payload.get("secret") or "").strip()

    if not url or not isinstance(events, list) or not events or not secret:
        return jsonify({"error": "url, events(array), secret are required"}), 400

    subscription = create_subscription(url, events, secret)
    return jsonify(subscription), 201


@webhook_bp.get("/subscriptions")
def get_subscriptions():
    return jsonify({"data": list_subscriptions()}), 200


@webhook_bp.delete("/subscriptions/<string:subscription_id>")
def remove_subscription(subscription_id: str):
    deleted = delete_subscription(subscription_id)
    if not deleted:
        return jsonify({"error": "Subscription not found"}), 404
    return "", 204


@webhook_bp.get("/deliveries")
def list_deliveries():
    return jsonify({"data": WEBHOOK_DELIVERY_LOG, "count": len(WEBHOOK_DELIVERY_LOG)}), 200
