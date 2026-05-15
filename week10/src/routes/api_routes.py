import logging
from datetime import datetime, timezone
from uuid import uuid4
from flask import Blueprint, jsonify, request

try:
    from ..config.logging_config import get_audit_logger
    from ..middleware.circuit_breaker import with_circuit_breaker
except ImportError:
    from config.logging_config import get_audit_logger
    from middleware.circuit_breaker import with_circuit_breaker


logger = logging.getLogger(__name__)
audit_logger = get_audit_logger()

api_bp = Blueprint("api", __name__, url_prefix="/api")

# In-memory user store
USERS = {}


def _log_audit(action: str, resource: str, user_id: str = "unknown", details: dict = None):
    audit_logger.info(
        {
            "action": action,
            "resource": resource,
            "user_id": user_id,
            "ip": request.remote_addr,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "details": details or {},
        }
    )


@api_bp.get("/users")
def list_users():
    logger.info(f"Listing users from {request.remote_addr}")
    _log_audit("list", "users")
    return jsonify(list(USERS.values())), 200


@api_bp.post("/users")
@with_circuit_breaker
def create_user():
    payload = request.get_json(silent=True) or {}
    name = (payload.get("name") or "").strip()
    email = (payload.get("email") or "").strip()

    if not name or not email:
        logger.warning(f"Invalid user creation attempt from {request.remote_addr}")
        _log_audit("create_failed", "users", details={"reason": "missing_fields"})
        return jsonify({"error": "name and email required"}), 400

    user_id = str(uuid4())
    user = {
        "id": user_id,
        "name": name,
        "email": email,
        "created_at": datetime.now(timezone.utc).isoformat(),
    }
    USERS[user_id] = user

    logger.info(f"User created: {user_id}")
    _log_audit("create", "users", details={"user_id": user_id, "email": email})
    return jsonify(user), 201


@api_bp.get("/users/<string:user_id>")
def get_user(user_id: str):
    user = USERS.get(user_id)
    if not user:
        logger.warning(f"User not found: {user_id}")
        _log_audit("get_failed", "users", details={"user_id": user_id, "reason": "not_found"})
        return jsonify({"error": "User not found"}), 404

    _log_audit("get", "users", details={"user_id": user_id})
    return jsonify(user), 200
