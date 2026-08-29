def test_login_success(client, create_user):
    create_user(username="alice", password="secret123")
    response = client.post("/auth/login", json={"username": "alice", "password": "secret123"})
    assert response.status_code == 200
    assert "access_token" in response.json()


def test_login_wrong_password(client, create_user):
    create_user(username="alice", password="secret123")
    response = client.post("/auth/login", json={"username": "alice", "password": "wrong"})
    assert response.status_code == 401


def test_protected_route_without_token(client):
    response = client.get("/listings/me")
    assert response.status_code == 401


def test_protected_route_with_token(client, auth_headers):
    headers, user = auth_headers(role="buyer")
    response = client.get("/listings/me", headers=headers)
    assert response.status_code == 200
    assert response.json()["user_id"] == user.id