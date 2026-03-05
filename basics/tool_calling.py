# Tool calling sample
import json
from function_schema import get_function_schema



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

#Functions ====

def get_weather(place : str):
    """
    This a function to get the weather of a 'place'. Please use lowercase only
    Allowed places are udupi, trivandrum and bombay 
    
    """
    try :    
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
        popular = food[place]
        return popular
    except Exception as e :
        return "The given place is not available"


tool_calls = [get_function_schema(get_weather),
              get_function_schema(get_school_count),
              get_function_schema(get_popular_food)]



function_mapping = {"get_weather":get_weather,
                    "get_school_count":get_school_count,
                    "get_popular_food":get_popular_food}


print(function_mapping["get_popular_food"]("udupi"))
