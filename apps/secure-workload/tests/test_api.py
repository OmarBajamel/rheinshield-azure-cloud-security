import importlib.util
from pathlib import Path

from fastapi.testclient import TestClient

MODULE_PATH = Path(__file__).parents[1] / "app" / "main.py"
spec = importlib.util.spec_from_file_location("rheinshield_workload", MODULE_PATH)
assert spec and spec.loader
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
client = TestClient(module.app)


def test_health_and_headers() -> None:
    response = client.get("/health", headers={"x-correlation-id": "test-correlation"})
    assert response.status_code == 200
    assert response.json()["synthetic"] is True
    assert response.headers["x-correlation-id"] == "test-correlation"
    assert response.headers["x-content-type-options"] == "nosniff"


def test_order_round_trip() -> None:
    created = client.post("/orders", json={"product_id": "prd-secure01", "quantity": 2})
    assert created.status_code == 201
    payload = created.json()
    assert payload["synthetic"] is True
    fetched = client.get(f"/orders/{payload['order_id']}")
    assert fetched.status_code == 200
    assert fetched.json() == payload


def test_rejects_invalid_product() -> None:
    response = client.post("/orders", json={"product_id": "../../secret", "quantity": 1})
    assert response.status_code == 422


def test_missing_order_is_safe() -> None:
    response = client.get("/orders/ord-doesnotexist")
    assert response.status_code == 404
    assert "Synthetic" in response.json()["detail"]
