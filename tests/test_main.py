# tests/test_main.py
import pytest
from fastapi.testclient import TestClient
from app.main import app
from unittest.mock import patch

client = TestClient(app)

@pytest.fixture
def mock_celery_task(mocker):
    return mocker.patch('app.tasks.fetch_and_process_data.delay')

def test_process_endpoint(mock_celery_task):
    response = client.post("/process", json={"user_email": "test@example.com"})
    assert response.status_code == 200
    assert response.json() == {"message": "Processing started"}
    mock_celery_task.assert_called_once_with("test@example.com")
