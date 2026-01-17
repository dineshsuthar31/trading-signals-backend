import uuid

def test_signals_free_user_gets_limited_signals(client):
    email = f"test_{uuid.uuid4().hex[:8]}@gmail.com"
    password = "Test@123"

    client.post("/auth/signup", json={"email": email, "password": password})

    login_res = client.post("/auth/login", json={"email": email, "password": password})
    token = login_res.json()["access_token"]

    res = client.get("/signals", headers={"Authorization": f"Bearer {token}"})
    assert res.status_code == 200

    data = res.json()
    assert "signals" in data
    assert len(data["signals"]) == 3