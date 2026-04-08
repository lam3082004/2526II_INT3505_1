from __future__ import annotations

from datetime import date
from typing import Any

from flask import Blueprint, jsonify, request

try:
    from .data import BOOKS, LOANS, MEMBERS
    from .helpers import (
        cursor_paginate,
        enrich_book,
        find_by_id,
        offset_paginate,
        page_paginate,
        parse_bool,
        parse_positive_int,
    )
except ImportError:
    from data import BOOKS, LOANS, MEMBERS
    from helpers import (
        cursor_paginate,
        enrich_book,
        find_by_id,
        offset_paginate,
        page_paginate,
        parse_bool,
        parse_positive_int,
    )

api_bp = Blueprint("api", __name__)


@api_bp.route("/", methods=["GET"])
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


@api_bp.route("/health", methods=["GET"])
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


@api_bp.route("/books", methods=["GET"])
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


@api_bp.route("/books/search", methods=["GET"])
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


@api_bp.route("/books/<int:book_id>", methods=["GET"])
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


@api_bp.route("/members", methods=["GET"])
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


@api_bp.route("/members/<int:member_id>", methods=["GET"])
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


@api_bp.route("/members/<int:member_id>/loans", methods=["GET"])
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


@api_bp.route("/loans/<int:loan_id>", methods=["GET"])
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
