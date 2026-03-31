from __future__ import annotations

import base64
import os
from datetime import date
from typing import Any

from flask import Flask, jsonify, request
from flasgger import Swagger

app = Flask(__name__)

swagger_template = {
    "swagger": "2.0",
    "info": {
        "title": "Week5 Library Management API",
        "description": "Resource modeling + search + pagination strategies (offset/page/cursor)",
        "version": "1.0.0",
    },
    "basePath": "/",
    "schemes": ["http"],
}

Swagger(app, template=swagger_template)

AUTHORS = [
    {"id": 1, "name": "Robert C. Martin"},
    {"id": 2, "name": "Martin Fowler"},
    {"id": 3, "name": "Eric Evans"},
    {"id": 4, "name": "Kent Beck"},
]

BOOKS = [
    {"id": 1, "title": "Clean Code", "author_id": 1, "category": "software", "year": 2008, "available": False},
    {"id": 2, "title": "Refactoring", "author_id": 2, "category": "software", "year": 1999, "available": True},
    {"id": 3, "title": "Domain-Driven Design", "author_id": 3, "category": "software", "year": 2003, "available": True},
    {"id": 4, "title": "Test-Driven Development", "author_id": 4, "category": "software", "year": 2002, "available": False},
    {"id": 5, "title": "Patterns of Enterprise Application Architecture", "author_id": 2, "category": "architecture", "year": 2002, "available": True},
    {"id": 6, "title": "The Clean Coder", "author_id": 1, "category": "software", "year": 2011, "available": True},
    {"id": 7, "title": "Refactoring UI", "author_id": 2, "category": "design", "year": 2018, "available": True},
    {"id": 8, "title": "Extreme Programming Explained", "author_id": 4, "category": "software", "year": 1999, "available": False},
]

MEMBERS = [
    {"id": 1, "name": "Alice", "email": "alice@example.com"},
    {"id": 2, "name": "Bob", "email": "bob@example.com"},
    {"id": 3, "name": "Carol", "email": "carol@example.com"},
]

LOANS = [
    {"id": 1, "book_id": 1, "member_id": 1, "borrowed_at": "2026-03-10", "returned_at": None},
    {"id": 2, "book_id": 4, "member_id": 2, "borrowed_at": "2026-03-15", "returned_at": None},
    {"id": 3, "book_id": 8, "member_id": 1, "borrowed_at": "2026-03-20", "returned_at": None},
]


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


@app.route("/", methods=["GET"])
def home() -> tuple[Any, int]:
    """
    API home
    ---
    tags:
      - Meta
    responses:
      200:
        description: API info
    """
    return jsonify({"message": "Week5 API is running", "docs": "/apidocs/"}), 200


@app.route("/health", methods=["GET"])
def health() -> tuple[Any, int]:
    """
    Health check
    ---
    tags:
      - Meta
    responses:
      200:
        description: Service health
    """
    return jsonify({"status": "ok", "date": date.today().isoformat()}), 200


@app.route("/books", methods=["GET"])
def list_books() -> tuple[Any, int]:
    """
    Get books with pagination
    ---
    tags:
      - Books
    parameters:
      - in: query
        name: pagination
        required: false
        type: string
        enum: [offset, page, cursor]
        default: offset
      - in: query
        name: offset
        required: false
        type: integer
      - in: query
        name: limit
        required: false
        type: integer
      - in: query
        name: page
        required: false
        type: integer
      - in: query
        name: page_size
        required: false
        type: integer
      - in: query
        name: cursor
        required: false
        type: string
    responses:
      200:
        description: Paginated books
      400:
        description: Invalid pagination parameters
    """
    try:
        strategy = request.args.get("pagination", "offset").strip().lower()
        data = [enrich_book(book) for book in BOOKS]

        if strategy == "offset":
            offset = parse_positive_int("offset", default_value=0, minimum=0)
            limit = parse_positive_int("limit", default_value=5, minimum=1)
            return jsonify(offset_paginate(data, offset, limit)), 200

        if strategy == "page":
            page = parse_positive_int("page", default_value=1, minimum=1)
            page_size = parse_positive_int("page_size", default_value=5, minimum=1)
            return jsonify(page_paginate(data, page, page_size)), 200

        if strategy == "cursor":
            cursor = request.args.get("cursor")
            limit = parse_positive_int("limit", default_value=5, minimum=1)
            return jsonify(cursor_paginate(data, cursor, limit)), 200

        return jsonify({"error": "pagination must be offset, page, or cursor"}), 400
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 400


