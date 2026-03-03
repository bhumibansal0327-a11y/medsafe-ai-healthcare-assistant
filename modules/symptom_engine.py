# ============================================
# MedSafe AI - Symptom Engine (Groq Version)
# ============================================

from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

MODEL_NAME = "llama-3.1-8b-instant"

HIGH_RISK_KEYWORDS = [
    "chest pain",
    "breathing difficulty",
    "unconscious",
    "severe bleeding",
    "seizure"
]


def basic_symptom_risk(symptoms_text):

    symptoms_text = symptoms_text.lower()

    for keyword in HIGH_RISK_KEYWORDS:
        if keyword in symptoms_text:
            return "HIGH"

    return "LOW"


def generate_symptom_guidance(symptoms_text):

    prompt = f"""
A user reports the following symptoms:
{symptoms_text}

Provide:
- Possible general reasons (non-diagnostic)
- Basic home care suggestions
- Lifestyle tips
- Warning signs to watch for

Do NOT diagnose.
Do NOT prescribe medication.
Encourage seeking medical care if symptoms persist.

End with:
"This information is for educational purposes only."
"""

    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": "You are an educational medical assistant."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
        )

        return response.choices[0].message.content

    except Exception as e:
        return f"AI error: {str(e)}"