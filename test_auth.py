import requests
import json

base = 'http://127.0.0.1:8000'

print("=== Testing Register ===")
try:
    r = requests.post(f'{base}/api/register', json={
        'name': 'Admin User',
        'email': 'admin2@test.com',
        'password': 'admin123'  # Short password
    })
    print(f"Status: {r.status_code}")
    print(f"Response: {r.text}")
except Exception as e:
    print(f"Error: {e}")

print("\n=== Testing Login ===")
try:
    r = requests.post(f'{base}/api/login', json={
        'email': 'admin2@test.com',
        'password': 'admin123'
    })
    print(f"Status: {r.status_code}")
    resp = r.json()
    print(f"Response: {json.dumps(resp, indent=2)}")
    if 'access_token' in resp:
        token = resp['access_token']
        print(f"\nToken received: {token[:30]}...")
        
        print("\n=== Testing GET /me ===")
        r = requests.get(f'{base}/api/me', headers={'Authorization': f'Bearer {token}'})
        print(f"Status: {r.status_code}")
        print(f"Response: {r.json()}")
except Exception as e:
    print(f"Error: {e}")

