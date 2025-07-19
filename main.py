import anthropic

from datetime import date
from dotenv import load_dotenv

# local imports
import data

API_KEY = load_dotenv()
TICKERS = ["AAPL", "TSLA", "AMZN", "GOOG"]

client = anthropic.Client(api_key=API_KEY)

start_date = date(2023, 7, 19)
end_date = date(2025, 7, 19)

if __name__ == "__main__":
    # Never have to do again unless downloading new stocks
    #data.download_first_data(TICKERS, start_date, end_date)

    #data.download_first_data(TICKERS, start_date, end_date)

    df = data.read_stocks_data()
    print(df.style)
