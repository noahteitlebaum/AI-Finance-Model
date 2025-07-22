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
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

# Starting and ending data for stock data gathering
start_date = date(2023, 7, 19)
end_date = date.today()

def ask_ai_about_stock(ticker: str, df: pd.DataFrame) -> str:
    """
    Uses Claude to analyze the historical stock data and provide an outlook.
    """

    history = formatter.summarize_stock_history(df)
    prompt = (
        f"You are a financial analyst. Here is the past 30 days of data for {ticker}:\n\n"
        f"{history}\n\n"
        f"Based on this, what patterns do you observe, and what might happen in the next week or two? "
        "Explain your reasoning clearly but concisely. Don't give investment advice, just trends and analysis."
    )

    response = client.messages.create(
        model="claude-3-haiku-20240307",
        max_tokens=500,
        temperature=0.7,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    
    return response.content[0].text

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

        # Get AI insights
        print(f"\nAI Insight for {ticker}:")
        try:
            insight = ask_ai_about_stock(ticker, df)
            print(insight)
        except Exception as e:
            print(f"Error fetching insight: {e}")