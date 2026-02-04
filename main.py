import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.utils import setup_env
from src.data_cleaning import clean_data
from src.agent_setup import create_restaurant_agent

RAW_DATA_PATH = "data/raw/restaurant_sales_raw.csv"
CLEAN_DATA_PATH = "data/processed/cleaned_data.csv"


def main():
    print("\n" + "="*50)
    print(" 🤖  RESTAURANT AI ANALYST STARTING...")
    print("="*50 + "\n")

    setup_env()

    if not os.path.exists(RAW_DATA_PATH):
        print(f"❌ Error: Raw data file missing at {RAW_DATA_PATH}")
        return

    print("Step 1: Running Data Cleaning Pipeline...")
    clean_data(RAW_DATA_PATH, CLEAN_DATA_PATH)

    print("Step 2: Initializing AI Brain (Loading LLM)...")
    agent = create_restaurant_agent(CLEAN_DATA_PATH)
    print("✅ AI Agent is ready to serve!")

    print("\n" + "-"*50)
    print(" COMMANDS: Type 'exit' or 'quit' to stop.")
    print("-"*50 + "\n")

    while True:
        user_query = input("User 👤: ")

        if user_query.lower() in ["exit", "quit", "bye"]:
            print("AI 🤖: Goodbye! Have a great service.")
            break

        response = agent.invoke(user_query)
        print(f"\nAI 🤖: {response['output']}\n")


if __name__ == "__main__":
    main()