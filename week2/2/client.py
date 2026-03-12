import requests, json

BASE = "http://localhost:5002"

def show(label, r):
    print(f"\n{'='*45}")
    print(f"  {label}")
    print(f"  {r.request.method} {r.request.url}")
    print(f"  Status: {r.status_code}")
    print(json.dumps(r.json(), indent=2, ensure_ascii=False))

if __name__ == "__main__":
    r = requests.get(f"{BASE}/users")
    show("GET all users", r)

    r = requests.get(f"{BASE}/users/1")
    show("GET user id=1", r)

    r = requests.post(f"{BASE}/users", json={"name": "Dave", "email": "dave@example.com"})
    show("POST create user", r)

    r = requests.put(f"{BASE}/users/2", json={"email": "bob_new@example.com"})
    show("PUT update user id=2", r)

    r = requests.delete(f"{BASE}/users/3")
    show("DELETE user id=3", r)

    r = requests.get(f"{BASE}/users/999")
    show("GET user id=999 (not found)", r)
