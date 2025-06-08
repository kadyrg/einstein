import smtplib
from email.message import EmailMessage
from fastapi import HTTPException

from app.core import settings


class MailManager:
    def __init__(self, email, host, port, password):
        self.email = email
        self.host = host
        self.port = port
        self.password = password


    def send_mail(self, to: str, code: str):
        subject = "Verification code"
        body = f"Your verification code is {code}"
        
        msg = EmailMessage()
        
        msg["Subject"] = subject
        msg["From"] = self.email
        msg["To"] = to
        msg.set_content(body)

        try:
            with smtplib.SMTP(self.host, int(self.port)) as server:
                server.ehlo()
                server.starttls()
                server.ehlo()
                server.login(self.email, self.password)
                server.send_message(msg)

        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Verification code couldn't be sent. {e}")


mail_manager = MailManager(
    email = settings.EMAIL_USER,
    host = settings.EMAIL_HOST,
    port = settings.EMAIL_PORT,
    password = settings.EMAIL_PASS
)
