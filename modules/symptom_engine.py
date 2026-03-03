import ollama

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
You are an educational medical assistant.

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
End with: "This information is for educational purposes only."
"""

    response = ollama.chat(
        model="phi3",
        messages=[{"role": "user", "content": prompt}]
    )

    return response["message"]["content"]