FROM python:3.10-slim

# Install system dependencies
RUN apt-get update && apt-get install -y curl gnupg && \
    curl -fsSL https://ollama.com/install.sh | sh

# Install Python dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy app and start script
COPY . /app
WORKDIR /app

# Download the Ollama model in advance (optional but recommended)
RUN ollama pull mistral

# Expose the port Streamlit will run on
EXPOSE 10000

# Run start script
CMD ["./start.sh"]
