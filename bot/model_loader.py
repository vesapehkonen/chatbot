import os
MODEL_NAME = os.environ.get("MODEL_NAME", "tinyllama")

if MODEL_NAME == "tinyllama":
    from .tinyllama_model import load_model, build_prompt, generate_response, summarize_history
elif MODEL_NAME == "mistral":
    from .mistral_model import load_model, build_prompt, generate_response, summarize_history
elif MODEL_NAME == "openai":
    from .openai_model import load_model, build_prompt, generate_response, summarize_history
elif MODEL_NAME == "remote":
    from .remote_model import load_model, build_prompt, generate_response, summarize_history
else:
    raise ValueError(f"Unsupported model: {MODEL_NAME}")

