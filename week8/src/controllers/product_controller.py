from __future__ import annotations

from datetime import datetime, timezone

from bson import ObjectId
from pymongo import DESCENDING

try:
    from ..config.db import get_products_collection
    from ..models.product import normalize_product_payload, serialize_product
except ImportError:
    from config.db import get_products_collection
    from models.product import normalize_product_payload, serialize_product


def list_products():
    collection = get_products_collection()
    rows = collection.find().sort("createdAt", DESCENDING)
    return [serialize_product(row) for row in rows]


def create_product(payload: dict):
    clean_payload, error = normalize_product_payload(payload, partial=False)
    if error:
        return None, error, 400

    now = datetime.now(timezone.utc)
    clean_payload["createdAt"] = now
    clean_payload["updatedAt"] = now

    collection = get_products_collection()
    result = collection.insert_one(clean_payload)
    created = collection.find_one({"_id": result.inserted_id})

    return serialize_product(created), None, 201


def get_product(product_id: str):
    if not ObjectId.is_valid(product_id):
        return None, "Product not found", 404

    collection = get_products_collection()
    product = collection.find_one({"_id": ObjectId(product_id)})
    if product is None:
        return None, "Product not found", 404

    return serialize_product(product), None, 200


def update_product(product_id: str, payload: dict):
    if not ObjectId.is_valid(product_id):
        return None, "Product not found", 404

    clean_payload, error = normalize_product_payload(payload, partial=True)
    if error:
        return None, error, 400

    clean_payload["updatedAt"] = datetime.now(timezone.utc)

    collection = get_products_collection()
    result = collection.update_one(
        {"_id": ObjectId(product_id)},
        {"$set": clean_payload},
    )
    if result.matched_count == 0:
        return None, "Product not found", 404

    updated = collection.find_one({"_id": ObjectId(product_id)})
    return serialize_product(updated), None, 200


def delete_product(product_id: str):
    if not ObjectId.is_valid(product_id):
        return "Product not found", 404

    collection = get_products_collection()
    result = collection.delete_one({"_id": ObjectId(product_id)})
    if result.deleted_count == 0:
        return "Product not found", 404

    return None, 204

