from typing import List
from openai.types.chat import ChatCompletionMessageParam

from config.llm import client

messages: List[ChatCompletionMessageParam] = [
{"role":"system","content":"You are a helpful assistant"}
]
while (query := input("User (press 'q' to exit): ")) != 'q':
        user_message: ChatCompletionMessageParam = {"role":"user","content":query}
        messages.append(user_message)
        response = client.chat.completions.create(
            messages=messages,
            # tools=
            model="liquid/lfm2-24b-a2b",
            temperature=0.7,
            max_tokens=200
        )
        messages.append({"role":"assistant","content":response.choices[0].message.content})
        print("LLM Response : ",response.choices[0].message.content)
        print("\n******")
        print("LLM Usage :",response.usage.model_dump_json(indent=2),"\n")