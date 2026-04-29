from __future__ import annotations

from datetime import datetime, timedelta, timezone
from functools import wraps
import os

import jwt
from flask import g, jsonify, request
from werkzeug.security import check_password_hash, generate_password_hash

JWT_SECRET = os.getenv("JWT_SECRET", "week8-super-secret-key-at-least-32-bytes")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
JWT_EXPIRE_MINUTES = int(os.getenv("JWT_EXPIRE_MINUTES", "60"))


# In-memory users (demo purpose, same approach as week6).
USERS: dict[str, dict[str, str]] = {
    "admin": {"username": "admin", "password_hash": generate_password_hash("123456")},
    "tester": {"username": "tester", "password_hash": generate_password_hash("123456")},
}


def create_access_token(username: str) -> str:
    now = datetime.now(timezone.utc)
    payload = {
        "sub": username,
        "iat": now,
        "exp": now + timedelta(minutes=JWT_EXPIRE_MINUTES),
    }
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)


def parse_credentials() -> tuple[str, str]:
    data = request.get_json(silent=True) or {}
    username = (data.get("username") or "").strip()
    password = data.get("password") or ""
    return username, password


def register_user(username: str, password: str) -> tuple[dict[str, str] | None, str | None, int]:
    if not username or not password:
        return None, "Missing username or password", 400
    if username in USERS:
        return None, "Username already exists", 409

    USERS[username] = {"username": username, "password_hash": generate_password_hash(password)}
    return {"message": "Register success", "username": username}, None, 201


def login_user(username: str, password: str) -> tuple[dict[str, object] | None, str | None, int]:
    if not username or not password:
        return None, "Missing username or password", 400

    user = USERS.get(username)
    if not user or not check_password_hash(user["password_hash"], password):
        return None, "Invalid credentials", 401

    token = create_access_token(username)
    return {
        "access_token": token,
        "token_type": "Bearer",
        "expires_in_minutes": JWT_EXPIRE_MINUTES,
    }, None, 200


def require_jwt(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        auth_header = request.headers.get("Authorization", "")
        if not auth_header.startswith("Bearer "):
            return jsonify({"error": "Missing Bearer token"}), 401

        token = auth_header.split(" ", 1)[1].strip()
        try:
            payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        except jwt.ExpiredSignatureError:
            return jsonify({"error": "Token expired"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"error": "Invalid token"}), 401

        g.current_user = payload.get("sub")
        return func(*args, **kwargs)

    return wrapper

