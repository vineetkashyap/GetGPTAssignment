# tests/test_tasks.py
import pytest
import requests_mock
from app.tasks import fetch_and_process_data

@pytest.fixture
def mock_requests():
    with requests_mock.Mocker() as m:
        yield m

def test_fetch_and_process_data(mock_requests, mocker):
    # Mock the API responses
    mock_requests.get("https://24pullrequests.com/users.json?page=1", json=[{
        "username": "user1",
        "pull_requests": [{"repo_name": "repo1", "title": "PR1"}]
    }])
    
    # Mock the email sending function
    mock_send_email = mocker.patch('app.tasks.send_email')
    
    # Call the task
    fetch_and_process_data("test@example.com")
    
    # Check if the CSV file is created and email is sent
    mock_send_email.assert_called_once_with("test@example.com", "data_test@example.com.csv")
    
    with open("data_test@example.com.csv") as f:
        lines = f.readlines()
        assert lines[0].strip() == "repo_name,title"
        assert lines[1].strip() == "repo1,PR1"
