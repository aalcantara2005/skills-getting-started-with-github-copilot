from fastapi.testclient import TestClient

from src.app import app


client = TestClient(app)


def test_unregister_participant_from_activity():
    activity_name = "Chess Club"
    email = "michael@mergington.edu"

    response = client.delete(f"/activities/{activity_name}/participants/{email}")

    assert response.status_code == 200
    payload = response.json()
    assert payload["message"] == f"Removed {email} from {activity_name}"
    assert email not in client.get("/activities").json()[activity_name]["participants"]

    # Restore state for clean test isolation
    client.post(f"/activities/{activity_name}/signup?email={email}")


def test_unregister_missing_participant_returns_404():
    response = client.delete("/activities/Chess Club/participants/ghost@mergington.edu")

    assert response.status_code == 404
    assert response.json()["detail"] == "Participant not found in activity"
