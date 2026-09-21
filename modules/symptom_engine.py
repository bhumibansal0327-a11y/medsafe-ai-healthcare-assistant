# # ============================================
# # MedSafe AI - Symptom Engine (Groq Version)
# # ============================================

# from groq import Groq
# from dotenv import load_dotenv
# import os

# load_dotenv()

# client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# MODEL_NAME = "openai/gpt-oss-20b"

# HIGH_RISK_KEYWORDS = [
#    "chest pain",
#     "severe chest pain",
#     "difficulty breathing",
#     "breathing difficulty",
#     "shortness of breath",
#     "unconscious",
#     "fainted",
#     "severe bleeding",
#     "heavy bleeding",
#     "seizure",
#     "convulsion",
#     "stroke",
#     "face drooping",
#     "slurred speech",
#     "weakness on one side",
#     "severe allergic reaction",
#     "anaphylaxis",
#     "poisoning",
#     "snake bite",
#     "snakebite",
#     "electric shock",
#     "severe burn",
#     "major burn"
# ]


# def basic_symptom_risk(symptoms_text):

#     symptoms_text = symptoms_text.lower()

#     for keyword in HIGH_RISK_KEYWORDS:
#         if keyword in symptoms_text:
#             return "HIGH"

#     return "LOW"


# def generate_symptom_guidance(symptoms_text):

#     prompt = f"""
# A user reports the following symptoms:
# {symptoms_text}

# Provide:
# - Possible general reasons (non-diagnostic)
# - Basic home care suggestions
# - Lifestyle tips
# - Warning signs to watch for

# Do NOT diagnose.
# Do NOT prescribe medication.
# Encourage seeking medical care if symptoms persist.

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


# ============================================
# MedSafe AI - India Symptom Engine (Groq)
# ============================================

from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

MODEL_NAME = "openai/gpt-oss-20b"


# ============================================
# HIGH-RISK SYMPTOMS
# ============================================

HIGH_RISK_KEYWORDS = [
    "chest pain",
    "severe chest pain",
    "difficulty breathing",
    "breathing difficulty",
    "shortness of breath",
    "unconscious",
    "fainted",
    "severe bleeding",
    "heavy bleeding",
    "seizure",
    "convulsion",
    "stroke",
    "face drooping",
    "slurred speech",
    "weakness on one side",
    "severe allergic reaction",
    "anaphylaxis",
    "poisoning",
    "snake bite",
    "snakebite",
    "electric shock",
    "severe burn",
    "major burn",
]


def basic_symptom_risk(symptoms_text):

    symptoms_text = symptoms_text.lower()

    for keyword in HIGH_RISK_KEYWORDS:

        if keyword in symptoms_text:
            return "HIGH"

    return "LOW"


# ============================================
# INDIA-SPECIFIC EMERGENCY MESSAGE
# ============================================

def emergency_message():

    return """
⚠️ POSSIBLE MEDICAL EMERGENCY

Some of the symptoms you reported may require urgent medical attention.

If the person is unconscious, having severe difficulty breathing,
experiencing severe chest pain, having a seizure, suffering severe
bleeding, showing signs of stroke, or has another serious emergency:

• Call India's emergency number: 112
• Go to the nearest emergency department/hospital.
• Do not drive yourself if you are seriously unwell.
• If possible, have another person stay with you.

This AI cannot determine whether a condition is an emergency.
When in doubt, seek urgent medical care.
"""


# ============================================
# AI SYMPTOM GUIDANCE
# ============================================

def generate_symptom_guidance(symptoms_text):

    risk = basic_symptom_risk(symptoms_text)

    prompt = f"""
You are MedSafe AI, an educational health-information assistant
designed specifically for people in India.

A user reports these symptoms:

{symptoms_text}

Your task is to provide SAFE, GENERAL, NON-DIAGNOSTIC health information.

IMPORTANT RULES:

1. Do NOT diagnose the user.
2. Do NOT claim that the user has a particular disease.
3. Do NOT prescribe medicines.
4. Do NOT provide prescription drug dosages.
5. Do NOT tell the user to start, stop, or change prescription medication.
6. Do NOT assume the user's symptoms have a single cause.
7. Clearly distinguish possible causes from a diagnosis.
8. If symptoms could potentially indicate a serious condition,
   recommend appropriate medical evaluation.
9. Use healthcare guidance relevant to India.
10. Mention appropriate Indian healthcare options such as:
    - nearby clinic
    - qualified doctor
    - Primary Health Centre (PHC)
    - Community Health Centre (CHC)
    - district hospital
    - government hospital
    - private hospital
11. For emergencies in India, advise calling 112 or going to the
    nearest emergency department.
12. If the user appears to have a medical emergency, prioritize
    urgent-care instructions over lifestyle advice.
13. Do not unnecessarily alarm the user.
14. Use simple language that an average Indian user can understand.

Respond using this structure:

1. What the symptoms may generally be
   - Give a few broad, non-diagnostic possibilities.
   - Explain that symptoms alone cannot determine the cause.

2. What the person can do now
   - Give safe general self-care measures where appropriate.
   - Do not recommend prescription medication.

3. When to see a doctor
   - Explain situations where medical evaluation is appropriate.
   - Mention an Indian PHC, CHC, clinic, government hospital,
     or private hospital when appropriate.

4. Emergency warning signs
   - Clearly list serious symptoms requiring urgent medical attention.
   - If present, advise calling 112 or going to the nearest emergency
     department.

5. Prevention / lifestyle
   - Give relevant general lifestyle or prevention advice.

Keep the response concise and easy to understand.

The information is educational and does not replace examination,
diagnosis, or treatment by a qualified healthcare professional.

End with exactly:

"This information is for educational purposes only and is not a
substitute for professional medical advice."
"""

    try:

        response = client.chat.completions.create(
            model=MODEL_NAME,

            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are MedSafe AI, an educational medical "
                        "information assistant for users in India. "
                        "You must provide cautious, non-diagnostic "
                        "health information and encourage appropriate "
                        "professional medical care."
                    )
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],

            temperature=0.2,
        )

        ai_response = response.choices[0].message.content

        # Add emergency information if local rule engine
        # detects a high-risk symptom.
        if risk == "HIGH":

            return emergency_message() + "\n\n" + ai_response

        return ai_response

    except Exception as e:

        return f"AI error: {str(e)}"
