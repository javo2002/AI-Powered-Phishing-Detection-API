# Phishing Detection API

## Overview
This project is a **Machine Learning-powered Phishing Detection API**, deployed on a **webpage** to analyze email content and detect phishing attempts. The model processes email text, identifies phishing indicators, and provides a confidence score along with reasons for classification.

## Screenshots
### Email Input Page
![Email Input](screenshots/screenshot1.png)
This screenshot shows the user interface where users can input the email text they want to analyze. The page provides a text box for entering email content and a submit button to send the request to the phishing detection API.

### Detection Result Page
![Detection Result](screenshots/screenshot2.png)
This screenshot displays the results after an email is analyzed. It shows whether the email is classified as phishing or legitimate, along with a confidence score and explanations for the classification.

### Return button
![Returen Button](screenshots/screenshot3.png)
The return Button returns you back to the input page.

## Deployment Architecture
```
+-------------------+       +-------------------+       +-----------------------+
|                   |       |                   |       |                       |
|     VS Code       | ----> |      Docker        | ----> |   Web Hosting Platform|
|                   |       |                   |       | (e.g., AWS, GCP, Heroku)|
+-------------------+       +-------------------+       +-----------------------+
```

## Features
- **Machine Learning Model**: Uses NLP-based phishing detection.
- **Web UI**: Interactive webpage for testing emails.
- **API-Driven**: REST API for phishing detection.
- **Threat Intelligence Integration**: Leverages VirusTotal API for URL analysis.

## Tech Stack
- **Backend**: Flask (Python)
- **Frontend**: HTML, CSS, JavaScript
- **ML Model**: Scikit-learn, TensorFlow
- **Deployment**: Docker, Gunicorn, Heroku/AWS/GCP

## Installation & Setup
### Prerequisites
- Python 3.x
- Docker (Optional for containerized deployment)
- Virtual environment (Recommended)

### Steps
1. **Clone Repository**
   ```bash
   git clone https://github.com/yourusername/phishing-detection-api.git
   cd phishing-detection-api
   ```
2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```
3. **Run Locally**
   ```bash
   python app.py
   ```
4. **Run with Docker**
   ```bash
   docker build -t phishing-api .
   docker run -p 5000:5000 phishing-api
   ```
5. **Deploy to Heroku (Example)**
   ```bash
   heroku create
   git push heroku main
   heroku open
   ```

## Usage
### API Endpoint
- **POST /predict**
  - **Request**: `{ "email_content": "Your account is locked! Click here to verify." }`
  - **Response**:
    ```json
    {
      "prediction": "Phishing",
      "confidence": 0.89,
      "reasons": ["Urgent language detected", "Verification request"]
    }
    ```

### Web Interface
Navigate to `http://127.0.0.1:5000` (or hosted domain) to test emails visually.

### Postman Testing
Postman was used to test API requests and responses efficiently.

## Future Improvements
- Add support for **real-time email scanning**
- Enhance ML model using **Transformer-based NLP models**
- Improve UI/UX with **React.js**

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Author
Developed by [Your Name](https://github.com/yourusername). Contributions are welcome!

