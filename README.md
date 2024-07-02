# FastAPI Celery Application

This project demonstrates a scalable FastAPI application that leverages Celery for asynchronous processing. The application consists of an API endpoint that triggers background tasks to fetch data from an external API, process it, and send an email with the processed data.

## Features

- FastAPI: Building efficient RESTful APIs.
- Celery: Managing asynchronous tasks and background processing.
- Asynchronous Programming: Optimizing API performance and responsiveness.

## Requirements

- Python 3.9+
- Redis (for Celery message broker and backend)
- SMTP server for sending emails

## Installation

1. **Clone the repository:**

    ```bash
    git clone https://github.com/yourusername/fastapi-celery-app.git
    cd fastapi-celery-app
    ```

2. **Create and activate a virtual environment:**

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3. **Install the dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4. **Set up environment variables:**

    Create a `.env` file in the project root and add the following configurations:

    ```env
    CELERY_BROKER_URL=redis://localhost:6379/0
    CELERY_RESULT_BACKEND=redis://localhost:6379/0
    EMAIL_SENDER=your-email@example.com
    EMAIL_PASSWORD=your-email-password
    EMAIL_SMTP_SERVER=smtp.example.com
    EMAIL_SMTP_PORT=587
    ```

## Running the Application

1. **Start the FastAPI server:**

    ```bash
    uvicorn app.main:app --reload
    ```

2. **Start the Celery worker:**

    ```bash
    celery -A celery_worker.celery_app worker --loglevel=info -Q data_processing
    ```

## Testing the Application

### Using Postman

1. **Create a new Postman request:**

    - Method: `POST`
    - URL: `http://127.0.0.1:8000/process`
    - Headers: `Content-Type: application/json`
    - Body: 
      ```json
      {
        "user_email": "test@example.com"
      }
      ```

2. **Send the request and verify the response:**

    You should receive a response with:
    ```json
    {
      "message": "Processing started"
    }
    ```

3. **Monitor the Celery worker logs** to ensure the task is being processed, and check for the creation of the CSV file and the sending of the email.

### Running Unit and Integration Tests

1. **Install the testing dependencies:**

    ```bash
    pip install pytest pytest-asyncio httpx requests-mock pytest-mock
    ```

2. **Run the tests:**

    ```bash
    pytest tests/
    ```

### Test Files

- **tests/test_main.py**: Contains tests for the FastAPI endpoint.
- **tests/test_tasks.py**: Contains tests for the Celery tasks.

## Project Structure

