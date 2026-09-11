import httpx

with httpx.Client(follow_redirects=False, timeout=30.0) as client:
    resp = client.post("http://localhost:8000/auth/login", data={"username": "superadmin@gmail.com", "password": "superadmin123"})
    print("Status Code:", resp.status_code)
    print("Headers:", resp.headers)
    print("Body:", resp.text[:500])
