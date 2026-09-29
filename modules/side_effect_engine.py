# # ============================================
# # MedSafe AI - Side Effect Engine (Groq Version)
# # ============================================

# import json
# from groq import Groq
# from dotenv import load_dotenv
# import os

# load_dotenv()

# client = Groq(api_key=os.getenv("GROQ_API_KEY"))
# MODEL_NAME = "openai/gpt-oss-20b"

# DATABASE_PATH = "database/medicine_db.json"

# HIGH_RISK_SIDE_EFFECTS = [
#     "breathing difficulty",
#     "severe rash",
#     "unconscious",
#     "swelling of face",
#     "seizure"
# ]


# # --------------------------------------------
# # Load Medicine Database
# # --------------------------------------------

# def load_database():
#     with open(DATABASE_PATH, "r") as f:
#         return json.load(f)


# # --------------------------------------------
# # Risk Score Calculation
# # --------------------------------------------

# def calculate_side_effect_risk(age, medicines, reported_effect):

#     data = load_database()
#     score = 0
#     reported_effect = reported_effect.lower()

#     for med in medicines:
#         if med in data:
#             known_effects = data[med].get("common_side_effects", [])
#             for effect in known_effects:
#                 if effect.lower() in reported_effect:
#                     score += 30

#     # Age-based risk
#     if age >= 60:
#         score += 20

#     # High-risk keywords
#     for keyword in HIGH_RISK_SIDE_EFFECTS:
#         if keyword in reported_effect:
#             score += 50

#     if score > 100:
#         score = 100

#     return score


# # --------------------------------------------
# # Risk Level Classification
# # --------------------------------------------

# def side_effect_risk_level(score):

#     if score >= 80:
#         return "CRITICAL"
#     elif score >= 50:
#         return "HIGH"
#     elif score >= 20:
#         return "MODERATE"
#     else:
#         return "LOW"


# # --------------------------------------------
# # AI Guidance (Groq)
# # --------------------------------------------

# def generate_side_effect_guidance(age, medicines, reported_effect):

#     prompt = f"""
# User details:
# Age: {age}
# Medicines taken: {medicines}
# Reported experience: {reported_effect}

# Provide:
# - Possible general explanation
# - Whether symptom may relate to medicine
# - One precaution to watch for
# - When to consult a doctor

# Do NOT diagnose.
# Do NOT prescribe medication.

# End with:
# "This information is for educational purposes only."
# """

#     try:
#         response = client.chat.completions.create(
#             model=MODEL_NAME,
#             messages=[
#                 {"role": "system", "content": "You are an educational medical assistant."},
#                 {"role": "user", "content": prompt}
#             ],
#             temperature=0.3,
#         )

#         return response.choices[0].message.content

#     except Exception as e:
#         return f"AI error: {str(e)}"


