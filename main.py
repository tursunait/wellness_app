import os
import logging
import streamlit as st
import datetime
from features.calculations import (
    calculate_bmi,
    calculate_bmr,
    calculate_tdee,
    interpret_bmi,
)
from features.llm_claude import call_claude
from features.downloads import download_meal_plan_txt, download_meal_plan_pdf
from features.dynamo import save_profile_to_dynamodb
from features.history import display_meal_plan_history
from dotenv import load_dotenv
from features.diet_tracking import diet_tracking_page
from PIL import Image


load_dotenv()
st.set_page_config(page_title="Wellness Meal Plan Generator", layout="wide")


logging.basicConfig(level=logging.DEBUG)
st.write("✅ Streamlit started")
st.write("✅ App running. ENV =", os.getenv("ENV", "not set"))
# Load and display logo with title
col1, col2 = st.columns([1, 5])

# Sidebar with Menu
st.sidebar.header("📋 Menu")
page = st.sidebar.radio("🔄 Select Feature", ["Meal Plan Generator", "Diet Tracking"])

if page == "Meal Plan Generator":
    st.title("🌱 Wellness Daily Meal Plan Generator")

    # 🔹 USER PROFILE FORM
    with st.form("user_profile_form"):
        st.header("👤 Your Health & Lifestyle Info")

        col1, col2 = st.columns(2)
        age = col1.number_input("Age", min_value=10, max_value=100)
        gender = col2.selectbox("Gender", ["Female", "Male", "Other"])

        col3, col4 = st.columns(2)
        height = col3.number_input("Height (cm)", min_value=100, max_value=250)
        weight = col4.number_input("Weight (kg)", min_value=30, max_value=200)

        body_fat = st.slider("Body Fat Percentage (if known)", 5.0, 50.0, 20.0)

        activity_level = st.selectbox(
            "Activity Level",
            [
                "Sedentary (little or no exercise)",
                "Lightly active (light exercise/sports 1–3 days/week)",
                "Moderately active (moderate exercise/sports 3–5 days/week)",
                "Very active (hard exercise/sports 6–7 days/week)",
                "Super active (very hard exercise/physical job)",
            ],
        )

        with st.expander("❓ Not sure which activity level? Click for examples"):
            st.markdown(
                """
        - **Sedentary**: Desk job, under 3,000 steps/day, little to no exercise  
        - **Lightly active**: 3,000–7,000 steps/day, light exercise 1–3 times/week  
        - **Moderately active**: 7,000–10,000 steps/day, regular workouts 3–5 times/week  
        - **Very active**: 10,000–15,000 steps/day, hard exercise 6–7 days/week  
        - **Super active**: Intense daily training or physically demanding job  
        """
            )

        st.markdown("#### 🥚 Allergies or Intolerances")

        common_allergies = [
            "Dairy",
            "Eggs",
            "Fish",
            "Gluten",
            "Peanuts",
            "Shellfish",
            "Soy",
            "Tree nuts",
            "Wheat",
        ]

        selected_allergies = st.multiselect(
            "Select any known allergies/intolerances (you can choose multiple):",
            options=common_allergies,
        )

        custom_allergies = st.text_input(
            "Or enter any other allergies (comma-separated):"
        )

        allergies_combined = selected_allergies + [
            a.strip() for a in custom_allergies.split(",") if a.strip()
        ]

        diet_type = st.selectbox(
            "Diet Type", ["None", "Vegetarian", "Vegan", "Keto", "Paleo", "Other"]
        )
        cooking_equipment = st.text_input("Available Cooking Equipment")

        st.markdown("#### 🌟 Health Goals")

        goal_options = [
            "Lose weight",
            "Gain muscle",
            "Improve metabolic markers",
            "Maintain weight",
            "Other",
        ]

        selected_goals = st.multiselect(
            "Select your health goals (you can choose more than one):",
            options=goal_options,
        )

        custom_goal = st.text_input("Any other goals or motivations? (optional):")

        goals_combined = (
            selected_goals + [custom_goal.strip()]
            if custom_goal.strip()
            else selected_goals
        )

        goal_details = st.text_area("Specific goal details or timeline (optional)")

        submitted = st.form_submit_button("Save Profile")

    if submitted:
        profile = {
            "age": age,
            "gender": gender,
            "height": height,
            "weight": weight,
            "body_fat": body_fat,
            "activity_level": activity_level,
            "allergies": ", ".join(allergies_combined),
            "diet_type": diet_type,
            "cooking_equipment": cooking_equipment,
            "goal": ", ".join(goals_combined),
            "goal_details": goal_details,
        }

        bmi = calculate_bmi(weight, height)
        bmr = calculate_bmr(weight, height, age, gender)
        tdee = calculate_tdee(bmr, activity_level)

        profile["bmi"] = bmi
        profile["bmr"] = bmr
        profile["tdee"] = tdee

        st.session_state["profile"] = profile
        user_id = save_profile_to_dynamodb(profile)
        st.session_state["user_id"] = user_id

        st.success("✅ Profile saved and health stats calculated!")

        with st.expander("📊 See personalized health strategy"):
            st.markdown(
                f"""
                    ### 📊 Your Body Stats
                    - **BMI**: `{bmi}` – {interpret_bmi(bmi)}
                    - **BMR**: `{bmr} kcal/day` – Basal calories your body needs at rest
                    - **TDEE**: `{tdee} kcal/day` – Estimated daily calories needed with your activity level
                    """
            )

            goal_lower = profile["goal"].lower()

            if "lose weight" in goal_lower:
                st.markdown(
                    f"""
                    To lose weight, aim to eat **10–25% fewer calories than your TDEE**:
                    - Target intake: `{round(tdee * 0.75)}–{round(tdee * 0.9)} kcal/day`
                    - This creates a safe calorie deficit for fat loss while preserving muscle.
                    - Focus on **high protein**, **fiber-rich** foods, and hydration.
                    """
                )
            elif "gain muscle" in goal_lower:
                st.markdown(
                    f"""
                    To gain lean muscle, aim to eat **10–20% more than your TDEE**:
                    - Target intake: `{round(tdee * 1.1)}–{round(tdee * 1.2)} kcal/day`
                    - Prioritize **protein**, **resistance training**, and **meal timing**.
                    """
                )
            elif "improve metabolic markers" in goal_lower:
                st.markdown(
                    f"""
                    Stabilizing blood sugar and improving markers means:
                    - Prioritize **complex carbs**, **healthy fats**, and **moderate calories**
                    - Aim to stay close to your TDEE: `{tdee} kcal/day`
                    - Avoid extreme deficits or surpluses.
                    """
                )
            else:
                st.markdown(
                    "Stick to your **TDEE range** for maintenance and adjust as needed."
                )
            st.markdown(
                f"**BMI**: {bmi} | **BMR**: {bmr} kcal/day | **TDEE**: {tdee} kcal/day"
            )

    # 🍳 Meal Plan Customization
    st.header("🍳 Meal Plan Customization")

    plan_scope = st.radio(
        "How long should the meal plan cover?",
        ["1 Day", "7 Days (Week)"],
        horizontal=True,
    )

    st.markdown("#### 🥗 Provide available foods")
    uploaded_files = st.file_uploader(
        "📷 Upload up to 3 images (grocery receipt or fridge)",
        type=["jpg", "jpeg", "png"],
        accept_multiple_files=True,
        help="Upload up to 3 images",
        key="multi_uploader",
    )

    fridge_items = st.text_area(
        "🥗 Enter a list of ingredients or foods in your fridge"
    )

    generate_plan_clicked = st.button("🍽️ Generate Meal Plan")

    if generate_plan_clicked:
        if "profile" not in st.session_state:
            st.warning("⚠️ Please fill out and save your profile first.")
        else:
            profile = st.session_state["profile"]

            if plan_scope == "1 Day":
                prompt = f"""
You are a certified nutritionist and wellness coach. Create a 1-day meal plan.
Include breakfast, lunch, dinner, and 1–2 snacks with estimated portion sizes and macronutrients (calories, protein, carbs, fat).
User Info:
- Age: {profile['age']} years
- Gender: {profile['gender']}
- Height: {profile['height']} cm
- Weight: {profile['weight']} kg
- Body Fat: {profile['body_fat']}%
- Activity Level: {profile['activity_level']}
- Allergies/Intolerances: {profile['allergies']}
- Diet Type: {profile['diet_type']}
- Cooking Equipment: {profile['cooking_equipment']}
- Goal: {profile['goal']}
- Details: {profile['goal_details']}
- BMI: {profile['bmi']}
- BMR: {profile['bmr']} kcal/day
- TDEE: {profile['tdee']} kcal/day
"""
                output = call_claude(prompt)
            else:
                output = ""
                for i in range(1, 8):
                    prompt = f"""
You are a certified nutritionist and wellness coach. Create a meal plan for **Day {i}**.
Include breakfast, lunch, dinner, and 1–2 snacks with estimated portion sizes and macronutrients PER MEAL (calories, protein, carbs, fat). Only include calories and macronutrients per meal.
Try to keep it precise yet informative.
User Info:
- Age: {profile['age']} years
- Gender: {profile['gender']}
- Height: {profile['height']} cm
- Weight: {profile['weight']} kg
- Body Fat: {profile['body_fat']}%
- Activity Level: {profile['activity_level']}
- Allergies/Intolerances: {profile['allergies']}
- Diet Type: {profile['diet_type']}
- Cooking Equipment: {profile['cooking_equipment']}
- Goal: {profile['goal']}
- Details: {profile['goal_details']}
- BMI: {profile['bmi']}
- BMR: {profile['bmr']} kcal/day
- TDEE: {profile['tdee']} kcal/day
"""
                    if uploaded_files:
                        prompt += "\nUse the uploaded grocery images to infer available ingredients."

                    if fridge_items.strip():
                        prompt += f"\nAvailable Ingredients: {fridge_items}"
                    else:
                        prompt += "\nNo specific ingredients were provided. Use general healthy foods."

                    with st.spinner(f"Generating meal plan for Day {i}..."):
                        daily_plan = call_claude(prompt)
                        output += f"\n\n### Day {i}\n{daily_plan.strip()}"

            st.subheader("📋 Your Personalized Meal Plan")
            st.write(output)

            txt = download_meal_plan_txt(output)
            pdf = download_meal_plan_pdf(output)
            st.download_button("📄 Download as TXT", txt, file_name="meal_plan.txt")
            st.download_button("📄 Download as PDF", pdf, file_name="meal_plan.pdf")

    if "history" in st.session_state:
        display_meal_plan_history(st.session_state["history"])

elif page == "Diet Tracking":
    diet_tracking_page()
