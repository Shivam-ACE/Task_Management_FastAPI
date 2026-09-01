from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType
from pydantic import EmailStr, BaseModel
# from typing import List

conf = ConnectionConfig(
    MAIL_USERNAME = "shivamdhanuka050@gmail.com",
    MAIL_PASSWORD = "kise mafb becn kehc",
    MAIL_FROM = "shivamdhanuka050@gmail.com",
    MAIL_PORT = 587,
    MAIL_SERVER = "smtp.gmail.com",
    MAIL_FROM_NAME="Shivam",
    MAIL_STARTTLS = True,
    MAIL_SSL_TLS = False,
    USE_CREDENTIALS = True,
    VALIDATE_CERTS = True
)

async def send_email(emails: list[str]):
    html = """<p>Hi, thanks for registration. We will connect with u soon !</p> """

    message = MessageSchema(
        subject="Registration Successful",
        recipients=emails,
        body=html,
        subtype=MessageType.html)

    fm = FastMail(conf)
    await fm.send_message(message)
    # return {"message": "email has been sent"}
    print({"message": "email has been sent"})