import lightgbm as lgb
import numpy as np
import pandas as pd

from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split

def comp_features(df: pd.DataFrame) -> pd.DataFrame:
    """ 
    """

    df = df.copy()
    df["Return_1d"] = df["Close"].pct_change()
    df["MA_5"] = df["Close"].rolling(window=5).mean()
    df["MA_10"] = df["Close"].rolling(window=10).mean()
    df["STD_5"] = df["Close"].rolling(window=5).std()
    df["Volume_Change"] = df["Volume"].pct_change()
    df["Target"] = df["Close"].shift(-1)  # Next-day close

    df = df.dropna()
    return df

def train(df: pd.DataFrame) -> lgb.LGBMRegressor:
    """ADD DOCUMENTATION
    """
    
    features = ["Return_1d", "MA_5", "MA_10", "STD_5", "Volume_Change"]
    target = "Target"

    X = df[features]
    y = df[target]

    X_train, X_test, y_train, y_test = train_test_split(X, y, shuffle=False, test_size=0.2)

    model = lgb.LGBMRegressor()
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)

    print(f"Backtest MSE: {mse:.6f}")
    return model

def train_on_all_tickers(stock_data: dict[str, pd.DataFrame]) -> dict[str, lgb.LGBMRegressor]:
    models = {}

    for ticker, df in stock_data.items():
        print(f"\nTraining model for {ticker}...")
        df = comp_features(df)
        if len(df) < 50:
            print(f"Not enough data for {ticker}, skipping...")
            continue
        model = train(df)
        models[ticker] = model

    return models

def optimize(df: pd.DataFrame):
    """ADD DOCUMENTATION
    """
    pass

def backtest(df: pd.DataFrame):
    """ADD DOCUMENTATION
    """
    pass