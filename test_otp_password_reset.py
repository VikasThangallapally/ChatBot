#!/usr/bin/env python
"""Test script for OTP-based password reset functionality"""

import requests
import json
import time

BASE_URL = "http://127.0.0.1:8000"
TIMEOUT = 10

def test_forgot_password(email):
    """Test forgot password endpoint"""
    print("\n" + "="*60)
    print(f"TEST: Request OTP for {email}")
    print("="*60)
    
    try:
        print(f"POST {BASE_URL}/api/auth/forgot-password")
        response = requests.post(
            f"{BASE_URL}/api/auth/forgot-password",
            json={"email": email},
            timeout=TIMEOUT
        )
        
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            print("✅ OTP request successful!")
            return True
        else:
            print(f"❌ Failed with status {response.status_code}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to backend")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_reset_password(email, otp_code, new_password):
    """Test reset password endpoint"""
    print("\n" + "="*60)
    print(f"TEST: Reset password with OTP {otp_code}")
    print("="*60)
    
    payload = {
        "email": email,
        "otp_code": otp_code,
        "new_password": new_password
    }
    
    try:
        print(f"POST {BASE_URL}/api/auth/reset-password")
        print(f"Payload: {json.dumps(payload, indent=2)}")
        
        response = requests.post(
            f"{BASE_URL}/api/auth/reset-password",
            json=payload,
            timeout=TIMEOUT
        )
        
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            print("✅ Password reset successful!")
            return True
        else:
            print(f"❌ Failed with status {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_invalid_otp(email):
    """Test reset password with invalid OTP"""
    print("\n" + "="*60)
    print("TEST: Invalid OTP (should fail)")
    print("="*60)
    
    payload = {
        "email": email,
        "otp_code": "000000",  # Invalid OTP
        "new_password": "NewPassword123!"
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/auth/reset-password",
            json=payload,
            timeout=TIMEOUT
        )
        
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 400 and "Invalid OTP" in response.text:
            print("✅ Correctly rejected invalid OTP")
            return True
        else:
            print(f"⚠️  Unexpected response")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    print("\n" + "🔐 "+"="*56 + " 🔐")
    print("  OTP-BASED PASSWORD RESET - FUNCTIONAL TEST")
    print("🔐 " + "="*56 + " 🔐")
    
    test_email = f"testuser{int(time.time())}@example.com"
    test_otp = "123456"  # Replace with actual OTP from email
    new_password = "ResetPassword123!"
    
    print(f"\n📧 Test Email: {test_email}")
    print(f"🔑 Test OTP: {test_otp} (you must get this from your actual email)")
    print(f"🔐 New Password: {new_password}")
    
    print("\n" + "-"*60)
    print("IMPORTANT: Replace test_otp with the actual 6-digit code")
    print("you receive in your email after requesting OTP!")
    print("-"*60)
    
    # Test 1: Request OTP
    if not test_forgot_password(test_email):
        print("\n❌ Backend not responding or OTP request failed")
        print("Make sure the backend is running:")
        print("  python -m uvicorn app.main:app --reload --port 8000")
        return
    
    print("\n📬 Check your email for the OTP code!")
    print("Copy the 6-digit OTP from the email.")
    
    # Prompt user for actual OTP
    actual_otp = input("\n🔐 Enter the OTP you received (6 digits): ").strip()
    
    if not actual_otp or len(actual_otp) != 6 or not actual_otp.isdigit():
        print("❌ Invalid OTP format. Must be 6 digits.")
        return
    
    # Test 2: Invalid OTP first
    print("\n--- Testing with invalid OTP first ---")
    test_invalid_otp(test_email)
    
    # Test 3: Valid reset password with correct OTP
    print("\n--- Testing with valid OTP ---")
    if test_reset_password(test_email, actual_otp, new_password):
        print("\n✅ PASSWORD RESET FLOW WORKING!")
        print(f"Try logging in with:")
        print(f"  Email: {test_email}")
        print(f"  Password: {new_password}")
    else:
        print("\n❌ Password reset failed")
    
    print("\n" + "="*60)
    print("TEST COMPLETED")
    print("="*60 + "\n")

if __name__ == "__main__":
    main()
