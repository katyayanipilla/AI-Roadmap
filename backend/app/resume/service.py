import os
from groq import Groq
import json

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def generate_resume(data):

    prompt = f"""
You are a senior corporate resume writer.

Generate a professional ATS-optimized resume for:

Career Goal: {data.career_goal}
Skills: {data.skills}
Projects: {data.projects}
Experience Level: {data.experience_level}

Return JSON:
{{
 "resume_content": "Full professional resume formatted cleanly",
 "score": 0-100,
 "improvements": "What to improve"
}}
"""

    response = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.5
    )

    return json.loads(response.choices[0].message.content)