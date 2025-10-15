import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data

def test_signup_and_unregister():
    # Sign up a new participant
    email = "testuser@mergington.edu"
    activity = "Chess Club"
    signup_resp = client.post(f"/activities/{activity}/signup", params={"email": email})
    assert signup_resp.status_code == 200 or signup_resp.status_code == 400
    # Unregister the participant
    unregister_resp = client.delete(f"/activities/{activity}/unregister", params={"email": email})
    assert unregister_resp.status_code == 200 or unregister_resp.status_code == 404

def test_signup_duplicate():
    email = "daniel@mergington.edu"
    activity = "Chess Club"
    # Try to sign up an existing participant
    resp = client.post(f"/activities/{activity}/signup", params={"email": email})
    assert resp.status_code == 400
    assert resp.json()["detail"] == "Student already signed up"

def test_unregister_nonexistent():
    email = "notfound@mergington.edu"
    activity = "Chess Club"
    resp = client.delete(f"/activities/{activity}/unregister", params={"email": email})
    assert resp.status_code == 404
    assert resp.json()["detail"] == "Participant not found"
