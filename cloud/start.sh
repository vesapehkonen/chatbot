#!/bin/bash
# Activate virtual environment
. ~/.venv/bin/activate

# Start the cloud model server with API key
MODEL_API_KEY=98765 MAX_TOKENS=150 MODEL_PATH=/mnt/models/mythomax-l2-13b.Q4_K_M.gguf python cloud_model_server.py
