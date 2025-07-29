from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from db import get_async_session

app = FastAPI()

@app.get("/ping-db")
async def ping_db(session: AsyncSession = Depends(get_async_session)):
    result = await session.execute(text("SELECT 1"))
    return {"db_ok": result.scalar() == 1}