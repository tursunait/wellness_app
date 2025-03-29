def calculate_bmi(weight_kg, height_cm):
    height_m = height_cm / 100
    return round(weight_kg / (height_m**2), 2)


def calculate_bmr(weight, height, age, gender):
    if gender.lower() == "male":
        return round(10 * weight + 6.25 * height - 5 * age + 5)
    else:
        return round(10 * weight + 6.25 * height - 5 * age - 161)


def calculate_tdee(bmr, activity_level):
    multiplier = {
        "Sedentary (little or no exercise)": 1.2,
        "Lightly active (light exercise/sports 1–3 days/week)": 1.375,
        "Moderately active (moderate exercise/sports 3–5 days/week)": 1.55,
        "Very active (hard exercise/sports 6–7 days/week)": 1.725,
        "Super active (very hard exercise/physical job)": 1.9,
    }
    return round(bmr * multiplier.get(activity_level, 1.2))


def interpret_bmi(bmi):
    if bmi < 18.5:
        return "Underweight – consider nutrient-dense meals and strength training"
    elif 18.5 <= bmi < 24.9:
        return "Normal weight – keep maintaining with a balanced diet"
    elif 25 <= bmi < 29.9:
        return "Overweight – slight calorie deficit and movement can help"
    else:
        return "Obese – focus on sustainable weight loss and whole foods"
