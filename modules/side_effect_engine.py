# ============================================
# MedSafe AI - Side Effect Engine (Groq Version)
# ============================================

import json
from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))
MODEL_NAME = "llama-3.1-8b-instant"

DATABASE_PATH = "database/medicine_db.json"

HIGH_RISK_SIDE_EFFECTS = [
    "breathing difficulty",
    "severe rash",
    "unconscious",
    "swelling of face",
    "seizure"
]


# --------------------------------------------
# Load Medicine Database
# --------------------------------------------

def load_database():
    with open(DATABASE_PATH, "r") as f:
        return json.load(f)


# --------------------------------------------
# Risk Score Calculation
# --------------------------------------------

def calculate_side_effect_risk(age, medicines, reported_effect):

    data = load_database()
    score = 0
    reported_effect = reported_effect.lower()

    for med in medicines:
        if med in data:
            known_effects = data[med].get("common_side_effects", [])
            for effect in known_effects:
                if effect.lower() in reported_effect:
                    score += 30

    # Age-based risk
    if age >= 60:
        score += 20

    # High-risk keywords
    for keyword in HIGH_RISK_SIDE_EFFECTS:
        if keyword in reported_effect:
            score += 50

    if score > 100:
        score = 100

    return score


# --------------------------------------------
# Risk Level Classification
# --------------------------------------------

def side_effect_risk_level(score):

    if score >= 80:
        return "CRITICAL"
    elif score >= 50:
        return "HIGH"
    elif score >= 20:
        return "MODERATE"
    else:
        return "LOW"


# --------------------------------------------
# AI Guidance (Groq)
# --------------------------------------------

def generate_side_effect_guidance(age, medicines, reported_effect):

    prompt = f"""
User details:
Age: {age}
Medicines taken: {medicines}
Reported experience: {reported_effect}

Provide:
- Possible general explanation
- Whether symptom may relate to medicine
- One precaution to watch for
- When to consult a doctor

Do NOT diagnose.
Do NOT prescribe medication.

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