[![Build & Push to ECR](https://github.com/tursunait/wellness_app/actions/workflows/deploy.yml/badge.svg)](https://github.com/tursunait/wellness_app/actions/workflows/deploy.yml)

# 🥗 Wellness Meal Plan Generator

**Personalized Wellness App**  
A full-stack Streamlit web application that generates AI-personalized meal plans based on user profile, lifestyle, health goals, and available food items. Built with AWS integration, Claude AI (via Bedrock), and hosted on an EC2 instance with a custom domain.

---

## 📌 Features

- 🧬 **Personalized User Profile Form** (age, gender, weight, height, goals, allergies, and more)
- 🧠 **Smart Meal Plan Generation** using Claude (Anthropic) via AWS Bedrock
- 🗓️ Generate meal plans for **1 Day or 7 Days**, with **calorie & macronutrient breakdown**
- 📸 Upload grocery/fridge images + type in available ingredients for better personalization
- 📝 **Diet tracking** section with DynamoDB-powered logging and daily nutrition summaries
- 📥 **Download meal plans** as PDF or TXT
- ☁️ **Hosted on AWS EC2** with a custom domain via Namecheap

---

## 🚀 Live Demo

🔗 [https://wellness-app-tursunai.online](http://wellness-app-tursunai.online:8501)

---

## 🖥️ Tech Stack

| Layer         | Tools / Services Used                                  |
|---------------|--------------------------------------------------------|
| **Frontend**  | `Streamlit`, `PIL`, `HTML/CSS Markdown`               |
| **Backend**   | `Python`, `Claude AI via AWS Bedrock`, `uuid`, `boto3` |
| **Database**  | `Amazon DynamoDB`                                      |
| **Cloud**     | `AWS EC2`, `AWS IAM`, `AWS Bedrock`, `AWS CLI`, `.env` |
| **Dev Tools** | `pip`, `venv`, `dotenv`, `GitHub`, `Namecheap DNS`     |

---

## 📂 Project Structure

```
wellness_app/
├── main.py                        # Main Streamlit app
├── features/
│   ├── calculations.py           # BMI, BMR, TDEE logic
│   ├── llm_claude.py             # Claude AI prompt calling logic
│   ├── downloads.py              # TXT & PDF download functions
│   ├── dynamo.py                 # DynamoDB connection and storage
│   ├── diet_tracking.py          # Logging meals and daily summaries
│   └── history.py                # View meal plan generation history
├── requirements.txt
├── .env                          # AWS Keys, Region
└── README.md
```

---

## 🔐 Environment Variables

Set up a `.env` file in the root directory:

```dotenv
AWS_ACCESS_KEY_ID=your_key_id
AWS_SECRET_ACCESS_KEY=your_secret
AWS_REGION=us-east-1
```

**Never commit your `.env` file to version control.**

---

## 📦 Installation & Local Setup

```bash
# 1. Clone the repo
git clone https://github.com/tursunait/wellness_app.git
cd wellness_app

# 2. Create a virtual environment
python3 -m venv venv
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Create and fill in the .env file (see above)

# 5. Run the app
streamlit run main.py
```

---

## 🌐 Deployment on AWS EC2

1. Launch EC2 instance (Ubuntu)
2. SSH into the server
3. Install Python 3.12, pip, and virtualenv
4. Clone this repo and follow local setup instructions
5. Run the app:
   ```bash
   nohup streamlit run main.py --server.port 8501 --server.address 0.0.0.0 &
   ```
6. Point your domain to EC2 IP (via A record in Namecheap)

---

## 🧠 Claude Prompt Logic

Claude generates structured meal plans based on:
- User input: age, gender, weight, goals, equipment, ingredients
- Meal format: Day-by-day, breakfast/lunch/dinner/snacks
- Macronutrient output per meal (calories, protein, carbs, fat)

---

## 📘 Future Improvements

- ✅ Add user authentication
- ✅ Display macronutrient totals per day
- 📈 Visualize nutrition progress in charts
- 💬 Add chatbot to answer nutrition questions
- 📱 Build a mobile-friendly interface
- 🧾 Integrate image-to-text parsing for groceries
- 📤 Enable email or SMS export of plans

---

## 👩‍💻 Author

**Tursunai Turumbekova**  
AI Engineer | Duke IDS Student  
🌐 [LinkedIn](https://www.linkedin.com/in/tursunai/) | ✨ [tursunait.github.io](https://tursunait.github.io)

---

## 🛡️ License

This project is licensed under the [MIT License](LICENSE).

---

## ⭐️ Support

If you like this project, please consider giving it a ⭐ on GitHub.  
Feel free to open issues or suggestions — contributions are welcome!

