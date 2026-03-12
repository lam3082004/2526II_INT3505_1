from flask import Flask, request, jsonify

app = Flask(__name__)

users = [
    {"id": 1, "name": "Alice", "email": "alice@example.com"},
    {"id": 2, "name": "Bob",   "email": "bob@example.com"},
    {"id": 3, "name": "Carol", "email": "carol@example.com"},
]
posts = [
    {"id": 1, "user_id": 1, "title": "Hello World", "body": "My first post"},
    {"id": 2, "user_id": 2, "title": "Flask Tips",  "body": "Use blueprints!"},
]

@app.route("/action", methods=["POST"])
def action():
    data = request.json
    act = data.get("action")

    if act == "get_users":
        return jsonify(users)

    elif act == "get_user":
        uid = data.get("id")
        for u in users:
            if u["id"] == uid:
                return jsonify(u)
        return jsonify({"msg": "not found"})

    elif act == "create_user":
        new = {"id": len(users) + 1, "name": data["name"], "email": data["email"]}
        users.append(new)
        return jsonify({"msg": "ok", "user": new})

    elif act == "update_email":
        uid = data.get("id")
        for u in users:
            if u["id"] == uid:
                u["email"] = data["email"]
                return jsonify({"msg": "ok"})
        return jsonify({"msg": "not found"})

    elif act == "delete_user":
        uid = data.get("id")
        for i, u in enumerate(users):
            if u["id"] == uid:
                users.pop(i)
                return jsonify({"msg": "deleted"})
        return jsonify({"msg": "not found"})

    return jsonify({"msg": "unknown action"})


if __name__ == "__main__":
    print("V1 Server running on http://localhost:5001")
    app.run(port=5001, debug=True)
