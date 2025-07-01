from fastapi.testclient import TestClient
from api.analyze import app

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

def test_analysis_endpoint():
    test_task = """
    Analyze this sample data:
    1,2,3
    4,5,6
    
    Questions:
    1. What's the average of column 1?
    """
    
    response = client.post("/api/", files={"file": ("test.txt", test_task)})
    assert response.status_code == 200
    assert "average" in str(response.json())