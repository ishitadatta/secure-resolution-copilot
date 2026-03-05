from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health() -> None:
    response = client.get("/v1/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_intake_and_ticket_flow() -> None:
    intake = client.post(
        "/v1/chat/intake",
        json={"user_id": "u-123", "message": "Suspicious email asked me to click link and enter credentials"},
    )
    assert intake.status_code == 200
    ticket_id = intake.json()["ticket_id"]

    no_approval_execute = client.post(f"/v1/tickets/{ticket_id}/execute", json={"analyst": "soc-1"})
    assert no_approval_execute.status_code == 403

    approve = client.post(
        f"/v1/tickets/{ticket_id}/approve",
        json={"analyst": "soc-1", "approve": True, "override_recommendation": False},
    )
    assert approve.status_code == 200

    execute = client.post(f"/v1/tickets/{ticket_id}/execute", json={"analyst": "soc-1"})
    assert execute.status_code == 200
    assert execute.json()["status"] == "RESOLVED"
