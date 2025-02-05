from fastapi.testclient import TestClient
from app.main import app


client = TestClient(app)

def test_create_package():
    response = client.post(
        "/packages/",
        json={
            "name": "Test Package",
            "weight": 2.5,
            "content_cost": 100.0,
            "package_type_id": 1
        }
    )
    assert response.status_code == 200
    assert response.json()["name"] == "Test Package"