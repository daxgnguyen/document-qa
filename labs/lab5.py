import requests
import streamlit as st
import json
from openai import OpenAI


def get_current_weather(location, weather_api_key, units='imperial'):
    url = (
        f"http://api.openweathermap.org/data/2.5/weather?"
        f"q={location}&appid={weather_api_key}&units={units}"
 )
    response = requests.get(url)
    if response.status_code == 401:
        raise Exception("Authentication failed: Invalid API key.")
    if response.status_code == 404:
        error_message = response.json().get("message")
        raise Exception(f"404 error: {error_message}")
    data = response.json()
    temp = data['main']['temp']
    feels_like = data['main']['feels_like']
    temp_min = data['main']['temp_min']
    temp_max = data['main']['temp_max']
    humidity = data['main']['humidity']
    return {'location':location,
        'temperature':round(temp, 2),
        'feels_like': round(feels_like, 2),
        'temp_min': round(temp_min, 2),
        'temp_max': round(temp_max, 2),
        'humidity': round(humidity, 2)
    }

weather_tool = {
    "type": "function",
    "function": {
        "name": "get_current_weather",
        "description": "Get the current weather for a location",
        "parameters": {
            "type": "object",
            "properties": {
                "location": {
                    "type": "string",
                    "description": "The city and state, e.g. Syracuse, NY"
                }
            },
            "required": ["location"]
        }
    }
}

client = OpenAI(api_key=st.secrets["openai_api_key"])

# Show title and description.
st.title("Weather Bot")
st.write(
    "Get recommendations on what to wear based on the current weather! "
)

with st.sidebar:
    city = st.text_input("Location:", value="Syracuse, NY")
    go = st.button("Get Weather")

if go:
    r1 = client.chat.completions.create(
        model='gpt-4o-mini',
        messages=[{"role": "user", "content": f"Recommend what to wear based on the current weather in {city}."}],
        tools=[weather_tool],
        tool_choice="auto"
    )
    msg = r1.choices[0].message

    if msg.tool_calls:
        tc = msg.tool_calls[0]
        args = json.loads(tc.function.arguments)
        weather = get_current_weather(city, st.secrets["weather_api_key"])
        st.json(weather)

        r2 = client.chat.completions.create(
            model='gpt-4o-mini',
            messages=[
                {"role": "user", "content": f"Recommend what to wear based on the current weather in {city}."},
                msg,
                {"role": "tool", "tool_call_id": tc.id, "content": json.dumps(weather)}
            ]
        )

        st.write(r2.choices[0].message.content)