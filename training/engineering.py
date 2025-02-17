import pandas as pd
import re
import os
import logging

def extract_features(df):
    """Create phishing email features"""
    try:
        # Text-based features
        df['text_length'] = df['text_combined'].str.len()
        df['num_links'] = df['text_combined'].str.count(r'http[s]?://')
        df['num_special_chars'] = df['text_combined'].str.count(r'[^\w\s]')  # Improved regex
        
        # Keyword features
        keywords = ['password', 'verify', 'urgent', 'account', 'login']
        for word in keywords:
            df[f'has_{word}'] = df['text_combined'].str.contains(word, regex=False).astype(int)
        
        return df
    except Exception as e:
        logging.error(f"Feature extraction failed: {str(e)}")
        raise

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    try:
        # Load cleaned data
        input_path = os.path.join("data", "phishing.csv")
        if not os.path.exists(input_path):
            raise FileNotFoundError(f"Data not found at {input_path}")
        
        df = pd.read_csv(input_path, dtype={'text_combined': 'string', 'label': 'int'})
        
        # Validate columns
        required_columns = ['text_combined', 'label']
        if not set(required_columns).issubset(df.columns):
            missing = set(required_columns) - set(df.columns)
            raise ValueError(f"Missing required columns: {missing}")
        
        # Clean data
        df = df.dropna(subset=['text_combined', 'label'])
        
        # Extract features
        df = extract_features(df)
        
        # Save featured data
        output_path = os.path.join("data", "featured_phishing.csv")
        df.to_csv(output_path, index=False)
        
        logging.info(f"Feature engineering completed. Saved to {output_path}")
        logging.info(f"Generated features: {list(df.columns)}")
        print("Feature engineering successful!")
        print(df.head())
    
    except Exception as e:
        logging.error(f"Error in feature engineering: {str(e)}")
        print(f"Error: {str(e)}")