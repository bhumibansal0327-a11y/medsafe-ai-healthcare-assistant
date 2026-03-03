# ============================================
# MedSafe AI - Emergency Risk Engine (Groq Version)
# ============================================

from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

MODEL_NAME = "llama-3.1-8b-instant"

# --------------------------------------------
# Risk Keyword Scoring Map
# --------------------------------------------

RISK_POINTS = {
    "chest pain": 40,
    "breathing difficulty": 50,
    "shortness of breath": 50,
    "unconscious": 70,
    "seizure": 60,
    "severe bleeding": 60,
    "high fever": 30,
    "persistent vomiting": 30,
    "severe headache": 40,
    "confusion": 40,
    "vision loss": 60,
    "paralysis": 70
}

# --------------------------------------------
# Calculate Risk Score
# --------------------------------------------

def calculate_risk_score(symptoms_text):

    symptoms_text = symptoms_text.lower()
    score = 0
    matched_keywords = []

    for keyword, points in RISK_POINTS.items():
        if keyword in symptoms_text:
            score += points
            matched_keywords.append(keyword)

    if score > 100:
        score = 100

    return score, matched_keywords

# --------------------------------------------
# Risk Level Classification
# --------------------------------------------

def risk_level_from_score(score):

    if score >= 80:
        return "CRITICAL"
    elif score >= 50:
        return "HIGH"
    elif score >= 20:
        return "MODERATE"
    else:
        return "LOW"

# --------------------------------------------
# AI Emergency Guidance Generator
# --------------------------------------------

def generate_emergency_guidance(symptoms_text, risk_level):

    prompt = f"""
Symptoms:
{symptoms_text}

Calculated Risk Level: {risk_level}

Explain:
- Why symptoms may be concerning
- Immediate precautions
- When to seek medical care

Do NOT diagnose.
Keep tone calm and educational.

End with:
"This information is for educational purposes only and does not replace professional medical advice."
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