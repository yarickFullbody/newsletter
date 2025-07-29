import os
import json
from aiokafka import AIOKafkaConsumer
import aioredis
from dotenv import load_dotenv

load_dotenv()

KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS")
KAFKA_TOPIC = os.getenv("KAFKA_TOPIC")
REDIS_URL = os.getenv("REDIS_URL")

async def handle_message(redis, email: str, is_subscribed: bool):
    if is_subscribed:
        await redis.sadd("subscribed_emails", email)
    else:
        await redis.srem("subscribed_emails", email)

async def consume():
    redis = await aioredis.from_url(REDIS_URL, encoding="utf-8", decode_responses=True)
    consumer = AIOKafkaConsumer(
        KAFKA_TOPIC,
        bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
        value_deserializer=lambda m: json.loads(m.decode("utf-8")),
        enable_auto_commit=True,
        auto_offset_reset="earliest",
    )
    await consumer.start()
    try:
        async for msg in consumer:
            data = msg.value
            email = data.get("email")
            is_subscribed = data.get("is_subscribed")
            if email is not None and is_subscribed is not None:
                await handle_message(redis, email, is_subscribed)
    finally:
        await consumer.stop()
        await redis.close() 