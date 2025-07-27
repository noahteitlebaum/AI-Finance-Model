import handler.anthropic as anthropic
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

start_date = date(2023, 7, 19)
end_date = date.today()

if __name__ == "__main__":
    state = GameState.MAIN
    running = True

    ticker_dict = {}

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
            menuhandler.handle_train(ticker_dict)
            state = GameState.MAIN

        elif state == GameState.DISPLAY:
            menuhandler.handle_display(ticker_dict)
            state = GameState.MAIN

        elif state == GameState.QUIT:
            print("\nExiting program.")
            running = False