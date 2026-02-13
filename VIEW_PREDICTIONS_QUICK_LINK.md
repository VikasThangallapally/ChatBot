# Quick Links to View Brain MRI Predictions

## 🌐 Live Application

### 1. **Main User Interface** ← Best way to see predictions
- **URL**: `http://localhost:5173` (local development)
- **What you see**: Beautiful UI with:
  - 📊 Confidence percentage for top prediction
  - 📈 Confidence breakdown chart for all tumor types
  - 🏥 Medical analysis and recommendations
  - 📋 Detailed medical information

### 2. **Backend API Health Check**
- **URL**: `http://localhost:8000/health`
- **Shows**: API is running and ready for predictions

### 3. **API Prediction Endpoint** (Technical)
- **URL**: `http://localhost:8000/api/predict` (POST endpoint)
- **Method**: Upload MRI image file
- **Returns**: Raw JSON with all predictions and medical analysis

---

## 📊 How to See Predictions

### Step 1: Start the Application
```bash
# Terminal 1 - Start Backend API Server
cd c:\Users\vikas\Downloads\neuroAssist-main\neuroAssist-main
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Terminal 2 - Start Frontend Web Server
cd frontend
npm run dev
```

### Step 2: Upload MRI Image
1. Go to `http://localhost:5173` in your browser
2. Click "Upload MRI Scan" or drag & drop
3. Select a brain MRI image file

### Step 3: View Predictions
You'll see:
- ✅ **Top Prediction**: Which type of tumor (or "No Tumor")
- 📊 **Confidence Score**: How confident the AI is (0-100%)
- 📈 **Breakdown**: Scores for all 4 tumor types:
  - Glioma Tumor
  - Meningioma Tumor
  - No Tumor
  - Pituitary Tumor
- 🏥 **Medical Information**: Details about the predicted condition

---

## 🔍 Where to Look for Raw Predictions

### Option A: Browser Developer Tools (Console)
1. Open browser DevTools: `F12` or `Ctrl+Shift+I`
2. Go to **Console** tab
3. Type: `window.latestPrediction`
4. See the full JSON response with all predictions

### Option B: Browser Developer Tools (Network)
1. Open DevTools: `F12`
2. Go to **Network** tab
3. Filter by "predict"
4. Upload an MRI image
5. Click the `/api/predict` request
6. Go to **Response** tab to see raw data

### Option C: Terminal Logs
When you run the backend server, you'll see prediction logs:
```
INFO: Starting inference on app/static/uploads/brain_mri_001.jpg
INFO: Image validation: Valid=True
INFO: Using trained model for predictions
DEBUG: Glioma: 0.1523
DEBUG: Meningioma: 0.0352
DEBUG: No Tumor: 0.7234
DEBUG: Pituitary: 0.0891
INFO: Inference completed. Top prediction: No Tumor (72.34%)
```

---

## 🧠 Understanding the Predictions

### Example Response:
```json
{
  "top_prediction": {
    "label": "No Tumor",
    "confidence": 0.7234,
    "percentage": 72.34
  },
  "predictions": [
    {"label": "No Tumor", "percentage": 72.34},
    {"label": "Glioma Tumor", "percentage": 15.23},
    {"label": "Pituitary Tumor", "percentage": 8.91},
    {"label": "Meningioma Tumor", "percentage": 3.52}
  ],
  "status": "success",
  "medical_analysis": {
    "description": "No brain tumor detected...",
    "severity_level": "None",
    "recommendations": [...]
  }
}
```

### What Each Field Means:
- **top_prediction**: The AI's best guess (highest confidence)
- **confidence**: How sure the AI is (0.72 = 72% sure)
- **predictions**: All 4 tumor type scores sorted by confidence
- **status**: "success" = valid prediction, "invalid_image" = bad image
- **medical_analysis**: Detailed medical information about the prediction

---

## ✅ Verify Everything is Working

### Health Check
```bash
curl http://localhost:8000/health
# Should return: {"status": "healthy", ...}
```

### Prediction Test (API Direct)
```bash
curl -X POST http://localhost:8000/api/predict \
  -F "file=@path/to/your_mri.jpg"
# Should return complete JSON with predictions
```

### Frontend Check
- Visit `http://localhost:5173`
- Should see Beautiful UI with upload area
- Try uploading an MRI image

---

## 🔧 Common Issues & Fixes

| Issue | Solution |
|-------|----------|
| "Cannot connect to API" | Make sure backend is running on port 8000 |
| "Invalid image" error | Image is not a brain MRI - upload valid brain scan |
| No predictions showing | Check browser console (F12) for errors |
| 404 on localhost:5173 | Make sure frontend dev server is running |
| No logs in terminal | Enable debug logging: `export LOG_LEVEL=DEBUG` |

---

## 📂 Project Structure

```
neuroAssist-main/
├── app/                          # Backend API
│   ├── services/inference.py      # 🧠 Prediction logic
│   ├── api/routes/predict.py      # 📡 API endpoint
│   ├── core/image_utils.py        # 🖼️ Image preprocessing
│   └── models/                    # 🤖 Trained model files
│
├── frontend/                      # Web Interface
│   ├── src/components/
│   │   ├── UploadCard.jsx         # 📤 Upload UI
│   │   ├── ResultPanel.jsx        # 📊 Prediction display
│   │   └── MedicalAnalysis.jsx    # 🏥 Medical info
│   │
│   ├── src/config/api.js          # 🔗 API configuration
│   └── index.html                 # Main page
│
└── PREDICTION_DEBUGGING_GUIDE.md   # 📖 Detailed guide
```

---

## 🚀 Quick Start

```bash
# 1. Install dependencies (one time)
cd frontend
npm install

# 2. Start backend (Terminal 1)
cd ..
python -m uvicorn app.main:app --reload

# 3. Start frontend (Terminal 2)
cd frontend
npm run dev

# 4. Open browser
# http://localhost:5173
# Upload your brain MRI image and see predictions!
```

---

## 📞 Support

- **Detailed debugging guide**: Read `PREDICTION_DEBUGGING_GUIDE.md`
- **Backend logs**: Check terminal running uvicorn
- **Frontend errors**: Open browser DevTools (F12) → Console
- **Network issues**: DevTools → Network tab → filter "predict"

---

**Ready to see predictions? Start the servers and upload an MRI image!** 🧠
