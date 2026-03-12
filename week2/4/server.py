from flask import Flask, request, jsonify, make_response
from functools import wraps
import hashlib, json
from datetime import datetime, timezone

app = Flask(__name__)

users = [
    {"id": 1, "name": "Alice", "email": "alice@example.com"},
    {"id": 2, "name": "Bob",   "email": "bob@example.com"},
    {"id": 3, "name": "Carol", "email": "carol@example.com"},
]

VALID_TOKENS = {"secret-token-alice": 1, "secret-token-bob": 2}

@app.before_request
def log_request():
    app.logger.info(f"→ {request.method} {request.path}")

@app.after_request
def log_response(response):
    app.logger.info(f"← {response.status_code}")
    return response

def require_auth(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        auth = request.headers.get("Authorization", "")
        if not auth.startswith("Bearer "):
            return jsonify({"error": "Missing Authorization"}), 401
        token = auth.split(" ", 1)[1]
        if token not in VALID_TOKENS:
            return jsonify({"error": "Invalid token"}), 401
        return f(*args, **kwargs)
    return wrapper

def make_etag(data):
    return hashlib.md5(json.dumps(data, sort_keys=True).encode()).hexdigest()

def cached_response(data, max_age=30):
    etag = make_etag(data)
    client_etag = request.headers.get("If-None-Match")

    if client_etag == etag:
        res = make_response("", 304)
        res.headers["ETag"] = etag
        return res

    res = make_response(jsonify(data), 200)
    res.headers["ETag"] = etag
    res.headers["Cache-Control"] = f"public, max-age={max_age}"
    res.headers["Last-Modified"] = datetime.now(timezone.utc).strftime(
        "%a, %d %b %Y %H:%M:%S GMT"
    )
    return res

def find_user(uid):
    return next((u for u in users if u["id"] == uid), None)

@app.route("/users", methods=["GET"])
@require_auth
def get_users():
    return cached_response(users, max_age=30)

@app.route("/users/<int:uid>", methods=["GET"])
@require_auth
def get_user(uid):
    u = find_user(uid)
    if not u:
        return jsonify({"error": "User not found"}), 404
    return cached_response(u, max_age=60)

@app.route("/users", methods=["POST"])
@require_auth
def create_user():
    data = request.json
    if not data or "name" not in data or "email" not in data:
        return jsonify({"error": "Missing name or email"}), 400
    new = {"id": len(users) + 1, "name": data["name"], "email": data["email"]}
    users.append(new)
    res = make_response(jsonify(new), 201)
    res.headers["Location"] = f"/users/{new['id']}"
    res.headers["Cache-Control"] = "no-store"
    return res

@app.route("/users/<int:uid>", methods=["PUT"])
@require_auth
def update_user(uid):
    u = find_user(uid)
    if not u:
        return jsonify({"error": "User not found"}), 404
    data = request.json
    if not data:
        return jsonify({"error": "No data"}), 400
    u.update({k: v for k, v in data.items() if k in ("name", "email")})
    res = make_response(jsonify(u), 200)
    res.headers["Cache-Control"] = "no-store"
    return res

@app.route("/users/<int:uid>", methods=["DELETE"])
@require_auth
def delete_user(uid):
    u = find_user(uid)
    if not u:
        return jsonify({"error": "User not found"}), 404
    users.remove(u)
    res = make_response("", 204)
    res.headers["Cache-Control"] = "no-store"
    return res

@app.errorhandler(404)
def not_found(e):
    return jsonify({"error": "Endpoint not found"}), 404

@app.errorhandler(405)
def method_not_allowed(e):
    return jsonify({"error": "Method not allowed"}), 405


if __name__ == "__main__":
    print("V4 Server running on http://localhost:5004")
    app.run(port=5004, debug=True)
