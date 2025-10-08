import os
import requests

# Load API key from environment variable for security.
API_KEY = os.getenv("WEATHER_API")

Weather_URL = "https://api.openweathermap.org/data/2.5/weather"

def get_weather(city: str) -> None:
    """Fetch and display the current weather for the given city."""
    params = {
        "q": city,
        "appid": API_KEY,
        "units": "metric",
    }

    try:
        # Make a GET request to the weather API.
        response = requests.get(Weather_URL, params=params, timeout=5)
        response.raise_for_status()  # Raises HTTPError for bad responses.

        # Parse the JSON response into a Python dict.
        data = response.json()

        # OpenWeatherMap sometimes returns 200 even for errors, so check 'cod'.
        if data.get("cod") != 200:
            print(f"Error: {data.get('message', 'Unknown error')}")
            return

        # Extract relevant fields from the response.
        # Use .get() with defaults to avoid KeyError if API changes.
        city_name = data.get("name", "Unknown city")
        country = data.get("sys", {}).get("country", "Unknown country")
        main = data.get("main", {})
        temp = main.get("temp", 0.0)
        feels_like = main.get("feels_like", 0.0)
        humidity = main.get("humidity", 0)
        weather = data.get("weather", [{}])
        condition = weather[0].get("description", "No data").capitalize()
        wind_speed = data.get("wind", {}).get("speed", 0.0)

        # Output: Clean, readable weather report.
        print("\n--- Weather Report ---")
        print(f"{city_name}, {country}")
        print(f"Condition:   {condition}")
        print(f"Temp:        {temp:.1f}°C (feels like {feels_like:.1f}°C)")
        print(f"Humidity:    {humidity}%")
        print(f"Wind Speed:  {wind_speed} m/s")
        print("-" * 25)
    
    # Error handling: Specific cases for common API errors.
    except requests.exceptions.HTTPError as e:
        status_code = e.response.status_code if e.response else None
        if status_code == 401:
            print("Invalid API key.")  # Most common setup mistake.
        elif status_code == 404:
            print(f"City '{city}' not found.")  # User typo or invalid city.
        else:
            print(f"HTTP error occurred: {e}")
    except requests.exceptions.ConnectionError:
        print("Network error. Please check your connection.")  # Covers DNS, offline, etc.
    except Exception as e:
        print(f"Unexpected error: {e}")  # Catch-all for anything else.

if __name__ == "__main__":
    print("Welcome to the Weather App!")
    
    # Check the weather for any city as many times as you like
    while True:
        city = input("\nEnter a city (or type 'quit' to exit): ").strip()
        if city.lower() == "quit":
            print("Goodbye!")
            break

        if city:
            get_weather(city)
            print("Please enter a valid city name.")
            continue

        choice = input("Wanna try with another city? (y/n): ").strip().lower()
        # Quick way to try another city without restarting.
