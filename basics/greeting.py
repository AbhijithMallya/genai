from openai import OpenAI
from typing import List
from openai.types.chat import ChatCompletionMessageParam
from datetime import datetime
import os

client = OpenAI(api_key="1234",
                base_url="http://127.0.0.1:8000/v1")

# Time of day
hour = datetime.now().hour
if hour < 12:
    time_of_day = "morning"
elif hour < 17:
    time_of_day = "afternoon"
else:
    time_of_day = "evening"

# Username from Mac
username = os.getlogin()
first_name = username.split(".")[0].capitalize()

messages: List[ChatCompletionMessageParam] = [
    {"role": "system", "content": "You are a helpful assistant"}
]

# Greeting
try:
    greeting_prompt: ChatCompletionMessageParam = {
        "role": "user",
        "content": f"Greet me with Good {time_of_day} {first_name} in one line only."
    }
    greeting_response = client.chat.completions.create(
        messages=messages + [greeting_prompt],
        model="liquid/lfm2-24b-a2b",
        temperature=0.7,
        max_tokens=50,
        timeout=5
    )
    greeting = greeting_response.choices[0].message.content
except Exception as e:
    greeting = f"Good {time_of_day} {first_name}!"  # fallback

print(f"\n {greeting}\n")

# User - Assistant Loop (your original working code)
while (query := input("User (press 'q' to exit): ")) != 'q':
    user_message: ChatCompletionMessageParam = {"role": "user", "content": query}
    messages.append(user_message)

    response = client.chat.completions.create(
        messages=messages,
        model="liquid/lfm2-24b-a2b",
        temperature=0.7,
        max_tokens=200
    )

    messages.append({"role": "assistant", "content": response.choices[0].message.content})
    print("LLM Response : ", response.choices[0].message.content)
    print("\n******")
    if response.usage:
        print("LLM Usage :", response.usage.model_dump_json(indent=2), "\n")
    else:
        print(f"Model : {response.model}\n")

print(f"\n👋 Goodbye {first_name}! Have a great {time_of_day}!")