from pydantic import BaseModel
from datetime import date

class RecordCreate(BaseModel):
    amount: float
    type: str
    category: str
    date: date
    notes: str | None = None


class RecordResponse(BaseModel):
    id: int
    amount: float
    type: str
    category: str
    date: date
    notes: str | None

    class Config:
        from_attributes = True