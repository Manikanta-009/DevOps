import os
import requests

# Fields required to fetch currency details
API_KEY = os.getenv("CURRENCY_API")
CURRENCY_URL = "https://api.freecurrencyapi.com/v1/latest"

def convert_currency(amount, from_currency, to_currencies):
    """
    Convert an amount from one currency to multiple target currencies using FreeCurrencyAPI.
    """

    from_currency = from_currency.strip().upper()

    # Clean up input: remove spaces and convert currency codes to uppercase (e.g., INR, USD, GBP, EUR)
    to_currencies = ','.join([c.strip().upper() for c in to_currencies.split(',')])

    params = {
        'apikey': API_KEY,
        'base_currency': from_currency,
        'currencies': to_currencies
    }

    print("\nRetrieving the latest exchange rates...\n")

    try:
        resp = requests.get(CURRENCY_URL, params=params, timeout=5)
        resp.raise_for_status()
        data = resp.json()

        rates = data.get('data', {})
        if not rates:
            print("No data received. Please verify the currency codes and try again.")
            return None

        print("Exchange rates successfully retrieved.\n")

        print(f"Converting {amount} {from_currency} to: {to_currencies}\n")

        for cur, rate in rates.items():
            converted = amount * rate
            print(f"{amount} {from_currency} = {converted:.2f} {cur}")

        print("\nConversion completed.\n")

    except requests.exceptions.Timeout:
        print("Request timed out. Please check your internet connection and try again.")
    except requests.exceptions.HTTPError as e:
        print(f"HTTP Error: {e.response.status_code} - {e.response.reason}")
    except requests.exceptions.ConnectionError:
        print("Unable to connect to the currency API. Please check your network.")
    except requests.exceptions.RequestException as e:
        print(f"An error occurred during the request: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    from_currency = input("Enter the base currency (e.g., USD): ")
    amount = float(input("Enter the amount to convert: "))
    to_currencies = input("Enter target currencies (comma separated, e.g., INR, EUR, GBP): ")

    convert_currency(amount, from_currency, to_currencies)
