import streamlit as st
import datetime
import uuid
import base64
import boto3
from features.llm_claude import call_claude
from decimal import Decimal
from features.env_loader import load_env_variables
from dotenv import load_dotenv

load_dotenv()

# Load environment variables from .env
load_env_variables()

# Get AWS region from env
region = os.getenv("AWS_REGION") or "us-east-1"

# Initialize DynamoDB resource with region
dynamodb = boto3.resource("dynamodb", region_name=region)
table = dynamodb.Table("wellness-app")


def save_diet_entry(user_id, date, time, input_type, food_description, feedback=None):
    log_id = str(uuid.uuid4())
    item = {
        "user_id": user_id,
        "log_id": log_id,
        "date": date,
        "time": time,
        "meal": input_type,
        "food": food_description,
        "likes_dislikes": feedback or "",
    }
    table.put_item(Item=item)


def fetch_diet_logs(user_id):
    response = table.scan(
        FilterExpression=boto3.dynamodb.conditions.Attr("user_id").eq(user_id)
    )
    return response.get("Items", [])


def diet_tracking_page():
    st.title("🥗 Baseline Diet Tracking")

    profile = st.session_state.get("profile")
    user_id = profile.get("user_id") if profile else None

    if not user_id:
        st.warning("⚠️ Please generate and save your profile first.")
        return

    st.subheader("🍽️ Log a Meal")
    date = st.date_input("Date of Meal", value=datetime.date.today())

    col1, col2 = st.columns(2)
    meal_time = col1.text_input("Time (e.g. 08:30 AM)", value="")
    meal_time_picker = col2.time_input("Select Time")
    if not meal_time:
        meal_time = meal_time_picker.strftime("%I:%M %p")

    input_type = st.radio("Meal Input Type", ["Text", "Image", "Audio"])

    food_description = ""
    if input_type == "Text":
        food_description = st.text_area("Describe your meal:")

    elif input_type == "Image":
        uploaded_image = st.file_uploader(
            "Upload meal photo", type=["jpg", "jpeg", "png"]
        )
        if uploaded_image:
            image_bytes = uploaded_image.read()
            with st.spinner("🔍 Analyzing image to describe the meal..."):
                prompt = "Describe the food content and estimate calories/macros from this image of a meal."
                food_description = call_claude(prompt, image=image_bytes)
                st.markdown(f"**Detected meal (Claude):** {food_description}")

    elif input_type == "Audio":
        uploaded_audio = st.file_uploader(
            "Upload audio description", type=["mp3", "wav", "m4a"]
        )
        if uploaded_audio:
            audio_bytes = uploaded_audio.read()
            with st.spinner("🔍 Transcribing audio to describe the meal..."):
                prompt = "Transcribe and summarize the food mentioned in the audio, with calorie/macro estimates."
                # Assuming audio handling is future work; for now use base64 or fallback
                food_description = call_claude(prompt)
                st.markdown(f"**Detected meal (Claude):** {food_description}")

    feedback = st.text_input("Likes/Dislikes about the meal (optional)")

    if st.button("➕ Log Meal"):
        if not food_description:
            st.warning("Please enter or upload your meal.")
        else:
            save_diet_entry(
                user_id, str(date), meal_time, input_type, food_description, feedback
            )
            st.success("✅ Meal logged!")

    st.subheader("🗕️ View Logged Meals")
    logs = fetch_diet_logs(user_id)

    if not logs:
        st.info("No meals logged yet.")
        return

    date_options = sorted(
        set(log.get("date", "") for log in logs if "date" in log), reverse=True
    )

    selected_date = st.selectbox("Choose a date", date_options)

    day_logs = [log for log in logs if log.get("date") == selected_date]
    for log in sorted(day_logs, key=lambda x: x.get("time", "")):
        time_str = log.get("time", "[Unknown time]")
        meal_type = log.get("meal", "[Unknown type]")
        st.markdown(f"**{time_str}** — {meal_type}")
        st.write(log.get("food", "[No description available]"))
        if log.get("likes_dislikes"):
            st.markdown(f"_Feedback_: {log['likes_dislikes']}")

    if st.button("🧐 Summarize This Day’s Meals"):
        summary_prompt = "\n".join(
            f"Time: {log.get('time', '[Unknown time]')} — {log.get('food', '[Image/Audio Upload]')}"
            for log in day_logs
        )
        summary_prompt += "\n\nSummarize total calories, macros, and meal patterns."

        with st.spinner("Analyzing with Claude..."):
            summary = call_claude(summary_prompt)
            st.success("📜 Daily Summary")
            st.write(summary)

        if st.button("🔁 Do you want to adjust your daily meal plan?"):
            st.session_state["diet_summary"] = summary
            st.switch_page("main.py")
