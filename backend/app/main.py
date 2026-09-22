from fastapi import FastAPI
from app.database import engine, Base
from app.models import user
from app.users.routes import router as user_router
from app.auth.routes import router as auth_router
from app.models import roadmap
from app.models import quiz
from app.roadmap.routes import router as roadmap_router
from app.quiz.routes import router as quiz_router
from app.interview.routes import router as interview_router
from app.resume.routes import router as resume_router




Base.metadata.create_all(bind=engine)

app = FastAPI(title="AI Career Platform API")

app.include_router(resume_router)

app.include_router(auth_router, prefix="/auth", tags=["Authentication"])

app.include_router(user_router, prefix="/users", tags=["Users"])

app.include_router(roadmap_router, prefix="/roadmap", tags=["Roadmap"])


app.include_router(quiz_router, prefix="/quiz", tags=["Quiz"])

@app.get("/")
def root():
    return {"message": "AI Career Platform API Running"}

app.include_router(interview_router)