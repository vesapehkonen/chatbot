#!/bin/bash
# Activate virtual environment and clear chat history
. ~/.venv/bin/activate
python clear_chat_history.py

# To switch model backend, uncomment the desired line below

# Run app with remote model
# MODEL_API_KEY=98765 MODEL_NAME=remote REMOTE_MODEL_URL=http://remote-ip:5000/generate python app.py

# Run app with openai model
# OPENAI_API_KEY=openai-api-key MODEL_NAME=openai python app.py

# Run app with local mistral model
# MODEL_NAME=mistral python app.py

# Run app with local tinyllama model
MODEL_NAME=tinyllama python app.py
