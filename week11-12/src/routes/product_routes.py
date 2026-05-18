from __future__ import annotations

from datetime import datetime, timezone
from uuid import uuid4

from flask import Blueprint, jsonify, request

try:
    from ..storage import PRODUCTS
    from ..utils.hateoas import pagination_links, product_links
except ImportError:
    from storage import PRODUCTS
    from utils.hateoas import pagination_links, product_links


product_bp = Blueprint("products", __name__, url_prefix="/api/products")


@product_bp.post("")
def create_product():
    payload = request.get_json(silent=True) or {}
    name = (payload.get("name") or "").strip()
    category = (payload.get("category") or "").strip()
    price = payload.get("price")

    if not name or not category or not isinstance(price, (int, float)):
        return jsonify({"error": "name, category, price are required"}), 400

    product_id = str(uuid4())
    product = {
        "id": product_id,
        "name": name,
        "category": category,
        "price": float(price),
        "created_at": datetime.now(timezone.utc).isoformat(),
        "updated_at": datetime.now(timezone.utc).isoformat(),
    }
    PRODUCTS[product_id] = product

    response = {**product, "_links": product_links(product_id)}
    return jsonify(response), 201


@product_bp.get("")
def list_products():
    category = request.args.get("category")
    search = request.args.get("search")
    min_price = request.args.get("min_price", type=float)
    max_price = request.args.get("max_price", type=float)
    sort = request.args.get("sort", "-created_at")
    page = max(request.args.get("page", 1, type=int), 1)
    limit = min(max(request.args.get("limit", 10, type=int), 1), 100)

    items = list(PRODUCTS.values())

    if category:
        items = [x for x in items if x["category"].lower() == category.lower()]
    if search:
        lowered = search.lower()
        items = [x for x in items if lowered in x["name"].lower()]
    if min_price is not None:
        items = [x for x in items if x["price"] >= min_price]
    if max_price is not None:
        items = [x for x in items if x["price"] <= max_price]

    reverse = sort.startswith("-")
    sort_field = sort[1:] if reverse else sort
    if sort_field in {"name", "price", "created_at", "updated_at"}:
        items.sort(key=lambda x: x[sort_field], reverse=reverse)

    total = len(items)
    start = (page - 1) * limit
    end = start + limit
    paged_items = items[start:end]

    data = [{**x, "_links": product_links(x["id"])} for x in paged_items]
    return (
        jsonify(
            {
                "data": data,
                "pagination": {
                    "page": page,
                    "limit": limit,
                    "total_items": total,
                    "total_pages": max((total + limit - 1) // limit, 1),
                },
                "_links": pagination_links("/api/products", page, limit, total),
            }
        ),
        200,
    )


@product_bp.get("/<string:product_id>")
def get_product(product_id: str):
    product = PRODUCTS.get(product_id)
    if not product:
        return jsonify({"error": "Product not found"}), 404
    return jsonify({**product, "_links": product_links(product_id)}), 200


@product_bp.put("/<string:product_id>")
def update_product(product_id: str):
    product = PRODUCTS.get(product_id)
    if not product:
        return jsonify({"error": "Product not found"}), 404

    payload = request.get_json(silent=True) or {}
    if "name" in payload and isinstance(payload["name"], str):
        product["name"] = payload["name"].strip() or product["name"]
    if "category" in payload and isinstance(payload["category"], str):
        product["category"] = payload["category"].strip() or product["category"]
    if "price" in payload and isinstance(payload["price"], (int, float)):
        product["price"] = float(payload["price"])
    product["updated_at"] = datetime.now(timezone.utc).isoformat()

    return jsonify({**product, "_links": product_links(product_id)}), 200


@product_bp.delete("/<string:product_id>")
def delete_product(product_id: str):
    if product_id not in PRODUCTS:
        return jsonify({"error": "Product not found"}), 404
    del PRODUCTS[product_id]
    return "", 204
