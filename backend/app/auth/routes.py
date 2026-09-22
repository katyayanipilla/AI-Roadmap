from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.auth.schemas import LoginSchema
from app.auth.utils import verify_password, create_access_token

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/login")
def login(data: LoginSchema, db: Session = Depends(get_db)):

    # 1️⃣ Find user
    user = db.query(User).filter(User.email == data.email).first()

    if not user:
        raise HTTPException(status_code=400, detail="Invalid credentials")

    # 2️⃣ Verify password
    if not verify_password(data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid credentials")

    # 3️⃣ Create JWT token
    token = create_access_token({"user_id": user.id})

    # 4️⃣ Return token
    return {
        "access_token": token,
        "token_type": "bearer"
    }