# # ============================================
# # MedSafe AI - Emergency Risk Engine (Groq Version)
# # ============================================

# from groq import Groq
# from dotenv import load_dotenv
# import os

# load_dotenv()

# client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# MODEL_NAME = "openai/gpt-oss-20b"

# # --------------------------------------------
# # Risk Keyword Scoring Map
# # --------------------------------------------

# RISK_POINTS = {
#     "chest pain": 40,
#     "breathing difficulty": 50,
#     "shortness of breath": 50,
#     "unconscious": 70,
#     "seizure": 60,
#     "severe bleeding": 60,
#     "high fever": 30,
#     "persistent vomiting": 30,
#     "severe headache": 40,
#     "confusion": 40,
#     "vision loss": 60,
#     "paralysis": 70
# }

# # --------------------------------------------
# # Calculate Risk Score
# # --------------------------------------------

# def calculate_risk_score(symptoms_text):

#     symptoms_text = symptoms_text.lower()
#     score = 0
#     matched_keywords = []

#     for keyword, points in RISK_POINTS.items():
#         if keyword in symptoms_text:
#             score += points
#             matched_keywords.append(keyword)

#     if score > 100:
#         score = 100

#     return score, matched_keywords

# # --------------------------------------------
# # Risk Level Classification
# # --------------------------------------------

# def risk_level_from_score(score):

#     if score >= 80:
#         return "CRITICAL"
#     elif score >= 50:
#         return "HIGH"
#     elif score >= 20:
#         return "MODERATE"
#     else:
#         return "LOW"

# # --------------------------------------------
# # AI Emergency Guidance Generator
# # --------------------------------------------

# def generate_emergency_guidance(symptoms_text, risk_level):

#     prompt = f"""
# Symptoms:
# {symptoms_text}

# Calculated Risk Level: {risk_level}

# Explain:
# - Why symptoms may be concerning
# - Immediate precautions
# - When to seek medical care

# Do NOT diagnose.
# Keep tone calm and educational.

# End with:
# "This information is for educational purposes only and does not replace professional medical advice."
# """

#     try:
#         response = client.chat.completions.create(
#             model=MODEL_NAME,
#             messages=[
#                 {"role": "system", "content": "You are an educational medical safety assistant."},
#                 {"role": "user", "content": prompt}
#             ],
#             temperature=0.3,
#         )

#         return response.choices[0].message.content

#     except Exception as e:
#         return f"AI error: {str(e)}"


# ============================================
# MedSafe AI - Emergency Risk Engine
# Groq + Fuzzy/Keyword Emergency Detection
# ============================================

from groq import Groq
from dotenv import load_dotenv
import os
import re

# --------------------------------------------
# Load Environment Variables
# --------------------------------------------

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY is not configured.")

client = Groq(api_key=GROQ_API_KEY)

MODEL_NAME = "openai/gpt-oss-20b"


# ============================================
# Emergency Risk Indicators
# ============================================

RISK_POINTS = {

    # -------------------------
    # Breathing
    # -------------------------
    "breathing difficulty": 50,
    "difficulty breathing": 50,
    "trouble breathing": 50,
    "shortness of breath": 50,
    "breathlessness": 50,
    "hard to breathe": 50,
    "having trouble breathing": 50,
    "cannot breathe": 80,
    "can't breathe": 80,
    "unable to breathe": 80,
    "not able to breathe": 80,

    # -------------------------
    # Chest / Heart
    # -------------------------
    "chest pain": 40,
    "chest hurts": 40,
    "chest pressure": 40,
    "chest tightness": 40,
    "pressure in chest": 40,
    "pain in chest": 40,

    # -------------------------
    # Consciousness / Neurological
    # -------------------------
    "unconscious": 70,
    "passed out": 70,
    "loss of consciousness": 70,
    "seizure": 60,
    "convulsion": 60,
    "confusion": 40,
    "severe confusion": 50,

    # -------------------------
    # Bleeding
    # -------------------------
    "severe bleeding": 60,
    "heavy bleeding": 60,
    "uncontrolled bleeding": 70,
    "bleeding heavily": 60,

    # -------------------------
    # Fever / Infection
    # -------------------------
    "high fever": 30,
    "very high fever": 40,

    # -------------------------
    # Vomiting
    # -------------------------
    "persistent vomiting": 30,
    "continuous vomiting": 30,
    "vomiting repeatedly": 30,
    "severe vomiting": 40,

    # -------------------------
    # Head / Neurological
    # -------------------------
    "severe headache": 40,
    "worst headache": 60,
    "sudden severe headache": 60,

    # -------------------------
    # Vision
    # -------------------------
    "vision loss": 60,
    "loss of vision": 60,
    "cannot see": 70,
    "sudden blindness": 80,

    # -------------------------
    # Paralysis / Stroke-like
    # -------------------------
    "paralysis": 70,
    "paralyzed": 70,
    "face drooping": 60,
    "facial drooping": 60,
    "weakness on one side": 70,
    "one sided weakness": 70,
    "unable to move": 70
}


