import uuid
from fastapi.testclient import TestClient

from src.app import app


client = TestClient(app)


def test_get_activities():
    resp = client.get("/activities")
    assert resp.status_code == 200
    data = resp.json()
    # basic sanity: at least one known activity exists
    assert "Chess Club" in data


def test_signup_and_delete_participant():
    activity = "Chess Club"
    email = f"pytest-{uuid.uuid4().hex}@example.com"

    # ensure not present
    resp = client.get("/activities")
    assert resp.status_code == 200
    assert email not in resp.json()[activity]["participants"]

    # signup
    resp = client.post(f"/activities/{activity}/signup?email={email}")
    assert resp.status_code == 200
    assert resp.json().get("message") and email in resp.json().get("message")

    # verify present
    resp = client.get("/activities")
    assert email in resp.json()[activity]["participants"]

    # duplicate signup should return 400
    resp = client.post(f"/activities/{activity}/signup?email={email}")
    assert resp.status_code == 400

    # delete
    resp = client.delete(f"/activities/{activity}/signup?email={email}")
    assert resp.status_code == 200
    assert resp.json().get("message") and email in resp.json().get("message")

    # verify removed
    resp = client.get("/activities")
    assert email not in resp.json()[activity]["participants"]
