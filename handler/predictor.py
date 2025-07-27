import pandas as pd
import numpy as np
import joblib
import os

def predict_next_prices(ticker: str, df: pd.DataFrame, days_ahead: int = 5, model_dir: str = "models") -> list[float]:
    """
    Loads model for ticker and predicts future prices.
    """

    model_path = os.path.join(model_dir, f"{ticker}.joblib")

    if not os.path.exists(model_path):
        return ["Model not found"]

    model = joblib.load(model_path)
    df = df.sort_values("Date").dropna()
    last_day = len(df) - 1
    future_days = np.arange(last_day + 1, last_day + 1 + days_ahead).reshape(-1, 1)

    predictions = model.predict(future_days)
    return [round(p, 2) for p in predictions]
