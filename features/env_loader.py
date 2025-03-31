# features/env_loader.py
from dotenv import load_dotenv
import os


def load_env_variables():
    load_dotenv()  # Looks for .env in the root directory

    # Optional logging for debugging (remove in production)
    required_vars = ["AWS_ACCESS_KEY_ID", "AWS_SECRET_ACCESS_KEY", "AWS_REGION"]

    for var in required_vars:
        if not os.getenv(var):
            print(f"⚠️ Warning: {var} is not set in .env")
