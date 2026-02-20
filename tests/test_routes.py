from fastapi.testclient import TestClient

from src.main import app


client = TestClient(app)


def test_healthz_status_code_is_success():
    response = client.get("/_healthz")
    assert response.status_code in {200, 201}


def test_probe_status_code_is_success():
    response = client.get("/_probe")
    assert response.status_code in {200, 201}
