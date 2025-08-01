from math import log10
from fastapi import APIRouter, Depends, HTTPException, Response
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from db import get_async_session
from core.models import ExecuteLog
from core.serializers.execute_log import ExecuteLogRead, ExecuteLogUpdate
from typing import List
import logging

logging.basicConfig(level=logging.INFO)

router = APIRouter(prefix="/execute_log", tags=["execute_log"])

# get all execute logs
@router.get("/", response_model=List[ExecuteLogRead])
async def list_execute_logs(session: AsyncSession = Depends(get_async_session)):
    result = await session.execute(select(ExecuteLog))
    logs = result.scalars().all()
    return logs

# get execute log by id
@router.get("/{log_id}", response_model=ExecuteLogRead)
async def get_execute_log(log_id: int, session: AsyncSession = Depends(get_async_session)):
    result = await session.execute(select(ExecuteLog).where(ExecuteLog.id == log_id))
    log = result.scalar_one_or_none()
    if not log:
        raise HTTPException(status_code=404, detail="Invalid ExecuteLog id")
    return log

# update execute log by id
@router.put("/{log_id}", response_model=ExecuteLogRead)
async def update_execute_log(log_id: int, log_update: ExecuteLogUpdate, session: AsyncSession = Depends(get_async_session)):
    result = await session.execute(select(ExecuteLog).where(ExecuteLog.id == log_id))
    log = result.scalar_one_or_none()
    if not log:
        raise HTTPException(status_code=404, detail="Invalid ExecuteLog id")
    log.emails_sent = log_update.emails_sent
    try:
        await session.commit()
        await session.refresh(log)
    except Exception as e:
        logging.exception(f"Failed to update ExecuteLog with id {log_id}")
        raise HTTPException(status_code=500, detail="Database error.")
    return log

# delete execute log by id
@router.delete("/{log_id}")
async def delete_execute_log(log_id: int, session: AsyncSession = Depends(get_async_session)):
    result = await session.execute(select(ExecuteLog).where(ExecuteLog.id == log_id))
    log = result.scalar_one_or_none()
    if not log:
        raise HTTPException(status_code=404, detail="Invalid ExecuteLog id")
    try:
        await session.delete(log)
        await session.commit()
    except Exception as e:
        logging.exception(f"Failed to delete ExecuteLog with id {log_id}")
        raise HTTPException(status_code=500, detail="Database error.")
    return Response(status_code=204) 