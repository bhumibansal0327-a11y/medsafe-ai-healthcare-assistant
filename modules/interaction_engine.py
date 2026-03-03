import json

DATABASE_PATH = "database/medicine_db.json"

def check_interactions(medicines):
    with open(DATABASE_PATH, "r") as f:
        data = json.load(f)

    warnings = []

    for med in medicines:
        interactions = data.get(med, {}).get("interactions", [])
        for interaction in interactions:
            other_med = interaction["with"]
            if other_med in medicines:
                warnings.append({
                    "medicine_1": med,
                    "medicine_2": other_med,
                    "severity": interaction["severity"],
                    "description": interaction["description"]
                })

    return warnings