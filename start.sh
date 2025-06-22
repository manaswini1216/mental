#!/bin/bash

# Start Ollama server in the background
ollama serve &

# Give it 3 seconds to boot up
sleep 3

# Run Streamlit app
streamlit run app.py --server.port=10000 --server.enableCORS=false
