from __future__ import annotations

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
