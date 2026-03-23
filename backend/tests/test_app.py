import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app
import json

def test_health_check():
    client = app.test_client()
    response = client.get("/")
    assert response.status_code == 200
    data = json.loads(response.data)
    assert "status" in data

def test_get_transactions():
    client = app.test_client()
    response = client.get("/api/transactions")
    assert response.status_code == 200
    assert isinstance(json.loads(response.data), list)

def test_get_stats():
    client = app.test_client()
    response = client.get("/api/stats")
    assert response.status_code == 200
    data = json.loads(response.data)
    assert "total_transactions" in data

def test_predict_missing_fields():
    client = app.test_client()
    response = client.post("/api/predict",
        data=json.dumps({}),
        content_type="application/json")
    assert response.status_code == 400
