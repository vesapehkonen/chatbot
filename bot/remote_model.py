import requests
import os
import hashlib

REMOTE_URL = os.environ.get("REMOTE_MODEL_URL", "http://YOUR.CLOUD.IP:5000/generate")
API_KEY = os.environ.get("MODEL_API_KEY", "mysecretkey")  # match cloud key

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

def load_model():
    pass  # nothing local

def build_prompt(history, message, concise=True):
    prompt = ""

    if concise:
        prompt += "You are an assistant that always gives short answers, no more than two sentences, even for creative or roleplay prompts."
        
    for m in history:
        if m['role'] == 'user':
            prompt += f"### Instruction:\n{m['message'].strip()}\n"
        elif m['role'] == 'bot':
            prompt += f"### Response:\n{m['message'].strip()}\n"

    prompt += f"### Instruction:\n{message.strip()}\n### Response:\n"
    return prompt


# In-memory summary cache
summary_cache = {}

def hash_messages(messages):
    """Create a hash from a list of message dicts (user/assistant turns)."""
    joined = "\n".join(f"{m['role']}:{m['message']}" for m in messages)
    return hashlib.md5(joined.encode()).hexdigest()

def summarize_history(messages, keep_last_n=1):
    """Summarize early messages using remote LLM, with cache."""
    if len(messages) <= keep_last_n * 2:
        return messages

    # Split early and recent messages
    earlier_msgs = messages[:-keep_last_n * 2]
    recent_msgs = messages[-keep_last_n * 2:]

    # Generate a cache key for earlier messages
    cache_key = hash_messages(earlier_msgs)

    if cache_key in summary_cache:
        summary = summary_cache[cache_key]
        print("✅ Using cached summary")
    else:
        # Build summary prompt
        plain_history = ""
        for m in earlier_msgs:
            prefix = "User" if m["role"] == "user" else "Assistant"
            plain_history += f"{prefix}: {m['message']}\n"

        summary_prompt = (
            "### Instruction:\nSummarize the following conversation:\n\n"
            f"{plain_history}\n\n### Response:\n"
        )

        print("⏳ Generating new summary")
        res = requests.post(REMOTE_URL, json={
            "prompt": summary_prompt
        }, headers=headers)
        res.raise_for_status()

        summary = res.json()["reply"].strip()

        summary_cache[cache_key] = summary

    # Return compressed chat history
    summarized = {
        "role": "user",
        "message": f"(Earlier summary: {summary})"
    }

    return [summarized] + recent_msgs

"""
def summarize_history(messages, keep_last_n=1):
    if len(messages) <= keep_last_n * 2:
        return messages

    earlier_msgs = messages[:-keep_last_n * 2]
    recent_msgs = messages[-keep_last_n * 2:]

    plain_history = ""
    for m in earlier_msgs:
        prefix = "User" if m["role"] == "user" else "Assistant"
        plain_history += f"{prefix}: {m['message']}\n"

    # Create a summarization prompt
    summary_prompt = (
        "### Instruction:\nSummarize the following conversation:\n\n"
        f"{plain_history}\n\n### Response:\n"
    )

    # Call your cloud model server
    res = requests.post(REMOTE_URL, json={
        "prompt": summary_prompt
    }, headers=headers)
    res.raise_for_status()
    summary = res.json()["reply"].strip()

    summarized = {
        "role": "user",
        "message": f"(Earlier summary: {summary})"
    }

    return [summarized] + recent_msgs
"""

def generate_response(prompt):
    res = requests.post(REMOTE_URL, json={
        "prompt": prompt,
        "stop": ["### Instruction", "### Response"]
    }, headers=headers)
    res.raise_for_status()
    return res.json()["reply"]
