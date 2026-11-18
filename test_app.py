from app import app


def test_home():
    response = app.test_client().get("/")
    assert response.status_code == 200
    assert response.get_json()["message"] == "Hello from GitOps!"


def test_health():
    response = app.test_client().get("/health")
    assert response.status_code == 200
    assert response.get_json()["status"] == "ok"


def test_metrics():
    client = app.test_client()
    client.get("/")
    response = client.get("/metrics")
    assert response.status_code == 200
    assert b"http_requests_total" in response.data


def test_fault_route_is_disabled_by_default():
    response = app.test_client().get("/fail")
    assert response.status_code == 404
