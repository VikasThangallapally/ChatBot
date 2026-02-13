# Brain MRI Prediction - Common Issues & Solutions

## Issue 1: Invalid Image Error When Uploading MRI

### Error Message
```
"The uploaded file does not appear to be a valid brain MRI scan"
```

### Root Causes & Fixes

#### Cause 1: Image Too Small
- **Problem**: Image dimensions < 150x150 pixels
- **Fix**: Use larger image or scale up the image before uploading
- **Verification**: Check image properties - should be at least 150x150px

#### Cause 2: Wrong Image Type
- **Problem**: Image is not a brain scan (e.g., chest X-ray, regular photo)
- **Fix**: Upload actual brain MRI scan in DICOM, JPEG, or PNG format
- **Verification**: Image should show brain cross-section

#### Cause 3: Poor Image Quality
- **Problem**: Image too dark, too bright, or low contrast
- **Fix**: 
  1. Use image editor (Photoshop, GIMP) to adjust:
     - Brightness/Contrast
     - Levels
     - Curves
  2. Ensure image has visible detail
- **Check**: Image should show clear brain structures

#### Cause 4: Corrupted File
- **Problem**: Image file is damaged or incomplete
- **Fix**: 
  1. Re-export the image
  2. Try converting to different format (JPG ↔ PNG)
  3. Download fresh copy from source

### Test with Different Images
```bash
# If you have test images, try:
curl -X POST http://localhost:8000/api/predict \
  -F "file=@test_mri_1.jpg"

curl -X POST http://localhost:8000/api/predict \
  -F "file=@test_mri_2.png"
```

---

## Issue 2: Model Not Found Error

### Error Message
```
"Model file not found at app/models/brain_tumor_model.h5"
```

### Solution

The trained model file is missing. You need to train the model first:

#### Step 1: Check if Model Exists
```bash
# Windows
dir app/models/

# Should show: brain_tumor_model.h5
```

#### Step 2: If Not Found, Train the Model
```bash
python training/train_on_uploads.py
```

#### Step 3: Verify Model Was Created
```bash
# Windows
dir app/models/
# Look for brain_tumor_model.h5 (should be 50-200 MB)
```

#### Step 4: Restart Backend
```bash
# Kill the current backend server and restart:
python -m uvicorn app.main:app --reload
```

---

## Issue 3: Predictions Don't Appear on Frontend

### Debug Steps

#### Step 1: Check Backend is Running
```bash
# In browser console, run:
fetch('http://localhost:8000/health')
  .then(r => r.json())
  .then(d => console.log(d))

# Should show: {status: "healthy", ...}
```

#### Step 2: Check Frontend is Connecting to Backend
```javascript
// Open browser console (F12) and type:
window.latestPrediction

// Should show prediction data after upload
// If undefined, check browser console for errors
```

#### Step 3: Check API Base URL
Look at `frontend/src/config/api.js`:
```javascript
export const API_BASE_URL = 'http://localhost:8000'  // or your API URL
```

For **production deployment**, ensure this matches your deployed backend URL.

#### Step 4: Check Browser Console for Errors
1. Open DevTools (`F12`)
2. Go to **Console** tab
3. Upload an MRI image
4. Look for red error messages
5. Common errors:
   - CORS error → Check backend CORS settings
   - 404 error → API URL is wrong
   - Network error → Backend not running

#### Step 5: Check Network Tab
1. Open DevTools (`F12`)
2. Go to **Network** tab
3. Upload image
4. Find request to `/api/predict`
5. Check:
   - **Status**: Should be `200` (success) or `400` (invalid image)
   - **Response**: Should show prediction JSON
   - **Request size**: Shows file was uploaded

---

## Issue 4: Low Confidence Predictions

### What It Means
```json
{
  "top_prediction": {
    "label": "Glioma Tumor",
    "confidence": 0.45  // ← Low confidence!
  }
}
```

### Reasons
- Image quality is poor
- Ambiguous tumor appearance
- Image is not a typical MRI layout
- Model uncertainty on this case

### What To Do
- ✅ **< 50%**: Model is guessing - seek professional medical opinion
- ✅ **50-75%**: Fair confidence - provide specialist review
- ✅ **> 75%**: Good confidence - still recommend specialist verification

### Example Interpretation
```
Confidence  |  Meaning              | Action
-----------|----------------------|----------
85%        | High confidence       | Generally trustworthy
72%        | Good confidence       | Reasonable prediction
55%        | Fair confidence       | Verify with specialist  
35%        | Low confidence        | Seek specialist opinion
```

---

## Issue 5: All Predictions Equal Probability

### Symptom
```json
{
  "predictions": [
    {"label": "Glioma", "percentage": 25},
    {"label": "Meningioma", "percentage": 25},
    {"label": "No Tumor", "percentage": 25},
    {"label": "Pituitary", "percentage": 25}
  ]
}
```

