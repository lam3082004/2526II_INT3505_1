from __future__ import annotations

import hashlib
import hmac
import json
import os
from datetime import datetime, timezone
from uuid import uuid4

import requests

try:
    from ..storage import WEBHOOK_DELIVERY_LOG, WEBHOOK_SUBSCRIPTIONS
except ImportError:
    from storage import WEBHOOK_DELIVERY_LOG, WEBHOOK_SUBSCRIPTIONS


def create_subscription(url: str, events: list[str], secret: str) -> dict:
    subscription_id = str(uuid4())
    subscription = {
        "id": subscription_id,
        "url": url,
        "events": events,
        "secret": secret,
        "created_at": datetime.now(timezone.utc).isoformat(),
    }
    WEBHOOK_SUBSCRIPTIONS[subscription_id] = subscription
    return subscription


def list_subscriptions() -> list[dict]:
    return list(WEBHOOK_SUBSCRIPTIONS.values())


def delete_subscription(subscription_id: str) -> bool:
    if subscription_id not in WEBHOOK_SUBSCRIPTIONS:
        return False
    del WEBHOOK_SUBSCRIPTIONS[subscription_id]
    return True


def _build_signature(secret: str, payload: dict) -> str:
    raw = json.dumps(payload, sort_keys=True).encode("utf-8")
    return hmac.new(secret.encode("utf-8"), raw, hashlib.sha256).hexdigest()


def dispatch_event(event: dict) -> list[dict]:
    timeout_seconds = int(os.getenv("WEBHOOK_TIMEOUT_SECONDS", "3"))
    event_type = event["type"]
    payload = {
        "event": event_type,
        "timestamp": event["timestamp"],
        "data": event["data"],
    }

    results: list[dict] = []

    for subscription in WEBHOOK_SUBSCRIPTIONS.values():
        supports_event = event_type in subscription["events"] or "*" in subscription["events"]
        if not supports_event:
            continue

        signature = _build_signature(subscription["secret"], payload)
        headers = {
            "Content-Type": "application/json",
            "X-Event-Type": event_type,
            "X-Webhook-Signature": signature,
        }

        result = {
            "subscription_id": subscription["id"],
            "target_url": subscription["url"],
            "event": event_type,
            "delivered_at": datetime.now(timezone.utc).isoformat(),
        }

        try:
            response = requests.post(
                subscription["url"],
                json=payload,
                headers=headers,
                timeout=timeout_seconds,
            )
            result["status"] = "success"
            result["http_status"] = response.status_code
        except requests.RequestException as error:
            result["status"] = "failed"
            result["error"] = str(error)

        WEBHOOK_DELIVERY_LOG.append(result)
        results.append(result)

    return results
