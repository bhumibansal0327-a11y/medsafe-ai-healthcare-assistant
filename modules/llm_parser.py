# ============================================
# MedSafe AI - LLM Parser (Groq Version)
# ============================================

from groq import Groq
from dotenv import load_dotenv
import os
import json
import re

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

MODEL_NAME = "llama-3.1-8b-instant"


def generate_interaction_summary(warnings):

    prompt = f"""
Explain the following medicine interaction(s) clearly in simple language.
Do NOT diagnose.
Do NOT recommend stopping medication.
Encourage consulting a healthcare professional.

End with:
"This information is for educational purposes only."

Interaction Data:
{warnings}
"""

    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": "You are an educational medical safety assistant."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
        )

        return response.choices[0].message.content

    except Exception as e:
        return f"AI error: {str(e)}"


def parse_prescription_text(raw_text):

    prompt = f"""
Extract medicine names and active salts from the prescription text.

Return ONLY valid JSON in this format:

{{
  "medicines": [
    {{
      "name": "",
      "salt": ""
    }}
  ]
}}

Prescription Text:
{raw_text}
"""

    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": "You are an assistant that returns only valid JSON."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.2,
        )

        content = response.choices[0].message.content

        match = re.search(r'\{.*\}', content, re.DOTALL)
        if match:
            return json.loads(match.group())

        return {"error": "No JSON detected"}

    except Exception as e:
        return {"error": str(e)}