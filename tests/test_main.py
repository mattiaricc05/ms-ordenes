from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_crear_retiro():
    data = {
        "producto": "Guantes de seguridad",
        "cantidad": 20,
        "operario": "María López"
    }
    response = client.post("/retiros", json=data)
    assert response.status_code == 201
    assert response.json()["producto"] == data["producto"]

def test_sql_test():
    response = client.get("/sql-test?producto=test")
    assert response.status_code == 200
    assert "protection" in response.json()