import requests
import json
from app.config import settings


def send_email(recipient_add):
    # Set up email message parameters
    data = {
        'sender': {'name': 'Test Assessment', 'email': settings.sender_email_add},
        'to': [{'email': recipient_add}],
        'subject': 'File Upload: Test Assessment',
        'htmlContent': '<p>Your file has been uploaded successfully without errors!</p>'
    }

    # Send email using Sendinblue API
    response = requests.post(
        settings.sendinblue_endpoint,
        headers={'api-key': settings.sendinblue_endpoint},
        data=json.dumps(data)
    )

    return response
