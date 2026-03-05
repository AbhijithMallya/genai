from typing import List
from openai.types.chat import ChatCompletionMessageParam
from datetime import datetime

from config.llm import client

present= datetime.now()
username = input("Please Enter Your Name :")
messages: List[ChatCompletionMessageParam] = [
    {"role": "system", "content": "You are a helpful assistant"}
]

greeting_prompt: ChatCompletionMessageParam = {
    "role": "user",
    "content": f"Greet {username} in oneline ar this time of the day {present}"
}

greeting_response = client.chat.completions.create(
    messages=messages + [greeting_prompt],
    model="liquid/lfm2-24b-a2b",
    temperature=0.7,
    max_tokens=200,
)
greeting = greeting_response.choices[0].message.content
print(f"\n {greeting}\n")

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
