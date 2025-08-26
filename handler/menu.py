import pandas as pd

from datetime import date

# Local Dependencies
from . import data
from . import formatter
from . import anthropic
from . import trainer
from . import predictor

def menu(): 
    print("\n--- MAIN MENU ---")
    print("1. Download Stock Data")
    print("2. Train Model")
    print("3. Display Results")
    print("4. Quit")

def handle_download(start_date: date, end_date: date) -> dict[str, pd.DataFrame]:
    """
    """
    print("\n[DOWNLOAD MODE]")
    input("Press ENTER to simulate download.\n")

    try:
        # Get desired tickers from data dir
        desired_tickers = data.get_desired_tickers()

        # Check already downloaded
        downloaded_tickers = data.get_downloaded_tickers()

        # Compute missing tickers
        tickers_to_download = data.get_tickers_to_download(desired_tickers, downloaded_tickers)

        # Read the combined data and print latest date info
        data.download_data(tickers_to_download, start_date, end_date)

        print("Data download complete.")
        input("Press ANY KEY to return to the main menu...")

        return data.read_all_tickers()
    except Exception as e:
        print(f"Error during download: {e}")
        input("Press ANY KEY to return to the main menu...")

    return {}

def handle_train(ticker_dict: dict[str, pd.DataFrame]):
    if len(ticker_dict) == 0:
        print("\nNo data available. Please download stock data first!")
        input("Press ANY KEY to return to the main menu...")
        return

    print("\n[TRAIN MODE]")
    input("Press ENTER to train models.\n")

    trainer.train_and_save_models(ticker_dict)
    
    print("\nTraining complete!")
    input("Press ANY KEY to return to the main menu...")

def handle_display(ticker_dict: dict[str, pd.DataFrame]):
    if len(ticker_dict) == 0:
        print("\nNo data available. Please download stock data first!")
        input("Press ANY KEY to return to the main menu...")
        return
    
    print("\n[DISPLAY MODE]")
    input("Press ENTER to display.\n")

    for ticker, df in ticker_dict.items():
        latest_date = df["Date"].max()
        latest_df = df[df["Date"] == latest_date]
        formatter.print_stock_table(latest_df, title=f"📊 Latest Stock Data Per Ticker ({latest_date.strftime('%Y-%m-%d')})")

        # AI Insight
        print(f"\nClaude AI Insight for {ticker}:")
        try:
            insight = anthropic.ask_ai_about_stock(ticker, df)
            print(insight)
        except Exception as e:
            print(f"Error fetching insight: {e}")

        import warnings
        from sklearn.exceptions import DataConversionWarning

        print(f"\nModel Prediction for {ticker} (next 5 days):")
        try:
            # Suppress the specific warning from sklearn about feature names
            with warnings.catch_warnings():
                warnings.simplefilter("ignore", category=UserWarning)
                warnings.simplefilter("ignore", category=DataConversionWarning)
                
                predictions = predictor.predict_next_prices(ticker, df, days_ahead=5)
            
            # Format nicely (convert numpy floats to python floats)
            clean_preds = [float(p) for p in predictions]
            
            # Print in a friendly way, e.g. as a bullet list or comma-separated string
            print(", ".join(f"{p:.2f}" for p in clean_preds))
        except Exception as e:
            print(f"Error making prediction: {e}")
        
    print("\nDisplaying complete!")
    input("Press ANY KEY to return to the main menu...")
    return