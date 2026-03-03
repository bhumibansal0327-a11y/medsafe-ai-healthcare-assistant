from modules.medicine_identifier import identify_medicines
from modules.interaction_engine import check_interactions
from modules.llm_parser import generate_interaction_summary
from modules.ocr_engine import extract_text_from_image
from modules.llm_parser import parse_prescription_text
from modules.symptom_engine import basic_symptom_risk, generate_symptom_guidance
from modules.side_effect_engine import (
    calculate_side_effect_risk,
    side_effect_risk_level,
    generate_side_effect_guidance
)
from modules.risk_engine import (
    calculate_risk_score,
    risk_level_from_score,
    generate_emergency_guidance
)
import streamlit as st

st.set_page_config(
    page_title="MedSafe AI",
    layout="wide",
)

st.title("🩺 MedSafe AI - Intelligent Medicine Safety Assistant")

tabs = st.tabs([
    "💊 Medicine Interaction Checker",
    "📄 Prescription OCR",
    "🧠 Symptom & Doubt Solver",
    "⚠ Side-Effect Monitor",
    "🚨 Emergency Risk Predictor"
])

# ==============================
# TAB 1 - Interaction Checker
# ==============================
with tabs[0]:
    st.header("💊 Medicine Interaction Checker")

    medicines = st.text_input("Enter medicines (comma separated)")

    if st.button("Check Interactions"):
        detected = identify_medicines(medicines)

        if not detected:
            st.warning("No valid medicines detected.")
        else:
            st.success(f"Detected Medicines: {', '.join(detected)}")

            warnings = check_interactions(detected)

            if warnings:
                st.error("⚠ Interaction Detected!")

                for w in warnings:
                    st.markdown(f"""
                    **{w['medicine_1'].capitalize()}** + 
                    **{w['medicine_2'].capitalize()}**

                    Severity: {w['severity'].capitalize()}  
                    {w['description']}
                    """)

                st.divider()
                st.info("🤖 Generating AI Safety Summary...")

                summary = generate_interaction_summary(warnings)

                st.success("AI Educational Summary")
                st.write(summary)

            else:
                st.success("No known interactions found.")

# ==============================
# TAB 2 - Prescription OCR
# ==============================
with tabs[1]:
    st.header("📄 Prescription OCR")

    image = st.file_uploader("Upload prescription image", type=["png","jpg","jpeg"])

    if image:
        st.image(image, caption="Uploaded Prescription", use_column_width=True)

        if st.button("Extract Medicines", key="ocr_button"):

            raw_text = extract_text_from_image(image)

            st.subheader("🔍 Raw Extracted Text")
            st.text(raw_text)

            parsed = parse_prescription_text(raw_text)

            st.subheader("🧠 Structured Medicine Data")

            if "error" in parsed:
                st.error(parsed["error"])

            elif "medicines" in parsed and parsed["medicines"]:

                # Show extracted medicines nicely
                for med in parsed["medicines"]:
                    name = med.get("name", "Unknown")
                    salt = med.get("salt", "Not Available")

                    st.success(f"💊 Medicine: {name}")
                    st.info(f"🧪 Active Salt: {salt}")
                    st.divider()

                # Validate medicines
                extracted_names = [
                    m["name"].lower()
                    for m in parsed["medicines"]
                    if "name" in m
                ]

                detected = identify_medicines(",".join(extracted_names))

                if detected:
                    st.success(f"Validated Medicines: {', '.join(detected)}")

                    warnings = check_interactions(detected)

                    if warnings:
                        st.error("⚠ Interaction Detected From Prescription!")

                        for w in warnings:
                            st.markdown(f"""
                            **{w['medicine_1'].capitalize()}** + 
                            **{w['medicine_2'].capitalize()}**

                            Severity: {w['severity'].capitalize()}  
                            {w['description']}
                            """)

                        st.divider()
                        summary = generate_interaction_summary(warnings)

                        st.success("AI Educational Summary")
                        st.write(summary)

                    else:
                        st.success("No known interactions found.")

                else:
                    st.warning("No valid medicines identified after validation.")

            else:
                st.warning("No medicines found in prescription.")
# ==============================
# TAB 3 - Symptom Solver
# ==============================
with tabs[2]:
    st.header("🧠 Symptom & Doubt Solver")

    symptoms = st.text_area("Describe your symptoms")

    if st.button("Analyze Symptoms"):

        if symptoms.strip() == "":
            st.warning("Please enter symptoms.")
        else:
            risk_level = basic_symptom_risk(symptoms)

            if risk_level == "HIGH":
                st.error("⚠ High Risk Symptoms Detected! Seek immediate medical attention.")
            else:
                st.success("No immediate emergency keywords detected.")

            st.divider()
            st.info("Generating educational guidance...")

            guidance = generate_symptom_guidance(symptoms)

            st.success("AI Educational Guidance")
            st.write(guidance)

# ==============================
# TAB 4 - Side Effect Monitor
# ==============================
with tabs[3]:
    st.header("⚠ Experience & Side-Effect Monitor")

    age = st.number_input("Enter your age", min_value=0, max_value=120)
    gender = st.selectbox("Select gender", ["Male","Female","Other"])

    medicine_input = st.text_input("Enter medicine(s) taken (comma-separated)")
    reported_effect = st.text_area("Describe your experience after taking medicine")

    if st.button("Analyze Side Effect"):

        if medicine_input.strip() == "" or reported_effect.strip() == "":
            st.warning("Please enter medicine and experience details.")
        else:
            medicines = identify_medicines(medicine_input)

            score = calculate_side_effect_risk(age, medicines, reported_effect)
            level = side_effect_risk_level(score)

            st.metric("Side-Effect Risk Score (%)", f"{score}%")
            st.progress(score)

            if level == "CRITICAL":
                st.error("🚨 Critical risk — Seek medical attention immediately.")
            elif level == "HIGH":
                st.error("⚠ High risk — Consult a doctor soon.")
            elif level == "MODERATE":
                st.warning("⚠ Moderate risk — Monitor symptoms.")
            else:
                st.success("Low immediate risk based on current information.")

            st.divider()
            st.info("Generating AI Educational Guidance...")

            guidance = generate_side_effect_guidance(age, medicines, reported_effect)
            st.write(guidance)

# ==============================
# TAB 5 - Emergency Predictor
# ==============================
with tabs[4]:
    st.header("🚨 Emergency Risk Predictor")

    emergency_symptoms = st.text_area("Describe emergency symptoms")

    if st.button("Calculate Emergency Risk"):

        if emergency_symptoms.strip() == "":
            st.warning("Please describe symptoms.")
        else:
            score, matched = calculate_risk_score(emergency_symptoms)
            level = risk_level_from_score(score)

            st.metric("Emergency Risk Score (%)", f"{score}%")
            st.progress(score)

            if matched:
                st.info(f"Detected Risk Indicators: {', '.join(matched)}")

            if level == "CRITICAL":
                st.error("🚨 CRITICAL RISK - Seek emergency care immediately.")
            elif level == "HIGH":
                st.error("⚠ HIGH RISK - Urgent medical evaluation recommended.")
            elif level == "MODERATE":
                st.warning("⚠ Moderate risk - Monitor closely.")
            else:
                st.success("Low immediate risk based on detected indicators.")

            st.divider()
            st.info("Generating AI Emergency Guidance...")

            guidance = generate_emergency_guidance(emergency_symptoms, level)
            st.write(guidance)