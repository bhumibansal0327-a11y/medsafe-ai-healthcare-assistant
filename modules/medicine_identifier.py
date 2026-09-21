# import json
# from rapidfuzz import process

# DATABASE_PATH = "database/medicine_db.json"

# def load_medicine_names():
#     with open(DATABASE_PATH, "r") as f:
#         data = json.load(f)
#     return list(data.keys())

# def identify_medicines(user_input):
#     medicine_list = load_medicine_names()
#     detected = []

#     inputs = [m.strip().lower() for m in user_input.split(",")]

#     for med in inputs:
#         match, score, _ = process.extractOne(med, medicine_list)
#         if score >= 80:
#             detected.append(match)

#     return list(set(detected))

import json
from rapidfuzz import process, fuzz

DATABASE_PATH = "database/medicine_db.json"


def load_database():
    with open(DATABASE_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def load_medicine_names():
    data = load_database()

    # Only actual medicines, not metadata/aliases
    return list(data.get("medicines", data).keys())


def load_aliases():
    data = load_database()

    return data.get("medicine_aliases", {})


def normalize_medicine_name(name):
    """
    Converts a brand name or medicine name into
    the generic medicine key used by the database.
    """

    name = name.strip().lower()

    if not name:
        return None

    data = load_database()

    medicines = data.get("medicines", data)
    aliases = data.get("medicine_aliases", {})

    # Exact generic medicine
    if name in medicines:
        return name

    # Exact brand alias
    if name in aliases:
        return aliases[name]

    # Fuzzy match against generic medicines
    medicine_names = list(medicines.keys())

    match = process.extractOne(
        name,
        medicine_names,
        scorer=fuzz.ratio
    )

    if match:
        matched_name, score, _ = match

        if score >= 85:
            return matched_name

    # Fuzzy match against brand aliases
    alias_names = list(aliases.keys())

    if alias_names:

        match = process.extractOne(
            name,
            alias_names,
            scorer=fuzz.ratio
        )

        if match:
            matched_alias, score, _ = match

            if score >= 85:
                return aliases[matched_alias]

    return None


def identify_medicines(user_input):
    """
    Identify medicines from comma-separated user input.

    Examples:

    Dolo 650, Brufen
    ->
    ['paracetamol', 'ibuprofen']

    paracetamol, ibuprofen
    ->
    ['paracetamol', 'ibuprofen']
    """

    if not user_input:
        return []

    inputs = [
        item.strip().lower()
        for item in user_input.split(",")
        if item.strip()
    ]

    detected = []

    for medicine in inputs:

        normalized = normalize_medicine_name(medicine)

        if normalized and normalized not in detected:
            detected.append(normalized)

    return detected
