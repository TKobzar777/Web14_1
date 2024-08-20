from fastapi_mail import ConnectionConfig, FastMail, MessageSchema

from config.general import settings

"""
Configuration for the email connection.
"""
mail_conf = ConnectionConfig(
    MAIL_USERNAME=settings.mail_username,
    MAIL_PASSWORD=settings.mail_password,
    MAIL_FROM=settings.mail_from,
    MAIL_PORT=settings.mail_port,
    MAIL_SERVER=settings.mail_server,
    MAIL_STARTTLS=False,
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=True,

)


async def send_verification(email: str, email_body: str):
    """
    Send a verification email to the specified email address.

    Args:
        email (str): The recipient's email address.
        email_body (str): The HTML body of the verification email.
    """
    message = MessageSchema(
        subject="Email Verification",
        recipients=[email],
        body=email_body,
        subtype="html",
    )
    fm = FastMail(mail_conf)
    await fm.send_message(message)
