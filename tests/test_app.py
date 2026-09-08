from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)


def test_signup_duplicate_rejected():
    activity_name = "Chess Club"
    email = "duplicate@example.com"

    # ensure clean state
    app.state if hasattr(app, 'state') else None
    activities = __import__('src.app', fromlist=['activities']).activities
    if email in activities[activity_name]["participants"]:
        activities[activity_name]["participants"].remove(email)

    first = client.post(f"/activities/{activity_name}/signup?email={email}")
    second = client.post(f"/activities/{activity_name}/signup?email={email}")

    assert first.status_code == 200
    assert second.status_code == 400
    assert activities[activity_name]["participants"].count(email) == 1


def test_unregister_removes_participant():
    activity_name = "Chess Club"
    email = "remove@example.com"
    activities = __import__('src.app', fromlist=['activities']).activities
    if email not in activities[activity_name]["participants"]:
        activities[activity_name]["participants"].append(email)

    response = client.delete(f"/activities/{activity_name}/participants/{email}")

    assert response.status_code == 200
    assert email not in activities[activity_name]["participants"]
