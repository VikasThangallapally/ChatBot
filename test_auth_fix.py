#!/usr/bin/env python
"""Test script to validate auth endpoints with service_role key."""

import requests
import json
import time
import sys

BASE_URL = "http://127.0.0.1:8000"
TIMEOUT = 10

def test_register():
    """Test user registration."""
    print("\n" + "="*60)
    print("TEST 1: User Registration")
    print("="*60)
    
    payload = {
        "name": "Test User",
        "email": "testuser@example.com",
        "password": "Test123!@"
    }
    
    try:
        print(f"POST {BASE_URL}/api/register")
        print(f"Payload: {json.dumps(payload, indent=2)}")
        
        response = requests.post(
            f"{BASE_URL}/api/register",
            json=payload,
            timeout=TIMEOUT
        )
        
        print(f"\nStatus Code: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            print("✅ Registration SUCCESSFUL!")
            return response.json()
        else:
            print(f"❌ Registration FAILED with status {response.status_code}")
            return None
            
    except requests.exceptions.ConnectionError:
        print("❌ Connection Error: Backend not responding at http://127.0.0.1:8000")
        print("   Make sure backend is running: 'uvicorn app.main:app --reload --port 8000'")
        return None
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

def test_login(email, password):
    """Test user login."""
    print("\n" + "="*60)
    print("TEST 2: User Login")
    print("="*60)
    
    payload = {
        "email": email,
        "password": password
    }
    
    try:
        print(f"POST {BASE_URL}/api/login")
        print(f"Payload: {json.dumps(payload, indent=2)}")
        
        response = requests.post(
            f"{BASE_URL}/api/login",
            json=payload,
            timeout=TIMEOUT
        )
        
        print(f"\nStatus Code: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            print("✅ Login SUCCESSFUL!")
            return response.json()
        else:
            print(f"❌ Login FAILED with status {response.status_code}")
            return None
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

def test_me_endpoint(token):
    """Test get current user endpoint."""
    print("\n" + "="*60)
    print("TEST 3: Get Current User (/me endpoint)")
    print("="*60)
    
    headers = {
        "Authorization": f"Bearer {token}"
    }
    
    try:
        print(f"GET {BASE_URL}/api/me")
        print(f"Headers: {headers}")
        
        response = requests.get(
            f"{BASE_URL}/api/me",
            headers=headers,
            timeout=TIMEOUT
        )
        
        print(f"\nStatus Code: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            print("✅ Get current user SUCCESSFUL!")
            return response.json()
        else:
            print(f"❌ Get current user FAILED with status {response.status_code}")
            return None
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

if __name__ == "__main__":
    print("\n" + "🔍 TESTING AUTH ENDPOINTS WITH SERVICE_ROLE KEY" + "\n")
    
    # Test registration
    user_data = test_register()
    
    if user_data:
        # Test login
        login_data = test_login("testuser@example.com", "Test123!@")
        
        if login_data and "access_token" in login_data:
            # Test me endpoint
            test_me_endpoint(login_data["access_token"])
        else:
            print("\n⚠️  Skipping /me test (no token from login)")
    else:
        print("\n⚠️  Skipping remaining tests (registration failed)")
    
    print("\n" + "="*60)
    print("TESTING COMPLETE")
    print("="*60 + "\n")
