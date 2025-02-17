from flask import Flask, request, render_template, redirect, url_for, flash
from werkzeug.utils import secure_filename
import json
from datetime import datetime
import os
import joblib
import re
import requests
import base64
import shap
from urllib.parse import urlparse
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

app = Flask(__name__)

# Security: Rate Limiting
limiter = Limiter(app=app, key_func=get_remote_address)

# Load models
model = joblib.load("models/phishing_model.pkl")  # Load phishing model
vectorizer = joblib.load("models/tfidf_vectorizer.pkl")  # Load TF-IDF vectorizer
explainer = shap.LinearExplainer(model, vectorizer.transform([""] * 100))

# API Config
GOOGLE_API_KEY = "your_key"
VIRUSTOTAL_API_KEY = "your_key"


# Configuration
HISTORY_FILE = 'prediction_history.json'
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'eml', 'txt'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = os.environ.get('FLASK_SECRET_KEY', 'fallback-dev-key')

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def check_url_virustotal(url):
    """Check URL against VirusTotal API"""
    headers = {"x-apikey": VIRUSTOTAL_API_KEY}
    url_id = base64.urlsafe_b64encode(url.encode()).decode().strip("=")
    
    try:
        response = requests.get(
            f"https://www.virustotal.com/api/v3/urls/{url_id}",
            headers=headers,
            timeout=5
        )
        if response.status_code == 200:
            stats = response.json()['data']['attributes']['last_analysis_stats']
            return {
                "status": "Malicious" if stats['malicious'] > 0 else "Clean",
                "malicious": stats['malicious'],
                "suspicious": stats['suspicious']
            }
        return {"status": "Unknown", "malicious": 0, "suspicious": 0}
    except Exception:
        return {"status": "Error", "malicious": 0, "suspicious": 0}

def analyze_url_security(url):
    return {
        "google_safe": check_google_safe_browsing(url),
        "virustotal": check_url_virustotal(url),
        "features": extract_url_features(url)
    }

def extract_url_features(url):
    """Extract URL security features with error handling"""
    parsed = urlparse(url)
    features = {
        "is_shortened": any(x in parsed.netloc for x in ['bit.ly', 'goo.gl']),
        "has_ip": bool(re.match(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', parsed.netloc)),
        "redirect_depth": 0  # Default value
    }

    try:
        response = requests.get(url, allow_redirects=True, timeout=5)
        features["redirect_depth"] = len(response.history)
    except Exception as e:
        print(f"URL analysis error: {str(e)}")
    
    return features

def check_google_safe_browsing(url):
    """Google Safe Browsing check with error handling"""
    try:
        payload = {
            "client": {"clientId": "phishing-detector", "clientVersion": "1.0"},
            "threatInfo": {
                "threatTypes": ["MALWARE", "SOCIAL_ENGINEERING"],
                "threatEntries": [{"url": url}]
            }
        }
        response = requests.post(
            f"https://safebrowsing.googleapis.com/v4/threatMatches:find?key={GOOGLE_API_KEY}",
            json=payload,
            timeout=5
        )
        return response.json().get('matches', [])
    except Exception as e:
        print(f"Google API error: {str(e)}")
        return []

def get_shap_explanation(text):
    """Generate SHAP explanation"""
    vectorized = vectorizer.transform([text])
    shap_values = explainer.shap_values(vectorized)
    words = vectorizer.get_feature_names_out()
    return sorted(zip(words, shap_values[0].flatten()), 
                key=lambda x: abs(x[1]), reverse=True)[:10]
# Custom Jinja filter for datetime formatting

def save_prediction(email_content, prediction, probability):
    """Save prediction to history file"""
    entry = {
        "timestamp": datetime.now().isoformat(),
        "content": email_content[:500],  # Store first 500 characters
        "prediction": int(prediction),
        "probability": float(probability)
    }
    
    try:
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(HISTORY_FILE), exist_ok=True)
        
        with open(HISTORY_FILE, 'a') as f:
            f.write(json.dumps(entry) + '\n')
    except Exception as e:
        print(f"Error saving history: {str(e)}")

def format_datetime(value):
    try:
        dt = datetime.fromisoformat(value)
        return dt.strftime("%Y-%m-%d %H:%M:%S")
    except:
        return value

# Register the filter
app.jinja_env.filters['datetimeformat'] = format_datetime

@app.template_filter('datetimeformat')
def format_datetime(value):
    try:
        return datetime.fromisoformat(value).strftime("%Y-%m-%d %H:%M")
    except:
        return value

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/predict", methods=["POST"])
@limiter.limit("10/minute")
def predict():
    try:
        email_content = ""
        uploaded_file = None
        probability = 0.0
        prediction = 0

        # Handle file upload
        if 'email-file' in request.files:
            file = request.files['email-file']
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(file_path)
                with open(file_path, 'r') as f:
                    email_content = f.read()
                os.remove(file_path)

        # Fallback to textarea
        if not email_content:
            email_content = request.form.get("email-content", "").strip()

        # Validate input
        if not email_content or len(email_content.split()) < 3:
            flash("Please provide valid email content (minimum 3 words)")
            return redirect(url_for('home'))

        # Process content
        email_vectorized = vectorizer.transform([email_content])
        prediction = model.predict(email_vectorized)[0]
        save_prediction(email_content, prediction, probability)  # <-- This must be called
        probability = model.predict_proba(email_vectorized)[0][1]

        # URL analysis
        urls = re.findall(r'https?://[^\s]+', email_content)
        url_analysis = [analyze_url_security(url) for url in urls]

        # SHAP explanation
        shap_results = get_shap_explanation(email_content)

        return render_template("result.html",
            email_content=email_content,
            prediction=prediction,
            probability=probability,
            url_analysis=url_analysis,
            shap_results=shap_results,
            header_analysis={
                "spf_fail": False,
                "dkim_mismatch": False
            }
        )

    except Exception as e:
        flash(f"Error processing request: {str(e)}")
        return redirect(url_for('home'))

@app.route("/dashboard")
def dashboard():
    history = []
    try:
        with open(HISTORY_FILE, 'r') as f:
            for line in f:
                history.append(json.loads(line))
    except FileNotFoundError:
        pass
    
    stats = {
        "total": len(history),
        "phishing": sum(1 for entry in history if entry['prediction'] == 1),
        "recent": history[-10:] if history else []
    }
    
    return render_template("dashboard.html", stats=stats)

if __name__ == "__main__":
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    app.run(debug=True)
