from __future__ import annotations

from datetime import datetime, timezone
from uuid import uuid4

from flask import Blueprint, jsonify, request

payment_bp = Blueprint("payments", __name__)

# In-memory storage for demo lifecycle/versioning only.
PAYMENTS: list[dict] = []
SUNSET_HEADER_VALUE = "Wed, 31 Jul 2026 23:59:59 GMT"


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def _add_deprecation_headers(response):
    response.headers["Deprecation"] = "true"
    response.headers["Sunset"] = SUNSET_HEADER_VALUE
    response.headers["Link"] = '</MIGRATION_PLAN.md>; rel="deprecation"'
    return response


def _resolve_version(default_version: str = "1") -> str:
    query_version = (request.args.get("version") or "").strip()
    if query_version in {"1", "2"}:
        return query_version

    header_version = (request.headers.get("X-API-Version") or "").strip()
    if header_version in {"1", "2"}:
        return header_version

    return default_version


def _parse_v1_payload(payload: dict) -> tuple[dict | None, str | None]:
    user_id = (payload.get("user_id") or "").strip()
    payment_method = (payload.get("payment_method") or "").strip()
    amount = payload.get("amount")

    if not user_id or not payment_method:
        return None, "user_id and payment_method are required"
    if isinstance(amount, bool) or not isinstance(amount, (int, float)):
        return None, "amount must be a number"
    if amount <= 0:
        return None, "amount must be > 0"

    return {
        "customer_id": user_id,
        "amount_cents": int(round(float(amount) * 100)),
        "currency": "USD",
        "method": {"type": payment_method},
    }, None


def _parse_v2_payload(payload: dict) -> tuple[dict | None, str | None]:
    customer_id = (payload.get("customer_id") or "").strip()
    currency = (payload.get("currency") or "").strip().upper()
    amount_cents = payload.get("amount_cents")
    method = payload.get("method") or {}
    method_type = (method.get("type") or "").strip() if isinstance(method, dict) else ""

    if not customer_id or not currency or not method_type:
        return None, "customer_id, currency and method.type are required"
    if isinstance(amount_cents, bool) or not isinstance(amount_cents, int):
        return None, "amount_cents must be an integer"
    if amount_cents <= 0:
        return None, "amount_cents must be > 0"

    return {
        "customer_id": customer_id,
        "amount_cents": amount_cents,
        "currency": currency,
        "method": {"type": method_type},
    }, None


def _to_v1_view(item: dict) -> dict:
    return {
        "id": item["id"],
        "user_id": item["customer_id"],
        "amount": item["amount_cents"] / 100,
        "payment_method": item["method"]["type"],
        "status": item["status"],
        "created_at": item["created_at"],
    }


def _to_v2_view(item: dict) -> dict:
    return {
        "id": item["id"],
        "customer_id": item["customer_id"],
        "money": {
            "amount_cents": item["amount_cents"],
            "currency": item["currency"],
        },
        "method": item["method"],
        "status": item["status"],
        "created_at": item["created_at"],
        "updated_at": item.get("updated_at"),
    }


def _find_payment(payment_id: str) -> dict | None:
    return next((item for item in PAYMENTS if item["id"] == payment_id), None)


def _json_for_version(data, version: str, status_code: int = 200):
    if isinstance(data, list):
        view = [_to_v1_view(item) if version == "1" else _to_v2_view(item) for item in data]
    else:
        view = _to_v1_view(data) if version == "1" else _to_v2_view(data)

    response = jsonify(view)
    response.status_code = status_code
    if version == "1":
        _add_deprecation_headers(response)
    return response


@payment_bp.get("/api/lifecycle")
def lifecycle_info():
    return jsonify(
        {
            "supported_versions": ["v1", "v2"],
            "default_version": "v1",
            "deprecated_versions": ["v1"],
            "sunset": {"v1": SUNSET_HEADER_VALUE},
        }
    ), 200


@payment_bp.post("/api/v1/payments")
def create_payment_v1():
    payload = request.get_json(silent=True) or {}
    canonical, error = _parse_v1_payload(payload)
    if error:
        response = jsonify({"error": error})
        response.status_code = 400
        return _add_deprecation_headers(response)

    payment = {
        "id": str(uuid4()),
        **canonical,
        "status": "created",
        "created_at": _now_iso(),
    }
    PAYMENTS.append(payment)
    return _json_for_version(payment, "1", 201)


@payment_bp.post("/api/v2/payments")
def create_payment_v2():
    payload = request.get_json(silent=True) or {}
    canonical, error = _parse_v2_payload(payload)
    if error:
        return jsonify({"error": error}), 400

    payment = {
        "id": str(uuid4()),
        **canonical,
        "status": "created",
        "created_at": _now_iso(),
    }
    PAYMENTS.append(payment)
    return _json_for_version(payment, "2", 201)


@payment_bp.get("/api/v1/payments")
def list_payments_v1():
    return _json_for_version(PAYMENTS, "1", 200)


@payment_bp.get("/api/v2/payments")
def list_payments_v2():
    return _json_for_version(PAYMENTS, "2", 200)


@payment_bp.get("/api/v1/payments/<string:payment_id>")
def get_payment_v1(payment_id: str):
    payment = _find_payment(payment_id)
    if not payment:
        response = jsonify({"error": "Payment not found"})
        response.status_code = 404
        return _add_deprecation_headers(response)
    return _json_for_version(payment, "1", 200)


@payment_bp.get("/api/v2/payments/<string:payment_id>")
def get_payment_v2(payment_id: str):
    payment = _find_payment(payment_id)
    if not payment:
        return jsonify({"error": "Payment not found"}), 404
    return _json_for_version(payment, "2", 200)


@payment_bp.put("/api/v1/payments/<string:payment_id>")
def update_payment_v1(payment_id: str):
    payment = _find_payment(payment_id)
    if not payment:
        response = jsonify({"error": "Payment not found"})
        response.status_code = 404
        return _add_deprecation_headers(response)

    payload = request.get_json(silent=True) or {}
    canonical, error = _parse_v1_payload(payload)
    if error:
        response = jsonify({"error": error})
        response.status_code = 400
        return _add_deprecation_headers(response)

    payment.update(canonical)
    payment["updated_at"] = _now_iso()
    return _json_for_version(payment, "1", 200)


@payment_bp.put("/api/v2/payments/<string:payment_id>")
def update_payment_v2(payment_id: str):
    payment = _find_payment(payment_id)
    if not payment:
        return jsonify({"error": "Payment not found"}), 404

    payload = request.get_json(silent=True) or {}
    canonical, error = _parse_v2_payload(payload)
    if error:
        return jsonify({"error": error}), 400

    payment.update(canonical)
    payment["updated_at"] = _now_iso()
    return _json_for_version(payment, "2", 200)


@payment_bp.route("/api/payments", methods=["GET", "POST"])
def payments_by_header_or_query():
    version = _resolve_version(default_version="1")

    if request.method == "GET":
        return _json_for_version(PAYMENTS, version, 200)

    payload = request.get_json(silent=True) or {}
    parser = _parse_v1_payload if version == "1" else _parse_v2_payload
    canonical, error = parser(payload)
    if error:
        response = jsonify({"error": error})
        response.status_code = 400
        if version == "1":
            _add_deprecation_headers(response)
        return response

    payment = {
        "id": str(uuid4()),
        **canonical,
        "status": "created",
        "created_at": _now_iso(),
    }
    PAYMENTS.append(payment)
    return _json_for_version(payment, version, 201)