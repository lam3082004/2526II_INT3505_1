from __future__ import annotations


OPENAPI_SPEC = {
    "openapi": "3.0.3",
    "info": {
        "title": "Week11-12 API Design Patterns",
        "version": "1.0.0",
        "description": (
            "Demo API combining CRUD, Query, HATEOAS, Event-driven, "
            "and Webhook patterns."
        ),
    },
    "servers": [{"url": "http://127.0.0.1:5013"}],
    "tags": [
        {"name": "Root", "description": "Service discovery"},
        {"name": "Products", "description": "CRUD, query, pagination, HATEOAS"},
        {"name": "Notifications", "description": "Notification resources"},
        {"name": "Orders", "description": "Order events"},
        {"name": "Events", "description": "In-memory event log"},
        {"name": "Webhooks", "description": "Webhook subscriptions and deliveries"},
    ],
    "paths": {
        "/": {
            "get": {
                "tags": ["Root"],
                "summary": "Get service metadata and HATEOAS links",
                "responses": {
                    "200": {
                        "description": "Service metadata",
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/RootResponse"}
                            }
                        },
                    }
                },
            }
        },
        "/api/products": {
            "post": {
                "tags": ["Products"],
                "summary": "Create a product",
                "requestBody": {
                    "required": True,
                    "content": {
                        "application/json": {
                            "schema": {"$ref": "#/components/schemas/ProductInput"},
                            "example": {
                                "name": "Python API Patterns",
                                "category": "book",
                                "price": 35,
                            },
                        }
                    },
                },
                "responses": {
                    "201": {
                        "description": "Product created",
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/Product"}
                            }
                        },
                    },
                    "400": {"$ref": "#/components/responses/BadRequest"},
                },
            },
            "get": {
                "tags": ["Products"],
                "summary": "List products with query pattern",
                "parameters": [
                    {
                        "name": "category",
                        "in": "query",
                        "schema": {"type": "string"},
                        "example": "book",
                    },
                    {
                        "name": "search",
                        "in": "query",
                        "schema": {"type": "string"},
                        "example": "python",
                    },
                    {
                        "name": "min_price",
                        "in": "query",
                        "schema": {"type": "number"},
                        "example": 10,
                    },
                    {
                        "name": "max_price",
                        "in": "query",
                        "schema": {"type": "number"},
                        "example": 50,
                    },
                    {
                        "name": "sort",
                        "in": "query",
                        "schema": {
                            "type": "string",
                            "enum": [
                                "name",
                                "-name",
                                "price",
                                "-price",
                                "created_at",
                                "-created_at",
                                "updated_at",
                                "-updated_at",
                            ],
                            "default": "-created_at",
                        },
                    },
                    {
                        "name": "page",
                        "in": "query",
                        "schema": {"type": "integer", "minimum": 1, "default": 1},
                    },
                    {
                        "name": "limit",
                        "in": "query",
                        "schema": {
                            "type": "integer",
                            "minimum": 1,
                            "maximum": 100,
                            "default": 10,
                        },
                    },
                ],
                "responses": {
                    "200": {
                        "description": "Paged products",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/ProductListResponse"
                                }
                            }
                        },
                    }
                },
            },
        },
        "/api/products/{product_id}": {
            "get": {
                "tags": ["Products"],
                "summary": "Get a product",
                "parameters": [{"$ref": "#/components/parameters/ProductId"}],
                "responses": {
                    "200": {
                        "description": "Product found",
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/Product"}
                            }
                        },
                    },
                    "404": {"$ref": "#/components/responses/NotFound"},
                },
            },
            "put": {
                "tags": ["Products"],
                "summary": "Update a product",
                "parameters": [{"$ref": "#/components/parameters/ProductId"}],
                "requestBody": {
                    "required": True,
                    "content": {
                        "application/json": {
                            "schema": {"$ref": "#/components/schemas/ProductInput"}
                        }
                    },
                },
                "responses": {
                    "200": {
                        "description": "Product updated",
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/Product"}
                            }
                        },
                    },
                    "404": {"$ref": "#/components/responses/NotFound"},
                },
            },
            "delete": {
                "tags": ["Products"],
                "summary": "Delete a product",
                "parameters": [{"$ref": "#/components/parameters/ProductId"}],
                "responses": {
                    "204": {"description": "Product deleted"},
                    "404": {"$ref": "#/components/responses/NotFound"},
                },
            },
        },
        "/api/notifications": {
            "post": {
                "tags": ["Notifications"],
                "summary": "Create notification and publish notification.created",
                "requestBody": {
                    "required": True,
                    "content": {
                        "application/json": {
                            "schema": {
                                "$ref": "#/components/schemas/NotificationInput"
                            },
                            "example": {
                                "message": "Order paid",
                                "recipient": "user_01",
                                "channel": "email",
                            },
                        }
                    },
                },
                "responses": {
                    "201": {
                        "description": "Notification created",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/Notification"
                                }
                            }
                        },
                    },
                    "400": {"$ref": "#/components/responses/BadRequest"},
                },
            },
            "get": {
                "tags": ["Notifications"],
                "summary": "List notifications",
                "responses": {
                    "200": {
                        "description": "Notifications",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "properties": {
                                        "data": {
                                            "type": "array",
                                            "items": {
                                                "$ref": "#/components/schemas/Notification"
                                            },
                                        }
                                    },
                                }
                            }
                        },
                    }
                },
            },
        },
        "/api/notifications/{notification_id}": {
            "get": {
                "tags": ["Notifications"],
                "summary": "Get a notification",
                "parameters": [{"$ref": "#/components/parameters/NotificationId"}],
                "responses": {
                    "200": {
                        "description": "Notification found",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/Notification"
                                }
                            }
                        },
                    },
                    "404": {"$ref": "#/components/responses/NotFound"},
                },
            }
        },
        "/api/orders": {
            "post": {
                "tags": ["Orders"],
                "summary": "Create order and publish order.created",
                "requestBody": {
                    "required": True,
                    "content": {
                        "application/json": {
                            "schema": {"$ref": "#/components/schemas/OrderInput"},
                            "example": {"customer_id": "user_01", "amount": 99.5},
                        }
                    },
                },
                "responses": {
                    "201": {
                        "description": "Order created",
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/Order"}
                            }
                        },
                    },
                    "400": {"$ref": "#/components/responses/BadRequest"},
                },
            }
        },
        "/api/events": {
            "get": {
                "tags": ["Events"],
                "summary": "List published events",
                "responses": {
                    "200": {
                        "description": "Event log",
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/EventList"}
                            }
                        },
                    }
                },
            }
        },
        "/api/webhooks/subscriptions": {
            "post": {
                "tags": ["Webhooks"],
                "summary": "Register a webhook subscription",
                "requestBody": {
                    "required": True,
                    "content": {
                        "application/json": {
                            "schema": {
                                "$ref": "#/components/schemas/WebhookSubscriptionInput"
                            },
                            "example": {
                                "url": "https://webhook.site/YOUR_ID",
                                "events": ["notification.created", "order.created"],
                                "secret": "demo-secret",
                            },
                        }
                    },
                },
                "responses": {
                    "201": {
                        "description": "Webhook subscription created",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/WebhookSubscription"
                                }
                            }
                        },
                    },
                    "400": {"$ref": "#/components/responses/BadRequest"},
                },
            },
            "get": {
                "tags": ["Webhooks"],
                "summary": "List webhook subscriptions",
                "responses": {
                    "200": {
                        "description": "Webhook subscriptions",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "properties": {
                                        "data": {
                                            "type": "array",
                                            "items": {
                                                "$ref": (
                                                    "#/components/schemas/"
                                                    "WebhookSubscription"
                                                )
                                            },
                                        }
                                    },
                                }
                            }
                        },
                    }
                },
            },
        },
        "/api/webhooks/subscriptions/{subscription_id}": {
            "delete": {
                "tags": ["Webhooks"],
                "summary": "Delete a webhook subscription",
                "parameters": [{"$ref": "#/components/parameters/SubscriptionId"}],
                "responses": {
                    "204": {"description": "Webhook subscription deleted"},
                    "404": {"$ref": "#/components/responses/NotFound"},
                },
            }
        },
        "/api/webhooks/deliveries": {
            "get": {
                "tags": ["Webhooks"],
                "summary": "List webhook delivery attempts",
                "responses": {
                    "200": {
                        "description": "Webhook delivery log",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/WebhookDeliveryList"
                                }
                            }
                        },
                    }
                },
            }
        },
    },
    "components": {
        "parameters": {
            "ProductId": {
                "name": "product_id",
                "in": "path",
                "required": True,
                "schema": {"type": "string", "format": "uuid"},
            },
            "NotificationId": {
                "name": "notification_id",
                "in": "path",
                "required": True,
                "schema": {"type": "string", "format": "uuid"},
            },
            "SubscriptionId": {
                "name": "subscription_id",
                "in": "path",
                "required": True,
                "schema": {"type": "string", "format": "uuid"},
            },
        },
        "responses": {
            "BadRequest": {
                "description": "Invalid request",
                "content": {
                    "application/json": {
                        "schema": {"$ref": "#/components/schemas/Error"}
                    }
                },
            },
            "NotFound": {
                "description": "Resource not found",
                "content": {
                    "application/json": {
                        "schema": {"$ref": "#/components/schemas/Error"}
                    }
                },
            },
        },
        "schemas": {
            "Error": {
                "type": "object",
                "properties": {"error": {"type": "string"}},
            },
            "Link": {
                "type": "object",
                "properties": {
                    "href": {"type": "string"},
                    "method": {"type": "string"},
                },
            },
            "Links": {
                "type": "object",
                "additionalProperties": {"$ref": "#/components/schemas/Link"},
            },
            "RootResponse": {
                "type": "object",
                "properties": {
                    "service": {"type": "string"},
                    "patterns": {"type": "array", "items": {"type": "string"}},
                    "_links": {"$ref": "#/components/schemas/Links"},
                },
            },
            "ProductInput": {
                "type": "object",
                "required": ["name", "category", "price"],
                "properties": {
                    "name": {"type": "string"},
                    "category": {"type": "string"},
                    "price": {"type": "number"},
                },
            },
            "Product": {
                "allOf": [
                    {"$ref": "#/components/schemas/ProductInput"},
                    {
                        "type": "object",
                        "properties": {
                            "id": {"type": "string", "format": "uuid"},
                            "created_at": {"type": "string", "format": "date-time"},
                            "updated_at": {"type": "string", "format": "date-time"},
                            "_links": {"$ref": "#/components/schemas/Links"},
                        },
                    },
                ],
            },
            "Pagination": {
                "type": "object",
                "properties": {
                    "page": {"type": "integer"},
                    "limit": {"type": "integer"},
                    "total_items": {"type": "integer"},
                    "total_pages": {"type": "integer"},
                },
            },
            "ProductListResponse": {
                "type": "object",
                "properties": {
                    "data": {
                        "type": "array",
                        "items": {"$ref": "#/components/schemas/Product"},
                    },
                    "pagination": {"$ref": "#/components/schemas/Pagination"},
                    "_links": {"$ref": "#/components/schemas/Links"},
                },
            },
            "NotificationInput": {
                "type": "object",
                "required": ["message", "recipient"],
                "properties": {
                    "message": {"type": "string"},
                    "recipient": {"type": "string"},
                    "channel": {"type": "string", "default": "email"},
                },
            },
            "Notification": {
                "allOf": [
                    {"$ref": "#/components/schemas/NotificationInput"},
                    {
                        "type": "object",
                        "properties": {
                            "id": {"type": "string", "format": "uuid"},
                            "status": {"type": "string", "example": "queued"},
                            "created_at": {"type": "string", "format": "date-time"},
                            "_links": {"$ref": "#/components/schemas/Links"},
                        },
                    },
                ],
            },
            "OrderInput": {
                "type": "object",
                "required": ["customer_id", "amount"],
                "properties": {
                    "customer_id": {"type": "string"},
                    "amount": {"type": "number"},
                },
            },
            "Order": {
                "allOf": [
                    {"$ref": "#/components/schemas/OrderInput"},
                    {
                        "type": "object",
                        "properties": {
                            "id": {"type": "string", "format": "uuid"},
                            "status": {"type": "string", "example": "created"},
                            "created_at": {"type": "string", "format": "date-time"},
                        },
                    },
                ],
            },
            "Event": {
                "type": "object",
                "properties": {
                    "type": {"type": "string", "example": "notification.created"},
                    "timestamp": {"type": "string", "format": "date-time"},
                    "data": {"type": "object", "additionalProperties": True},
                },
            },
            "EventList": {
                "type": "object",
                "properties": {
                    "data": {
                        "type": "array",
                        "items": {"$ref": "#/components/schemas/Event"},
                    },
                    "count": {"type": "integer"},
                },
            },
            "WebhookSubscriptionInput": {
                "type": "object",
                "required": ["url", "events", "secret"],
                "properties": {
                    "url": {"type": "string", "format": "uri"},
                    "events": {
                        "type": "array",
                        "items": {"type": "string"},
                        "example": ["notification.created", "order.created"],
                    },
                    "secret": {"type": "string"},
                },
            },
            "WebhookSubscription": {
                "allOf": [
                    {"$ref": "#/components/schemas/WebhookSubscriptionInput"},
                    {
                        "type": "object",
                        "properties": {
                            "id": {"type": "string", "format": "uuid"},
                            "created_at": {"type": "string", "format": "date-time"},
                        },
                    },
                ],
            },
            "WebhookDelivery": {
                "type": "object",
                "properties": {
                    "subscription_id": {"type": "string", "format": "uuid"},
                    "target_url": {"type": "string", "format": "uri"},
                    "event": {"type": "string"},
                    "delivered_at": {"type": "string", "format": "date-time"},
                    "status": {"type": "string", "enum": ["success", "failed"]},
                    "http_status": {"type": "integer"},
                    "error": {"type": "string"},
                },
            },
            "WebhookDeliveryList": {
                "type": "object",
                "properties": {
                    "data": {
                        "type": "array",
                        "items": {"$ref": "#/components/schemas/WebhookDelivery"},
                    },
                    "count": {"type": "integer"},
                },
            },
        },
    },
}
