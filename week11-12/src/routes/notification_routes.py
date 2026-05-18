from __future__ import annotations

from datetime import datetime, timezone
from uuid import uuid4

from flask import Blueprint, jsonify, request

try:
    from ..services.event_bus import EVENT_BUS
    from ..storage import NOTIFICATIONS, ORDERS, EVENT_LOG
    from ..utils.hateoas import notification_links
except ImportError:
    from services.event_bus import EVENT_BUS
    from storage import NOTIFICATIONS, ORDERS, EVENT_LOG
    from utils.hateoas import notification_links


notification_bp = Blueprint("notifications", __name__, url_prefix="/api")


@notification_bp.post("/notifications")
def create_notification():
    payload = request.get_json(silent=True) or {}
    message = (payload.get("message") or "").strip()
    recipient = (payload.get("recipient") or "").strip()
    channel = (payload.get("channel") or "email").strip()

    if not message or not recipient:
        return jsonify({"error": "message and recipient are required"}), 400

    notification_id = str(uuid4())
    notification = {
        "id": notification_id,
        "message": message,
        "recipient": recipient,
        "channel": channel,
        "status": "queued",
        "created_at": datetime.now(timezone.utc).isoformat(),
    }
    NOTIFICATIONS[notification_id] = notification

    EVENT_BUS.publish("notification.created", notification)

    return jsonify({**notification, "_links": notification_links(notification_id)}), 201


@notification_bp.get("/notifications/<string:notification_id>")
def get_notification(notification_id: str):
    notification = NOTIFICATIONS.get(notification_id)
    if not notification:
        return jsonify({"error": "Notification not found"}), 404
    return jsonify({**notification, "_links": notification_links(notification_id)}), 200


@notification_bp.get("/notifications")
def list_notifications():
    data = [
        {**item, "_links": notification_links(item["id"])}
        for item in NOTIFICATIONS.values()
    ]
    return jsonify({"data": data}), 200


@notification_bp.post("/orders")
def create_order():
    payload = request.get_json(silent=True) or {}
    customer_id = (payload.get("customer_id") or "").strip()
    amount = payload.get("amount")

    if not customer_id or not isinstance(amount, (int, float)):
        return jsonify({"error": "customer_id and numeric amount are required"}), 400

    order_id = str(uuid4())
    order = {
        "id": order_id,
        "customer_id": customer_id,
        "amount": float(amount),
        "status": "created",
        "created_at": datetime.now(timezone.utc).isoformat(),
    }
    ORDERS[order_id] = order

    EVENT_BUS.publish("order.created", order)

    return jsonify(order), 201


@notification_bp.get("/events")
def list_events():
    return jsonify({"data": EVENT_LOG, "count": len(EVENT_LOG)}), 200
