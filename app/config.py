import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    CELERY_BROKER_URL = os.getenv('CELERY_BROKER_URL', 'redis://localhost:6379/0')
    CELERY_RESULT_BACKEND = os.getenv('CELERY_RESULT_BACKEND', 'redis://localhost:6379/0')
    EMAIL_SENDER = os.getenv('EMAIL_SENDER', 'example@example.com')
    EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD', 'password')
    EMAIL_SMTP_SERVER = os.getenv('EMAIL_SMTP_SERVER', 'smtp.example.com')
    EMAIL_SMTP_PORT = int(os.getenv('EMAIL_SMTP_PORT', 587))
