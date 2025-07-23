import anthropic
import pandas as pd
import os
import platform

from datetime import date
from enum import Enum
from tabulate import tabulate
from dotenv import load_dotenv

# Local dependencies
import handler.menu as menuhandler
import handler.formatter as formatter

# Environment keys
class GameState(Enum):
    MAIN = "MAIN"
    DOWNLOAD = "DOWNLOAD"
    TRAIN = "TRAIN"
    DISPLAY = "DISPLAY"
    QUIT = "QUIT"

# Import environment variables and setup the anthropic interface
load_dotenv()
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

# Starting and ending data for stock data gathering
start_date = date(2023, 7, 19)
end_date = date.today()

def ask_ai_about_stock(ticker: str, df: pd.DataFrame) -> str:
    """
    Uses Claude to analyze the historical stock data and provide an outlook.
    """

    history = formatter.summarize_stock_history(df)
    prompt = (
        f"You are a financial analyst. Here is the past 30 days of data for {ticker}:\n\n"
        f"{history}\n\n"
        f"Based on this, what patterns do you observe, and what might happen in the next week or two? "
        "Explain your reasoning clearly but concisely. Don't give investment advice, just trends and analysis."
    )

    response = client.messages.create(
        model="claude-3-haiku-20240307",
        max_tokens=500,
        temperature=0.7,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    
    return response.content[0].text

if __name__ == "__main__":
    state = GameState.MAIN
    running = True

    ticker_dict = pd.DataFrame()

    while running:
        if state == GameState.MAIN:
            # Clears the terminal
            if platform.system() == "Windows":
                os.system("cls")
            else:
                os.system("clear")
            
            menuhandler.menu()
            choice = input("Enter choice: ").strip().upper()

            if choice == "1":
                state = GameState.DOWNLOAD
            elif choice == "2":
                state = GameState.TRAIN
            elif choice == "3":
                state = GameState.DISPLAY
            elif choice == "4":
                state = GameState.QUIT
            elif choice == "ESC":
                running = False
            else:
                print("Invalid choice. Please enter 1-4 or ESC.")

        elif state == GameState.DOWNLOAD:
            ticker_dict = menuhandler.handle_download(start_date, end_date)
            state = GameState.MAIN

        elif state == GameState.TRAIN:
            menuhandler.handle_train()
            state = GameState.MAIN

        elif state == GameState.DISPLAY:
            menuhandler.handle_display(ask_ai_about_stock, ticker_dict)
            state = GameState.MAIN

        elif state == GameState.QUIT:
            print("Exiting program.")
            running = False