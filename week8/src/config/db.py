from __future__ import annotations

from pymongo import MongoClient

_client: MongoClient | None = None
_database_name: str | None = None


def connect_db(mongodb_uri: str | None, database_name: str) -> None:
    global _client, _database_name

    if not mongodb_uri:
        raise ValueError("MONGODB_URI is required")

    if not database_name:
        raise ValueError("MONGODB_DB_NAME is required")

    _client = MongoClient(mongodb_uri)
    _database_name = database_name


def get_products_collection():
    if _client is None or _database_name is None:
        raise RuntimeError("Database is not connected")

    return _client[_database_name]["products"]

