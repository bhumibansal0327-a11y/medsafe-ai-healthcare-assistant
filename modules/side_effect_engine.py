import json
import ollama

DATABASE_PATH = "database/medicine_db.json"

HIGH_RISK_SIDE_EFFECTS = [
    "breathing difficulty",
    "severe rash",
    "unconscious",
    "swelling of face",
    "seizure"
]

def load_database():
    with open(DATABASE_PATH, "r") as f:
        return json.load(f)


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

    # High risk keywords
    for keyword in HIGH_RISK_SIDE_EFFECTS:
        if keyword in reported_effect:
            score += 50

    if score > 100:
        score = 100

    return score


def side_effect_risk_level(score):
    if score >= 80:
        return "CRITICAL"
    elif score >= 50:
        return "HIGH"
    elif score >= 20:
        return "MODERATE"
    else:
        return "LOW"


def generate_side_effect_guidance(age, medicines, reported_effect):
    prompt = f"""
You are an educational medical assistant.

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
End with: "This information is for educational purposes only."
"""

    response = ollama.chat(
        model="phi3",
        messages=[{"role": "user", "content": prompt}]
    )

    return response["message"]["content"]