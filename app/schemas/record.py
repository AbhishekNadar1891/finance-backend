from datetime import date
from enum import Enum

from pydantic import BaseModel, Field


class RecordType(str, Enum):
    income = "income"
    expense = "expense"

class RecordCreate(BaseModel):
    amount: float = Field(..., gt=0)
    type: RecordType
    category: str = Field(..., min_length=1)
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
