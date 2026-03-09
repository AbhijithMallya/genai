# python -m basics.tool_calling


# Tool calling sample
import json

from openai.types.chat import ChatCompletionMessageParam
from function_schema import get_function_schema
from config.llm import client

# DATA ====
weather = {
    "udupi":"26",
    "trivandrum":"20",
    "bombay":"15",
}

school_count = {
    "udupi" : 5,
    "trivandrum" : 7,
    "bombay" : 3
}

food = {
    "udupi" : "idli",
    "trivandrum" : "poori",
    "bombay" : "vadapav"
}
# DATA ====

#FUNCTIONS ====
def get_weather(place : str):
    """
    This a function to get the weather of a 'place'. Please use lowercase only
    Allowed places are udupi, trivandrum and bombay 
    
    """
    try :    
        print("executing get weather ...")
        temperature = weather[place]
        return temperature
    except Exception as e :
        return "The given place is not available"

def get_school_count(place : str):
    """
    This a function to get the number of schools in a 'place'. Please use lowercase only
    Allowed places are udupi, trivandrum and bombay 
    """
    try :    
        print("executing get school count")
        count = school_count[place]
        return count
    except Exception as e :
        return "The given place is not available"

def get_popular_food(place: str):
    """
    This a function to get the popular food of a 'place'. Please use lowercase only
    Allowed places are udupi, trivandrum and bombay 
    """
    try:
        print("executing. get popular food")
        popular = food[place]
        return popular
    except Exception as e :
        return "The given place is not available"
#FUNCTIONS ====

TOOLS = [
    {
    "type": "function",
    "function": get_function_schema(get_weather)},
    {"type": "function",
     "function":get_function_schema(get_school_count)},
    {"type":"function",
     "function":get_function_schema(get_popular_food)}
     ]
MODEL = "openai/gpt-oss-20b"
TEMP = 0.7

def get_function_by_name(name):
    if name == "get_weather":
        return get_weather
    elif name == "get_school_count":
        return get_school_count
    elif name =="get_popular_food":
        return get_popular_food
    else:
        raise RuntimeError(f"No function named {name}")


messages: list[ChatCompletionMessageParam] = []

while (query := input("User (press 'q' to exit): ")) != 'q':
        user_message: ChatCompletionMessageParam = {"role":"user","content":query}
        messages.append(user_message)
        completion = client.chat.completions.create(
            model = MODEL,
            temperature=TEMP,
            messages = messages,
            tools = TOOLS,
            tool_choice="auto"
        )
        print('Tool Calls : ',completion.choices[0].message.tool_calls)
        message = completion.choices[0].message
        messages.append(message)

        while len((tool_call := message.tool_calls) or []) != 0:
            tool_call = tool_call[0]
            function_name = tool_call.function.name
            arguments = json.loads(tool_call.function.arguments)
            result = get_function_by_name(function_name)(**arguments)
            print(f"--> Function Name : {function_name}\n--> Function Result : {result}")
            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": str(result),
            })
            completion = client.chat.completions.create(
                model = MODEL,
                temperature=TEMP,
                messages = messages,
                tools = TOOLS,
                tool_choice="auto"
            )
            message = completion.choices[0].message
        print("Assistant : ",message.content)