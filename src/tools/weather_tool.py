import os
import requests
from dotenv import load_dotenv

load_dotenv()

# MUST be defined before printing
API_KEY = os.getenv("WEATHER_API_KEY")

print("🌦️ WEATHER API KEY:", API_KEY)

def get_weather(city: str):
    if not API_KEY:
        return "❌ Weather API key not loaded. Check your .env file."

    url = "https://api.openweathermap.org/data/2.5/weather"

    params = {
        "q": city.strip(),
        "appid": API_KEY,
        "units": "metric"
    }
    

    try:
        response = requests.get(url, params=params, timeout=10)
    except Exception as e:
        return f"❌ Weather service error: {e}"

    if response.status_code != 200:
        return f"❌ Could not find weather for {city.title()}"

    data = response.json()

    temp = data["main"]["temp"]
    feels_like = data["main"]["feels_like"]
    desc = data["weather"][0]["description"]
    humidity = data["main"]["humidity"]
    wind = data["wind"]["speed"]

    return (
        f"🌤️ Weather in {city.title()}:\n"
        f"🌡️ Temperature: {temp}°C (Feels like {feels_like}°C)\n"
        f"💧 Humidity: {humidity}%\n"
        f"💨 Wind Speed: {wind} m/s\n"
        f"📌 Condition: {desc.capitalize()}"
    )
