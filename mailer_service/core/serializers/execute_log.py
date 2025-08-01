from pydantic import BaseModel
from datetime import datetime

class ExecuteLogRead(BaseModel):
    id: int
    executed_at: datetime
    emails_sent: int

    class Config:
        from_attributes = True

class ExecuteLogUpdate(BaseModel):
    emails_sent: int 