

from datetime import date, datetime
from pydantic import BaseModel, ConfigDict, EmailStr, Field


# user schemas
class UserCreate(BaseModel):
    username: str = Field(min_length=3, max_length=100)
    email: EmailStr
    password: str = Field(min_length=8)
    role: str = "employee"


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    role: str

    model_config = ConfigDict(from_attributes=True)


# token schema
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


# onboarding schemas
class OnboardingCreate(BaseModel):
    employee_id: int
    task_name: str = Field(min_length=1, max_length=200)
    status: str = "PENDING"
    due_date: date | None = None


class OnboardingResponse(BaseModel):
    id: int
    employee_id: int
    task_name: str
    status: str
    due_date: date | None

    model_config = ConfigDict(from_attributes=True)


# resignation schemas
class ResignationCreate(BaseModel):
    reason: str = Field(min_length=1)
    notice_period: int = Field(gt=0)


class ResignationUpdate(BaseModel):
    status: str = Field(pattern="^(APPROVED|REJECTED)$")


class ResignationResponse(BaseModel):
    id: int
    employee_id: int
    reason: str
    notice_period: int
    status: str
    created_at: datetime | None = None

    model_config = ConfigDict(from_attributes=True)


# announcement schemas
class AnnouncementCreate(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    message: str = Field(min_length=1)


class AnnouncementResponse(BaseModel):
    id: int
    title: str
    message: str
    created_by: int
    created_at: datetime | None = None

    model_config = ConfigDict(from_attributes=True)


# task schemas
class TaskCreate(BaseModel):
    assigned_to: int
    title: str = Field(min_length=1, max_length=200)
    description: str | None = None
    due_date: date | None = None


class TaskUpdate(BaseModel):
    status: str = Field(pattern="^(PENDING|COMPLETED)$")


class TaskResponse(BaseModel):
    id: int
    assigned_to: int
    title: str
    description: str | None
    due_date: date | None
    status: str

    model_config = ConfigDict(from_attributes=True)


# feedback schemas
class FeedbackCreate(BaseModel):
    message: str = Field(min_length=1)
    rating: int = Field(ge=1, le=5)


class FeedbackResponse(BaseModel):
    id: int
    employee_id: int
    message: str
    rating: int
    created_at: datetime | None = None

    model_config = ConfigDict(from_attributes=True)


# profile schemas
class ProfileUpdate(BaseModel):
    username: str | None = Field(default=None, min_length=3, max_length=100)
    email: EmailStr | None = None


class PasswordChange(BaseModel):
    current_password: str
    new_password: str = Field(min_length=8)
