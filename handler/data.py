import yfinance as yf
import pandas as pd
import pyarrow.parquet as pq
import pyarrow as pa
import os

from datetime import date

def download_data(tickers: list[str], start: date, end: date) -> None:
    """
    Downloads historical stock data for the given tickers between start and end dates
    using yfinance, and saves each ticker's data to a separate Parquet file.
    """
    
    # Ensure data directory exists
    os.makedirs("data", exist_ok=True)

    for ticker in tickers:
        print(f"Downloading {ticker}...")

        df = yf.download(ticker, start=start.strftime('%Y-%m-%d'), end=end.strftime('%Y-%m-%d'), group_by="ticker")

        # Check to see if there is stock data
        if df.empty:
            print(f"No data found for {ticker}")
            continue

        df.columns.names = ['Ticker', 'Attribute']
        df = df.stack(level=0).rename_axis(['Date', 'Ticker']).reset_index()

        table = pa.Table.from_pandas(df)
        pq.write_table(table, f"data/{ticker}.parquet", compression='snappy')

        print(f"{ticker} data downloaded")

def read_all_tickers(data_dir:str="data") -> dict[str, pd.DataFrame]: 
    """
    Reads all .parquet files in the given data directory and returns a dictionary
    mapping ticker symbols to their corresponding DataFrames.

    Each file is expected to be named as <ticker>.parquet.
    """

    stock_data = {}

    # Iterate through the downloaded tickers
    for filename in os.listdir(data_dir):
        if filename.endswith(".parquet"):
            ticker = filename.removesuffix(".parquet").upper()
            filepath = os.path.join(data_dir, filename)
            
            # Try to 
            try:
                df = pd.read_parquet(filepath)
                stock_data[ticker] = df
            except Exception as e:
                print(f"Failed to read {filepath}: {e}")

    return stock_data

def read_specified_tickers(tickers: list[str], data_dir:str="data") -> dict[str, pd.DataFrame]:
    """
    Reads .parquet files for the specified tickers from the given data directory and returns
    a dictionary mapping ticker symbols to their corresponding DataFrames.

    Parameters:
        tickers (list[str]): List of ticker symbols to load (case-insensitive).
        data_dir (str): Path to the directory containing <ticker>.parquet files.

    Returns:
        dict[str, pd.DataFrame]: A mapping from ticker symbols to DataFrames.
    """

    stock_data = {}
    for ticker in tickers:
        filename = f"{ticker.upper()}.parquet"
        filepath = os.path.join(data_dir, filename)

        if not os.path.exists(filepath):
            print(f"File not found for ticker: {ticker}")
            continue

        try:
            df = pd.read_parquet(filepath)
            stock_data[ticker.upper()] = df
        except Exception as e:
            print(f"Failed to read {filepath}: {e}")

    return stock_data

def get_desired_tickers(file_path: str = "tickers.txt") -> list[str]:
    """
    Reads tickers from a file.
    """

    with open(file_path, 'r') as f:
        return [line.strip().upper() for line in f if line.strip()]
    
def get_downloaded_tickers(data_dir:str="data") -> set[str]:
    """    
    Given a list of tickers, return those which have not yet been downloaded
    based on presence of corresponding <ticker>.parquet files in `data_dir`.
    """

    return {
        filename.removesuffix(".parquet")
        for filename in os.listdir(data_dir)
        if filename.endswith(".parquet")
    }

def get_tickers_to_download(desired: list[str], downloaded: set[str]) -> list[str]:
    """
    Checks for the difference between downloaded tickers and tickers that we have
    stored withind data/tickers.txt
    """

    tickers = []
    for ticker in desired:
        if ticker not in downloaded:
            tickers.append(ticker)

    return tickers