import pytest
from fastapi.testclient import TestClient

from src.app import app, activities


client = TestClient(app)


def test_get_activities():
    res = client.get("/activities")
    assert res.status_code == 200
    data = res.json()
    assert isinstance(data, dict)
    # Should contain some known activities
    assert "Chess Club" in data


def test_signup_and_unregister():
    activity = "Chess Club"
    email = "tester@example.com"

    # Ensure clean state: remove if present
    if email in activities[activity]["participants"]:
        activities[activity]["participants"].remove(email)

    # Sign up
    res = client.post(f"/activities/{activity}/signup", params={"email": email})
    assert res.status_code == 200
    assert email in activities[activity]["participants"]

    # Unregister
    res = client.delete(f"/activities/{activity}/unregister", params={"email": email})
    assert res.status_code == 200
    assert email not in activities[activity]["participants"]

    # Unregistering again should return 404
    res = client.delete(f"/activities/{activity}/unregister", params={"email": email})
    assert res.status_code == 404
