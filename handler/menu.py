import pandas as pd

from datetime import date

# Local Dependencies
from . import data
from . import formatter
from . import anthropic

def menu(): 
    print("\n--- MAIN MENU ---")
    print("1. Download Stock Data")
    print("2. Train Model")
    print("3. Display Results")
    print("4. Quit")
    print("Type ESC at any time to return to this menu.")

def handle_download(start_date: date, end_date: date) -> dict[str, pd.DataFrame]:
    """
    """
    print("\n[DOWNLOAD MODE]")
    input("Press ENTER to simulate download. Type ESC to return to menu.\n")

    # Get desired tickers from data dir
    desired_tickers = data.get_desired_tickers()

    # Check already downloaded
    downloaded_tickers = data.get_downloaded_tickers()

    # Compute missing tickers
    tickers_to_download = data.get_tickers_to_download(desired_tickers, downloaded_tickers)

    # Read the combined data and print latest date info
    data.download_data(tickers_to_download, start_date, end_date)

    # This is a dictionary now
    return data.read_all_tickers()

def handle_train():
    """
    """

    print("\n[TRAIN MODE]")
    input("Press ENTER to simulate training. Type ESC to return to menu.\n")

def handle_display(ticker_dict: dict[str, pd.DataFrame]):
    """
    """

    print("\n[DISPLAY MODE]")
    input("Press ENTER to simulate display. Type ESC to return to menu.\n")

    for ticker, df in ticker_dict.items():
        latest_date = df["Date"].max()
        latest_df = df[df["Date"] == latest_date]
        formatter.print_stock_table(latest_df, title=f"📊 Latest Stock Data Per Ticker ({latest_date.strftime('%Y-%m-%d')})")

        # Get AI insights
        print(f"\nAI Insight for {ticker}:")
        try:
            insight = anthropic.ask_ai_about_stock(ticker, df)
            print(insight)
        except Exception as e:
            print(f"Error fetching insight: {e}")