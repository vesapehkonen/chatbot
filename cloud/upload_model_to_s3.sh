#!/bin/bash
set -e

MODEL_DIR="/mnt/models"
MODEL_NAME="mythomax-l2-13b.Q4_K_M.gguf"
MODEL_PATH="$MODEL_DIR/$MODEL_NAME"
BUCKET="bucket-name"
S3_KEY="$MODEL_NAME"

if [ ! -f "$MODEL_PATH" ]; then
  echo "Model file not found at $MODEL_PATH"
  exit 1
fi

echo "Uploading model to S3..."
aws s3 cp "$MODEL_PATH" "s3://$BUCKET/$S3_KEY" --storage-class STANDARD_IA
