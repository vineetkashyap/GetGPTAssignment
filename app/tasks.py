import csv
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from celery import shared_task
import requests
from .config import Config

@shared_task
def fetch_and_process_data(user_email):
    base_url = "https://24pullrequests.com/users.json?page={}"
    data = []

    for page in range(1, 21):
        try:
            response = requests.get(base_url.format(page))
            response.raise_for_status()
            page_data = response.json()
            for user in page_data:
                for pr in user.get('pull_requests', []):
                    data.append({
                        'repo_name': pr.get('repo_name'),
                        'title': pr.get('title')
                    })
        except requests.exceptions.RequestException as error:
            print(f"An error occurred: {error}")
            return f"An error occurred: {error}"

    csv_file = f"data_{user_email}.csv"
    with open(csv_file, 'w', newline='') as csvfile:
        fieldnames = ['repo_name', 'title']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for row in data:
            writer.writerow(row)

    send_email(user_email, csv_file)

def send_email(recipient_email, attachment_file):
    sender_email = Config.EMAIL_SENDER
    password = Config.EMAIL_PASSWORD

    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = recipient_email
    message["Subject"] = "Processed Data"

    body = "Please find the attached processed data."
    message.attach(MIMEText(body, "plain"))

    try:
        with open(attachment_file, "rb") as attachment:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(attachment.read())

        encoders.encode_base64(part)
        part.add_header(
            "Content-Disposition",
            f"attachment; filename= {attachment_file}",
        )

        message.attach(part)

        text = message.as_string()

        with smtplib.SMTP(Config.EMAIL_SMTP_SERVER, Config.EMAIL_SMTP_PORT) as server:
            server.starttls()
            server.login(sender_email, password)
            server.sendmail(sender_email, recipient_email, text)
        print("Email sent successfully")
    except Exception as e:
        print(f"An error occurred while sending email: {e}")
