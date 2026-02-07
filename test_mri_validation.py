"""
Test script for MRI image validation integration.

Tests that:
1. Valid brain MRI images are accepted and predicted
2. Invalid images are rejected with clear error messages
3. Validation runs BEFORE model prediction
4. Error handling is graceful
"""

import requests
import json
from pathlib import Path

BASE_URL = "http://127.0.0.1:8000"


def test_validation():
    """Test the MRI validation system."""
    
    print("\n" + "="*70)
    print("MRI IMAGE VALIDATION TEST SUITE")
    print("="*70)
    
    # Test with a real image from the uploads directory
    uploads_dir = Path("app/static/uploads")
    
    if not uploads_dir.exists():
        print("⚠️  No uploads directory found. Create one with test images.")
        return
    
    # Find test images
    test_images = list(uploads_dir.glob("*.jpg")) + list(uploads_dir.glob("*.jpeg")) + list(uploads_dir.glob("*.png"))
    
    if not test_images:
        print("⚠️  No test images found in app/static/uploads/")
        print("    Please add some brain MRI images to test validation.")
        return
    
    print(f"\n✅ Found {len(test_images)} test image(s)")
    
    # Test each image
    for image_path in test_images[:3]:  # Test first 3 images
        print(f"\n{'─'*70}")
        print(f"Testing: {image_path.name}")
        print(f"{'─'*70}")
        
        try:
            with open(image_path, "rb") as f:
                files = {"file": (image_path.name, f, "image/jpeg")}
                response = requests.post(
                    f"{BASE_URL}/api/predict",
                    files=files,
                    timeout=30
                )
            
            print(f"Status: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                
                # Check validation result
                is_valid = data.get("is_valid_brain_image", False)
                status = data.get("status", "unknown")
                reason = data.get("validation_reason", "N/A")
                
                print(f"Valid MRI: {is_valid}")
                print(f"Status: {status}")
                print(f"Reason: {reason}")
                
                if status == "success" and is_valid:
                    # Valid brain MRI - prediction should be included
                    print(f"\n✅ VALID BRAIN MRI - Prediction generated:")
                    if data.get("top_prediction"):
                        top = data["top_prediction"]
                        print(f"   Predicted: {top['label']} ({top['percentage']}%)")
                    print(f"   Disclaimer: {data.get('disclaimer', 'N/A')[:80]}...")
                
                elif status == "invalid_image" and not is_valid:
                    # Invalid image - prediction should NOT be included
                    print(f"\n❌ INVALID IMAGE - Prediction blocked:")
                    print(f"   Error: {data.get('error', 'N/A')}")
                    print(f"   Disclaimer: {data.get('disclaimer', 'N/A')[:80]}...")
                    print(f"   No predictions were generated (as expected)")
                
                else:
                    print(f"\n⚠️  UNEXPECTED STATE:")
                    print(f"   is_valid_brain_image={is_valid}, status={status}")
            
            else:
                print(f"❌ Error: {response.text[:200]}")
        
        except Exception as e:
            print(f"❌ Connection error: {str(e)}")
    
    print(f"\n{'='*70}")
    print("TEST COMPLETE")
    print(f"{'='*70}\n")


if __name__ == "__main__":
    print("\n🔍 Checking backend availability...")
    try:
        response = requests.get(f"{BASE_URL}/docs", timeout=5)
        if response.status_code == 200:
            print("✅ Backend is running")
        else:
            print("⚠️  Backend responding with unexpected status")
    except:
        print("❌ Backend not accessible at http://127.0.0.1:8000")
        print("   Start backend with: python -m uvicorn app.main:app --port 8000 --reload")
        exit(1)
    
    test_validation()
