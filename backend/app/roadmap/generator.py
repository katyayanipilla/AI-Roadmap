from groq import Groq
from app.config import settings
import json

client = Groq(api_key=settings.GROQ_API_KEY)

def generate_structured_roadmap(role: str):

    prompt = f"""
    Create a structured 12-week roadmap for becoming a {role}.

    Include:
    - Weekly focus
    - Topics
    - Suggested resources (YouTube, documentation, projects)
    - Weekly project

    Return ONLY valid JSON:

    {{
      "weeks": [
        {{
          "week": 1,
          "focus": "",
          "topics": [],
          "resources": [],
          "project": ""
        }}
      ]
    }}
    """

    completion = client.chat.completions.create(
        model=settings.GROQ_MODEL,
        messages=[
            {"role": "system", "content": "Return only structured JSON."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.3
    )

    content = completion.choices[0].message.content
    return json.loads(content)