import requests, json

BASE   = "http://localhost:5004"
TOKEN  = "secret-token-alice"
HEADERS = {"Authorization": f"Bearer {TOKEN}"}

etag_store: dict[str, str] = {}

def show(label, r):
    print(f"\n{'='*50}")
    print(f"  {label}")
    print(f"  {r.request.method} {r.request.url}")
    print(f"  Status : {r.status_code}")
    if r.headers.get("ETag"):
        print(f"  ETag   : {r.headers['ETag']}")
    if r.headers.get("Cache-Control"):
        print(f"  Cache  : {r.headers['Cache-Control']}")
    if r.status_code == 304:
        print("  → 304 Not Modified: dùng bản cache, server không gửi body!")
    elif r.text:
        print(json.dumps(r.json(), indent=2, ensure_ascii=False))

def get_with_cache(url, label):
    hdrs = dict(HEADERS)
    if url in etag_store:
        hdrs["If-None-Match"] = etag_store[url]
        print(f"\n  [Cache] Gửi If-None-Match: {etag_store[url][:12]}...")

    r = requests.get(url, headers=hdrs)
    show(label, r)

    if r.status_code == 200 and r.headers.get("ETag"):
        etag_store[url] = r.headers["ETag"]
    return r

if __name__ == "__main__":
    url_users = f"{BASE}/users"

    print("\n" + "━"*50)
    print("  DEMO 1: Lần đầu GET → nhận data + ETag")
    get_with_cache(url_users, "GET /users (lần 1)")

    print("\n" + "━"*50)
    print("  DEMO 2: GET lại ngay → 304 Not Modified")
    get_with_cache(url_users, "GET /users (lần 2, ETag match)")

    print("\n" + "━"*50)
    print("  DEMO 3: Tạo user mới")
    r = requests.post(url_users, json={"name": "Dave", "email": "dave@example.com"}, headers=HEADERS)
    show("POST create user", r)
    print(f"  Location: {r.headers.get('Location')}")

    print("\n" + "━"*50)
    print("  DEMO 4: GET lại sau POST → 200 (ETag đổi)")
    get_with_cache(url_users, "GET /users (lần 3, sau POST)")

    print("\n" + "━"*50)
    print("  DEMO 5: Cập nhật user id=2")
    r = requests.put(f"{BASE}/users/2", json={"email": "bob_v4@example.com"}, headers=HEADERS)
    show("PUT update user id=2", r)

    print("\n" + "━"*50)
    print("  DEMO 6: Xóa user id=3 → 204 No Content")
    r = requests.delete(f"{BASE}/users/3", headers=HEADERS)
    show("DELETE user id=3", r)

    print("\n" + "━"*50)
    print("  DEMO 7: Không có token → 401")
    r = requests.get(url_users)
    show("GET /users (no token)", r)

    print("\n" + "━"*50)
    print("  DEMO 8: User không tồn tại → 404")
    r = requests.get(f"{BASE}/users/999", headers=HEADERS)
    show("GET /users/999", r)
