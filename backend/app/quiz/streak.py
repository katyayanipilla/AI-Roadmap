from datetime import datetime
from app.models.user import User

def update_streak(user: User, db):

    today = datetime.utcnow().date()
    last_active = user.created_at.date() if not hasattr(user, "last_quiz_date") else user.last_quiz_date

    if hasattr(user, "last_quiz_date") and user.last_quiz_date:
        diff = (today - user.last_quiz_date).days

        if diff == 1:
            user.streak += 1
        elif diff > 1:
            user.streak = 1
    else:
        user.streak = 1

    user.last_quiz_date = today
    db.commit()