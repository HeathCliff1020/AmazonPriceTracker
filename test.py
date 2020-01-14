# using SendGrid's Python Library
# https://github.com/sendgrid/sendgrid-python
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

api_key = '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'

message = Mail(
    from_email='mukeshbisht1020@gmail.com',
    to_emails='heathcliff1020@gmail.com',
    subject='Sending with Twilio SendGrid is Fun',
    html_content='<strong>and easy to do anywhere, even with Python</strong>')
try:
    sg = SendGridAPIClient(api_key)
    response = sg.send(message)
    print(response.status_code)
    print(response.body)
    print(response.headers)
except Exception as e:
    print(e.message)
