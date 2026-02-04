'''
   Configures the local Llama 3 model via Ollama and initializes the create_pandas_dataframe_agent.

   ===============================================================================================

   We implemented strict ReAct formatting rules and parsing error handlers to ensure the agent performs reliable data analysis.
   
'''



import pandas as pd
from datetime import timedelta
from dotenv import load_dotenv
from langchain_ollama import ChatOllama
from langchain_experimental.agents import create_pandas_dataframe_agent

load_dotenv()

def create_restaurant_agent(csv_path):
    df = pd.read_csv(csv_path)
    df['Date'] = pd.to_datetime(df['Date'])

    # Initialize Llama 3 via Ollama
    llm = ChatOllama(model="llama3", temperature=0)

    # REFINED PREFIX: Direct instructions to force the correct ReAct format
    prefix = """
    You are working with a pandas DataFrame named 'df'.
    You MUST use the following format for every step:

    Thought: (Explain what you are going to do)
    Action: python_repl_ast
    Action Input: (The exact python code to run)

    Rules:
    - For 'last week', filter data relative to df['Date'].max()
    - Always execute code via the python_repl_ast tool.
    - When you have the final answer, use: Final Answer: [your summary]
    """

    agent = create_pandas_dataframe_agent(
        llm,
        df,
        verbose=True,
        allow_dangerous_code=True,
        prefix=prefix,
        # FIX: Removed 'max_iterations' to stop the TypeError crash
        agent_executor_kwargs={
            "handle_parsing_errors": True 
        }
    )
    return agent