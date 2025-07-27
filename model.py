import lightgbm as lgb
import numpy as np
import pandas as pd

from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split

def comp_features(df: pd.DataFrame) -> pd.DataFrame:
    """ 
    Compute a set of features for stock price prediction.

    Features created:
    - 1-day return
    - 5-day and 10-day moving averages
    - 5-day rolling standard deviation (volatility proxy)
    - 1-day volume change
    - Target is next day's closing price

    Parameters:
    df (pd.DataFrame): DataFrame containing columns ['Open', 'High', 'Low', 'Close', 'Volume'] with datetime index.

    Returns:
    pd.DataFrame: DataFrame with engineered features and target, with NaNs dropped.
    """
    df = df.copy()

    # Daily return as a simple momentum indicator
    df["Return_1d"] = df["Close"].pct_change()

    # Moving averages capture trend
    df["MA_5"] = df["Close"].rolling(window=5).mean()
    df["MA_10"] = df["Close"].rolling(window=10).mean()
    
    # Volatility proxy using standard deviation
    df["STD_5"] = df["Close"].rolling(window=5).std()

    # Change in volume might indicate breakout or panic
    df["Volume_Change"] = df["Volume"].pct_change()

    # Shift the target column to align features with next-day prediction
    df["Target"] = df["Close"].shift(-1) 

    # Drop rows with NaN (caused by rolling and shift)
    df = df.dropna()

    return df

def train(df: pd.DataFrame) -> lgb.LGBMRegressor:
    """
    Train a LightGBM regression model to predict next-day stock prices.

    Parameters:
    df (pd.DataFrame): DataFrame with computed features and a target column.

    Returns:
    lgb.LGBMRegressor: Trained LightGBM model.
    """
    # Define which features to use (you can add more here)
    features = ["Return_1d", "MA_5", "MA_10", "STD_5", "Volume_Change"]
    target = "Target"

    # Split features and target
    X = df[features]
    y = df[target]

    # Use the most recent 20% for validation (no shuffle to preserve time ordering)
    X_train, X_test, y_train, y_test = train_test_split(X, y, shuffle=False, test_size=0.2)

    # Instantiate and train model with default parameters (tunable later)
    model = lgb.LGBMRegressor()
    model.fit(X_train, y_train)

    # Predict on the test set and print MSE
    y_pred = model.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    print(f"Backtest MSE: {mse:.6f}")

    return model

def train_on_all_tickers(stock_data: dict[str, pd.DataFrame]) -> dict[str, lgb.LGBMRegressor]:
    """
    Train one LightGBM model per ticker using engineered features.

    Parameters:
    stock_data (dict): Dictionary where each key is a ticker (str),
                       and each value is a pd.DataFrame with OHLCV data.

    Returns:
    dict: Dictionary mapping ticker symbols to their trained LightGBM models.
    """
    
    models = {}

    for ticker, df in stock_data.items():
        print(f"\nTraining model for {ticker}...")

        # Compute features and ensure there's enough data
        df = comp_features(df)
        if len(df) < 50:
            print(f"Not enough data for {ticker}, skipping...")
            continue

        # Train model and store it
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