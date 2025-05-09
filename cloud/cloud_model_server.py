from flask import Flask, request, jsonify
from llama_cpp import Llama
from flask_cors import CORS
import os
import time

app = Flask(__name__)
CORS(app)

API_KEY = os.environ.get("MODEL_API_KEY", "changeme")  # Set in environment
MODEL_PATH = os.environ.get("MODEL_PATH", "/mnt/models/mythomax-l2-13b.Q4_K_M.gguf")

print("Loading model...")

llm = Llama(
    model_path=MODEL_PATH,
    n_ctx=4096,
    n_threads=8,  # Use full CPU
    n_batch=64,
    backend="cuda",
    use_mlock=True,
    verbose=False
)

print("Model loaded.")

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"})

@app.route("/generate", methods=["POST"])
def generate():
    auth = request.headers.get("Authorization", "")
    if not auth.startswith("Bearer ") or auth.split()[1] != API_KEY:
        return jsonify({"error": "Unauthorized"}), 401

    data = request.get_json()
    prompt = data.get("prompt", "")
    stop = data.get("stop", ["### Instruction", "### Response"])

    print(f'Received prompt: {prompt}')

    if not prompt.strip():
        return jsonify({"error": "Prompt is required"}), 400

    start = time.time()
    output = llm(prompt, max_tokens=150, stop=stop)
    print(f"Inference took {time.time() - start:.2f} seconds")
    reply = output["choices"][0]["text"].strip()

    print(f'Response: {reply}')
    print('-----------------------------')
    return jsonify({"reply": reply})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
