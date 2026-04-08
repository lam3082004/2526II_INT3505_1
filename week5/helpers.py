from __future__ import annotations

import base64
from typing import Any

from flask import request

try:
    from .data import AUTHORS
except ImportError:
    from data import AUTHORS


def find_by_id(rows: list[dict[str, Any]], item_id: int) -> dict[str, Any] | None:
    return next((row for row in rows if row["id"] == item_id), None)


def enrich_book(book: dict[str, Any]) -> dict[str, Any]:
    author = find_by_id(AUTHORS, book["author_id"])
    data = dict(book)
    data["author"] = author["name"] if author else None
    return data


def parse_positive_int(name: str, default_value: int, minimum: int = 1) -> int:
    raw_value = request.args.get(name, str(default_value))
    try:
        value = int(raw_value)
    except ValueError:
        raise ValueError(f"{name} must be an integer")
    if value < minimum:
        raise ValueError(f"{name} must be >= {minimum}")
    return value


def parse_bool(name: str) -> bool | None:
    raw_value = request.args.get(name)
    if raw_value is None:
        return None
    lowered = raw_value.strip().lower()
    if lowered in {"true", "1", "yes"}:
        return True
    if lowered in {"false", "0", "no"}:
        return False
    raise ValueError(f"{name} must be true/false")


def encode_cursor(book_id: int) -> str:
    return base64.urlsafe_b64encode(f"book:{book_id}".encode("utf-8")).decode("utf-8")


def decode_cursor(cursor: str) -> int:
    try:
        raw = base64.urlsafe_b64decode(cursor.encode("utf-8")).decode("utf-8")
        prefix, value = raw.split(":", 1)
        if prefix != "book":
            raise ValueError
        return int(value)
    except Exception as exc:
        raise ValueError("cursor is invalid") from exc


def offset_paginate(data: list[dict[str, Any]], offset: int, limit: int) -> dict[str, Any]:
    total = len(data)
    items = data[offset : offset + limit]
    return {
        "strategy": "offset",
        "offset": offset,
        "limit": limit,
        "total": total,
        "items": items,
    }


def page_paginate(data: list[dict[str, Any]], page: int, page_size: int) -> dict[str, Any]:
    total = len(data)
    start = (page - 1) * page_size
    end = start + page_size
    items = data[start:end]
    total_pages = (total + page_size - 1) // page_size
    return {
        "strategy": "page",
        "page": page,
        "page_size": page_size,
        "total": total,
        "total_pages": total_pages,
        "items": items,
    }


def cursor_paginate(data: list[dict[str, Any]], cursor: str | None, limit: int) -> dict[str, Any]:
    ordered = sorted(data, key=lambda x: x["id"])
    start_index = 0
    if cursor:
        last_id = decode_cursor(cursor)
        for idx, row in enumerate(ordered):
            if row["id"] > last_id:
                start_index = idx
                break
        else:
            start_index = len(ordered)

    items = ordered[start_index : start_index + limit]
    next_cursor = encode_cursor(items[-1]["id"]) if len(items) == limit and items else None

    return {
        "strategy": "cursor",
        "cursor": cursor,
        "limit": limit,
        "next_cursor": next_cursor,
        "items": items,
    }
