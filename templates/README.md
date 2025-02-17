This folder contains the HTML templates for the Phishing Detection web application. Each file serves a specific function within the application.

## File Structure and Purpose

### 1. `index.html`
**Purpose**: Acts as the main landing page for the phishing detection system.
- Allows users to input email content or upload a file for analysis.
- Features a dark/light mode toggle.
- Provides form validation to ensure input is provided.
- Includes a sample phishing email for quick testing.

### 2. `result.html`
**Purpose**: Displays the results of the phishing detection analysis.
- Shows the original email content entered by the user.
- Indicates whether the email is "Phishing" or "Legitimate."
- Includes a visual threat meter based on probability.
- Provides SHAP-based word score polarities for explanation.
- Displays URL analysis results, checking against Google Safe and VirusTotal.
- Shows email header analysis (SPF, DKIM verification).
- Allows navigation to the dashboard for further insights.

### 3. `dashboard.html`
**Purpose**: (Not uploaded) Expected to serve as a visualization and logging page for detected phishing attempts.

## Execution Order
The application follows this flow:
1. **User accesses `index.html`** → Inputs email content or uploads a file.
2. **Form submission** → Sends data to the backend for phishing detection.
3. **User is redirected to `result.html`** → Displays classification results and analysis.
4. **User may navigate to `dashboard.html`** (if implemented) for further insights.

## Key Notes
- Ensure that `static/styles.css` is present for proper styling.
- Flash messages will display error or success notifications dynamically.
- Dark mode settings are stored in `localStorage` for user preference persistence.
- The application should be run in a Flask environment for `url_for()` functionality to work correctly.

For any issues, verify that the Flask routes and backend logic align with these templates.

