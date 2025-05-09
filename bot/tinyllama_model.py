import os
from llama_cpp import Llama

llm = None

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "..", "models", "mistral", "tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf")

def load_model():
    global llm
    llm = Llama(
        model_path=MODEL_PATH,
        n_ctx=2048,
        n_threads=4,
        n_batch=64,
        use_mlock=True,
        verbose=False
    )
    print("[TinyLLaMA] Model loaded.")

# Estimate token count for logging/debug
def estimate_tokens(text):
    return int(len(text.split()) * 1.5)

# Construct ChatML-style prompt from history + current message
def build_prompt(history, new_message):
    prompt = "<|system|>\nYou are a helpful assistant.\n"
    for m in history:
        tag = "<|user|>" if m['role'] == 'user' else "<|assistant|>"
        prompt += f"{tag}\n{m['message'].strip()}\n"
    prompt += f"<|user|>\n{new_message.strip()}\n<|assistant|>\n"
    return prompt

def summarize_history(history, keep_last_n=1):
    return history[-keep_last_n:]

# Run model and return assistant's reply
def generate_response(prompt):
    output = llm(
        prompt,
        max_tokens=100,
        stop=["<|user|>", "<|assistant|>", "<|system|>"]
    )
    response = output["choices"][0]["text"].strip()

    print("----- PROMPT SENT TO MODEL -----")
    print(prompt)
    print(f"[Estimated tokens: {estimate_tokens(prompt)}]")
    print(f"Assistant: {response}")
    print("--------------------------------")

    return response
