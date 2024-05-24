from fastapi.testclient import TestClient
# from TodoApp import main
from ..main import app
from fastapi import status

# client = TestClient(main.app)
client = TestClient(app)

def health_check():
    response = client.get("/healthy")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {'status': 'Healthy'}


