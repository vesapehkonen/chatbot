#!/bin/bash
set -e

MODEL_DIR="/mnt/models"
MODEL_NAME="mythomax-l2-13b.Q4_K_M.gguf"
MODEL_PATH="$MODEL_DIR/$MODEL_NAME"
BUCKET="bucket-name"
S3_KEY="$MODEL_NAME"

command -v aws >/dev/null 2>&1 || { echo >&2 "** AWS CLI not installed."; exit 1; }

mkdir -p "$MODEL_DIR"
if [ ! -f "$MODEL_PATH" ]; then
  echo "☁️ Downloading model from S3..."
  aws s3 cp "s3://$BUCKET/$S3_KEY" "$MODEL_PATH"
else
  echo "Model already exists at $MODEL_PATH"
fi
