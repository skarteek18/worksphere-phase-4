

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from models import Task, User
from schemas import TaskCreate, TaskUpdate, TaskResponse
from auth import get_current_user, require_hr_or_admin

router = APIRouter()


# assign task to employee (hr/admin only)
@router.post("/", response_model=TaskResponse)
def create_task(
    task: TaskCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_hr_or_admin)
):
    employee = db.query(User).filter(
        User.id == task.assigned_to
    ).first()

    if not employee:
        raise HTTPException(
            status_code=404,
            detail="Employee not found"
        )

    new_task = Task(
        assigned_to=task.assigned_to,
        title=task.title,
        description=task.description,
        due_date=task.due_date,
        status="PENDING"
    )

    db.add(new_task)
    db.commit()
    db.refresh(new_task)

    return new_task


# view tasks (employees see only their own tasks)
@router.get("/", response_model=list[TaskResponse])
def get_tasks(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    query = db.query(Task)

    if current_user.role.lower() not in ["admin", "hr"]:
        query = query.filter(
            Task.assigned_to == current_user.id
        )

    return query.order_by(Task.id.desc()).all()


# view one task
@router.get("/{task_id}", response_model=TaskResponse)
def get_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    task = db.query(Task).filter(Task.id == task_id).first()

    if not task:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    if (
        current_user.role.lower() not in ["admin", "hr"]
        and task.assigned_to != current_user.id
    ):
        raise HTTPException(
            status_code=403,
            detail="You cannot view another employee's task"
        )

    return task


# update task status
@router.patch("/{task_id}/status", response_model=TaskResponse)
def update_task_status(
    task_id: int,
    update: TaskUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    task = db.query(Task).filter(Task.id == task_id).first()

    if not task:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    if (
        current_user.role.lower() not in ["admin", "hr"]
        and task.assigned_to != current_user.id
    ):
        raise HTTPException(
            status_code=403,
            detail="You cannot update another employee's task"
        )

    task.status = update.status
    db.commit()
    db.refresh(task)

    return task


# delete task (hr/admin only)
@router.delete("/{task_id}")
def delete_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_hr_or_admin)
):
    task = db.query(Task).filter(Task.id == task_id).first()

    if not task:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    db.delete(task)
    db.commit()

    return {"message": "Task deleted successfully"}
