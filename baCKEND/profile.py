

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from passlib.context import CryptContext

from database import get_db
from models import User
from schemas import UserResponse, ProfileUpdate, PasswordChange
from auth import get_current_user

router = APIRouter()

password_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)

# temporary in-memory notification preferences
# use a database table for persistent preferences in production
notification_preferences = {}


class NotificationPreferences(BaseModel):
    email_notifications: bool = True
    task_notifications: bool = True
    announcement_notifications: bool = True


# view profile
@router.get("/", response_model=UserResponse)
def get_profile(
    current_user: User = Depends(get_current_user)
):
    return current_user


# update profile details
@router.put("/", response_model=UserResponse)
def update_profile(
    profile: ProfileUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if profile.username is not None:
        existing_username = db.query(User).filter(
            User.username == profile.username,
            User.id != current_user.id
        ).first()

        if existing_username:
            raise HTTPException(
                status_code=400,
                detail="Username already exists"
            )

        current_user.username = profile.username

    if profile.email is not None:
        existing_email = db.query(User).filter(
            User.email == profile.email,
            User.id != current_user.id
        ).first()

        if existing_email:
            raise HTTPException(
                status_code=400,
                detail="Email already exists"
            )

        current_user.email = profile.email

    db.commit()
    db.refresh(current_user)

    return current_user


# change password
@router.post("/change-password")
def change_password(
    password_data: PasswordChange,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if not password_context.verify(
        password_data.current_password,
        current_user.hashed_password
    ):
        raise HTTPException(
            status_code=400,
            detail="Current password is incorrect"
        )

    if password_data.current_password == password_data.new_password:
        raise HTTPException(
            status_code=400,
            detail="New password must be different from current password"
        )

    current_user.hashed_password = password_context.hash(
        password_data.new_password
    )

    db.commit()

    return {"message": "Password changed successfully"}


# view notification preferences
@router.get("/preferences", response_model=NotificationPreferences)
def get_preferences(
    current_user: User = Depends(get_current_user)
):
    return notification_preferences.get(
        current_user.id,
        NotificationPreferences().model_dump()
    )


# update notification preferences
@router.put("/preferences", response_model=NotificationPreferences)
def update_preferences(
    preferences: NotificationPreferences,
    current_user: User = Depends(get_current_user)
):
    notification_preferences[current_user.id] = preferences.model_dump()
    return preferences
