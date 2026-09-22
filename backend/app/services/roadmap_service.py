def generate_roadmap(skills: list[str]):

    roadmap = {
        "current_skills": skills,
        "recommended_roles": [],
        "learning_path": []
    }

    if "python" in skills:
        roadmap["recommended_roles"].append("Backend Developer")
        roadmap["learning_path"].extend([
            "Advanced Python",
            "FastAPI",
            "SQL & Databases",
            "Docker",
            "System Design"
        ])

    if "machine learning" in skills:
        roadmap["recommended_roles"].append("ML Engineer")
        roadmap["learning_path"].extend([
            "Statistics",
            "Deep Learning",
            "MLOps",
            "Deployment"
        ])

    return roadmap

def generate_weekly_roadmap(skills: list[str], weeks: int = 12):
    roadmap = []
    base_topics = []

    if "python" in skills:
        base_topics += ["Advanced Python", "FastAPI", "SQL", "Docker", "System Design"]
    if "machine learning" in skills:
        base_topics += ["Statistics", "Deep Learning", "MLOps", "Deployment"]
    if "frontend" in skills:
        base_topics += ["HTML/CSS", "JavaScript", "React", "UI/UX"]

    # Divide topics across weeks
    for i in range(weeks):
        weekly = {
            "week": i + 1,
            "topics": base_topics[i::weeks],  # distribute topics
            "resources": [f"https://www.youtube.com/results?search_query={t.replace(' ', '+')}" for t in base_topics[i::weeks]]
        }
        roadmap.append(weekly)

    return {
        "skills": skills,
        "weeks": weeks,
        "roadmap": roadmap
    }