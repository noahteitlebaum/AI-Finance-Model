import anthropic
import pandas as pd
import os

from datetime import date
from tabulate import tabulate
from dotenv import load_dotenv

# Local dependencies
import handler.data as datahandler
import handler.format as formatter

# Import environment variables and setup the anthropic interface
load_dotenv()
API_KEY = os.getenv("ANTHROPIC_API_KEY")
client = anthropic.Client(api_key=API_KEY)

# Starting and ending data for stock data gathering
start_date = date(2023, 7, 19)
end_date = date.today()

if __name__ == "__main__":
    # Get desired tickers from data dir
    desired_tickers = datahandler.get_desired_tickers()

    # Check already downloaded
    downloaded_tickers = datahandler.get_downloaded_tickers()

    # Compute missing tickers
    tickers_to_download = datahandler.get_tickers_to_download(desired_tickers, downloaded_tickers)

    # Read the combined data and print latest date info
    datahandler.download_data(tickers_to_download, start_date, end_date)

    # This is a dictionary now
    ticker_dict = datahandler.read_all_tickers()

    for ticker, df in ticker_dict.items():
        latest_date = df["Date"].max()
        latest_df = df[df["Date"] == latest_date]
        formatter.print_stock_table(latest_df, title=f"📊 Latest Stock Data Per Ticker ({latest_date.strftime('%Y-%m-%d')})")