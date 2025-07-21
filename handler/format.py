import pandas as pd

from tabulate import tabulate

def print_stock_table(df: pd.DataFrame, title: str) -> None:
    """Create docstring
    
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
