# 🧠 Complete Step-by-Step Guide to See MRI Predictions

## 📋 Prerequisites
- Python 3.8+ installed
- Node.js installed
- Brain MRI image files (JPEG or PNG)
- TensorFlow model trained (or follow training steps below)

---

## 🚀 Step 1: Prepare Your Environment

### Windows PowerShell / Command Prompt

```powershell
# Navigate to project directory
cd c:\Users\vikas\Downloads\neuroAssist-main\neuroAssist-main

# Verify you're in the right place
dir  # Should show: app/, frontend/, requirements.txt, etc.
```

---

## 🏋️ Step 2: Install Python Dependencies

```powershell
# Install required Python packages
pip install -r requirements.txt

# Verify TensorFlow installed
python -c "import tensorflow as tf; print(f'TensorFlow {tf.__version__} installed')"

# Should show: TensorFlow 2.x.x installed
```

---

## 🤖 Step 3: Train the Model (If Not Already Done)

### Check if Model Exists
```powershell
# Check if model file exists
dir app\models\

# If brain_tumor_model.h5 exists → SKIP THIS STEP
# If NOT → Follow below to train it
```

### Train Model (Only If Needed)

```powershell
# Ensure you have training data:
# app/static/Brain Folders/Training/
#   ├── Glioma/
#   ├── Meningioma/
#   ├── NoTumor/
#   └── Pituitary/

# Run training script
python training/train_on_uploads.py

# This will take 5-30 minutes depending on your computer
# When done, model is saved to: app/models/brain_tumor_model.h5

# Verify model was created
dir app\models\brain_tumor_model.h5  # Should show file
```

---

## 🌐 Step 4: Start the Backend API Server

Open PowerShell/Command Prompt and run:

```powershell
# Set debug logging (optional but helpful)
$env:LOG_LEVEL="INFO"

# Start the FastAPI backend server
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Expected output:
# INFO:     Uvicorn running on http://0.0.0.0:8000
# INFO:     Application startup complete
```

**Important**: Keep this terminal open! Don't close it.

### Verify Backend is Running
Open a new browser tab and go to:
```
http://localhost:8000/health
```

You should see:
```json
{
  "status": "healthy",
  "service": "Brain Tumor Chatbot",
  "version": "1.0.0"
}
```

---

## 🎨 Step 5: Start the Frontend Web Server

Open **Another** PowerShell/Command Prompt:

```powershell
# Navigate to frontend directory
cd frontend

# Install JavaScript dependencies (run only ONCE)
npm install

# Start development server
npm run dev

# Expected output:
# ➜  Local:   http://localhost:5173/
# ➜  press h to show help
```

**Important**: Keep this terminal open too!

---

## 🌐 Step 6: Open the Web Application

In your browser, go to:
```
http://localhost:5173
```

You should see:
- 🧠 "Brain Tumor AI Assistant" title
- 📤 "Upload MRI Scan" upload area
- 3D brain animation on the right

---

## 📤 Step 7: Upload Your MRI Image

### Option A: Drag & Drop
1. Find a brain MRI image (JPEG or PNG)
2. Drag the image file to the upload area
3. The file will upload automatically

### Option B: Click to Select
1. Click the upload area
2. Browse and select your brain MRI image
3. Click "Open"

### Expected Behavior
1. Upload progress bar appears (0% → 100%)
2. Image preview appears on the right side
3. Results panel appears below

---

## 📊 Step 8: View Your Predictions

After successful upload, you'll see:

### In the Results Panel:
```
━━━━━━━━━━━━━━━━━━━━━━
📊 PREDICTION RESULT
━━━━━━━━━━━━━━━━━━━━━━

🧠 No Tumor

Confidence: 72.34%
Severity: None

━━━━━━━━━━━━━━━━━━━━━━
📈 CONFIDENCE BREAKDOWN
━━━━━━━━━━━━━━━━━━━━━━

No Tumor ████████████████ 72.34%
Glioma   ███░░░░░░░░░░░░ 15.23%
Pituitary ██░░░░░░░░░░░░░ 8.91%
Meningioma █░░░░░░░░░░░░░░ 3.52%

━━━━━━━━━━━━━━━━━━━━━━
🏥 MEDICAL ANALYSIS
━━━━━━━━━━━━━━━━━━━━━━

📋 About This Result:
No brain tumor detected. The MRI scan appears normal with no abnormal masses...

⚕️ Possible Symptoms & Effects:
• If symptoms persist, requires investigation...
• Small lesions may not be detected...

👨‍⚕️ Medical Consultation:
→ Neurologist (if symptoms persist)
→ Primary Care Physician
```

---

## 🔍 Step 9: View Detailed Prediction Data

### Method 1: Browser Console (Easiest)
1. Right-click anywhere on the page → Inspect (or F12)
2. Click "Console" tab
3. Type this in the console:
   ```javascript
   window.latestPrediction
   ```
4. Press Enter
5. You'll see full prediction JSON with all scores

### Method 2: Network Tab (For Developers)
1. Open DevTools (F12)
2. Go to "Network" tab
3. Filter for "predict"
4. Look for `/api/predict` request
5. Click it
6. Go to "Response" tab to see raw data

