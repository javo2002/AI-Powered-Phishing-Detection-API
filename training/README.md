Here's the **correct execution order** for your machine learning pipeline, ensuring all dependencies are met:

---

### **1. Data Preparation & Feature Engineering**
```bash
python engineering.py
```
**Purpose**: Creates basic text features from raw data  
**Input**: `data/phishing.csv`  
**Output**: `data/featured_phishing.csv`  

---

### **2. (Optional) Feature Validation**
```bash
python feature_check.py
```
**Purpose**: Verify feature distribution and data quality  
**Input**: `data/featured_phishing.csv`  
**Output**: Console log of feature statistics  

---

### **3. Text Vectorization**
```bash
python vectorization.py
```
**Purpose**: Convert text to TF-IDF numerical features  
**Input**: `data/featured_phishing.csv`  
**Output**:  
- `data/tfidf_features.npz` (TF-IDF matrix)  
- `models/tfidf_vectorizer.pkl` (Vectorizer object)  

---

### **4. Model Training**
```bash
python train_model.py
```
**Purpose**: Train logistic regression classifier  
**Input**: `data/tfidf_features.npz`  
**Output**:  
- `models/phishing_model.pkl` (Trained model)  
- `data/X_test.npz` & `data/y_test.csv` (Test set)  

---

### **5. Model Evaluation**
```bash
python evaluate.py
```
**Purpose**: Evaluate model performance on unseen data  
**Input**:  
- `models/phishing_model.pkl`  
- `data/X_test.npz`  
- `data/y_test.csv`  
**Output**:  
- Classification report  
- Confusion matrix visualization  

---

### **Full Command Sequence**
```bash
# Clean previous outputs (optional)
rm -rf data/featured_phishing.csv data/tfidf_features.npz models/*

# Execute in order
python engineering.py
python vectorization.py
python train_model.py
python evaluate.py
```

---

### **Key Notes**
1. **Prerequisite**: Ensure `data/phishing.csv` exists before starting.
2. **Error Handling**: If any step fails, fix issues before proceeding to the next.
3. **Dependency Flow**:
   ```
   Raw Data → Feature Engineering → Vectorization → Training → Evaluation
   ```

This sequence ensures proper data flow and prevents `FileNotFound` errors. Let me know if you need help debugging any step!
