from __future__ import annotations

from flask import Blueprint, jsonify, g

try:
    from ..auth.jwt_auth import login_user, parse_credentials, register_user, require_jwt
except ImportError:
    from auth.jwt_auth import login_user, parse_credentials, register_user, require_jwt


auth_bp = Blueprint("auth", __name__, url_prefix="/auth")


@auth_bp.post("/register")
def register_endpoint():
    username, password = parse_credentials()
    payload, error, status_code = register_user(username, password)
    if error:
        return jsonify({"error": error}), status_code
    return jsonify(payload), status_code


@auth_bp.post("/login")
def login_endpoint():
    username, password = parse_credentials()
    payload, error, status_code = login_user(username, password)
    if error:
        return jsonify({"error": error}), status_code
    return jsonify(payload), status_code


@auth_bp.get("/me")
@require_jwt
def me_endpoint():
    return jsonify({"username": g.current_user}), 200

