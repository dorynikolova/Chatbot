import os
from dotenv import load_dotenv
from huggingface_hub import InferenceClient
from personality import BILBO_PERSONALITY
import json

load_dotenv()

HF_API_KEY = os.getenv("HF_API_KEY")
MEMORY_PATH = os.path.join(os.path.dirname(__file__), "memory.json") 
with open(MEMORY_PATH, "r", encoding="utf-8") as f: 
    BILBO_MEMORY = json.load(f)

client = InferenceClient(
    model="Qwen/Qwen2.5-7B-Instruct",
    token=HF_API_KEY
)

def build_system_prompt():
    memory_text = (
        f"User name: {BILBO_MEMORY.get('user_name', 'unknown')}.\n"
        f"Spanish level: {BILBO_MEMORY.get('language_level', 'unknown')}.\n"
        f"Exam date: {BILBO_MEMORY.get('exam_date', 'unknown')}.\n"
        f"Weak areas: {', '.join(BILBO_MEMORY.get('weak_areas', []))}.\n"
        f"Preferences: tone {BILBO_MEMORY.get('preferences', {}).get('tone', 'neutral')}.\n"
    )

    return (
        BILBO_PERSONALITY
        + "\n\nHere is what you know about the user:\n"
        + memory_text
        + "\nAlways adapt your explanations and exercises to this profile."
    )

def ask_bilbo(history):
    #messages = [
     #   {"role": "system", "content": BILBO_PERSONALITY},
     #   {"role": "user", "content": user_message}
    #]

    messages = []
    system_prompt = build_system_prompt()
    messages.append({"role": "system", "content": BILBO_PERSONALITY})

    for msg in history:
        if msg["role"] == "user":
            messages.append({"role": "user", "content": msg["content"]})
        else:
            messages.append({"role": "assistant", "content": msg["content"]})

    response = client.chat_completion(
        messages=messages,
        max_tokens=1000, # max words
        temperature=0.7, # controlls randomness, the higher the more creative, but chaotic
        #top_p=0.9 # nucleus sampling, model only samples from the top 90% most likely tokens
    )
    return response.choices[0].message["content"]


