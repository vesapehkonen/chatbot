#!/bin/bash
set -e

MODEL_DIR="/mnt/models"
MODEL_NAME="mythomax-l2-13b.Q4_K_M.gguf"
MODEL_PATH="$MODEL_DIR/$MODEL_NAME"
MODEL_URL="https://huggingface.co/TheBloke/MythoMax-L2-13B-GGUF/resolve/main/$MODEL_NAME"

mkdir -p "$MODEL_DIR"

if [ ! -f "$MODEL_PATH" ]; then
  echo "Downloading model from Hugging Face..."
  wget --show-progress -O "$MODEL_PATH" "$MODEL_URL"
else
  echo "Model already exists at $MODEL_PATH"
fi
