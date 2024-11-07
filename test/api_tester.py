import requests
import json
import time
from pathlib import Path

class APITester:
    def __init__(self, base_url):
        self.base_url = base_url.rstrip('/')
        self.access_token = None
        self.headers = {"Content-Type": "application/json"}
    
    def register_user(self, username, password):
        """Register a new user"""
        endpoint = f"{self.base_url}/api/v1/auth/register"
        payload = {
            "username": username,
            "password": password
        }
        
        response = requests.post(endpoint, json=payload)
        print("\n=== User Registration ===")
        print(f"Status Code: {response.status_code}")
        print("Response:", json.dumps(response.json(), indent=2))
        return response.json()
    
    def login_user(self, username, password):
        """Login user and get access token"""
        endpoint = f"{self.base_url}/api/v1/auth/login"
        payload = {
            "username": username,
            "password": password
        }
        
        response = requests.post(endpoint, json=payload)
        print("\n=== User Login ===")
        print(f"Status Code: {response.status_code}")
        print("Response:", json.dumps(response.json(), indent=2))
        
        if response.status_code == 200:
            self.access_token = response.json()["data"]["access_token"]
            self.headers["Authorization"] = f"Bearer {self.access_token}"
        
        return response.json()
    
    def analyze_sentiment(self, text):
        """Test sentiment analysis endpoint"""
        if not self.access_token:
            print("Error: Not authenticated. Please login first.")
            return
        
        endpoint = f"{self.base_url}/api/v1/analysis/sentiment"
        payload = {"text": text}
        
        response = requests.post(endpoint, json=payload, headers=self.headers)
        print(f"\n=== Sentiment Analysis for: '{text}' ===")
        print(f"Status Code: {response.status_code}")
        print("Response:", json.dumps(response.json(), indent=2))
        return response.json()
    
    def analyze_document(self, file_path):
        """Test document analysis endpoint"""
        if not self.access_token:
            print("Error: Not authenticated. Please login first.")
            return
        
        endpoint = f"{self.base_url}/api/v1/documents/analyze"
        files = {"file": open(file_path, "rb")}
        headers = {"Authorization": f"Bearer {self.access_token}"}
        
        response = requests.post(endpoint, files=files, headers=headers)
        print(f"\n=== Document Analysis for: {file_path} ===")
        print(f"Status Code: {response.status_code}")
        print("Response:", json.dumps(response.json(), indent=2))
        return response.json()
    
    def test_rate_limiting(self, text, num_requests=10, delay=0.1):
        """Test rate limiting by making multiple requests in quick succession"""
        print("\n=== Testing Rate Limiting ===")
        print(f"Making {num_requests} requests with {delay}s delay between each")
        
        results = []
        for i in range(num_requests):
            print(f"\nRequest {i+1}/{num_requests}")
            response = requests.post(
                f"{self.base_url}/api/v1/analysis/sentiment",
                json={"text": text},
                headers=self.headers
            )
            results.append({
                "request_num": i+1,
                "status_code": response.status_code,
                "response": response.json() if response.status_code == 200 else response.text
            })
            time.sleep(delay)
        
        return results

def main():
    # Initialize the API tester with your Railway URL
    api = APITester("https://flaskie.up.railway.app")
    
    # Test user registration
    api.register_user("testuser", "testpass123")
    
    # Test user login
    api.login_user("testuser", "testpass123")
    
    # Test sentiment analysis with different examples
    positive_texts = [
        "This product exceeds all my expectations! Absolutely wonderful!",
        "The customer service team was incredibly helpful and responsive."
    ]
    
    negative_texts = [
        "This service is terrible, I'm very disappointed with the results.",
        "The interface is confusing and the documentation is unclear."
    ]
    
    for text in positive_texts + negative_texts:
        api.analyze_sentiment(text)
        time.sleep(1)  # Add delay between requests
    
    # Create and test with a sample document
    sample_text = """This is a sample document for testing the document analysis endpoint.
    It contains multiple sentences and paragraphs.
    The API should be able to analyze this content and provide meaningful insights."""
    
    with open("sample.txt", "w") as f:
        f.write(sample_text)
    
    # Test document analysis
    if Path("sample.txt").exists():
        api.analyze_document("sample.txt")
    
    # Test rate limiting
    rate_limit_results = api.test_rate_limiting(
        "Testing rate limiting with this text",
        num_requests=5,
        delay=0.5
    )
    
    print("\n=== Rate Limiting Test Results ===")
    for result in rate_limit_results:
        print(f"\nRequest {result['request_num']}")
        print(f"Status Code: {result['status_code']}")
        print("Response:", json.dumps(result['response'], indent=2))

if __name__ == "__main__":
    main()