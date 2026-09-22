from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app.database import get_db
from app.models.user import User
from app.auth.dependencies import get_current_user

router = APIRouter()

class ProfileUpdate(BaseModel):
    username: str | None = None
    profile_image: str | None = None

@router.get("/me")
def get_profile(current_user: User = Depends(get_current_user)):
    return current_user

@router.put("/update")
def update_profile(data: ProfileUpdate,
                   db: Session = Depends(get_db),
                   current_user: User = Depends(get_current_user)):

    if data.username:
        current_user.username = data.username

    if data.profile_image:
        current_user.profile_image = data.profile_image

    db.commit()
    db.refresh(current_user)

    return {"message": "Profile updated", "user": current_user}