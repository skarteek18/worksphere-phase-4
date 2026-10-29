from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from models import Feedback, User
from schemas import FeedbackCreate, FeedbackResponse
from auth import get_current_user, require_hr_or_admin

router = APIRouter()


# submit employee feedback
@router.post("/", response_model=FeedbackResponse)
def submit_feedback(
    feedback: FeedbackCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role.lower() in ["admin", "hr"]:
        raise HTTPException(
            status_code=403,
            detail="Only employees can submit feedback"
        )

    new_feedback = Feedback(
        employee_id=current_user.id,
        message=feedback.message,
        rating=feedback.rating
    )

    db.add(new_feedback)
    db.commit()
    db.refresh(new_feedback)

    return new_feedback


# view feedback (hr/admin only)
@router.get("/", response_model=list[FeedbackResponse])
def get_all_feedback(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_hr_or_admin)
):
    return (
        db.query(Feedback)
        .order_by(Feedback.created_at.desc())
        .all()
    )


# view own feedback submissions
@router.get("/my", response_model=list[FeedbackResponse])
def get_my_feedback(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return (
        db.query(Feedback)
        .filter(Feedback.employee_id == current_user.id)
        .order_by(Feedback.created_at.desc())
        .all()
    )


# delete feedback (hr/admin only)
@router.delete("/{feedback_id}")
def delete_feedback(
    feedback_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_hr_or_admin)
):
    feedback = db.query(Feedback).filter(
        Feedback.id == feedback_id
    ).first()

    if not feedback:
        raise HTTPException(
            status_code=404,
            detail="Feedback not found"
        )

    db.delete(feedback)
    db.commit()

    return {"message": "Feedback deleted successfully"}
