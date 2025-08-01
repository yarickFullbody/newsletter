from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import DateTime, func
from db import Base

class ExecuteLog(Base):
    __tablename__ = "execute_log"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    executed_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    emails_sent: Mapped[int] = mapped_column(nullable=False)
