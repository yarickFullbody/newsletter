from sqlalchemy import Column, Integer, DateTime, func
from db import Base

class ExecuteLog(Base):
    __tablename__ = "execute_log"

    id = Column(Integer, primary_key=True, autoincrement=True)
    executed_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    emails_sent = Column(Integer, nullable=False)
