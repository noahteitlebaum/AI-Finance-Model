import anthropic
from dotenv import load_dotenv
import pandas as pd
import os

# local imports
import data
from datetime import date
from tabulate import tabulate

load_dotenv()
API_KEY = os.getenv("ANTHROPIC_API_KEY")
client = anthropic.Client(api_key=API_KEY)

TICKERS = ["AAPL", "TSLA", "AMZN", "GOOG", "MSFT", "NFLX", "META", "NVDA", "AMD", "INTC"]
start_date = date(2023, 7, 19)
end_date = date.today()

def print_stock_table(df: pd.DataFrame, title: str) -> None:
    if df.empty:
        print("No data to display.")
        return

    # Pick desired columns (flexible if more columns appear)
    cols_to_show = ["Open", "High", "Low", "Close", "Volume"]
    display_df = df[["Ticker", "Date"] + cols_to_show]
    display_df["Date"] = pd.to_datetime(display_df["Date"]).dt.date

    # Round and format
    display_df[cols_to_show] = display_df[cols_to_show].round(2)

    # Set Ticker as index
    display_df = display_df.set_index("Ticker")

    # Print nicely
    print(f"\n{title}")
    print(tabulate(display_df, headers="keys", tablefmt="fancy_grid"))

if __name__ == "__main__":
    # Read the combined data and print latest date info
    # data.download_data(TICKERS, start_date, end_date)

    df = data.read_stocks_data()
    latest_date = df["Date"].max()
    latest_df = df[df["Date"] == latest_date]
    
    print_stock_table(latest_df, title=f"📊 Latest Stock Data Per Ticker ({latest_date.strftime('%Y-%m-%d')})")