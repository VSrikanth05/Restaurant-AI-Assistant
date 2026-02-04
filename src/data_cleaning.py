import pandas as pd
import os

def clean_data(input_path, output_path):
    """
    Data Preprocessing Pipeline
    ===========================
    
    Purpose:
    --------
    Prepares raw CSV data for consumption by the AI Agent. 
    AI models are sensitive to data types—they cannot easily perform math on 
    strings (text) or filter dates if formats are inconsistent.

    Args:
        input_path (str): Location of the raw Kaggle dataset.
        output_path (str): Where to save the sanitized file.
    """
    
    print(f"🔄 Loading raw data from: {input_path}...")
    
    # 1. Validation: Ensure the file actually exists before crashing
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"❌ Input file not found at {input_path}. Please download the dataset.")

    # Load into Pandas (Dataframe is like an Excel sheet in memory)
    df = pd.read_csv(input_path)

    # --- CLEANING LOGIC START ---

    # 2. Date Standardization
    # logic: We force the 'Date' column into a Python datetime object.
    # Why? So the AI can understand "Last Week", "Month of May", or "Next 7 Days".
    # Without this, 'Date' is just dumb text to the computer.
    if 'Date' in df.columns:
        df['Date'] = pd.to_datetime(df['Date'], format='mixed', dayfirst=True, errors='coerce')
    
    # 3. Currency Cleaning
    # Logic: Remove '$', ',' or other symbols from price columns.
    # Why? The computer cannot calculate " $5.00 + $2.00 ". It needs " 5.0 + 2.0 ".
    numeric_cols = ['Total Amount', 'Price', 'Transaction Amount'] # Add any relevant columns here
    for col in numeric_cols:
        if col in df.columns and df[col].dtype == 'object':
            # Regex replace: remove anything that isn't a digit or a decimal point
            df[col] = df[col].astype(str).str.replace(r'[$,]', '', regex=True)
            df[col] = pd.to_numeric(df[col], errors='coerce')

    # 4. Null Handling
    # Logic: Drop rows where critical info is missing.
    # Why? A sale without a price or item name is useless for analysis and breaks calculations.
    df.dropna(inplace=True)

    # --- CLEANING LOGIC END ---

    # Save the clean file
    # We use 'os.makedirs' to ensure the 'data/processed' folder exists before saving
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    df.to_csv(output_path, index=False)
    print(f"✅ Data cleaning complete. Optimized file saved to: {output_path}")
    
    return output_path