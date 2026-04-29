from __future__ import annotations

from flask import Blueprint, jsonify, request

try:
    from ..auth.jwt_auth import require_jwt
    from ..controllers.product_controller import (
        create_product,
        delete_product,
        get_product,
        list_products,
        update_product,
    )
except ImportError:
    from auth.jwt_auth import require_jwt
    from controllers.product_controller import (
        create_product,
        delete_product,
        get_product,
        list_products,
        update_product,
    )


product_bp = Blueprint("product", __name__)


@product_bp.get("/products")
def list_products_endpoint():
    return jsonify(list_products()), 200


@product_bp.post("/products")
@require_jwt
def create_product_endpoint():
    payload = request.get_json(silent=True) or {}
    product, error, status_code = create_product(payload)
    if error:
        return jsonify({"error": error}), status_code
    return jsonify(product), status_code


@product_bp.get("/products/<string:product_id>")
def get_product_endpoint(product_id: str):
    product, error, status_code = get_product(product_id)
    if error:
        return jsonify({"error": error}), status_code
    return jsonify(product), status_code


@product_bp.put("/products/<string:product_id>")
@require_jwt
def update_product_endpoint(product_id: str):
    payload = request.get_json(silent=True) or {}
    product, error, status_code = update_product(product_id, payload)
    if error:
        return jsonify({"error": error}), status_code
    return jsonify(product), status_code


@product_bp.delete("/products/<string:product_id>")
@require_jwt
def delete_product_endpoint(product_id: str):
    error, status_code = delete_product(product_id)
    if error:
        return jsonify({"error": error}), status_code
    return "", status_code

