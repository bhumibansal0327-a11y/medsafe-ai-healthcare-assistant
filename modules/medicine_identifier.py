import json
from rapidfuzz import process

DATABASE_PATH = "database/medicine_db.json"

def load_medicine_names():
    with open(DATABASE_PATH, "r") as f:
        data = json.load(f)
    return list(data.keys())

def identify_medicines(user_input):
    medicine_list = load_medicine_names()
    detected = []

    inputs = [m.strip().lower() for m in user_input.split(",")]

    for med in inputs:
        match, score, _ = process.extractOne(med, medicine_list)
        if score >= 80:
            detected.append(match)

    return list(set(detected))