# ============================================
# Critical Emergency Phrases
# These override normal scoring.
# ============================================

CRITICAL_PHRASES = [

    "cannot breathe",
    "can't breathe",
    "unable to breathe",
    "not able to breathe",
    "not breathing",

    "unconscious",
    "passed out",
    "loss of consciousness",

    "severe bleeding",
    "heavy bleeding",
    "uncontrolled bleeding",

    "sudden blindness",

    "paralysis",
    "paralyzed",

    "weakness on one side",
    "one sided weakness"
]


# ============================================
# Text Normalization
# ============================================

def normalize_text(text):

    if not text:
        return ""

    text = text.lower()

    # Replace punctuation with spaces
    text = re.sub(r"[^a-z0-9\s']", " ", text)

    # Remove multiple spaces
    text = re.sub(r"\s+", " ", text)

    return text.strip()


# ============================================
# Calculate Emergency Risk Score
# ============================================

def calculate_risk_score(symptoms_text):

    text = normalize_text(symptoms_text)

    if not text:
        return 0, []

    score = 0
    matched_keywords = []

    # ----------------------------------------
    # Check critical emergency phrases first
    # ----------------------------------------

    for phrase in CRITICAL_PHRASES:

        if phrase in text:

            # Add phrase only once
            if phrase not in matched_keywords:
                matched_keywords.append(phrase)

    # ----------------------------------------
    # Normal risk scoring
    # ----------------------------------------

    for keyword, points in RISK_POINTS.items():

        if keyword in text:

            if keyword not in matched_keywords:
                matched_keywords.append(keyword)

            score += points

    # ----------------------------------------
    # Critical override
    # ----------------------------------------

    if any(phrase in text for phrase in CRITICAL_PHRASES):

        score = max(score, 80)

    # ----------------------------------------
    # Special breathing detection
    # ----------------------------------------
    # Handles natural language such as:
    #
    # "I am having trouble breathing"
    # "I have trouble breathing"
    # "I am finding it difficult to breathe"
    # "I feel breathless"
    # ----------------------------------------

    breathing_patterns = [
        r"trouble\s+breath",
        r"difficult(y)?\s+breath",
        r"hard\s+to\s+breath",
        r"struggl(e|ing)\s+to\s+breath",
        r"cannot\s+breath",
        r"can't\s+breath",
        r"unable\s+to\s+breath",
        r"shortness\s+of\s+breath",
        r"breathless"
    ]

    breathing_detected = False

    for pattern in breathing_patterns:

        if re.search(pattern, text):

            breathing_detected = True
            break

    if breathing_detected:

        if "breathing difficulty" not in matched_keywords:
            matched_keywords.append("breathing difficulty")

        # Ensure breathing problems are never scored as zero
        score = max(score, 50)

    # ----------------------------------------
    # Cap score
    # ----------------------------------------

    score = min(score, 100)

    return score, matched_keywords


# ============================================
# Risk Level Classification
# ============================================

def risk_level_from_score(score):

    if score >= 80:
        return "CRITICAL"

    elif score >= 50:
        return "HIGH"

    elif score >= 20:
        return "MODERATE"

    else:
        return "LOW"


# ============================================
# AI Emergency Guidance Generator
# ============================================

def generate_emergency_guidance(symptoms_text, risk_level):

    prompt = f"""
You are an educational medical safety assistant.

User-reported symptoms:
{symptoms_text}

Calculated emergency risk level:
{risk_level}

Provide concise, safety-focused guidance.

Explain:

1. Why the reported symptoms may be concerning.
2. What immediate safety precautions the person should take.
3. When emergency medical care should be sought.
4. If symptoms could represent a medical emergency, clearly recommend
   contacting local emergency services or going to an emergency department.

Important rules:

- Do NOT diagnose the person.
- Do NOT claim certainty about the cause.
- Do NOT recommend prescription medication.
- Do NOT tell the user to ignore severe symptoms.
- Keep the tone calm, clear, and educational.
- For potentially life-threatening symptoms, prioritize immediate
  professional medical evaluation over additional questioning.

End with:

"This information is for educational purposes only and does not replace professional medical advice."
"""

    try:

        response = client.chat.completions.create(
            model=MODEL_NAME,

            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are an educational medical safety assistant. "
                        "Your role is to provide safety-oriented information, "
                        "not diagnosis or treatment."
                    )
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],

            temperature=0.2
        )

        return response.choices[0].message.content

    except Exception as e:

        return (
            "AI guidance could not be generated.\n\n"
            "Please rely on the calculated emergency risk and seek "
            "professional medical evaluation when appropriate.\n\n"
            f"Technical error: {str(e)}"
        )

