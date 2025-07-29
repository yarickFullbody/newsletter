from pydantic import BaseModel

class ExecuteLogRead(BaseModel):
    id: int
    executed_at: str
    emails_sent: int

    class Config:
        orm_mode = True

class ExecuteLogUpdate(BaseModel):
    emails_sent: int 