@app.route("/books/search", methods=["GET"])
def search_books() -> tuple[Any, int]:
    """
    Search books by text/filter with pagination
    ---
    tags:
      - Books
    parameters:
      - in: query
        name: q
        required: false
        type: string
      - in: query
        name: category
        required: false
        type: string
      - in: query
        name: available
        required: false
        type: string
      - in: query
        name: pagination
        required: false
        type: string
        enum: [offset, page, cursor]
        default: offset
      - in: query
        name: offset
        required: false
        type: integer
      - in: query
        name: limit
        required: false
        type: integer
      - in: query
        name: page
        required: false
        type: integer
      - in: query
        name: page_size
        required: false
        type: integer
      - in: query
        name: cursor
        required: false
        type: string
    responses:
      200:
        description: Search result
      400:
        description: Invalid query parameter
    """
    try:
        query_text = request.args.get("q", "").strip().lower()
        category = request.args.get("category", "").strip().lower()
        available = parse_bool("available")

        filtered = []
        for book in BOOKS:
            row = enrich_book(book)

            if query_text and query_text not in row["title"].lower() and query_text not in (row["author"] or "").lower():
                continue
            if category and row["category"].lower() != category:
                continue
            if available is not None and row["available"] is not available:
                continue

            filtered.append(row)

        strategy = request.args.get("pagination", "offset").strip().lower()

        if strategy == "offset":
            offset = parse_positive_int("offset", default_value=0, minimum=0)
            limit = parse_positive_int("limit", default_value=5, minimum=1)
            payload = offset_paginate(filtered, offset, limit)
        elif strategy == "page":
            page = parse_positive_int("page", default_value=1, minimum=1)
            page_size = parse_positive_int("page_size", default_value=5, minimum=1)
            payload = page_paginate(filtered, page, page_size)
        elif strategy == "cursor":
            cursor = request.args.get("cursor")
            limit = parse_positive_int("limit", default_value=5, minimum=1)
            payload = cursor_paginate(filtered, cursor, limit)
        else:
            return jsonify({"error": "pagination must be offset, page, or cursor"}), 400

        payload["filters"] = {
            "q": query_text or None,
            "category": category or None,
            "available": available,
        }
        return jsonify(payload), 200
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 400


@app.route("/books/<int:book_id>", methods=["GET"])
def get_book(book_id: int) -> tuple[Any, int]:
    """
    Get a book by id
    ---
    tags:
      - Books
    parameters:
      - in: path
        name: book_id
        required: true
        type: integer
    responses:
      200:
        description: Book detail
      404:
        description: Book not found
    """
    book = find_by_id(BOOKS, book_id)
    if not book:
        return jsonify({"error": "Book not found"}), 404
    return jsonify(enrich_book(book)), 200


@app.route("/members", methods=["GET"])
def list_members() -> tuple[Any, int]:
    """
    Get all members
    ---
    tags:
      - Members
    responses:
      200:
        description: Member list
    """
    return jsonify(MEMBERS), 200


@app.route("/members/<int:member_id>", methods=["GET"])
def get_member(member_id: int) -> tuple[Any, int]:
    """
    Get member by id
    ---
    tags:
      - Members
    parameters:
      - in: path
        name: member_id
        required: true
        type: integer
    responses:
      200:
        description: Member detail
      404:
        description: Member not found
    """
    member = find_by_id(MEMBERS, member_id)
    if not member:
        return jsonify({"error": "Member not found"}), 404
    return jsonify(member), 200


@app.route("/members/<int:member_id>/loans", methods=["GET"])
def member_loans(member_id: int) -> tuple[Any, int]:
    """
    Get one member's loans (resource tree)
    ---
    tags:
      - Members
      - Loans
    parameters:
      - in: path
        name: member_id
        required: true
        type: integer
    responses:
      200:
        description: Loans of member
      404:
        description: Member not found
    """
    member = find_by_id(MEMBERS, member_id)
    if not member:
        return jsonify({"error": "Member not found"}), 404

    loans = [loan for loan in LOANS if loan["member_id"] == member_id]
    response = []
    for loan in loans:
        book = find_by_id(BOOKS, loan["book_id"])
        item = dict(loan)
        item["book"] = enrich_book(book) if book else None
        response.append(item)

    return jsonify({"member": member, "loans": response}), 200


@app.route("/loans/<int:loan_id>", methods=["GET"])
def get_loan(loan_id: int) -> tuple[Any, int]:
    """
    Get loan by id
    ---
    tags:
      - Loans
    parameters:
      - in: path
        name: loan_id
        required: true
        type: integer
    responses:
      200:
        description: Loan detail
      404:
        description: Loan not found
    """
    loan = find_by_id(LOANS, loan_id)
    if not loan:
        return jsonify({"error": "Loan not found"}), 404

    member = find_by_id(MEMBERS, loan["member_id"])
    book = find_by_id(BOOKS, loan["book_id"])

    payload = dict(loan)
    payload["member"] = member
    payload["book"] = enrich_book(book) if book else None
    return jsonify(payload), 200


if __name__ == "__main__":
    port = int(os.getenv("PORT", "5008"))
    debug = os.getenv("FLASK_DEBUG", "0") == "1"
    print(f"Week5 API running at http://127.0.0.1:{port}/apidocs/")
    app.run(port=port, debug=debug)
