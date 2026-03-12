import requests, json

BASE = "http://localhost:5001/action"

def call(action, **kwargs):
    payload = {"action": action, **kwargs}
    r = requests.post(BASE, json=payload)
    print(f"\n[{action}] → {r.status_code}")
    print(json.dumps(r.json(), indent=2, ensure_ascii=False))

if __name__ == "__main__":
    call("get_users")
    call("get_user", id=1)
    call("create_user", name="Dave", email="dave@example.com")
    call("update_email", id=2, email="bob_new@example.com")
    call("delete_user", id=3)