### Example Response
```json
{
  "status": "success",
  "top_prediction": {
    "label": "No Tumor",
    "confidence": 0.7234,
    "percentage": 72.34,
    "class_index": 2
  },
  "predictions": [
    {
      "label": "No Tumor",
      "confidence": 0.7234,
      "percentage": 72.34,
      "class_index": 2
    },
    {
      "label": "Glioma Tumor",
      "confidence": 0.1523,
      "percentage": 15.23,
      "class_index": 0
    },
    {
      "label": "Pituitary Tumor",
      "confidence": 0.0891,
      "percentage": 8.91,
      "class_index": 3
    },
    {
      "label": "Meningioma Tumor",
      "confidence": 0.0352,
      "percentage": 3.52,
      "class_index": 1
    }
  ],
  "medical_analysis": {
    "tumor_type": "No Tumor",
    "description": "No brain tumor detected...",
    "severity_level": "None",
    "advantages": [...],
    "key_characteristics": [...],
    "recommended_next_steps": [...]
  },
  "image_path": "app/static/uploads/brain_mri_001.jpg",
  "is_valid_brain_image": true
}
```

---

## 🔬 Step 10: Monitor Backend Logs

### Real-time Backend Activity
Watch the Terminal where backend is running (Step 4):

```
INFO: Starting inference on app/static/uploads/brain_mri_001.jpg
INFO: Image validation: Valid=True, Confidence=0.92
INFO: Image preprocessed and normalized
INFO: Using trained model for predictions
DEBUG:   Glioma Tumor: 0.1523 (15.23%)
DEBUG:   Meningioma Tumor: 0.0352 (3.52%)
DEBUG:   No Tumor: 0.7234 (72.34%)
DEBUG:   Pituitary Tumor: 0.0891 (8.91%)
INFO: Inference completed. Top prediction: No Tumor (72.34%)
```

---

## 🔄 Step 11: Upload Another Image

1. Scroll back to the top
2. Click the upload area again
3. Select a different brain MRI image
4. New predictions appear immediately

---

## ✅ Verification Checklist

After completing all steps, ensure:

```
✅ Backend running on http://localhost:8000/health
✅ Frontend running on http://localhost:5173
✅ Can upload MRI images without errors
✅ Predictions appear in browser
✅ Results panel shows confidence scores
✅ Medical analysis displays correctly
✅ Can view raw data in browser console
✅ Backend logs show prediction steps
```

---

## 🆘 Troubleshooting Quick Fixes

### "Cannot connect to http://localhost:8000"
```powershell
# Make sure backend is running in another terminal
# Verify with: http://localhost:8000/health
```

### "Cannot connect to http://localhost:5173"
```powershell
# Make sure frontend is running in another terminal
# Should see: "➜  Local:   http://localhost:5173/"
```

### "Invalid image" error on upload
- Make sure image is a brain MRI scan
- Image should be at least 150x150 pixels
- Try PNG or JPEG format
- Ensure image has clear contrast

### "Model not found" error
```powershell
# Train the model first:
python training/train_on_uploads.py

# Or copy existing model to:
# app/models/brain_tumor_model.h5
```

### Predictions showing all 25% equally
- This means model is unavailable
- Restart backend server
- Check logs for "Model loading failed"

---

## 📱 Testing with Different Images

### Test Images to Try:
1. Image with obvious tumor → Should get HIGH confidence
2. Clear normal brain scan → Should get high "No Tumor"
3. Low quality image → Should show "Invalid image" or low confidence
4. Non-brain image (chest X-ray, etc.) → Should reject

---

## 🎓 Understanding the Output

| Field | Meaning | Example |
|-------|---------|---------|
| top_prediction | Best guess | "No Tumor" |
| confidence | How certain (0-1) | 0.7234 (72.34% sure) |
| percentage | Confidence as % | 72.34% |
| status | Upload success | "success" or "invalid_image" |
| medical_analysis | Medical info | Description, risks, next steps |
| severity_level | How serious | "None", "Low", "Medium", "High" |

---

## 🔒 Keep Running

**Important**: While you're using the application:
- Keep both terminals open (backend + frontend)
- Don't close either terminal
- If you close terminal, that server stops
- To stop: Press `Ctrl+C` in the terminal

To restart after closing:
```powershell
# Terminal 1 - Backend
python -m uvicorn app.main:app --reload

# Terminal 2 - Frontend  
cd frontend && npm run dev
```

---

## 📚 Related Documentation

For more detailed info, see:
- `PREDICTION_DEBUGGING_GUIDE.md` - Deep dive debugging
- `VIEW_PREDICTIONS_QUICK_LINK.md` - Quick reference
- `PREDICTION_ISSUES_AND_FIXES.md` - Common issues

---

## 🎉 You're Done!

You can now:
1. ✅ Upload brain MRI images
2. ✅ Get AI predictions with confidence scores
3. ✅ View detailed medical analysis
4. ✅ Monitor prediction quality
5. ✅ Debug any prediction issues

**Next Steps**:
- Try uploading multiple images
- Test with different image types
- Check the medical analysis for insights
- Read comments in code to understand how predictions work

---

**Last Updated**: February 2026
**Version**: 1.0.0
