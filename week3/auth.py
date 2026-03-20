from datetime import datetime, timedelta, timezone
from functools import wraps
import os

import jwt
from flask import Blueprint, g, jsonify, request
from werkzeug.security import check_password_hash, generate_password_hash

JWT_SECRET = os.getenv("JWT_SECRET", "week3-super-secret-key-at-least-32-bytes")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
JWT_EXPIRE_MINUTES = int(os.getenv("JWT_EXPIRE_MINUTES", "60"))

USERS = {
    "admin": {
        "username": "admin",
        "password_hash": generate_password_hash("123456"),
    },
    "tester": {
        "username": "tester",
        "password_hash": generate_password_hash("123456"),
    },
}

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")


def create_access_token(username):
    now = datetime.now(timezone.utc)
    payload = {
        "sub": username,
        "iat": now,
        "exp": now + timedelta(minutes=JWT_EXPIRE_MINUTES),
    }
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)


def get_request_credentials():
    data = request.get_json(silent=True) or {}
    username = (data.get("username") or "").strip()
    password = data.get("password") or ""
    return username, password


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


@auth_bp.route("/register", methods=["POST"])
def register():
    """
    Register new account
    ---
    tags:
      - Auth
    consumes:
      - application/json
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - username
            - password
          properties:
            username:
              type: string
              example: newuser
            password:
              type: string
              example: "123456"
    responses:
      201:
        description: Register success
      400:
        description: Missing username or password
      409:
        description: Username already exists
    """
    username, password = get_request_credentials()

    if not username or not password:
        return jsonify({"error": "Missing username or password"}), 400

    if username in USERS:
        return jsonify({"error": "Username already exists"}), 409

    USERS[username] = {
        "username": username,
        "password_hash": generate_password_hash(password),
    }
    return jsonify({"message": "Register success", "username": username}), 201


@auth_bp.route("/login", methods=["POST"])
def login():
    """
    Login to get JWT token
    ---
    tags:
      - Auth
    consumes:
      - application/json
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - username
            - password
          properties:
            username:
              type: string
              example: admin
            password:
              type: string
              example: "123456"
    responses:
      200:
        description: Login success and return JWT
      400:
        description: Missing username or password
      401:
        description: Invalid credentials
    """
    username, password = get_request_credentials()

    if not username or not password:
        return jsonify({"error": "Missing username or password"}), 400

    user = USERS.get(username)
    if not user or not check_password_hash(user["password_hash"], password):
        return jsonify({"error": "Invalid credentials"}), 401

    token = create_access_token(username)
    return jsonify(
        {
            "access_token": token,
            "token_type": "Bearer",
            "expires_in_minutes": JWT_EXPIRE_MINUTES,
        }
    ), 200


@auth_bp.route("/me", methods=["GET"])
@require_jwt
def me():
    """
    Get current authenticated user
    ---
    tags:
      - Auth
    security:
      - BearerAuth: []
    responses:
      200:
        description: Current user info
      401:
        description: Missing or invalid token
    """
    return jsonify({"username": g.current_user}), 200


