import pytest
pytest.importorskip('fastapi')
from fastapi.testclient import TestClient
from main import app
def test_health_and_cors():
    with TestClient(app) as client:
        assert client.get('/api/health').status_code==200
        assert client.options('/api/health',headers={'Origin':'http://localhost','Access-Control-Request-Method':'GET'}).headers['access-control-allow-origin']=='*'
def test_invalid_segment_and_conditions():
    with TestClient(app) as client:
        assert client.get('/api/segments/999999').status_code==404
        assert client.post('/api/risk/batch',json={'conditions':{'weather':'snow'}}).status_code==422
