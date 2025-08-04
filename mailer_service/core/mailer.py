import aiosmtplib
from email.message import EmailMessage
from core.redis_client import get_redis
from core.settings import Settings

settings = Settings()

async def get_all_email_addresses():
    redis = await get_redis()
    email_addresses = await redis.smembers("emails")
    return list(email_addresses)

async def send_email(recipients, subject, content, html_content=None, attachments=None):
    message = EmailMessage()
    message["From"] = settings.smtp_from
    message["To"] = ", ".join(recipients)
    message["Subject"] = subject
    message.set_content(content)

    if html_content:
        message.add_alternative(html_content, subtype="html")

    if attachments:
        for filename, file_bytes, mime_type in attachments:
            maintype, subtype = mime_type.split("/", 1)
            message.add_attachment(file_bytes, maintype=maintype, subtype=subtype, filename=filename)

    await aiosmtplib.send(
        message,
        hostname=settings.smtp_host,
        port=settings.smtp_port,
        username=settings.smtp_user,
        password=settings.smtp_password,
        use_tls=settings.smtp_tls,
    ) 