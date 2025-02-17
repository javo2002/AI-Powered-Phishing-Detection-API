[Kaggle Dataset](https://www.kaggle.com/datasets/naserabdullahalam/phishing-email-dataset)


Here’s the **correct execution order** for `download.py` and `preprocess.py`, assuming these scripts are part of your data pipeline:

---

### **1. Run `download.py`**
```bash
python download.py
```
**Purpose**: Downloads raw data from a source (e.g., API, URL, or database)  
**Input**: None (or configuration file if specified)  
**Output**: Raw data file (e.g., `data/raw/phishing_data.csv`)  

---

### **2. Run `preprocess.py`**
```bash
python preprocess.py
```
**Purpose**: Cleans and prepares raw data for feature engineering  
**Input**: Raw data file (e.g., `data/raw/phishing_data.csv`)  
**Output**: Cleaned data file (e.g., `data/phishing.csv`)  

---

### **Full Command Sequence**
```bash
# Clean previous outputs (optional)
rm -rf data/raw/* data/phishing.csv

# Execute in order
python download.py
python preprocess.py
```

---

### **Key Note**
**Prerequisite**: Ensure `download.py` and `preprocess.py` are correctly configured (e.g., file paths, API keys, etc.).

---

### **Execution Flow**
1. **`download.py`**:
   - Downloads raw data from a source (e.g., URL, API, or database).
   - Saves it to `data/raw/phishing_data.csv`.

2. **`preprocess.py`**:
   - Cleans and prepares the raw data.
   - Saves the cleaned data to `data/phishing.csv`.

3. **Next Steps**:
   - Run `engineering.py` to generate features.
   - Continue with the rest of the pipeline.
  
4. **Error Handling**: If `download.py` fails, `preprocess.py` won’t run. Fix issues in the first script before proceeding.


---

This ensures your data pipeline is complete and ready for machine learning. Let me know if you need further assistance!
