""" Market Service """

"""_summary_
this file to write any business logic for the Market
"""

import os
from dotenv import load_dotenv
import requests

from .market_schema import Market

# load .env variables
load_dotenv()
RAPID_API_KEY = os.getenv("RAPID_API_KEY")
RAPID_API_HOST = os.getenv("RAPID_API_HOST")
RAPID_DATA_URL = os.getenv("RAPID_DATA_URL")

tickers = ["AAPL", "MSFT", "GOOG", "AMZN", "META"]

# TODO: convert to async requests to speed up results


def get_market_data() -> list[Market]:

    headers = {"x-rapidapi-key": RAPID_API_KEY, "x-rapidapi-host": RAPID_API_HOST}

    tickers_data = []
    for ticker in tickers:
        try:
            querystring = {"ticker": ticker, "type": "STOCKS"}
            response = requests.get(RAPID_DATA_URL, headers=headers, params=querystring)
            response.raise_for_status()
            data = response.json()
            symbol = data["body"]["symbol"]
            price = float(data["body"]["primaryData"]["lastSalePrice"].strip("$"))
            tickers_data.append(Market(symbol=symbol, price=price))

        # gpt generated
        except requests.exceptions.HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")  # e.g., 404 Not Found
        except requests.exceptions.RequestException as req_err:
            print(f"Request error occurred: {req_err}")  # Network-related issues
        except ValueError as val_err:
            print(
                f"Value error occurred: {val_err}"
            )  # Errors during parsing/formatting
        except KeyError as key_err:
            print(
                f"Key error occurred: {key_err}"
            )  # If any expected field is missing in response

    return tickers_data
