import requests
import json

base = 'http://127.0.0.1:8000'

print("=== Testing Register with Simple Endpoint ===")
try:
    # Test with HTTP POST - check if it works
    r = requests.post(f'{base}/api/register-simple', json={
        'name': 'Test User',
        'email': 'test@example.com',
        'password': 'admin123'
    })
    print(f"Status: {r.status_code}")
    print(f"Response: {r.text}")
except Exception as e:
    print(f"Error: {e}")
