import yfinance as yf
import pandas as pd
import pyarrow.parquet as pq
import pyarrow as pa

from typing import Union
from datetime import date

_filepath = "data/stocks.parquet"

def download_first_data(tickers: list[str], start: date , end: date) -> None:
    """ONLY RUN ONCE

        %Y-%m-%d for time formating
    """

    print(f"Trying to download data from: {tickers}") 

    # Potential ticker validation
    # for ticker in tickers: 
    #     if(not yf.Ticker(ticker).info):
    #         tickers.remove(ticker) 

    try:
        for ticker in tickers:
            df = yf.download(ticker, start=start.strftime('%Y-%m-%d'), end=end.strftime("%Y-%m-%d"), group_by=ticker)

            # Flatten MultiIndex columns
            df.columns.names = ['Ticker', 'Attribute']
            df = df.stack(level=0).rename_axis(['Date', 'Ticker']).reset_index()

            # Write the data to the parquet
            table = pa.Table.from_pandas(df)
            pq.write_table(table, _filepath, compression='snappy')    

    except FileNotFoundError:
        print(FileNotFoundError)

def update_stock_data(ticker) -> None:
    """ ADD DOCUMENTATION HERE
    """
    # Load current data

    try: 
        current_df = pd.read_parquet(_filepath)
        last_date = current_df[current_df["Ticker"] == ticker]["Date"].max()
        
        # Download new data
        new_df = yf.download(ticker, start=str(last_date + pd.Timedelta(days=1)))
        if not new_df.empty:
            new_df = new_df.reset_index()
            new_df["Ticker"] = ticker
            updated_df = pd.concat([current_df, new_df], ignore_index=True)
            pq.write_table(pa.Table.from_pandas(updated_df), _filepath, compression="snappy")

    except FileExistsError:
        print(FileNotFoundError)

def read_stocks_data() -> pd.DataFrame: 
    """ADD DOCUMENTATION HERE
    """
    return pd.DataFrame(pd.read_parquet(_filepath))
