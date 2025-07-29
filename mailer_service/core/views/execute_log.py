from fastapi import APIRouter, Depends, HTTPException, Response
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from db import get_async_session
from core.models import ExecuteLog
from core.serializers.execute_log import ExecuteLogRead, ExecuteLogUpdate
from typing import List

router = APIRouter(prefix="/execute_log", tags=["execute_log"])

# get all execute logs
@router.get("/", response_model=List[ExecuteLogRead])
async def list_execute_logs(session: AsyncSession = Depends(get_async_session)):
    result = await session.execute(select(ExecuteLog))
    logs = result.scalars().all()
    return JSONResponse(status_code=200, content=[log.__dict__ for log in logs])

# get execute log by id
@router.get("/{log_id}", response_model=ExecuteLogRead)
async def get_execute_log(log_id: int, session: AsyncSession = Depends(get_async_session)):
    result = await session.execute(select(ExecuteLog).where(ExecuteLog.id == log_id))
    log = result.scalar_one_or_none()
    if not log:
        raise HTTPException(status_code=404, detail="Invalid ExecuteLog id")
    return JSONResponse(status_code=200, content=log.__dict__)

# update execute log by id
@router.put("/{log_id}", response_model=ExecuteLogRead)
async def update_execute_log(log_id: int, log_update: ExecuteLogUpdate, session: AsyncSession = Depends(get_async_session)):
    result = await session.execute(select(ExecuteLog).where(ExecuteLog.id == log_id))
    log = result.scalar_one_or_none()
    if not log:
        raise HTTPException(status_code=404, detail="Invalid ExecuteLog id")
    log.emails_sent = log_update.emails_sent
    await session.commit()
    await session.refresh(log)
    return JSONResponse(status_code=200, content=log.__dict__)

# delete execute log by id
@router.delete("/{log_id}")
async def delete_execute_log(log_id: int, session: AsyncSession = Depends(get_async_session)):
    result = await session.execute(select(ExecuteLog).where(ExecuteLog.id == log_id))
    log = result.scalar_one_or_none()
    if not log:
        raise HTTPException(status_code=404, detail="Invalid ExecuteLog id")
    await session.delete(log)
    await session.commit()
    return Response(status_code=204) 