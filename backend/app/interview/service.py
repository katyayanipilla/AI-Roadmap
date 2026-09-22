import os
from groq import Groq
import json

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def generate_next_question(career_goal, history):
    prompt = f"""
You are a senior technical interviewer.

Career Goal: {career_goal}

Conversation so far:
{history}

Ask the next professional interview question.
Ask follow-up if needed.
Be realistic and corporate.
Return only the question.
"""

    response = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )

    return response.choices[0].message.content


def evaluate_interview(career_goal, conversation):
    prompt = f"""
You are a corporate hiring panel.

Evaluate this full interview for a {career_goal} candidate.

Conversation:
{conversation}

Return JSON:
{{
  "technical_score": 0-100,
  "communication_score": 0-100,
  "confidence_score": 0-100,
  "problem_solving_score": 0-100,
  "overall_score": 0-100,
  "feedback": "Detailed professional feedback"
}}
"""

    response = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )

    return json.loads(response.choices[0].message.content)