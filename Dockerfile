# Base image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

COPY .env .env

# Copy dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy rest of the app
COPY . .


# Expose default Streamlit port
EXPOSE 8501

# Run Streamlit app (change if not named main.py)
CMD ["streamlit", "run", "main.py", "--server.port=8501", "--server.address=0.0.0.0"]