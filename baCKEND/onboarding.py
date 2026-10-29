

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from models import Onboarding, User
from schemas import OnboardingCreate, OnboardingResponse
from auth import get_current_user, require_hr_or_admin

router = APIRouter()


# assign onboarding task (hr/admin only)
@router.post("/", response_model=OnboardingResponse)
def create_onboarding_task(
    task: OnboardingCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_hr_or_admin)
):
    employee = db.query(User).filter(
        User.id == task.employee_id
    ).first()

    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")

    new_task = Onboarding(
        employee_id=task.employee_id,
        task_name=task.task_name,
        status="PENDING",
        due_date=task.due_date
    )

    db.add(new_task)
    db.commit()
    db.refresh(new_task)

    return new_task


# view onboarding checklist
@router.get("/", response_model=list[OnboardingResponse])
def get_onboarding_tasks(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role.lower() in ["admin", "hr"]:
        return db.query(Onboarding).all()

    return db.query(Onboarding).filter(
        Onboarding.employee_id == current_user.id
    ).all()


# update onboarding task status
@router.patch("/{task_id}/complete", response_model=OnboardingResponse)
def complete_onboarding_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    task = db.query(Onboarding).filter(
        Onboarding.id == task_id
    ).first()

    if not task:
        raise HTTPException(status_code=404, detail="Onboarding task not found")

    if current_user.role.lower() not in ["admin", "hr"]:
        if task.employee_id != current_user.id:
            raise HTTPException(
                status_code=403,
                detail="You cannot update another employee's onboarding task"
            )

    task.status = "COMPLETED"
    db.commit()
    db.refresh(task)

    return task


# track onboarding progress
@router.get("/progress")
def get_onboarding_progress(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    query = db.query(Onboarding)

    if current_user.role.lower() not in ["admin", "hr"]:
        query = query.filter(
            Onboarding.employee_id == current_user.id
        )

    tasks = query.all()
    total_tasks = len(tasks)
    completed_tasks = sum(
        1 for task in tasks if task.status == "COMPLETED"
    )

    progress = (
        round((completed_tasks / total_tasks) * 100, 2)
        if total_tasks > 0 else 0
    )

    return {
        "total_tasks": total_tasks,
        "completed_tasks": completed_tasks,
        "pending_tasks": total_tasks - completed_tasks,
        "progress_percentage": progress
    }
