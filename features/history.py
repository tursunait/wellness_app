import streamlit as st


def display_meal_plan_history(history_list):
    st.markdown("## 🕒 Previous Meal Plans")
    for i, plan in enumerate(reversed(history_list)):
        st.markdown(f"### Day {i+1} ({plan['date']})")
        st.text(plan["meal_plan"])
