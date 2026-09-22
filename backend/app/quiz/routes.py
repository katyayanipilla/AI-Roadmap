from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.auth.dependencies import get_current_user
from app.models.user import User
from app.models.quiz import Quiz, QuizAttempt
from app.quiz.generator import generate_quiz
from app.quiz.streak import update_streak
from datetime import datetime

router = APIRouter()

@router.post("/generate")
def create_quiz(subject: str,
                db: Session = Depends(get_db),
                current_user: User = Depends(get_current_user)):

    quiz_data = generate_quiz(subject)

    quiz = Quiz(
        user_id=current_user.id,
        subject=subject,
        questions=quiz_data
    )

    db.add(quiz)
    db.commit()
    db.refresh(quiz)

    return quiz_data


@router.post("/submit")
def submit_quiz(quiz_id: int,
                answers: dict,
                db: Session = Depends(get_db),
                current_user: User = Depends(get_current_user)):

    quiz = db.query(Quiz).filter(Quiz.id == quiz_id).first()

    score = 0
    total = len(quiz.questions["questions"])

    for index, question in enumerate(quiz.questions["questions"]):
        correct = question["correct_answer"]
        user_answer = answers.get(str(index))

        if user_answer == correct:
            score += 1

    attempt = QuizAttempt(
        quiz_id=quiz_id,
        user_id=current_user.id,
        score=score,
        total=total
    )

    db.add(attempt)
    db.commit()

    update_streak(current_user, db)

    skill_gap = 100 - int((score / total) * 100)

    return {
        "score": score,
        "total": total,
        "percentage": int((score / total) * 100),
        "skill_gap_percentage": skill_gap,
        "current_streak": current_user.streak
    }