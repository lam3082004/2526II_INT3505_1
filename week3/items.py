from flask import Blueprint, jsonify, request

try:
    from .auth import require_jwt
except ImportError:
    from auth import require_jwt

items_bp = Blueprint("items", __name__, url_prefix="/items")

ITEMS = [
    {"id": 1, "name": "Sample Item", "price": 9.99},
]


def find_item(item_id):
    return next((item for item in ITEMS if item["id"] == item_id), None)


def next_item_id():
    return max((item["id"] for item in ITEMS), default=0) + 1


@items_bp.route("", methods=["GET"])
@require_jwt
def get_items():
    """
    Get all items
    ---
    tags:
      - Items
    security:
      - BearerAuth: []
    responses:
      200:
        description: List of items
      401:
        description: Missing or invalid token
    """
    return jsonify(ITEMS), 200


@items_bp.route("", methods=["POST"])
@require_jwt
def create_item():
    """
    Create a new item
    ---
    tags:
      - Items
    security:
      - BearerAuth: []
    consumes:
      - application/json
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - name
            - price
          properties:
            name:
              type: string
              example: Keyboard
            price:
              type: number
              example: 29.99
    responses:
      201:
        description: Item created
      400:
        description: Invalid payload
      401:
        description: Missing or invalid token
    """
    data = request.get_json(silent=True) or {}
    if "name" not in data or "price" not in data:
        return jsonify({"error": "Missing name or price"}), 400

    new_item = {
        "id": next_item_id(),
        "name": data["name"],
        "price": data["price"],
    }
    ITEMS.append(new_item)
    return jsonify(new_item), 201


@items_bp.route("/<int:item_id>", methods=["GET"])
@require_jwt
def get_item(item_id):
    """
    Get item by ID
    ---
    tags:
      - Items
    security:
      - BearerAuth: []
    parameters:
      - in: path
        name: item_id
        type: integer
        required: true
    responses:
      200:
        description: Item detail
      401:
        description: Missing or invalid token
      404:
        description: Item not found
    """
    item = find_item(item_id)
    if not item:
        return jsonify({"error": "Item not found"}), 404
    return jsonify(item), 200


@items_bp.route("/<int:item_id>", methods=["PUT"])
@require_jwt
def update_item(item_id):
    """
    Update item by ID
    ---
    tags:
      - Items
    security:
      - BearerAuth: []
    consumes:
      - application/json
    parameters:
      - in: path
        name: item_id
        type: integer
        required: true
      - in: body
        name: body
        required: true
        schema:
          type: object
          properties:
            name:
              type: string
            price:
              type: number
    responses:
      200:
        description: Updated item
      400:
        description: Empty payload
      401:
        description: Missing or invalid token
      404:
        description: Item not found
    """
    item = find_item(item_id)
    if not item:
        return jsonify({"error": "Item not found"}), 404

    data = request.get_json(silent=True) or {}
    if not data:
        return jsonify({"error": "No data provided"}), 400

    if "name" in data:
        item["name"] = data["name"]
    if "price" in data:
        item["price"] = data["price"]

    return jsonify(item), 200


@items_bp.route("/<int:item_id>", methods=["DELETE"])
@require_jwt
def delete_item(item_id):
    """
    Delete item by ID
    ---
    tags:
      - Items
    security:
      - BearerAuth: []
    parameters:
      - in: path
        name: item_id
        type: integer
        required: true
    responses:
      204:
        description: Item deleted
      401:
        description: Missing or invalid token
      404:
        description: Item not found
    """
    item = find_item(item_id)
    if not item:
        return jsonify({"error": "Item not found"}), 404

    ITEMS.remove(item)
    return "", 204
