# Brain MRI Prediction Debugging Guide

## Overview
This guide explains how to see MRI predictions in real-time and debug any issues with the brain tumor detection system.

---

## 🔍 Where to View Predictions

### 1. **Frontend UI** (Real-time Visual Display)
After uploading an MRI image, predictions appear in the web interface:

- **Location**: `http://localhost:3000` (development) or your deployed URL
- **Prediction Display Panel**: Shows:
  - ✅ Top tumor prediction with confidence percentage
  - 📊 Confidence breakdown for all 4 classes (Glioma, Meningioma, No Tumor, Pituitary)
  - 🔴 Severity level (None, Low, Medium, High)
  - 📋 Medical analysis and recommendations

### 2. **Browser Developer Console** (Raw API Response)
To see the raw prediction data:

1. Open your browser's Developer Tools (`F12` or `Ctrl+Shift+I`)
2. Go to the **Console** tab
3. Upload an MRI image
4. The prediction will be logged as:
   ```javascript
   window.latestPrediction
   ```
5. Or check network traffic in **Network** tab → Find `predict` request → **Response** tab

### 3. **Browser Network Inspector** (API Endpoint)
To debug the API request/response:

1. Open Developer Tools (`F12`)
2. Go to **Network** tab
3. Upload an MRI image
4. Look for POST request to `/api/predict`
5. View:
   - **Request**: Shows uploaded file
   - **Response**: Shows prediction JSON with:
     - `predictions`: Array of all class probabilities
     - `top_prediction`: Best match with confidence
     - `medical_analysis`: Detailed medical insights
     - `status`: "success" or "invalid_image" or "error"

### 4. **Backend Logs** (Server-side Debugging)
To see server-side processing:

**Running locally:**
```bash
# Terminal where backend is running will show:
# - Image file received
# - MRI validation results
# - Model prediction scores
# - Processing time
```

**Example log output:**
```
INFO: Image loaded: app/static/uploads/brain_mri_001.jpg
INFO: MRI validation for brain_mri_001.jpg: valid=True
INFO: Image preprocessed and normalized
INFO: Using trained model for predictions
DEBUG: Glioma: 0.15
DEBUG: Meningioma: 0.08
DEBUG: No Tumor: 0.72
DEBUG: Pituitary: 0.05
INFO: Inference completed. Top prediction: No Tumor (72.00%)
```

---

## 📊 Understanding Predictions

### JSON Response Structure

```json
{
  "predictions": [
    {
      "class_index": 2,
      "label": "No Tumor",
      "confidence": 0.7234,
      "percentage": 72.34
    },
    {
      "class_index": 0,
      "label": "Glioma Tumor",
      "confidence": 0.1523,
      "percentage": 15.23
    },
    {
      "class_index": 3,
      "label": "Pituitary Tumor",
      "confidence": 0.0891,
      "percentage": 8.91
    },
    {
      "class_index": 1,
      "label": "Meningioma Tumor",
      "confidence": 0.0352,
      "percentage": 3.52
    }
  ],
  "top_prediction": {
    "class_index": 2,
    "label": "No Tumor",
    "confidence": 0.7234,
    "percentage": 72.34
  },
  "medical_analysis": {
    "tumor_type": "No Tumor",
    "description": "No brain tumor detected...",
    "severity_level": "None",
    "advantages": [...],
    "disadvantages": [...],
    "key_characteristics": [...],
    "recommended_next_steps": [...]
  },
  "status": "success",
  "is_valid_brain_image": true,
  "image_path": "app/static/uploads/brain_mri_001.jpg"
}
```

### Class Labels
- **0**: Glioma Tumor
- **1**: Meningioma Tumor
- **2**: No Tumor
- **3**: Pituitary Tumor

---

## 🔧 Troubleshooting Predictions

### Issue: Invalid Image Error
**Message**: `"The uploaded file does not appear to be a valid brain MRI scan"`

**Causes & Solutions**:
1. ❌ **Not a brain MRI** → Upload actual brain MRI scan
2. ❌ **Too small** (< 150x150 pixels) → Use larger image
3. ❌ **Wrong format** → Ensure JPEG, PNG, or DICOM
4. ❌ **Poor contrast** → Enhance image contrast in image editor
5. ❌ **Too dark/bright** → Adjust brightness/levels

### Issue: Model Not Found
**Message**: `"Model file not found at app/models/brain_tumor_model.h5"`

**Solution**:
1. Train the model first:
   ```bash
   python training/train_on_uploads.py
   ```
2. OR ensure `brain_tumor_model.h5` exists in `app/models/`

### Issue: Predictions Don't Update on Frontend
**Debug Steps**:
1. Check browser console for errors (`F12`)
2. Verify API_BASE_URL is correct in `frontend/src/config/api.js`
3. Check if backend is running (`http://localhost:8000/health`)
4. Verify CORS is enabled (should be in production too)

