# ============================================
# MedSafe AI - Emergency Risk Engine
# ============================================

import ollama

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
    """
    Calculates risk score (0–100) based on detected keywords.
    Returns:
        score (int)
        matched_keywords (list)
    """
    symptoms_text = symptoms_text.lower()
    score = 0
    matched_keywords = []

    for keyword, points in RISK_POINTS.items():
        if keyword in symptoms_text:
            score += points
            matched_keywords.append(keyword)

    # Cap score at 100
    if score > 100:
        score = 100

    return score, matched_keywords


# --------------------------------------------
# Risk Level Classification
# --------------------------------------------

def risk_level_from_score(score):
    """
    Converts numeric score into risk category.
    """
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
    """
    Generates educational emergency guidance using LLM.
    """

    prompt = f"""
You are an educational medical safety assistant.

The user reported the following emergency-related symptoms:
{symptoms_text}

The calculated emergency risk level is: {risk_level}

Provide:
- Why these symptoms may be concerning
- General immediate precautions
- Clear advice on when to seek medical care

Do NOT diagnose.
Do NOT prescribe medication.
Do NOT provide treatment plans.
Keep the tone calm, educational, and supportive.

End with:
"This information is for educational purposes only and does not replace professional medical advice."
"""

    try:
        response = ollama.chat(
            model="phi3",
            messages=[{"role": "user", "content": prompt}]
        )

        return response["message"]["content"]

    except Exception as e:
        return f"AI guidance unavailable. Error: {str(e)}"