import uuid

def test_signup(client):
    email = f"test_{uuid.uuid4().hex[:8]}@gmail.com"
    payload = {"email": email, "password": "Test@123"}

    res = client.post("/auth/signup", json=payload)
    assert res.status_code == 200


def test_login(client):
    email = f"test_{uuid.uuid4().hex[:8]}@gmail.com"
    password = "Test@123"

    client.post("/auth/signup", json={"email": email, "password": password})

    res = client.post("/auth/login", json={"email": email, "password": password})
    assert res.status_code == 200

    data = res.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
