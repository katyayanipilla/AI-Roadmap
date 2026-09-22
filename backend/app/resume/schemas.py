from pydantic import BaseModel

class ResumeGenerateSchema(BaseModel):
    career_goal: str
    skills: list[str]
    projects: list[str]
    experience_level: str