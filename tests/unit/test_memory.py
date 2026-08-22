from fastapi.testclient import TestClient

from main import app


def _create(client: TestClient, *, content: str, importance: float = 0.5) -> dict:
    response = client.post(
        "/api/v1/memories",
        json={
            "content": content,
            "memory_type": "preference",
            "user_id": "user-123",
            "importance": importance,
        },
    )
    assert response.status_code == 201
    return response.json()


def test_create_and_fetch_memory() -> None:
    with TestClient(app) as client:
        created = _create(
            client,
            content="User prefers Python 3.12 for AI projects.",
            importance=0.9,
        )

        fetched = client.get(f"/api/v1/memories/{created['id']}")
        assert fetched.status_code == 200
        payload = fetched.json()
        assert payload["content"] == created["content"]
        assert payload["access_count"] == 1


def test_update_search_and_delete_memory() -> None:
    with TestClient(app) as client:
        created = _create(client, content="User prefers JavaScript.", importance=0.4)

        updated = client.patch(
            f"/api/v1/memories/{created['id']}",
            json={"content": "User prefers Python for AI systems.", "importance": 0.95},
        )
        assert updated.status_code == 200
        assert updated.json()["importance"] == 0.95

        search = client.post(
            "/api/v1/memories/search",
            json={"user_id": "user-123", "query": "Python AI", "limit": 5},
        )
        assert search.status_code == 200
        assert search.json()[0]["memory"]["id"] == created["id"]
        assert search.json()[0]["score"] > 0

        deleted = client.delete(f"/api/v1/memories/{created['id']}")
        assert deleted.status_code == 204

        missing = client.get(f"/api/v1/memories/{created['id']}")
        assert missing.status_code == 404
