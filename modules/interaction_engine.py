# import json

# DATABASE_PATH = "database/medicine_db.json"

# def check_interactions(medicines):
#     with open(DATABASE_PATH, "r") as f:
#         data = json.load(f)

#     warnings = []

#     for med in medicines:
#         interactions = data.get(med, {}).get("interactions", [])
#         for interaction in interactions:
#             other_med = interaction["with"]
#             if other_med in medicines:
#                 warnings.append({
#                     "medicine_1": med,
#                     "medicine_2": other_med,
#                     "severity": interaction["severity"],
#                     "description": interaction["description"]
#                 })

#     return warnings


# 
# 2222222222222222222222222222222222222222
# 
# import json

# DATABASE_PATH = "database/medicine_db.json"


# def load_database():

#     with open(DATABASE_PATH, "r", encoding="utf-8") as f:
#         return json.load(f)


# def check_interactions(medicines):

#     data = load_database()

#     medicine_data = data.get("medicines", data)

#     warnings = []

#     # Normalize input
#     medicines = [
#         medicine.strip().lower()
#         for medicine in medicines
#         if medicine.strip()
#     ]

#     # Remove duplicates
#     medicines = list(dict.fromkeys(medicines))

#     # Keep track of already checked combinations
#     checked_pairs = set()

#     for medicine in medicines:

#         interactions = medicine_data.get(
#             medicine,
#             {}
#         ).get(
#             "interactions",
#             []
#         )

#         for interaction in interactions:

#             other_medicine = interaction.get(
#                 "with",
#                 ""
#             ).strip().lower()

#             if not other_medicine:
#                 continue

#             # Only report if the other medicine is also being taken
#             if other_medicine not in medicines:
#                 continue

#             # Prevent:
#             #
#             # paracetamol + ibuprofen
#             # ibuprofen + paracetamol
#             #
#             pair = tuple(
#                 sorted(
#                     [medicine, other_medicine]
#                 )
#             )

#             if pair in checked_pairs:
#                 continue

#             checked_pairs.add(pair)

#             warnings.append({
#                 "medicine_1": medicine,
#                 "medicine_2": other_medicine,
#                 "severity": interaction.get(
#                     "severity",
#                     "unknown"
#                 ),
#                 "description": interaction.get(
#                     "description",
#                     "Potential interaction identified."
#                 )
#             })

#     return warnings


import json
from difflib import SequenceMatcher

DATABASE_PATH = "database/medicine_db.json"

# Minimum similarity required for fuzzy matching
FUZZY_THRESHOLD = 0.80


def load_database():
    with open(DATABASE_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def normalize_medicine_name(name):
    """Normalize medicine name for comparison."""
    return (
        name.strip()
        .lower()
        .replace("-", " ")
        .replace("_", " ")
    )


def similarity(a, b):
    """Return similarity score between 0 and 1."""
    return SequenceMatcher(
        None,
        a,
        b
    ).ratio()


def fuzzy_find_medicine(input_name, medicine_data):
    """
    Find the closest medicine name from database.

    Returns:
        (matched_name, confidence)
        or
        (None, 0)
    """

    input_name = normalize_medicine_name(input_name)

    best_match = None
    best_score = 0

    for medicine_name in medicine_data.keys():

        medicine_name_normalized = normalize_medicine_name(
            medicine_name
        )

        score = similarity(
            input_name,
            medicine_name_normalized
        )

        if score > best_score:
            best_score = score
            best_match = medicine_name

    if best_score >= FUZZY_THRESHOLD:
        return best_match, best_score

    return None, 0


def check_interactions(medicines):

    data = load_database()

    medicine_data = data.get(
        "medicines",
        data
    )

    warnings = []

    # --------------------------------------------------
    # Normalize + fuzzy match medicines
    # --------------------------------------------------

    matched_medicines = {}

    for original_medicine in medicines:

        if not original_medicine or not original_medicine.strip():
            continue

        original_name = original_medicine.strip()

        normalized_name = normalize_medicine_name(
            original_name
        )

        # Exact match first
        exact_match = None

        for database_name in medicine_data.keys():

            if normalize_medicine_name(
                database_name
            ) == normalized_name:

                exact_match = database_name
                break

        if exact_match:

            matched_medicines[
                normalize_medicine_name(exact_match)
            ] = {
                "database_name": exact_match,
                "original_name": original_name,
                "confidence": 1.0
            }

            continue

        # --------------------------------------------------
        # Fuzzy matching
        # --------------------------------------------------

        fuzzy_match, confidence = fuzzy_find_medicine(
            original_name,
            medicine_data
        )

        if fuzzy_match:

            matched_medicines[
                normalize_medicine_name(fuzzy_match)
            ] = {
                "database_name": fuzzy_match,
                "original_name": original_name,
                "confidence": confidence
            }

    # --------------------------------------------------
    # Check interactions
    # --------------------------------------------------

    checked_pairs = set()

    for medicine_key, medicine_info in matched_medicines.items():

        medicine = medicine_info["database_name"]

        interactions = medicine_data.get(
            medicine,
            {}
        ).get(
            "interactions",
            []
        )

        for interaction in interactions:

            other_medicine = interaction.get(
                "with",
                ""
            ).strip()

            if not other_medicine:
                continue

            # Find database medicine corresponding to interaction
            other_match, other_confidence = fuzzy_find_medicine(
                other_medicine,
                medicine_data
            )

            if not other_match:
                continue

            other_key = normalize_medicine_name(
                other_match
            )

            # Only report if the other medicine is being taken
            if other_key not in matched_medicines:
                continue

            # Prevent duplicate pairs
            pair = tuple(
                sorted([
                    medicine_key,
                    other_key
                ])
            )

            if pair in checked_pairs:
                continue

            checked_pairs.add(pair)

            warnings.append({
                "medicine_1": medicine,
                "medicine_2": other_match,

                "severity": interaction.get(
                    "severity",
                    "unknown"
                ),

                "description": interaction.get(
                    "description",
                    "Potential interaction identified."
                ),

                "match_confidence_1": round(
                    medicine_info["confidence"] * 100,
                    1
                ),

                "match_confidence_2": round(
                    matched_medicines[other_key]["confidence"] * 100,
                    1
                )
            })

    return warnings
