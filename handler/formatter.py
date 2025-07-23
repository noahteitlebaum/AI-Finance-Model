import pandas as pd
from tabulate import tabulate

def print_stock_table(df: pd.DataFrame, title: str) -> None:
    """
    Create docstring in a neat format for the print_stock_table function.  
    """

    if df.empty:
        print("No data to display.")
        return

    # Pick desired columns 
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

def summarize_stock_history(df: pd.DataFrame, days: int = 30) -> str:
    """
    Takes the last `days` of stock data and returns a CSV-like string for LLM input.
    """
    
    df = df.sort_values("Date").tail(days)
    summary = df[["Date", "Open", "High", "Low", "Close", "Volume"]].to_csv(index=False)
    return summary