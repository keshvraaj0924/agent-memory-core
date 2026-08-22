from fastapi.testclient import TestClient

from main import app


def test_create_and_fetch_memory() -> None:
    with TestClient(app) as client:
        created = client.post(
            "/api/v1/memories",
            json={
                "content": "User prefers Python 3.12 for AI projects.",
                "memory_type": "preference",
                "user_id": "user-123",
                "importance": 0.9,
            },
        )

        assert created.status_code == 201
        payload = created.json()
        assert payload["memory_type"] == "preference"
        assert payload["importance"] == 0.9

        fetched = client.get(f"/api/v1/memories/{payload['id']}")
        assert fetched.status_code == 200
        assert fetched.json()["content"] == payload["content"]
