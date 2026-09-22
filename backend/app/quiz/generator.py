from groq import Groq
from app.config import settings
import json

client = Groq(api_key=settings.GROQ_API_KEY)

def generate_quiz(subject: str):

    prompt = f"""
    Generate 30 multiple choice questions for {subject}.

    Each question must have:
    - question
    - 4 options (A, B, C, D)
    - correct_answer (A/B/C/D)

    Return ONLY valid JSON:

    {{
      "questions": [
        {{
          "question": "",
          "options": {{
              "A": "",
              "B": "",
              "C": "",
              "D": ""
          }},
          "correct_answer": ""
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
        temperature=0.4
    )

    content = completion.choices[0].message.content
    return json.loads(content)