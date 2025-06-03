import smtplib
from email.message import EmailMessage
from fastapi import HTTPException

from core import settings


class MailManager:
    email = settings.EMAIL_USER
    host = settings.EMAIL_HOST
    port = settings.EMAIL_PORT
    password = settings.EMAIL_PASS


    @classmethod
    def send_mail(cls, to: str, code: str):
        subject = "Verification code"
        body = f"Your verification code is {code}"
        
        msg = EmailMessage()
        
        msg["Subject"] = subject
        msg["From"] = cls.email
        msg["To"] = to
        msg.set_content(body)

        try:
            with smtplib.SMTP(cls.host, int(cls.port)) as server:
                server.ehlo()
                server.starttls()
                server.ehlo()
                server.login(cls.email, cls.password)
                server.send_message(msg)
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Verification code couldn't be sent. {e}")


mail_manager = MailManager()
