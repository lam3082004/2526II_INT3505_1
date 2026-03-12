from flask import Flask, request, jsonify

app = Flask(__name__)

users = [
    {"id": 1, "name": "Alice", "email": "alice@example.com"},
    {"id": 2, "name": "Bob",   "email": "bob@example.com"},
    {"id": 3, "name": "Carol", "email": "carol@example.com"},
]

fake_session = {"logged_in_user": "admin"}

def find_user(uid):
    return next((u for u in users if u["id"] == uid), None)

@app.route("/users", methods=["GET"])
def get_users():
    return jsonify(users), 200

@app.route("/users/<int:uid>", methods=["GET"])
def get_user(uid):
    u = find_user(uid)
    if not u:
        return jsonify({"error": "User not found"}), 404
    return jsonify(u), 200

@app.route("/users", methods=["POST"])
def create_user():
    data = request.json
    new = {"id": len(users) + 1, "name": data["name"], "email": data["email"]}
    users.append(new)
    return jsonify(new), 201

@app.route("/users/<int:uid>", methods=["PUT"])
def update_user(uid):
    u = find_user(uid)
    if not u:
        return jsonify({"error": "User not found"}), 404
    data = request.json
    if "email" in data:
        u["email"] = data["email"]
    if "name" in data:
        u["name"] = data["name"]
    return jsonify(u), 200

@app.route("/users/<int:uid>", methods=["DELETE"])
def delete_user(uid):
    u = find_user(uid)
    if not u:
        return jsonify({"error": "User not found"}), 404
    users.remove(u)
    return jsonify({"message": f"User {uid} deleted"}), 200


if __name__ == "__main__":
    print("V2 Server running on http://localhost:5002")
    app.run(port=5002, debug=True)