```python
# ============================================
# MedSafe AI - Side Effect Engine
# ============================================

import json
import os
import re

from groq import Groq
from dotenv import load_dotenv


# ============================================
# ENVIRONMENT
# ============================================

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

MODEL_NAME = "openai/gpt-oss-20b"

DATABASE_PATH = "database/medicine_db.json"


# ============================================
# HIGH-RISK SYMPTOMS
# ============================================

HIGH_RISK_SIDE_EFFECTS = [
    "breathing difficulty",
    "difficulty breathing",
    "shortness of breath",
    "severe rash",
    "unconscious",
    "loss of consciousness",
    "swelling of face",
    "facial swelling",
    "seizure",
    "seizures",
    "chest pain"
]


# ============================================
# LOAD MEDICINE DATABASE
# ============================================

def load_database():

    try:

        with open(
            DATABASE_PATH,
            "r",
            encoding="utf-8"
        ) as f:

            data = json.load(f)

        # Supports both formats:
        #
        # {
        #     "medicines": {
        #         "paracetamol": {...}
        #     }
        # }
        #
        # AND:
        #
        # {
        #     "paracetamol": {...}
        # }

        return data.get("medicines", data)

    except Exception as e:

        print(f"Database error: {e}")

        return {}


# ============================================
# NORMALIZE TEXT
# ============================================

def normalize_text(text):

    if not text:
        return ""

    text = str(text).lower().strip()

    text = text.replace("-", " ")
    text = text.replace("_", " ")

    text = re.sub(
        r"[^\w\s]",
        " ",
        text
    )

    text = re.sub(
        r"\s+",
        " ",
        text
    )

    return text


# ============================================
# SIDE-EFFECT MATCHING
# ============================================

def effect_matches(
    reported_effect,
    known_effect
):

    reported = normalize_text(
        reported_effect
    )

    known = normalize_text(
        known_effect
    )

    if not reported or not known:
        return False

    # ----------------------------------------
    # Direct phrase match
    # ----------------------------------------

    if known in reported:
        return True

    # ----------------------------------------
    # Word match
    # ----------------------------------------

    known_words = set(
        known.split()
    )

    reported_words = set(
        reported.split()
    )

    if (
        known_words
        and known_words.issubset(reported_words)
    ):
        return True

    # ----------------------------------------
    # Common variations
    # ----------------------------------------

    variations = {

        "nausea": [
            "nauseous"
        ],

        "vomiting": [
            "vomit"
        ],

        "dizziness": [
            "dizzy"
        ],

        "headache": [
            "headaches"
        ],

        "diarrhea": [
            "diarrhoea"
        ],

        "rash": [
            "rashes"
        ],

        "swelling": [
            "swollen"
        ]
    }

    for word in known_words:

        if word in variations:

            for variation in variations[word]:

                if variation in reported_words:

                    return True

    return False


# ============================================
# CALCULATE SIDE-EFFECT RISK
# ============================================

def calculate_side_effect_risk(
    age,
    medicines,
    reported_effect
):

    data = load_database()

    reported_effect = normalize_text(
        reported_effect
    )

    score = 0

    matched_effects = []
    matched_medicines = []
    matched_high_risk = []

    # ========================================
    # VALIDATE MEDICINES
    # ========================================

    if not medicines:

        return 0

    # ========================================
    # CHECK MEDICINE SIDE EFFECTS
    # ========================================

    for med in medicines:

        med_key = normalize_text(
            med
        )

        medicine_info = data.get(
            med_key
        )

        # Case-insensitive lookup
        if medicine_info is None:

            for db_med, info in data.items():

                if normalize_text(
                    db_med
                ) == med_key:

                    medicine_info = info

                    break

        if not medicine_info:

            continue

        known_effects = medicine_info.get(
            "common_side_effects",
            []
        )

        medicine_matched = False

        for effect in known_effects:

            if effect_matches(
                reported_effect,
                effect
            ):

                matched_effects.append(
                    effect
                )

                medicine_matched = True

        if medicine_matched:

            matched_medicines.append(
                med
            )

    # ========================================
    # SCORE KNOWN SIDE EFFECTS
    # ========================================

    if matched_effects:

        score += min(
            len(matched_effects) * 25,
            50
        )

    # ========================================
    # AGE RISK
    # ========================================

    try:

        age = int(age)

    except (
        ValueError,
        TypeError
    ):

        age = 0

    if age >= 75:

        score += 20

    elif age >= 60:

        score += 10

    # ========================================
    # HIGH-RISK SYMPTOMS
    # ========================================

    for keyword in HIGH_RISK_SIDE_EFFECTS:

        if effect_matches(
            reported_effect,
            keyword
        ):

            matched_high_risk.append(
                keyword
            )

    if matched_high_risk:

        score += 50

    # ========================================
    # MULTIPLE MEDICINES
    # ========================================

    if len(medicines) >= 3:

        score += 10

    # ========================================
    # MAXIMUM SCORE
    # ========================================

    score = min(
        score,
        100
    )

    return score


# ============================================
# RISK LEVEL
# ============================================

def side_effect_risk_level(score):

    if score >= 80:

        return "CRITICAL"

    elif score >= 50:

        return "HIGH"

    elif score >= 20:

        return "MODERATE"

    else:

        return "LOW"


# ============================================
# AI GUIDANCE
# ============================================

def generate_side_effect_guidance(
    age,
    medicines,
    reported_effect
):

    medicine_text = (
        ", ".join(medicines)
        if medicines
        else "Not identified"
    )

    prompt = f"""
You are an educational medicine-safety assistant.

User age:
{age}

Medicines taken:
{medicine_text}

Reported experience:
{reported_effect}

Provide a concise educational response containing:

1. Possible general explanation
2. Whether the experience may be related to a medicine
3. One precaution to watch for
4. When to contact a doctor
5. Emergency warning signs if relevant

Important rules:

- Do NOT diagnose.
- Do NOT prescribe medication.
- Do NOT tell the user to start, stop,
  or change a medicine.
- Do NOT claim that the medicine definitely
  caused the symptom.
- Explain that symptoms can have other causes.
- If severe symptoms such as breathing difficulty,
  facial swelling, seizure, unconsciousness,
  severe rash, or chest pain are reported,
  recommend urgent/emergency medical evaluation.

End with:

"This information is for educational purposes only."
"""

    try:

        response = client.chat.completions.create(

            model=MODEL_NAME,

            messages=[

                {
                    "role": "system",
                    "content": (
                        "You are an educational "
                        "medical safety assistant. "
                        "Provide cautious, "
                        "non-diagnostic information."
                    )
                },

                {
                    "role": "user",
                    "content": prompt
                }

            ],

            temperature=0.3
        )

        return response.choices[0].message.content

    except Exception as e:

        return f"AI error: {str(e)}"
```
