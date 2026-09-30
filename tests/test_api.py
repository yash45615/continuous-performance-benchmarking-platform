from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_health():

    response = client.get("/health")

    assert response.status_code == 200

    assert response.json()["status"] == "ok"


def test_get_product():

    response = client.get("/api/products/101")

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == 101

    assert data["sku"] == "SKU-000101"


def test_create_item():

    response = client.post(
        "/api/items",
        json={
            "name": "Laptop",
            "value": 10
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["name"] == "Laptop"

    assert data["status"] == "created"