import requests
import json

base = 'http://127.0.0.1:8000'

# Get a valid token from login
print("=== Getting Auth Token ===")
r = requests.post(f'{base}/api/login', json={
    'email': 'admin2@test.com',
    'password': 'admin123'
})
token = r.json()['access_token']
print(f"Token: {token[:30]}...")

# Test /predict without token
print("\n=== Testing /predict WITHOUT Token ===")
try:
    r = requests.post(f'{base}/api/predict', files={'file': ('test.jpg', b'fake image')})
    print(f"Status: {r.status_code}")
    print(f"Response: {r.text[:200]}")
except Exception as e:
    print(f"Error: {e}")

# Test /predict with token
print("\n=== Testing /predict WITH Token ===")
try:
    headers = {'Authorization': f'Bearer {token}'}
    r = requests.post(
        f'{base}/api/predict', 
        files={'file': ('test.jpg', b'fake image')},
        headers=headers
    )
    print(f"Status: {r.status_code}")
    print(f"Response: {r.text[:300]}")
except Exception as e:
    print(f"Error: {e}")
