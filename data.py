import yfinance as yf
import pandas as pd
import pyarrow.parquet as pq
import pyarrow as pa

from typing import Union
from datetime import date

_FILEPATH = "data/stocks.parquet"

def download_data(tickers: list[str], start: date, end: date) -> None:
    print(f"📥 Downloading data for tickers: {tickers}")
    all_data = []

    for ticker in tickers:
        print(f"⬇️ Downloading {ticker}...")
        df = yf.download(
            ticker,
            start=start.strftime('%Y-%m-%d'),
            end=end.strftime('%Y-%m-%d'),
            group_by="ticker",
        )

        if df.empty:
            print(f"⚠️ No data found for {ticker}")
            continue

        df.columns.names = ['Ticker', 'Attribute']
        df = df.stack(level=0).rename_axis(['Date', 'Ticker']).reset_index()
        all_data.append(df)

    if all_data:
        combined_df = pd.concat(all_data, ignore_index=True)

        # Write once after combining ALL tickers
        table = pa.Table.from_pandas(combined_df)
        pq.write_table(table, _FILEPATH, compression='snappy')
        print(f"✅ Data written to {_FILEPATH}")
    else:
        print("❌ No data downloaded.")

def read_stocks_data() -> pd.DataFrame: 
    """ADD DOCUMENTATION HERE
    """
    return pd.DataFrame(pd.read_parquet(_FILEPATH))
