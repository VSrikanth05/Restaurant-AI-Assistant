import os
import sys
from dotenv import load_dotenv

def setup_env():
    """
    Environment Setup & Security Check
    ==================================
    
    Purpose:
    --------
    Loads sensitive configuration (API Keys) from the .env file into the system environment.
    This ensures credentials are rarely hardcoded in the source code, following 
    security best practices (The '12-Factor App' methodology).

    Logic:
    ------
    1. 'load_dotenv()' searches for a file named '.env'.
    2. It reads variables like GOOGLE_API_KEY=sk-...
    3. It injects them into 'os.environ', making them accessible like system variables.
    """
    
    # Attempt to load the .env file
    loaded = load_dotenv()
    
    # Check if the file was actually found
    if not loaded:
        print("Warning: .env file not found. Ensure you have created it in the root directory.")
    
    # validation: Verify the specific key we need exists
    # Check for OpenRouter Key
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        print("\n CRITICAL ERROR: GOOGLE_API_KEY is missing.")
        print("    Please create a file named '.env' in your project root.")
        print("    Add this line: GOOGLE_API_KEY=your-google-api-key-here\n")
        # Exit the program immediately if we can't authenticate
        sys.exit(1)
    
    # If successful, we silently continue. The key is now safe in memory.
    # We do NOT print the key here for security reasons.