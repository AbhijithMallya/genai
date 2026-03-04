from openai import OpenAI
from typing import List
from openai.types.chat import ChatCompletionMessageParam

client = OpenAI(api_key="1234",
                base_url="http://127.0.0.1:8000/v1")


messages: List[ChatCompletionMessageParam] = [
{"role":"system","content":"You are a helpful assistant"}
]

response = client.chat.completions.create(
    messages=messages,
    model="liquid/lfm2-24b-a2b",
    temperature=0.7,
    max_tokens=200
)

while (query := input("User (press 'q' to exit): ")) != 'q':
        user_message: ChatCompletionMessageParam = {"role":"user","content":query}
        response = client.chat.completions.create(
            messages=messages,
            model="liquid/lfm2-24b-a2b",
            temperature=0.7,
            max_tokens=200
        )
        messages.append({"role":"assistant","conten":response.choices[0].message.content})
        print("LLM Response : ",response.choices[0].message.content)
        print("\n******\n")
        print("LLM Usage : ",response.usage.model_dump_json(indent=2),"\n")