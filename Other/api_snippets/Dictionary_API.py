import requests

# URL for the free dictionary API
DICTIONARY_URL = "https://api.dictionaryapi.dev/api/v2/entries/en/"


def get_word_meaning(word: str):
    """Fetch and print the first available meaning of an English word."""
    try:
        # Make a GET request to the dictionary API
        response = requests.get(f"{DICTIONARY_URL}{word.strip().lower()}", timeout=5)
        response.raise_for_status()  # Raise an error if the request failed

        data = response.json()  # Parse the response as JSON
        # Get the first meaning from the response data
        meaning = data[0]["meanings"][0]["definitions"][0].get("definition", "Definition not found.")

        print(f"Word: {word}")
        print(f"Meaning: {meaning}")

    except requests.exceptions.ConnectionError:
        # Handle network errors
        print("Network error: Please check your internet connection.")
    except ValueError:
        # Handle JSON parsing errors
        print("Failed to parse response as JSON.")
    except Exception as e:
        # Handle any other unexpected errors
        print(f"Unexpected error: {e}")


if __name__ == "__main__":
    # Ask the user to enter a word
    word = input("Enter a word to check its meaning: ")
    get_word_meaning(word)
