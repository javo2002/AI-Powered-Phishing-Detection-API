from sklearn.feature_extraction.text import TfidfVectorizer
from scipy.sparse import save_npz
import joblib
import pandas as pd
import os

def vectorize_text(df, max_features=1000):
    """Convert text to TF-IDF features"""
    try:
        vectorizer = TfidfVectorizer(
            max_features=max_features,
            stop_words='english',
            ngram_range=(1, 2)
        )
        
        # Fit and transform the text data
        tfidf_matrix = vectorizer.fit_transform(df['text_combined'])
        
        # Save vectorizer and matrix
        os.makedirs("models", exist_ok=True)
        joblib.dump(vectorizer, "models/tfidf_vectorizer.pkl")
        save_npz("data/tfidf_features.npz", tfidf_matrix)
        
        print("TF-IDF vectorization completed!")
        return tfidf_matrix
    except Exception as e:
        print(f"Vectorization error: {str(e)}")
        raise

if __name__ == "__main__":
    try:
        # Load featured data
        input_path = os.path.join("data", "featured_phishing.csv")
        if not os.path.exists(input_path):
            raise FileNotFoundError(f"Featured data not found at {input_path}")
        
        df = pd.read_csv(input_path, dtype={'text_combined': 'string', 'label': 'int'})
        
        # Perform vectorization
        vectorize_text(df)
    except Exception as e:
        print(f"Error: {str(e)}")