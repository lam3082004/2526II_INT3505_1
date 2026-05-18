from __future__ import annotations


def product_links(product_id: str) -> dict:
    return {
        "self": {"href": f"/api/products/{product_id}", "method": "GET"},
        "update": {"href": f"/api/products/{product_id}", "method": "PUT"},
        "delete": {"href": f"/api/products/{product_id}", "method": "DELETE"},
        "collection": {"href": "/api/products", "method": "GET"},
    }


def notification_links(notification_id: str) -> dict:
    return {
        "self": {"href": f"/api/notifications/{notification_id}", "method": "GET"},
        "collection": {"href": "/api/notifications", "method": "GET"},
    }


def pagination_links(base_path: str, page: int, limit: int, total_items: int) -> dict:
    total_pages = max((total_items + limit - 1) // limit, 1)
    links = {
        "self": {"href": f"{base_path}?page={page}&limit={limit}", "method": "GET"},
        "first": {"href": f"{base_path}?page=1&limit={limit}", "method": "GET"},
        "last": {"href": f"{base_path}?page={total_pages}&limit={limit}", "method": "GET"},
    }
    if page > 1:
        links["prev"] = {
            "href": f"{base_path}?page={page - 1}&limit={limit}",
            "method": "GET",
        }
    if page < total_pages:
        links["next"] = {
            "href": f"{base_path}?page={page + 1}&limit={limit}",
            "method": "GET",
        }
    return links
