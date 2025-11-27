# Dockerfile for Shopping Assistant Chatbot Service

FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY chatbot/requirements.txt /app/chatbot/requirements.txt

# Install Python dependencies
RUN pip install --no-cache-dir -r chatbot/requirements.txt

# Copy application code
COPY chatbot/ /app/chatbot/
COPY .env.example /app/.env.example

# Create sessions directory
RUN mkdir -p /app/sessions

# Expose the chatbot service port
EXPOSE 5001

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV SESSION_STORAGE_DIR=/app/sessions

# Run the chatbot service
CMD ["python", "-m", "chatbot"]
