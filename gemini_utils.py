
import streamlit as st

from google import genai
import json

print("enter a gemini key: ")

key =input()

client = genai.Client(
    api_key=key

)



def summarize_text(text):
    prompt = f"""
Summarize the following YouTube transcript.

Keep the summary short.

Use headings and bullet points.

Transcript:

{text}
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    return response.text


def generate_quiz(transcript, difficulty, num_questions):

    prompt = f"""
You are an expert teacher.

Create EXACTLY {num_questions} multiple-choice questions based on the following YouTube transcript.

Difficulty: {difficulty}

Rules:

- Return ONLY valid JSON.
- Do not include markdown.
- Exactly 4 options per question.
- Only one correct answer.
- Include a short explanation.

JSON format:

{{
    "quiz":[
        {{
            "question":"",

            "options":[
                "",
                "",
                "",
                ""
            ],

            "answer":"",

            "explanation":""
        }}
    ]
}}

Transcript:

{transcript}
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    text = response.text.strip()

    if text.startswith("```"):
        text = text.replace("```json", "").replace("```", "").strip()

    return json.loads(text)
