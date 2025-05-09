import subprocess
import time
from llama_cpp import Llama

#MODEL_PATH = "/mnt/models/mythomax-l2-13b.Q4_K_M.gguf"
MODEL_PATH = "/mnt/models/mistral-7b-instruct-v0.1.Q4_K_M.gguf"

MAX_TOKENS = 100
PROMPT = "### Instruction:\nSay something smart.\n### Response:\n"

llm = Llama(
    model_path=MODEL_PATH,
    n_ctx=2048,
    n_batch=128,
    backend="cuda",
    verbose=True
)

def get_gpu_info():
    try:
        output = subprocess.check_output(["nvidia-smi", "--query-gpu=utilization.gpu,power.draw,memory.used", "--format=csv,noheader,nounits"])
        util, power, mem = map(str.strip, output.decode().strip().split(","))
        return f"GPU: {util}% | Power: {power}W | Mem: {mem} MiB"
    except Exception as e:
        return f"[nvidia-smi failed: {e}]"

print("\nChecking GPU before inference:")
print(get_gpu_info())

print("\nStarting inference...")
start = time.perf_counter()
output = llm(PROMPT, max_tokens=MAX_TOKENS, stop=["###"])
end = time.perf_counter()

response = output["choices"][0]["text"].strip()
print("\nModel Response:")
print(response)

print("\nInference Time: {:.2f} seconds".format(end - start))
print("GPU After Inference:")
print(get_gpu_info())
