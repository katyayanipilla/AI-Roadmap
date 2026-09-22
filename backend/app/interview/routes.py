from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.auth.utils import get_current_user
from .models import InterviewSession, InterviewMessage
from .schemas import StartInterviewSchema, AnswerSchema
from .service import generate_next_question, evaluate_interview

router = APIRouter(prefix="/interview", tags=["Interview"])

@router.post("/start")
def start_interview(data: StartInterviewSchema, db: Session = Depends(get_db), user=Depends(get_current_user)):

    session = InterviewSession(
        user_id=user.id,
        career_goal=data.career_goal
    )

    db.add(session)
    db.commit()
    db.refresh(session)

    first_question = generate_next_question(data.career_goal, "No previous conversation")

    msg = InterviewMessage(
        session_id=session.id,
        role="interviewer",
        content=first_question
    )

    db.add(msg)
    db.commit()

    return {
        "session_id": session.id,
        "question": first_question
    }


@router.post("/{session_id}/answer")
def answer_question(session_id: int, data: AnswerSchema, db: Session = Depends(get_db), user=Depends(get_current_user)):

    session = db.query(InterviewSession).filter_by(id=session_id, user_id=user.id).first()

    if not session:
        return {"error": "Session not found"}

    # Save candidate answer
    answer_msg = InterviewMessage(
        session_id=session.id,
        role="candidate",
        content=data.answer
    )
    db.add(answer_msg)
    db.commit()

    # Fetch full conversation
    messages = db.query(InterviewMessage).filter_by(session_id=session.id).all()

    history = "\n".join([f"{m.role}: {m.content}" for m in messages])

    next_question = generate_next_question(session.career_goal, history)

    interviewer_msg = InterviewMessage(
        session_id=session.id,
        role="interviewer",
        content=next_question
    )

    db.add(interviewer_msg)
    db.commit()

    return {"next_question": next_question}


@router.post("/{session_id}/complete")
def complete_interview(session_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):

    session = db.query(InterviewSession).filter_by(id=session_id, user_id=user.id).first()

    if not session:
        return {"error": "Session not found"}

    messages = db.query(InterviewMessage).filter_by(session_id=session.id).all()

    conversation = "\n".join([f"{m.role}: {m.content}" for m in messages])

    evaluation = evaluate_interview(session.career_goal, conversation)

    session.status = "completed"
    db.commit()

    return evaluation