from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.auth.utils import get_current_user
from app.models.user import User
from .models import Resume
from .schemas import ResumeGenerateSchema
from .service import generate_resume
from app.services.roadmap_service import generate_roadmap
from app.services.roadmap_service import generate_weekly_roadmap

router = APIRouter(prefix="/resume", tags=["Resume"])

@router.post("/generate")
def generate(data: ResumeGenerateSchema, db: Session = Depends(get_db), user: User = Depends(get_current_user)):

    result = generate_resume(data)

    resume = Resume(
        user_id=user.id,
        content=result["resume_content"],
        score=result["score"]
    )

    db.add(resume)
    db.commit()

    return result

@router.post("/resume")
def upload_resume(resume: ResumeGenerateSchema):

    roadmap = generate_roadmap(resume.skills)

    return roadmap


@router.post("/weekly")
def upload_resume_weekly(resume: ResumeGenerateSchema):
    roadmap = generate_weekly_roadmap(resume.skills)
    return roadmap