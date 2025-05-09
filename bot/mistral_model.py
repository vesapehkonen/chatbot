import os
from llama_cpp import Llama

llm = None

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "..", "models", "mistral", "mistral-7b-instruct-v0.1.Q4_K_M.gguf")


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
    print("[Mistral] Model loaded.")

def build_prompt(history, new_message):
    prompt = ""
    for m in history:
        if m['role'] == 'user':
            prompt += f"### Instruction:\n{m['message'].strip()}\n"
        elif m['role'] == 'bot':
            prompt += f"### Response:\n{m['message'].strip()}\n"
    prompt += f"### Instruction:\n{new_message.strip()}\n### Response:\n"
    return prompt

def summarize_history(history, keep_last_n=1):
    return history[-keep_last_n:]

def generate_response(prompt):
    output = llm(prompt, max_tokens=100, stop=["### Instruction", "### Response"])
    return output["choices"][0]["text"].strip()
