from datetime import date
from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import case, func
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.record import Record
from app.models.user import User
from app.schemas.record import RecordCreate, RecordResponse
from app.utils.auth import require_role

router = APIRouter(prefix="/records", tags=["Records"])


@router.post("/", response_model=RecordResponse)
def create_record(
    record: RecordCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(["admin", "viewer"]))
):
    new_record = Record(
        amount=record.amount,
        type=record.type,
        category=record.category,
        date=record.date,
        notes=record.notes,
        user_id=current_user.id,
    )

    db.add(new_record)
    db.commit()
    db.refresh(new_record)

    return new_record


@router.get("/", response_model=List[RecordResponse])
def get_records(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(["admin", "viewer"])),
    type: str = Query(None),
    category: str = Query(None),
    start_date: date = Query(None),
    end_date: date = Query(None),
    limit: int = Query(10, le=100),
    offset: int = Query(0, ge=0),
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

    return query.offset(offset).limit(limit).all()


@router.get("/summary")
def get_records_summary(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(["admin"]))
):
    totals = (
        db.query(
            func.coalesce(
                func.sum(case((Record.type == "income", Record.amount), else_=0.0)),
                0.0,
            ).label("total_income"),
            func.coalesce(
                func.sum(case((Record.type == "expense", Record.amount), else_=0.0)),
                0.0,
            ).label("total_expense"),
        )
        .filter(Record.user_id == current_user.id)
        .one()
    )

    category_totals = (
        db.query(
            Record.category,
            func.coalesce(func.sum(Record.amount), 0.0).label("total"),
        )
        .filter(Record.user_id == current_user.id)
        .group_by(Record.category)
        .all()
    )

    total_income = float(totals.total_income)
    total_expense = float(totals.total_expense)

    return {
        "total_income": total_income,
        "total_expense": total_expense,
        "balance": total_income - total_expense,
        "by_category": {
            category: float(total)
            for category, total in category_totals
        },
    }


@router.delete("/{record_id}")
def delete_record(
    record_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(["admin"]))
):
    record = db.query(Record).filter(
        Record.id == record_id,
        Record.user_id == current_user.id,
    ).first()

    if not record:
        raise HTTPException(status_code=404, detail="Record not found")

    db.delete(record)
    db.commit()

    return {"message": "Record deleted successfully"}
