

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from models import Announcement, User
from schemas import AnnouncementCreate, AnnouncementResponse
from auth import get_current_user, require_hr_or_admin

router = APIRouter()


# create announcement (hr/admin only)
@router.post("/", response_model=AnnouncementResponse)
def create_announcement(
    announcement: AnnouncementCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_hr_or_admin)
):
    new_announcement = Announcement(
        title=announcement.title,
        message=announcement.message,
        created_by=current_user.id
    )

    db.add(new_announcement)
    db.commit()
    db.refresh(new_announcement)

    return new_announcement


# view all announcements
@router.get("/", response_model=list[AnnouncementResponse])
def get_announcements(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return (
        db.query(Announcement)
        .order_by(Announcement.created_at.desc())
        .all()
    )


# view announcement details
@router.get("/{announcement_id}", response_model=AnnouncementResponse)
def get_announcement(
    announcement_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    announcement = db.query(Announcement).filter(
        Announcement.id == announcement_id
    ).first()

    if not announcement:
        raise HTTPException(
            status_code=404,
            detail="Announcement not found"
        )

    return announcement


# delete announcement (hr/admin only)
@router.delete("/{announcement_id}")
def delete_announcement(
    announcement_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_hr_or_admin)
):
    announcement = db.query(Announcement).filter(
        Announcement.id == announcement_id
    ).first()

    if not announcement:
        raise HTTPException(
            status_code=404,
            detail="Announcement not found"
        )

    db.delete(announcement)
    db.commit()

    return {"message": "Announcement deleted successfully"}
