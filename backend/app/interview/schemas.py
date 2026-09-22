from pydantic import BaseModel

class StartInterviewSchema(BaseModel):
    career_goal: str

class AnswerSchema(BaseModel):
    answer: str

class InterviewEvaluation(BaseModel):
    technical_score: int
    communication_score: int
    confidence_score: int
    problem_solving_score: int
    overall_score: int
    feedback: str