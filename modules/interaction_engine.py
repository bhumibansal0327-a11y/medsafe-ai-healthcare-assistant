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

import json

DATABASE_PATH = "database/medicine_db.json"


def load_database():

    with open(DATABASE_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def check_interactions(medicines):

    data = load_database()

    medicine_data = data.get("medicines", data)

    warnings = []

    # Normalize input
    medicines = [
        medicine.strip().lower()
        for medicine in medicines
        if medicine.strip()
    ]

    # Remove duplicates
    medicines = list(dict.fromkeys(medicines))

    # Keep track of already checked combinations
    checked_pairs = set()

    for medicine in medicines:

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
            ).strip().lower()

            if not other_medicine:
                continue

            # Only report if the other medicine is also being taken
            if other_medicine not in medicines:
                continue

            # Prevent:
            #
            # paracetamol + ibuprofen
            # ibuprofen + paracetamol
            #
            pair = tuple(
                sorted(
                    [medicine, other_medicine]
                )
            )

            if pair in checked_pairs:
                continue

            checked_pairs.add(pair)

            warnings.append({
                "medicine_1": medicine,
                "medicine_2": other_medicine,
                "severity": interaction.get(
                    "severity",
                    "unknown"
                ),
                "description": interaction.get(
                    "description",
                    "Potential interaction identified."
                )
            })

    return warnings
