# train_model.py
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from scipy.sparse import load_npz, save_npz
import pandas as pd
import joblib
import os

def train_model():
    """Train and save phishing detection model"""
    try:
        # Load preprocessed data
        X = load_npz("data/tfidf_features.npz")
        y = pd.read_csv("data/featured_phishing.csv")['label']
        
        # Split data (80% train, 20% test)
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
        
        # Train model
        model = LogisticRegression(max_iter=1000, class_weight='balanced')
        model.fit(X_train, y_train)
        
        # Save artifacts
        os.makedirs("models", exist_ok=True)
        joblib.dump(model, "models/phishing_model.pkl")
        
        # Save test set for evaluation
        save_npz("data/X_test.npz", X_test)
        pd.DataFrame(y_test).to_csv("data/y_test.csv", index=False)
        
        print("Model trained and saved successfully!")
        return model
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

if __name__ == "__main__":
    train_model()