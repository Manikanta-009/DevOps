import os
import requests

# Feiklds require to fecth the Currency detsild
API_KEY = os.getenv("CURRENCY_API")
CURRENCY_URL = "https://api.freecurrencyapi.com/v1/latest"


def fetch_rates(base_currency, target_currencies):
    params = {
        'apikey': API_KEY,
        'base_currency': base_currency,
        'currencies': ','.join(target_currencies)
    }
    try:
        
        response = requests.get(CURRENCY_URL, params=params, timeout=5)
        response.raise_for_status()
        
        data = response.json()
        
        rates = data.get('data')
        if not rates:
            raise ValueError("No rates returned. Check currency codes.")
        return rates
    
    except requests.exceptions.RequestException as exc:
        print(f"ERROR: Request failed: {exc}")
        raise
    except Exception as exc:
        print(f"ERROR: Unexpected error: {exc}")
        raise


def convert_amount(amount, rates):
    return {cur: amount * rate for cur, rate in rates.items()}


if __name__ == "__main__":
    base_currency = input("Base Currency (e.g. USD): ").strip().upper()
    try:
        amount = float(input("Amount: "))
    except ValueError:
        print("ERROR: Invalid amount entered.")
        exit(1)

    to_currencies = [currency.strip().upper() 
                     for currency in input("Currencies to convert to (comma separated, e.g. INR,EUR,GBP): ").split(',') 
                     if currency.strip()]

    if not API_KEY:
        print("ERROR: API key 'CURRENCY_API' is not available.")
        exit(1)

    try:
        rates = fetch_rates(base_currency, to_currencies)
        converted = convert_amount(amount, rates)
        for currency, value in converted.items():
            print(f"{amount} {base_currency} = {value:.2f} {currency}")
    except Exception:
        print("ERROR: Conversion failed.")
