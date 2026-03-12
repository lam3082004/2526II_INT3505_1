from flask import Flask, request, jsonify
from functools import wraps

app = Flask(__name__)

users = [
    {"id": 1, "name": "Alice", "email": "alice@example.com"},
    {"id": 2, "name": "Bob",   "email": "bob@example.com"},
    {"id": 3, "name": "Carol", "email": "carol@example.com"},
]

VALID_TOKENS = {"secret-token-alice": 1, "secret-token-bob": 2}

def require_auth(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        auth = request.headers.get("Authorization", "")
        if not auth.startswith("Bearer "):
            return jsonify({"error": "Missing Authorization header"}), 401
        token = auth.split(" ", 1)[1]
        if token not in VALID_TOKENS:
            return jsonify({"error": "Invalid token"}), 401
        return f(*args, **kwargs)
    return wrapper

def find_user(uid):
    return next((u for u in users if u["id"] == uid), None)

@app.route("/users", methods=["GET"])
@require_auth
def get_users():
    return jsonify(users), 200

@app.route("/users/<int:uid>", methods=["GET"])
@require_auth
def get_user(uid):
    u = find_user(uid)
    if not u:
        return jsonify({"error": "User not found"}), 404
    return jsonify(u), 200

@app.route("/users", methods=["POST"])
@require_auth
def create_user():
    data = request.json
    if not data or "name" not in data or "email" not in data:
        return jsonify({"error": "Missing name or email"}), 400
    new = {"id": len(users) + 1, "name": data["name"], "email": data["email"]}
    users.append(new)
    return jsonify(new), 201

@app.route("/users/<int:uid>", methods=["PUT"])
@require_auth
def update_user(uid):
    u = find_user(uid)
    if not u:
        return jsonify({"error": "User not found"}), 404
    data = request.json
    if not data:
        return jsonify({"error": "No data provided"}), 400
    u.update({k: v for k, v in data.items() if k in ("name", "email")})
    return jsonify(u), 200

@app.route("/users/<int:uid>", methods=["DELETE"])
@require_auth
def delete_user(uid):
    u = find_user(uid)
    if not u:
        return jsonify({"error": "User not found"}), 404
    users.remove(u)
    return jsonify({"message": f"User {uid} deleted"}), 200


if __name__ == "__main__":
    print("V3 Server running on http://localhost:5003")
    app.run(port=5003, debug=True)
