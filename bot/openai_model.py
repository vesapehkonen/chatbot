import openai
import os

client = openai.OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

def load_model():
    print("[Cloud] OpenAI client initialized.")

def build_prompt(history, new_message):
    messages = [{"role": "system", "content": "You are a helpful assistant."}]
    for m in history:
        role = "user" if m['role'] == 'user' else "assistant"
        messages.append({"role": role, "content": m['message'].strip()})
    messages.append({"role": "user", "content": new_message.strip()})
    return messages

def generate_response(messages):
    response = client.chat.completions.create(
        #model="gpt-3.5-turbo",
        model="gpt-4o",
        messages=messages,
        temperature=0.7
    )
    return response.choices[0].message.content.strip()

def summarize_history(history, keep_last_n=1):
    if len(history) <= keep_last_n:
        return history

    to_summarize = history[:-keep_last_n]
    keep_tail = history[-keep_last_n:]

    convo = ""
    for m in to_summarize:
        role = "User" if m['role'] == 'user' else "Assistant"
        convo += f"{role}: {m['message'].strip()}\n"

    summary_prompt = [
        {"role": "system", "content": "You are a helpful assistant that summarizes previous conversations."},
        {"role": "user", "content": f"Summarize the following conversation:\n\n{convo.strip()}"}
    ]

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=summary_prompt,
        temperature=0.3
    )
    summary = response.choices[0].message.content.strip()

    return [{"role": "system", "message": f"Earlier summary: {summary}"}] + keep_tail