### Cause
Model is using **fallback prediction** (model unavailable or error)

### Fix
1. Check if model file exists: `dir app/models/`
2. Check backend logs for errors
3. Restart backend server
4. Try again with different image

---

## Issue 6: CORS Errors on Frontend

### Error Message (Browser Console)
```
Access to XMLHttpRequest at 'http://localhost:8000/api/predict'
from origin 'http://localhost:5173' has been blocked by CORS policy
```

### Cause
Frontend and backend on different ports

### Solution - Already Fixed in Code
The backend should have CORS enabled:
```python
# app/main.py - Already configured
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

If error still occurs:
1. Restart backend: `python -m uvicorn app.main:app --reload`
2. Clear browser cache: `Ctrl+Shift+Del`
3. Hard refresh: `Ctrl+F5`

---

## Issue 7: File Too Large Error

### Error Message
```
"File too large"
```

### Cause
Image file > 10 MB (default limit)

### Fix
```python
# In app/config.py, if needed, increase limit:
MAX_UPLOAD_SIZE = 50 * 1024 * 1024  # 50 MB instead of 10 MB
```

Or compress image before uploading:
```bash
# Using ImageMagick or Python
# Reduce file size while maintaining quality
magick convert large.jpg -resize 1024x1024 small.jpg

# Or with Python
from PIL import Image
img = Image.open('large.jpg')
img.thumbnail((1024, 1024))
img.save('small.jpg')
```

---

## Issue 8: GPU/Memory Issues

### Error
```
CUDA out of memory
ResourceExhaustedError
```

### Solutions

#### Option 1: Run on CPU (Slower but works)
```python
# In app/core/model_loader.py, add at top:
import os
os.environ['CUDA_VISIBLE_DEVICES'] = '-1'  # Force CPU
```

#### Option 2: Use Smaller Batch Size
The system already uses batch size 1 (good for memory)

#### Option 3: Reduce Image Size
```python
# In app/config.py
IMAGE_SIZE = 128  # Was 150, now smaller
```

#### Option 4: Check Memory
```bash
# See available memory
nvidia-smi  # If GPU
free -h     # If CPU
```

---

## Issue 9: Model Training Failed

### Error When Running `training/train_on_uploads.py`
```
FileNotFoundError: Training dataset not found
```

### Solution
1. Ensure training data exists:
   ```bash
   dir "app/static/Brain Folders/Training/"
   # Should show folders: Glioma, Meningioma, NoTumor, Pituitary
   ```

2. If missing, copy training data:
   ```bash
   # Copy your brain MRI images to folders:
   app/static/Brain Folders/Training/Glioma/
   app/static/Brain Folders/Training/Meningioma/
   app/static/Brain Folders/Training/NoTumor/
   app/static/Brain Folders/Training/Pituitary/
   ```

3. Retry training:
   ```bash
   python training/train_on_uploads.py
   ```

---

## Issue 10: 500 Internal Server Error

### Error Message
```
500 Internal Server Error
```

### Debug Steps

1. **Check Backend Logs**
   - Look at terminal where backend is running
   - Error message should be shown there

2. **Check Exception Details**
   - Browser console → Network tab
   - Find `/api/predict` request
   - Go to Response tab to see full error

3. **Common Causes**:
   - Model loading failed → Restart backend
   - Out of memory → Kill other apps
   - Corrupted image → Try different image
   - Path issues → Check file paths in code

4. **Enable Debug Logging**
   ```bash
   set LOG_LEVEL=DEBUG
   python -m uvicorn app.main:app --reload
   ```

---

## Debugging Checklist

Print this checklist when troubleshooting:

```
☐ Backend running? http://localhost:8000/health
☐ Frontend running? http://localhost:5173
☐ Model file exists? app/models/brain_tumor_model.h5
☐ Image is valid brain MRI? (150x150+ pixels, clear contrast)
☐ Browser console shows no errors? (F12)
☐ Network tab shows 200 status? (F12 → Network → predict)
☐ latestPrediction exists? (Console: window.latestPrediction)
☐ API base URL correct? (frontend/src/config/api.js)
☐ CORS errors? (Restart backend with cors enabled)
☐ Cache cleared? (Ctrl+Shift+Del)
```

---

## Getting Help

### Where to Check
1. **Backend logs** → Terminal running uvicorn
2. **Frontend console** → Browser DevTools (F12) → Console
3. **Network logs** → Browser DevTools (F12) → Network
4. **Model logs** → Training terminal output
5. **Error documentation** → `PREDICTION_DEBUGGING_GUIDE.md`

### What to Provide When Asking for Help
1. Error message (exact text)
2. Screenshot of error
3. Backend logs (last 10 lines)
4. Browser console errors (F12)
5. Network response (DevTools → Network)

---

**Version**: 1.0.0
**Last Updated**: February 2026
