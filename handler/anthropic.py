import handler.anthropic as anthropic 
import pandas as pd
import os

from dotenv import load_dotenv
from . import formatter

# Import environment variables and setup the anthropic interface
load_dotenv()
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)


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