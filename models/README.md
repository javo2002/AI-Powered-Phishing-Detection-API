This folder contains the trained machine learning models and vectorizers used in the AI-Powered Phishing Detection System.

## Contents

### 1. `tfidf_vectorizer.pkl`
**Purpose**: Stores the trained TF-IDF vectorizer, which transforms email text into numerical features for model input.
- Converts raw email content into vectorized form for analysis.
- Must be loaded before making predictions with `phishing_model.pkl`.

### 2. `phishing_model.pkl`
**Purpose**: Contains the trained phishing detection model.
- Uses machine learning to classify emails as "Phishing" or "Legitimate."
- Works in conjunction with `tfidf_vectorizer.pkl` to analyze email text features.
- Supports explainability using SHAP values to highlight key phishing indicators.

## Notes
- Ensure both `tfidf_vectorizer.pkl` and `phishing_model.pkl` are present in the `models` folder before running the application.
- The model requires preprocessed input using the same vectorizer it was trained with.
- If retraining the model, update both `.pkl` files accordingly.

For any issues, verify that the model and vectorizer versions are compatible with your application.

