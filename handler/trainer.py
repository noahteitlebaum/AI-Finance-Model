from sklearn.linear_model import LinearRegression

import pandas as pd
import numpy as np
import os
import joblib

def train_and_save_models(ticker_dict: dict[str, pd.DataFrame], model_dir: str = "models") -> None:
    """
    Trains a simple linear regression model for each ticker and saves them.
    """

    os.makedirs(model_dir, exist_ok=True)

    for ticker, df in ticker_dict.items():
        df = df.sort_values("Date").dropna()
        df["Day"] = np.arange(len(df))  # numerical index for time
        X = df[["Day"]]
        y = df["Close"]

        # Train simple model
        model = LinearRegression()
        model.fit(X, y)

        # Save model
        model_path = os.path.join(model_dir, f"{ticker}.joblib")
        joblib.dump(model, model_path)
        print(f"Saved model for {ticker} to {model_path}")
