import pandas as pd
import re
import os
import logging

def extract_features(df):
    """Create phishing email features"""
    try:
        # Text-based features
        df['text_length'] = df['text_combined'].apply(len)
        df['num_links'] = df['text_combined'].apply(lambda x: len(re.findall(r'http[s]?://', x)))
        df['num_special_chars'] = df['text_combined'].apply(lambda x: len(re.findall(r'[!$%^&*()]', x)))
        
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
        
        df = pd.read_csv(input_path)
        
        # Extract features
        df = extract_features(df)
        
        # Save featured data
        output_path = os.path.join("data", "featured_phishing.csv")
        df.to_csv(output_path, index=False)
        
        logging.info(f"Feature engineering completed. Saved to {output_path}")
        print("Feature engineering successful!")
        print(df.head())
        
        # Check for non-zero values in feature columns
        feature_columns = ['has_password', 'has_verify', 'has_urgent', 'has_account', 'has_login']
        non_zero_summary = df[feature_columns].sum()
        print("\nSummary of non-zero values in feature columns:")
        print(non_zero_summary)
        
        # Print rows with non-zero values (if any)
        non_zero_rows = df[df[feature_columns].any(axis=1)]
        if not non_zero_rows.empty:
            print("\nRows with non-zero feature values:")
            print(non_zero_rows)
        else:
            print("\nAll feature columns have zero values.")
    
    except Exception as e:
        logging.error(f"Error in feature engineering: {str(e)}")
        print(f"Error: {str(e)}")