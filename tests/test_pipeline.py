from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_health_endpoint() -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_plan_video_job() -> None:
    response = client.post(
        "/api/v1/video-jobs/plan",
        json={
            "topic": "How AI agents create short videos",
            "audience": "new content creators",
            "platform": "youtube_shorts",
            "duration_seconds": 60,
            "tone": "educational",
        },
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["status"] == "planned"
    assert payload["request"]["duration_seconds"] == 60
    assert len(payload["research"]["key_points"]) >= 3
    assert len(payload["scenes"]) >= 3
