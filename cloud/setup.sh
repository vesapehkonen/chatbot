#!/bin/bash
set -e

# Update and install dependencies
sudo apt update
sudo apt install -y python3-venv python3-pip build-essential
sudo apt install -y nvidia-driver-525
sudo apt install -y nvidia-cuda-toolkit

# Setup Python virtual environment
if [ ! -d "$HOME/.venv" ]; then
  python3 -m venv $HOME/.venv
fi
source $HOME/.venv/bin/activate

# Install Python packages
pip install --upgrade pip
pip install flask flask-cors

# Install llama-cpp-python with CUDA support
CMAKE_ARGS="-DGGML_CUDA=on" pip install llama-cpp-python --force-reinstall --no-cache-dir

# Post-install verification (manual steps):
echo ""
echo " Setup complete. Next steps:"
echo "  - Run: 'nvcc --version'   # Verify CUDA toolkit is installed"
echo "  - Run: 'watch -n 1 nvidia-smi' while inference is running to confirm GPU usage"
