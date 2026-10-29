

from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from models import Resignation, User
from schemas import ResignationCreate, ResignationUpdate, ResignationResponse
from auth import get_current_user, require_hr_or_admin

router = APIRouter()


# submit resignation
@router.post("/", response_model=ResignationResponse)
def submit_resignation(
    resignation: ResignationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role.lower() in ["admin", "hr"]:
        raise HTTPException(
            status_code=403,
            detail="HR/Admin cannot submit resignation through this endpoint"
        )

    existing = db.query(Resignation).filter(
        Resignation.employee_id == current_user.id,
        Resignation.status == "PENDING"
    ).first()

    if existing:
        raise HTTPException(
            status_code=400,
            detail="You already have a pending resignation request"
        )

    new_resignation = Resignation(
        employee_id=current_user.id,
        reason=resignation.reason,
        notice_period=resignation.notice_period,
        status="PENDING"
    )

    db.add(new_resignation)
    db.commit()
    db.refresh(new_resignation)

    return new_resignation


# view resignation requests
@router.get("/", response_model=list[ResignationResponse])
def get_resignations(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    query = db.query(Resignation)

    if current_user.role.lower() not in ["admin", "hr"]:
        query = query.filter(
            Resignation.employee_id == current_user.id
        )

    return query.order_by(Resignation.id.desc()).all()


# view a specific resignation
@router.get("/{resignation_id}", response_model=ResignationResponse)
def get_resignation(
    resignation_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    resignation = db.query(Resignation).filter(
        Resignation.id == resignation_id
    ).first()

    if not resignation:
        raise HTTPException(
            status_code=404,
            detail="Resignation request not found"
        )

    if (
        current_user.role.lower() not in ["admin", "hr"]
        and resignation.employee_id != current_user.id
    ):
        raise HTTPException(
            status_code=403,
            detail="You cannot view another employee's resignation"
        )

    return resignation


# approve or reject resignation (hr/admin only)
@router.patch("/{resignation_id}/status", response_model=ResignationResponse)
def update_resignation_status(
    resignation_id: int,
    update: ResignationUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_hr_or_admin)
):
    resignation = db.query(Resignation).filter(
        Resignation.id == resignation_id
    ).first()

    if not resignation:
        raise HTTPException(
            status_code=404,
            detail="Resignation request not found"
        )

    if resignation.status != "PENDING":
        raise HTTPException(
            status_code=400,
            detail="Only pending resignations can be updated"
        )

    if update.status not in ["APPROVED", "REJECTED"]:
        raise HTTPException(
            status_code=400,
            detail="Status must be APPROVED or REJECTED"
        )

    resignation.status = update.status
    db.commit()
    db.refresh(resignation)

    return resignation
