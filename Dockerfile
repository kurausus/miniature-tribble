# Use official Python image as base
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy requirements file (if you have one)
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy your app code
COPY . .

# Expose the port your app listens on (e.g. 8000)
# EXPOSE 8000

# Run the app (adjust if your main script or command is different)
CMD ["uvicorn", "server_litellm:app", "--host", "0.0.0.0", "--port", "8080"]