### Issue: Low Confidence Score
**Interpretation**:
- Confidence < 60% → Model is uncertain, consider specialist review
- This is normal for ambiguous or poor quality images
- Always recommend professional medical consultation for low confidence

---

## 🚀 Real-Time Monitoring Setup

### Option 1: Backend Logs in Real-time
```bash
# Terminal 1: Start backend with verbose logging
export LOG_LEVEL=DEBUG
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Option 2: Frontend Network Monitoring
1. Open DevTools Network tab
2. Filter by "predict"
3. Upload MRI
4. Click request and monitor real-time response

### Option 3: Browser Console Script
Paste in browser console to auto-log predictions:
```javascript
window.addEventListener('predictionUpdated', (e) => {
  console.log('🧠 New Prediction:', e.detail);
  console.log('Top:', e.detail.top_prediction.label, 
              `(${e.detail.top_prediction.percentage}%)`);
  console.log('All:', e.detail.predictions);
});
```

---

## 📈 API Endpoints

### POST /api/predict
Upload MRI image and get predictions

**URL**: `http://localhost:8000/api/predict` (local)

**Request**:
```bash
curl -X POST http://localhost:8000/api/predict \
  -F "file=@brain_mri.jpg"
```

**Response**: Full prediction JSON (see structure above)

### GET /health
Check backend is running

**URL**: `http://localhost:8000/health`

**Response**:
```json
{
  "status": "healthy",
  "service": "Brain Tumor Chatbot",
  "version": "1.0.0"
}
```

---

## 🔬 Checking Prediction Quality

### Good Predictions (High Confidence):
- ✅ Confidence > 75%
- ✅ Clearer separation between top and 2nd choice
- ✅ Image is clear MRI scan

### Fair Predictions (Medium Confidence):
- ⚠️ Confidence 50-75%
- ⚠️ Shows uncertainty, recommend verification
- ⚠️ Specialist review recommended

### Poor Predictions (Low Confidence):
- ❌ Confidence < 50%
- ❌ Multiple classes similar probability
- ❌ Likely invalid/non-MRI image

---

## 🔐 Image Validation Details

The system validates images with these checks:

1. **Size Check**: Minimum 150x150 pixels
2. **Aspect Ratio**: Between 0.6 and 1.67 (allows rectangular images)
3. **Format Check**: RGB, Grayscale, RGBA, or Binary
4. **Brightness**: Mean intensity between 3-252 (not too dark/bright)
5. **Contrast**: Standard deviation > 5 (sufficient variation)
6. **Uniqueness**: At least 10 unique grayscale values

---

## 📝 Code Locations

| Component | Location | Purpose |
|-----------|----------|---------|
| Prediction Logic | `app/services/inference.py` | Main inference service |
| API Endpoint | `app/api/routes/predict.py` | API route handler |
| Image Processing | `app/core/image_utils.py` | Image preprocessing |
| Model Loader | `app/core/model_loader.py` | Model loading & caching |
| Frontend Display | `frontend/src/components/ResultPanel.jsx` | Prediction UI |
| Upload Handler | `frontend/src/components/UploadCard.jsx` | File upload |
| Medical Data | `app/services/inference.py` | Medical analysis database |

---

## 🧪 Testing Predictions

### Local Testing
```bash
# 1. Start backend
cd neuroAssist-main
python -m uvicorn app.main:app --reload

# 2. Start frontend (in another terminal)
cd frontend
npm install
npm run dev

# 3. Navigate to http://localhost:5173
# 4. Upload test MRI image
# 5. Check predictions appear in browser
```

### Test with API directly
```bash
# Upload file and get raw predictions
curl -X POST http://localhost:8000/api/predict \
  -F "file=@test_image.jpg" | python -m json.tool
```

---

## 📱 Mobile/Remote Testing

If deployed (e.g., Netlify, Render):

1. **Frontend URL**: Your Netlify/Vercel deployment URL
2. **Backend URL**: Your API deployment URL (Render, Railway, etc.)
3. **Update** `frontend/.env` with production API URL:
   ```
   VITE_API_BASE_URL=https://your-api-domain.com
   ```

---

## 🆘 Getting Help

**Check these files for detailed logs:**
- Backend logs: Terminal running uvicorn
- Error logs: Check `app/utils/logger.py`
- API responses: Browser DevTools → Network tab

**Common solutions:**
1. Clear browser cache (`Ctrl+Shift+Del`)
2. Restart backend server
3. Restart frontend dev server
4. Check network connectivity
5. Verify image is valid MRI

---

**Last Updated**: February 2026
**Version**: 1.0.0
