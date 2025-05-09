# Chatbot Web App with Pluggable LLM Backends

This is a Flask-based chatbot application that supports multiple LLM backends:
- Local models (TinyLlama, Mistral)
- Remote model API (e.g., via Flask server)
- OpenAI (e.g., GPT-4o)

## 📁 Directory Structure

```
chatbot/
├── app.py                     # Main Flask app
├── chat_memory.json          # Stores chat history
├── clear_chat_history.py     # Script to clear history
├── start.sh                  # Startup script
├── templates/                # HTML templates
│   ├── index.html
│   ├── login.html
│   └── register.html
├── bot/
│   ├── model_loader.py       # Dispatches to the correct model
│   ├── openai_model.py       # GPT-4o via OpenAI API
│   ├── remote_model.py       # For remote model API
│   ├── mistral_model.py      # Local Mistral model
│   └── tinyllama_model.py    # Local TinyLlama model
└── cloud/
    ├── cloud_model_server.py # Flask server to expose remote model
    ├── time_gpu_inference.py # Timing/debug script
    ├── start.sh              # Starts remote server
    ├── setup.sh              # Install CUDA + dependencies
    ├── mount_nvme.sh         # Mounts model storage
    ├── download_model.sh     # Download model from Hugging Face
    ├── download_model_from_s3.sh
    ├── upload_model_to_s3.sh
    └── setup_model_server.sh # Run setup + start

## 🚀 How to Run

### Prerequisites
- Python 3.10+
- Optional GPU (CUDA) for local model inference
- OpenAI API key for GPT-4o

### 🔹 Local app (with TinyLlama or Mistral)

```bash
. ~/.venv/bin/activate
MODEL_NAME=tinyllama python app.py
# or
MODEL_NAME=mistral python app.py
```

### 🔹 Local app with OpenAI GPT-4o

```bash
. ~/.venv/bin/activate
OPENAI_API_KEY=your-key MODEL_NAME=openai python app.py
```

### 🔹 Local app with remote model (served on cloud)

```bash
. ~/.venv/bin/activate
MODEL_API_KEY=98765 MODEL_NAME=remote REMOTE_MODEL_URL=http://your-cloud-ip:5000/generate python app.py
```

## 🌩️ Cloud Model Server Setup

On your cloud instance:
```bash
cd cloud
bash setup.sh
bash mount_nvme.sh
bash download_model.sh  # or download_model_from_s3.sh
bash start.sh
```

You can test performance using:

```bash
python time_gpu_inference.py
```

## 🔐 Environment Variables

- `MODEL_NAME`: `tinyllama`, `mistral`, `openai`, or `remote`
- `MODEL_API_KEY`: used by remote model server for auth
- `REMOTE_MODEL_URL`: URL for cloud model endpoint
- `OPENAI_API_KEY`: your OpenAI API key

## 🧠 Features

- Memory/history-based conversation
- Dynamic model backend switching
- Summarization for long chats
- Markdown-formatted bot output
- Roleplay capability (if model supports it)

## 📝 License

MIT License. Free to use and modify.