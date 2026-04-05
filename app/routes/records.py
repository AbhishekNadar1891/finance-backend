from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List
from datetime import date

from app.database import get_db
from app.models.record import Record
from app.schemas.record import RecordCreate, RecordResponse
from app.utils.auth import get_current_user
from app.models.user import User

router = APIRouter(prefix="/records", tags=["Records"])


@router.post("/", response_model=RecordResponse)
def create_record(
    record: RecordCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    new_record = Record(
        amount=record.amount,
        type=record.type,
        category=record.category,
        date=record.date,
        notes=record.notes,
        user_id=current_user.id
    )

    db.add(new_record)
    db.commit()
    db.refresh(new_record)

    return new_record


#  ADDED THIS BELOW (new function, not inside above)
@router.get("/", response_model=List[RecordResponse])
def get_records(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    type: str = Query(None),
    category: str = Query(None),
    start_date: date = Query(None),
    end_date: date = Query(None)
):
    
    query = db.query(Record).filter(Record.user_id == current_user.id)

    if type:
        query = query.filter(Record.type == type)

    if category:
        query = query.filter(Record.category == category)

    if start_date:
        query = query.filter(Record.date >= start_date)

    if end_date:
        query = query.filter(Record.date <= end_date)

    return query.all()