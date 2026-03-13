import json

import requests

BASE = "http://localhost:5005"
ACTION_URL = f"{BASE}/action"
TOKEN = "secret-token-alice"
HEADERS = {"Authorization": f"Bearer {TOKEN}"}

etag_store: dict[str, str] = {}


def show(label, response):
    print(f"\n{'=' * 56}")
    print(f"  {label}")
    print(f"  {response.request.method} {response.request.url}")
    print(f"  Status : {response.status_code}")

    auth = response.request.headers.get("Authorization")
    if auth:
        print(f"  Auth   : {auth}")

    etag = response.headers.get("ETag")
    cache_control = response.headers.get("Cache-Control")
    location = response.headers.get("Location")

    if etag:
        print(f"  ETag   : {etag}")
    if cache_control:
        print(f"  Cache  : {cache_control}")
    if location:
        print(f"  Loc    : {location}")

    if response.status_code == 304:
        print("  → 304 Not Modified: dùng bản cache, server không gửi body")
        return

    if not response.text:
        return

    try:
        print(json.dumps(response.json(), indent=2, ensure_ascii=False))
    except ValueError:
        print(response.text)


def call_action(action, **kwargs):
    payload = {"action": action, **kwargs}
    response = requests.post(ACTION_URL, json=payload, timeout=10)
    show(f"[RPC] {action}", response)
    return response


def get_with_cache(path, label):
    url = f"{BASE}{path}"
    headers = dict(HEADERS)

    if url in etag_store:
        headers["If-None-Match"] = etag_store[url]
        print(f"\n  [Cache] Gửi If-None-Match: {etag_store[url][:12]}...")

    response = requests.get(url, headers=headers, timeout=10)
    show(label, response)

    if response.status_code == 200 and response.headers.get("ETag"):
        etag_store[url] = response.headers["ETag"]

    return response


def rest_call(method, path, label, use_auth=True, **kwargs):
    url = f"{BASE}{path}"
    headers = kwargs.pop("headers", {})

    if use_auth:
        merged_headers = {**HEADERS, **headers}
    else:
        merged_headers = headers

    response = requests.request(method, url, headers=merged_headers, timeout=10, **kwargs)
    show(label, response)
    return response


if __name__ == "__main__":
    print("\n" + "━" * 56)
    print("  DEMO A: Legacy RPC (/action) - từ V1")
    call_action("get_users")
    call_action("get_user", id=1)
    call_action("create_user", name="Dave", email="dave@example.com")
    call_action("update_email", id=2, email="bob_legacy@example.com")
    call_action("delete_user", id=3)

    print("\n" + "━" * 56)
    print("  DEMO B: REST + Auth + Cache (ETag) - từ V2/V3/V4")
    get_with_cache("/users", "GET /users (lần 1)")
    get_with_cache("/users", "GET /users (lần 2, ETag match)")

    rest_call("POST", "/users", "POST create user", json={"name": "Eve", "email": "eve@example.com"})
    get_with_cache("/users", "GET /users (sau POST, ETag đổi)")

    rest_call("PUT", "/users/2", "PUT update user id=2", json={"email": "bob_rest@example.com"})
    rest_call("DELETE", "/users/1", "DELETE user id=1")

    rest_call("GET", "/users", "GET /users (no token) → 401", use_auth=False)
    rest_call(
        "GET",
        "/users/2",
        "GET with INVALID token → 401",
        use_auth=False,
        headers={"Authorization": "Bearer fake-token"},
    )
    rest_call("GET", "/users/999", "GET /users/999 → 404")
