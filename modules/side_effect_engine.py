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


import json
import os
import re

from groq import Groq
from dotenv import load_dotenv


load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

MODEL_NAME = "openai/gpt-oss-20b"

DATABASE_PATH = "database/medicine_db.json"


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


def load_database():

    try:

        with open(
            DATABASE_PATH,
            "r",
            encoding="utf-8"
        ) as file:

            data = json.load(file)

        return data.get(
            "medicines",
            data
        )

    except Exception as e:

        print("Database error:", e)

        return {}


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

    if known in reported:
        return True

    known_words = known.split()
    reported_words = reported.split()

    for word in known_words:

        if word in reported_words:
            continue

        if word == "nausea" and "nauseous" in reported_words:
            continue

        if word == "vomiting" and "vomit" in reported_words:
            continue

        if word == "dizziness" and "dizzy" in reported_words:
            continue

        if word == "headache" and "headaches" in reported_words:
            continue

        if word == "rash" and "rashes" in reported_words:
            continue

        if word == "swelling" and "swollen" in reported_words:
            continue

        return False

    return True


def calculate_side_effect_risk(
    age,
    medicines,
    reported_effect
):

    data = load_database()

    score = 0

    reported_effect = normalize_text(
        reported_effect
    )

    if not medicines:
        return 0

    matched_effects = []

    for medicine in medicines:

        medicine_name = normalize_text(
            medicine
        )

        medicine_info = data.get(
            medicine_name
        )

        if medicine_info is None:

            for db_name in data:

                if normalize_text(
                    db_name
                ) == medicine_name:

                    medicine_info = data[db_name]

                    break

        if not medicine_info:
            continue

        known_effects = medicine_info.get(
            "common_side_effects",
            []
        )

        for effect in known_effects:

            if effect_matches(
                reported_effect,
                effect
            ):

                if effect not in matched_effects:

                    matched_effects.append(
                        effect
                    )

    # Known medicine side effect
    if len(matched_effects) > 0:

        score += min(
            len(matched_effects) * 25,
            50
        )

    # Age factor
    try:

        age = int(age)

    except (ValueError, TypeError):

        age = 0

    if age >= 75:

        score += 20

    elif age >= 60:

        score += 10

    # High-risk symptoms
    for keyword in HIGH_RISK_SIDE_EFFECTS:

        if effect_matches(
            reported_effect,
            keyword
        ):

            score += 50

    # Multiple medicines
    if len(medicines) >= 3:

        score += 10

    return min(
        score,
        100
    )


def side_effect_risk_level(score):

    if score >= 80:

        return "CRITICAL"

    elif score >= 50:

        return "HIGH"

    elif score >= 20:

        return "MODERATE"

    else:

        return "LOW"


def generate_side_effect_guidance(
    age,
    medicines,
    reported_effect
):

    medicine_text = ", ".join(
        medicines
    )

    prompt = f"""
You are an educational medicine safety assistant.

Age:
{age}

Medicines:
{medicine_text}

Reported experience:
{reported_effect}

Explain:

1. Possible general explanation
2. Whether the symptom may be related to a medicine
3. One precaution
4. When to contact a doctor
5. Emergency warning signs if relevant

Important:
- Do not diagnose.
- Do not prescribe medication.
- Do not tell the user to start, stop,
  or change medication.
- Do not claim the medicine definitely
  caused the symptom.
- Explain that symptoms may have other causes.
- If breathing difficulty, facial swelling,
  seizure, unconsciousness, severe rash,
  or chest pain is present, recommend
  urgent medical evaluation.

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
                        "medical safety assistant."
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

        return "AI error: " + str(e)
