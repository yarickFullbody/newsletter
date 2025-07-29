from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from db import get_async_session
from core.views.execute_log import router as execute_log_router
import asyncio
from core.kafka_consumer import consume
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    loop = asyncio.get_event_loop()
    loop.create_task(consume())
    yield

app = FastAPI(lifespan=lifespan)

app.include_router(execute_log_router)

@app.get("/ping-db")
async def ping_db(session: AsyncSession = Depends(get_async_session)):
    result = await session.execute(text("SELECT 1"))
    return {"db_ok": result.scalar() == 1}