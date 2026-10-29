

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database import Base, engine
from auth import router as auth_router
from onboarding import router as onboarding_router
from resignations import router as resignations_router
from announcements import router as announcements_router
from tasks import router as tasks_router
from integrations import router as integrations_router
from feedback import router as feedback_router
from profile import router as profile_router

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="worksphere hrms",
    description="phase 4 - employee experience and system integrations",
    version="4.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(auth_router, prefix="/auth", tags=["authentication"])
app.include_router(onboarding_router, prefix="/onboarding", tags=["onboarding"])
app.include_router(resignations_router, prefix="/resignations", tags=["resignations"])
app.include_router(announcements_router, prefix="/announcements", tags=["announcements"])
app.include_router(tasks_router, prefix="/tasks", tags=["tasks"])
app.include_router(integrations_router, prefix="/integrations", tags=["integrations"])
app.include_router(feedback_router, prefix="/feedback", tags=["feedback"])
app.include_router(profile_router, prefix="/profile", tags=["profile"])


@app.get("/")
def home():
    return {
        "message": "welcome to worksphere hrms phase 4",
        "status": "running"
    }


@app.get("/health")
def health_check():
    return {"status": "healthy"}
