
from fastapi.testclient import TestClient
# Remplace 'main' par le nom de ton fichier s'il est différent
from main import app 

client = TestClient(app)

def test_health_check():
    """
    Teste que le endpoint /api/health répond avec un statut 200 et le bon JSON.
    """
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_prometheus_metrics_exposed():
    """
    Vérifie que l'instrumentation Prometheus est active sur /metrics.
    """
    response = client.get("/metrics")
    assert response.status_code == 200
    assert "process_cpu_seconds_total" in response.text

def test_docs_urls():
    """
    Vérifie que les URLs de documentation personnalisées fonctionnent.
    """
    # Test Redoc
    response_redoc = client.get("/docs")
    assert response_redoc.status_code == 200
    
    # Test Swagger UI
    response_swagger = client.get("/api/docs")
    assert response_swagger.status_code == 200

def test_cors_headers():
    """
    Vérifie que les headers CORS sont bien présents.
    """
    response = client.options(
        "/api/health",
        headers={
            "Origin": "http://localhost:3000",
            "Access-Control-Request-Method": "GET",
        },
    )
    assert response.status_code == 200
    assert response.headers["access-control-allow-origin"] == "*"