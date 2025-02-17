import requests

def check_url_virustotal(url, api_key):
    """Check if a URL is malicious using VirusTotal API"""
    # VirusTotal API endpoint for URL analysis
    api_url = "https://www.virustotal.com/api/v3/urls"

    # Headers with API key
    headers = {
        "x-apikey": api_key
    }

    # Payload with the URL to analyze
    payload = {
        "url": url
    }

    # Submit the URL for analysis
    response = requests.post(api_url, headers=headers, data=payload)
    if response.status_code == 200:
        # Get the analysis ID
        analysis_id = response.json()["data"]["id"]
        print(f"Analysis ID: {analysis_id}")

        # Retrieve the analysis report
        report_url = f"https://www.virustotal.com/api/v3/analyses/{analysis_id}"
        report_response = requests.get(report_url, headers=headers)
        if report_response.status_code == 200:
            return report_response.json()
        else:
            print(f"Error fetching report: {report_response.status_code}")
            return None
    else:
        print(f"Error submitting URL: {response.status_code}")
        return None

if __name__ == "__main__":
    # Replace with your VirusTotal API key
    api_key = "eb052f6f839b5e13e34774f1645401d8978f6372d563c33d87d17d5f0420a48a"
    
    # URL to check
    url = "http://example.com"
    
    # Check the URL
    result = check_url_virustotal(url, api_key)
    if result:
        print("VirusTotal Report:")
        print(result)

    