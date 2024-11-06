import requests
import json
import os
from time import sleep

BASE_URL = 'http://localhost:5000'

def test_api():
    # Test health check
    response = requests.get(f'{BASE_URL}/health')
    print('Health check:', response.json())

    # Register user
    register_data = {
        'username': 'testuser',
        'password': 'testpass123'
    }
    response = requests.post(
        f'{BASE_URL}/api/v1/auth/register',
        json=register_data
    )
    print('Register:', response.json())

    # Login
    login_response = requests.post(
        f'{BASE_URL}/api/v1/auth/login',
        json=register_data
    )
    print('Login:', login_response.json())
    
    # Get access token
    access_token = login_response.json()['access_token']
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }

    # Test sentiment analysis
    sentiment_data = {
        'text': 'This is a very positive and wonderful test message!'
    }
    response = requests.post(
        f'{BASE_URL}/api/v1/analysis/sentiment',
        headers=headers,
        json=sentiment_data
    )
    print('Sentiment analysis:', response.json())

    # Test text summary
    summary_data = {
        'text': '''
        Machine learning is a field of study that gives computers the ability 
        to learn without being explicitly programmed. It focuses on developing 
        computer programs that can access data and use it to learn for themselves.
        The process of learning begins with observations or data, such as examples, 
        direct experience, or instruction, in order to look for patterns in data 
        and make better decisions in the future based on the examples provided.
        '''
    }
    response = requests.post(
        f'{BASE_URL}/api/v1/analysis/summary',
        headers=headers,
        json=summary_data
    )
    print('Text summary:', response.json())

    # Test keyword extraction
    response = requests.post(
        f'{BASE_URL}/api/v1/analysis/keywords',
        headers=headers,
        json=summary_data
    )
    print('Keywords:', response.json())

    # Test document analysis
    # Create a sample text file
    with open('test.txt', 'w') as f:
        f.write(summary_data['text'])
    
    with open('test.txt', 'rb') as f:
        files = {'file': ('test.txt', f)}
        response = requests.post(
            f'{BASE_URL}/api/v1/documents/analyze',
            headers={'Authorization': f'Bearer {access_token}'},
            files=files
        )
    print('Document analysis:', response.json())
    
    # Clean up
    os.remove('test.txt')

    # Test user info
    response = requests.get(
        f'{BASE_URL}/api/v1/auth/me',
        headers=headers
    )
    print('User info:', response.json())

if __name__ == '__main__':
    test_api()
