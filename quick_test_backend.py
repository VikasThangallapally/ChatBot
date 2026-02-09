#!/usr/bin/env python
"""Quick test to check if backend is responding and register endpoint works"""

import requests
import json
import time

def test_backend():
    """Test if backend is running"""
    print("\n" + "="*60)
    print("CHECKING BACKEND STATUS")
    print("="*60)
    
    test_urls = [
        ("GET", "http://127.0.0.1:8000/docs", "Swagger UI"),
        ("GET", "http://127.0.0.1:8000/openapi.json", "OpenAPI Schema"),
    ]
    
    for method, url, desc in test_urls:
        try:
            print(f"\n Testing {desc}...")
            if method == "GET":
                r = requests.get(url, timeout=5)
                print(f"  ✓ {desc}: {r.status_code}")
                return True
        except requests.exceptions.ConnectionError:
            print(f"  ✗ {desc}: Connection refused")
        except Exception as e:
            print(f"  ✗ {desc}: {e}")
    
    return False

def test_register():
    """Test registration endpoint"""
    print("\n" + "="*60)
    print("TESTING REGISTER ENDPOINT")
    print("="*60)
    
    payload = {
        "name": "John Doe",
        "email": f"john{int(time.time())}@example.com",
        "password": "SecurePass123!"
    }
    
    try:
        print(f"\nSending POST request to http://127.0.0.1:8000/api/register")
        print(f"Payload: {json.dumps(payload, indent=2)}")
        
        response = requests.post(
            "http://127.0.0.1:8000/api/register",
            json=payload,
            timeout=10
        )
        
        print(f"\nStatus Code: {response.status_code}")
        print(f"Response Headers: {dict(response.headers)}")
        print(f"Response Body: {response.text}")
        
        if response.status_code == 200:
            print("\n✅ REGISTRATION SUCCESSFUL!")
            return True
        else:
            print(f"\n❌ Registration failed with status {response.status_code}")
            return False
            
    except requests.exceptions.ConnectionError as e:
        print(f"\n❌ ERROR: Cannot connect to backend")
        print(f"   Make sure backend is running on port 8000")
        print(f"   Run: cd neuroAssist-main && uvicorn app.main:app --reload --port 8000")
        return False
    except requests.exceptions.Timeout:
        print(f"\n❌ ERROR: Request timed out (backend not responding)")
        return False
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        return False

if __name__ == "__main__":
    print("\n🔍 NEUROASSIST AUTH SYSTEM TEST")
    
    # Check if backend is running
    if not test_backend():
        print("\n" + "="*60)
        print("⚠️  BACKEND NOT RESPONDING")
        print("="*60)
        print("\nStart the backend using:")
        print("  cd neuroAssist-main")
        print("  python -m uvicorn app.main:app --reload --port 8000")
    else:
        # Test registration
        test_register()
    
    print("\n" + "="*60)
    print("TEST COMPLETE")
    print("="*60 + "\n")
