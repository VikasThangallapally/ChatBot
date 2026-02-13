"""
Test script to verify that invalid images (non-brain MRI) are properly rejected
and do NOT generate tumor predictions.
"""

import requests
import numpy as np
from PIL import Image
import io
import json
import sys

# Configuration
API_URL = "http://localhost:8000/api/predict"
TIMEOUT = 30

def create_test_image(image_type="colored_photo"):
    """Create various test images to validate rejection"""
    
    if image_type == "colored_photo":
        # Create a colorful RGB image (like a photo)
        arr = np.random.randint(0, 256, (300, 300, 3), dtype=np.uint8)
        # Add some structure to make it look more like a photo
        for i in range(50, 250):
            for j in range(50, 250):
                arr[i, j] = [100, 150, 200]  # Flesh-like color
        img = Image.fromarray(arr, 'RGB')
        
    elif image_type == "random_noise":
        # Pure random noise
        arr = np.random.randint(0, 256, (150, 150), dtype=np.uint8)
        img = Image.fromarray(arr, 'L')
        
    elif image_type == "uniform_gray":
        # Uniform gray image (no variation)
        arr = np.ones((150, 150), dtype=np.uint8) * 128
        img = Image.fromarray(arr, 'L')
        
    elif image_type == "black_image":
        # All black
        arr = np.zeros((150, 150), dtype=np.uint8)
        img = Image.fromarray(arr, 'L')
        
    elif image_type == "high_contrast_bars":
        # Alternating black/white bars (extreme contrast)
        arr = np.zeros((150, 150), dtype=np.uint8)
        arr[::10, :] = 255
        img = Image.fromarray(arr, 'L')
        
    elif image_type == "small_image":
        # Too small (below 150x150)
        arr = np.random.randint(0, 256, (100, 100), dtype=np.uint8)
        img = Image.fromarray(arr, 'L')
    
    return img

def test_invalid_image(image_type):
    """Test an invalid image and verify it's rejected"""
    print(f"\n{'='*60}")
    print(f"Testing: {image_type}")
    print(f"{'='*60}")
    
    img = create_test_image(image_type)
    
    # Convert to bytes
    img_bytes = io.BytesIO()
    img.save(img_bytes, format='PNG')
    img_bytes.seek(0)
    
    # Send to API
    files = {'file': ('test.png', img_bytes, 'image/png')}
    
    try:
        response = requests.post(API_URL, files=files, timeout=TIMEOUT)
        
        if response.status_code == 200:
            result = response.json()
            
            print(f"Status: {result.get('status', 'N/A')}")
            print(f"Is Valid Brain Image: {result.get('is_valid_brain_image', 'N/A')}")
            print(f"Validation Passed: {result.get('validation_passed', 'N/A')}")
            
            # Check if predictions were generated (SHOULD BE EMPTY for invalid)
            predictions = result.get('predictions', [])
            print(f"Predictions Count: {len(predictions)}")
            
            if result.get('status') == 'invalid_image':
                print("✅ PASS: Correctly rejected as invalid_image")
                print(f"   Error: {result.get('error', 'N/A')}")
                if len(predictions) == 0:
                    print("✅ PASS: No predictions generated")
                else:
                    print(f"❌ FAIL: Predictions were generated for invalid image!")
                    for pred in predictions:
                        print(f"   - {pred}")
            else:
                print("❌ FAIL: Image was not rejected")
                print(f"   Got status: {result.get('status')}")
                if len(predictions) > 0:
                    print(f"❌ CRITICAL: Predictions made for invalid image!")
                    for pred in predictions:
                        print(f"   - {pred['label']}: {pred['confidence']:.2%}")
        else:
            print(f"❌ API Error: {response.status_code}")
            print(response.text)
            
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to API. Is the backend running on port 8000?")
        print("   Start it with: python -m uvicorn app.main:app --reload --port 8000")
        return False
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False
    
    return True

def main():
    print("\n" + "="*60)
    print("INVALID IMAGE VALIDATION TEST")
    print("Testing that non-brain-MRI images are properly rejected")
    print("="*60)
    
    test_cases = [
        "colored_photo",
        "random_noise",
        "uniform_gray",
        "black_image",
        "high_contrast_bars",
        "small_image"
    ]
    
    results = {}
    for test_case in test_cases:
        results[test_case] = test_invalid_image(test_case)
    
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    for test_case, passed in results.items():
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status}: {test_case}")
    
    all_passed = all(results.values())
    print("\n" + ("="*60))
    if all_passed:
        print("✅ ALL TESTS PASSED - Invalid images are properly rejected!")
    else:
        print("❌ SOME TESTS FAILED - Check the validation logic")
    print("="*60 + "\n")

if __name__ == "__main__":
    main()
