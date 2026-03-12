import requests, json

BASE = "http://localhost:5003"
TOKEN = "secret-token-alice"
HEADERS = {"Authorization": f"Bearer {TOKEN}"}

def show(label, r):
    print(f"\n{'='*45}")
    print(f"  {label}")
    print(f"  {r.request.method} {r.request.url}")
    print(f"  Auth: {r.request.headers.get('Authorization')}")
    print(f"  Status: {r.status_code}")
    print(json.dumps(r.json(), indent=2, ensure_ascii=False))

if __name__ == "__main__":
    r = requests.get(f"{BASE}/users", headers=HEADERS)
    show("GET all users (with token)", r)

    r = requests.get(f"{BASE}/users")
    show("GET users (NO token) → expect 401", r)

    r = requests.post(f"{BASE}/users",
                      json={"name": "Dave", "email": "dave@example.com"},
                      headers=HEADERS)
    show("POST create user", r)

    r = requests.put(f"{BASE}/users/2",
                     json={"email": "bob_new@example.com"},
                     headers=HEADERS)
    show("PUT update user id=2", r)

    r = requests.delete(f"{BASE}/users/3", headers=HEADERS)
    show("DELETE user id=3", r)

    r = requests.get(f"{BASE}/users/1",
                     headers={"Authorization": "Bearer fake-token"})
    show("GET with INVALID token → expect 401", r)
