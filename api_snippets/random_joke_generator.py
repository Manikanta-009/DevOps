import requests

JOKE_URL = "https://official-joke-api.appspot.com/random_joke"

def fetch_random_joke():
    """Fetch a random joke from the official joke API."""
    try:
        # Send GET request to joke API
        response = requests.get(JOKE_URL, timeout=5)
        response.raise_for_status()

        # Parse JSON response
        data = response.json()
        setup = data.get('setup', "Error: Failed to retrieve joke setup.")
        punchline = data.get('punchline', "Error: Failed to retrieve punchline.")

        print(f"Setup: {setup}")
        print(f"Punchline: {punchline}")

    except requests.exceptions.ConnectionError:
        print("Network error: Please check your internet connection.")
    except requests.exceptions.Timeout:
        print("Request timed out while fetching the joke.")
    except requests.exceptions.RequestException as e:
        print(f"HTTP error occurred: {e}")
    except ValueError:
        print("Failed to parse response as JSON.")
    except Exception as e:
        print(f"Unexpected error: {e}")

if __name__ == "__main__":
    # Run the joke fetcher
    fetch_random_joke()