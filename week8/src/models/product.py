from __future__ import annotations

from datetime import datetime, timezone
from typing import Any


def _as_utc_iso(value: Any) -> str | None:
    if not isinstance(value, datetime):
        return None

    if value.tzinfo is None:
        value = value.replace(tzinfo=timezone.utc)

    return value.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")


def serialize_product(doc: dict[str, Any]) -> dict[str, Any]:
    return {
        "id": str(doc["_id"]),
        "name": doc["name"],
        "description": doc.get("description", ""),
        "price": doc["price"],
        "category": doc["category"],
        "stock": doc["stock"],
        "imageUrl": doc.get("imageUrl", ""),
        "createdAt": _as_utc_iso(doc.get("createdAt")),
        "updatedAt": _as_utc_iso(doc.get("updatedAt")),
    }


def normalize_product_payload(
    payload: dict[str, Any],
    *,
    partial: bool,
) -> tuple[dict[str, Any], str | None]:
    if not isinstance(payload, dict):
        return {}, "Invalid JSON payload"

    required_fields = ["name", "price", "category", "stock"]
    if not partial:
        missing = [field for field in required_fields if field not in payload]
        if missing:
            return {}, f"Missing required field(s): {', '.join(missing)}"

    allowed_fields = {"name", "description", "price", "category", "stock", "imageUrl"}
    cleaned: dict[str, Any] = {}

    for key, value in payload.items():
        if key not in allowed_fields:
            continue

        if key in {"name", "category"}:
            if not isinstance(value, str) or not value.strip():
                return {}, f"{key} must be a non-empty string"
            cleaned[key] = value.strip()
            continue

        if key in {"description", "imageUrl"}:
            if not isinstance(value, str):
                return {}, f"{key} must be a string"
            cleaned[key] = value.strip()
            continue

        if key == "price":
            if isinstance(value, bool) or not isinstance(value, (int, float)):
                return {}, "price must be a number"
            if value < 0:
                return {}, "price must be >= 0"
            cleaned[key] = float(value)
            continue

        if key == "stock":
            if isinstance(value, bool) or not isinstance(value, int):
                return {}, "stock must be an integer"
            if value < 0:
                return {}, "stock must be >= 0"
            cleaned[key] = value

    if partial and not cleaned:
        return {}, "At least one updatable field is required"

    return cleaned, None

