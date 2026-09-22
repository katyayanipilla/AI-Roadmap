from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.roadmap import Roadmap
from app.auth.dependencies import get_current_user
from app.models.user import User
from app.roadmap.generator import generate_structured_roadmap

router = APIRouter()

@router.post("/generate")
def create_roadmap(role: str,
                   db: Session = Depends(get_db),
                   current_user: User = Depends(get_current_user)):

    roadmap_json = generate_structured_roadmap(role)

    roadmap = Roadmap(
        user_id=current_user.id,
        target_role=role,
        roadmap_data=roadmap_json
    )

    db.add(roadmap)
    db.commit()
    db.refresh(roadmap)

    return roadmap_json

@router.get("/my-roadmaps")
def get_my_roadmaps(db: Session = Depends(get_db),
                    current_user: User = Depends(get_current_user)):

    return db.query(Roadmap).filter(
        Roadmap.user_id == current_user.id
    ).all()