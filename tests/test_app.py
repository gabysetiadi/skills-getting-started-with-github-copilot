import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)


def test_root_redirect():
    response = client.get("/")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
    assert "Mergington High School" in response.text


def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data
    assert "participants" in data["Chess Club"]


def test_signup_success():
    response = client.post("/activities/Chess%20Club/signup?email=test@example.com")
    assert response.status_code == 200
    data = response.json()
    assert "Signed up" in data["message"]


def test_signup_duplicate():
    # First signup
    client.post("/activities/Chess%20Club/signup?email=duplicate@example.com")
    # Second signup should fail
    response = client.post("/activities/Chess%20Club/signup?email=duplicate@example.com")
    assert response.status_code == 400
    data = response.json()
    assert "already signed up" in data["detail"]


def test_signup_invalid_activity():
    response = client.post("/activities/Invalid%20Activity/signup?email=test@example.com")
    assert response.status_code == 404
    data = response.json()
    assert "Activity not found" in data["detail"]


def test_unregister_success():
    # First signup
    client.post("/activities/Programming%20Class/signup?email=unregister@example.com")
    # Then unregister
    response = client.delete("/activities/Programming%20Class/signup?email=unregister@example.com")
    assert response.status_code == 200
    data = response.json()
    assert "Unregistered" in data["message"]


def test_unregister_not_found():
    response = client.delete("/activities/Chess%20Club/signup?email=notfound@example.com")
    assert response.status_code == 404
    data = response.json()
    assert "Participant not found" in data["detail"]


def test_unregister_invalid_activity():
    response = client.delete("/activities/Invalid%20Activity/signup?email=test@example.com")
    assert response.status_code == 404
    data = response.json()
    assert "Activity not found" in data["detail"]