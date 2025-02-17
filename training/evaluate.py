from scipy.sparse import load_npz
import joblib
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os

def evaluate_model():
    """Evaluate the trained model on the test set"""
    try:
        # Load vectorized features
        tfidf_matrix = load_npz("data/tfidf_features.npz")
        
        # Load labels
        df = pd.read_csv("data/featured_phishing.csv", dtype={'text_combined': 'string', 'label': 'int'})
        labels = df['label']
        
        # Load the trained model
        model = joblib.load("models/phishing_model.pkl")
        
        # Split data into training and testing sets (if not already split)
        from sklearn.model_selection import train_test_split
       # And update split:
        X_train, X_test, y_train, y_test = train_test_split(tfidf_matrix, labels, test_size=0.2)
        
        # Evaluate the model on the test set
        y_pred = model.predict(X_test)
        
        # Print classification report
        print("\nClassification Report:")
        print(classification_report(y_test, y_pred))
        
        # Print accuracy
        print(f"Accuracy: {accuracy_score(y_test, y_pred):.4f}")
        
        # Create confusion matrix
        cm = confusion_matrix(y_test, y_pred)
        
        # Add row and column totals
        row_totals = cm.sum(axis=1, keepdims=True)  # Sum rows
        col_totals = cm.sum(axis=0, keepdims=True)  # Sum columns
        grand_total = cm.sum()  # Sum of all elements
        
        # Create a new matrix with totals
        cm_with_totals = np.block([
            [cm, row_totals],
            [col_totals, grand_total]
        ])
        
        # Plot confusion matrix with totals
        plt.figure(figsize=(10, 8))
        sns.heatmap(cm_with_totals, annot=True, fmt='d', cmap='Blues', 
                    xticklabels=['Legitimate', 'Phishing', 'Total'], 
                    yticklabels=['Legitimate', 'Phishing', 'Total'],
                    cbar=False)
        plt.xlabel('Predicted', fontsize=12)
        plt.ylabel('Actual', fontsize=12)
        plt.title('Confusion Matrix with Totals', fontsize=14)
        plt.tight_layout()  # Ensure labels fit properly
        plt.savefig("models/confusion_matrix_with_totals.png")
        plt.show()
        
        print("Evaluation completed. Confusion matrix with totals saved to models/confusion_matrix_with_totals.png")
    
    except Exception as e:
        print(f"Error during model evaluation: {str(e)}")
        raise

if __name__ == "__main__":
    evaluate_model()