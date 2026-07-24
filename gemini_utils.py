
import streamlit as st

from google import genai
import json

print("free key: AQ.Ab8RN6J6cE2ijoOBAoV0A974CwYE-68R6N8yIZpJ1Eenz27iNQ\n")

key = st.text_input(
    "Enter your Gemini API Key",
    type="password"
)

if not key:
    st.info("Please enter your Gemini API key.")
    st.stop()

client = genai.Client(api_key=key)

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
