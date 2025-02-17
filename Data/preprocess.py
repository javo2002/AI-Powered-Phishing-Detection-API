import pandas as pd
import os
import logging

def load_data(raw_path):
    """Load dataset from specified path"""
    try:
        # Verify file exists
        if not os.path.isfile(raw_path):
            raise FileNotFoundError(f"File not found at {raw_path}")
        
        # Read data with explicit dtypes to optimize memory usage
        df = pd.read_csv(raw_path, dtype={'text_combined': 'string', 'label': 'int'})
        
        # Verify output directory exists
        os.makedirs("data", exist_ok=True)
        
        logging.info(f"Data loaded successfully from {raw_path}")
        return df
    
    except Exception as e:
        logging.error(f"Loading failed: {str(e)}")
        raise

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    # Set correct path to phishing.csv
    raw_path = os.path.join("data", "phishing.csv")
    
    try:
        df = load_data(raw_path)
        print("Data loading completed successfully!")
        print(df.head())  # Print first few rows to verify
    except Exception as e:
        print(f"Error: {str(e)}")