from sqlalchemy import Column, Integer, String, Text, Date, DateTime, ForeignKey
from sqlalchemy.sql import func
from database import Base


# user model
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), unique=True, nullable=False)
    email = Column(String(150), unique=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    role = Column(String(20), default="employee", nullable=False)


# employee onboarding model
class Onboarding(Base):
    __tablename__ = "onboarding"

    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    task_name = Column(String(200), nullable=False)
    status = Column(String(20), default="PENDING", nullable=False)
    due_date = Column(Date, nullable=True)


# resignation model
class Resignation(Base):
    __tablename__ = "resignations"

    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    reason = Column(Text, nullable=False)
    notice_period = Column(Integer, nullable=False)
    status = Column(String(20), default="PENDING", nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


# announcement model
class Announcement(Base):
    __tablename__ = "announcements"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    message = Column(Text, nullable=False)
    created_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


# task assignment model
class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    assigned_to = Column(Integer, ForeignKey("users.id"), nullable=False)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    due_date = Column(Date, nullable=True)
    status = Column(String(20), default="PENDING", nullable=False)


# employee feedback model
class Feedback(Base):
    __tablename__ = "feedback"

    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    message = Column(Text, nullable=False)
    rating = Column(Integer, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
