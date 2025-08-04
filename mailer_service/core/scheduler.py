from apscheduler.schedulers.asyncio import AsyncIOScheduler
from core.mailer import get_all_email_addresses, send_email
import asyncio

scheduler = AsyncIOScheduler()

async def mailing_job():
    email_addresses = await get_all_email_addresses()
    if email_addresses:
        await send_email(
            recipients=email_addresses,
            subject="Daily newsletter",
            content="This is a test email."
        )

@scheduler.scheduled_job('interval', days=1)
def scheduled_mailing():
    asyncio.create_task(mailing_job())

def start_scheduler():
    scheduler.start() 