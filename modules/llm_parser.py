import ollama

import json
import re


def generate_interaction_summary(warnings):
    prompt = f"""
You are an educational medical safety assistant.

Explain the following medicine interaction(s) in simple language.
Do NOT diagnose.
Do NOT recommend stopping medication.
Encourage consulting a healthcare professional.
End with: "This information is for educational purposes only."

Interaction Data:
{warnings}
"""

    response = ollama.chat(
        model="phi3",
        messages=[{"role": "user", "content": prompt}]
    )

    return response["message"]["content"]

def parse_prescription_text(raw_text):
    prompt = f"""
You are a medical text parser.

From the following prescription text, extract medicine names and their active salts.

Return ONLY valid JSON in this format:

{{
  "medicines": [
    {{
      "name": "",
      "salt": ""
    }}
  ]
}}

No explanation. No extra text.

Prescription Text:
{raw_text}
"""

    response = ollama.chat(
        model="phi3",
        messages=[{"role": "user", "content": prompt}]
    )

    content = response["message"]["content"]

    # Extract JSON safely
    match = re.search(r'\{.*\}', content, re.DOTALL)
    if match:
        try:
            return json.loads(match.group())
        except:
            return {"error": "Invalid JSON from model"}

    return {"error": "No JSON detected"}