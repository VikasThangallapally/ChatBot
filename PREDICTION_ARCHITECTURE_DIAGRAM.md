# 🧠 Brain MRI Prediction System - Architecture & Data Flow

## System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        USER BROWSER                              │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │        Frontend Web Application (React + Vite)           │  │
│  │  http://localhost:5173                                   │  │
│  │                                                          │  │
│  │  ┌─────────────────────────────────────────────────┐   │  │
│  │  │ Header: Brain Tumor AI Assistant               │   │  │
│  │  │ ┌──────────────────┐  ┌──────────────────────┐ │   │  │
│  │  │ │ Upload Card      │  │ 3D Brain Animation   │ │   │  │
│  │  │ │ • Drag & Drop    │  │ (or MRI Preview)     │ │   │  │
│  │  │ │ • Click Upload   │  │                      │ │   │  │
│  │  │ │ • Progress Bar   │  │                      │ │   │  │
│  │  │ └──────────────────┘  └──────────────────────┘ │   │  │
│  │  │                                                 │   │  │
│  │  │ ┌────────────────────────────────────────────┐ │   │  │
│  │  │ │ Results Panel (After Prediction)          │ │   │  │
│  │  │ │ • Top Prediction (Glioma/Meningioma/...)  │ │   │  │
│  │  │ │ • Confidence Percentage (0-100%)          │ │   │  │
│  │  │ │ • Circular Progress Indicator             │ │   │  │
│  │  │ │ • Confidence Breakdown (all 4 classes)    │ │   │  │
│  │  │ │ • Medical Analysis & Severity Level        │ │   │  │
│  │  │ └────────────────────────────────────────────┘ │   │  │
│  │  └─────────────────────────────────────────────────┘   │  │
│  └──────────────────────────────────────────────────────────┘  │
└─────────────┬──────────────────────────────────────────────────┘
              │
              │ HTTP POST /api/predict
              │ (FormData with image file)
              │
              ▼
┌─────────────────────────────────────────────────────────────────┐
│                   BACKEND API SERVER                             │
│  Python FastAPI  http://localhost:8000                           │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ main.py - FastAPI Application                           │  │
│  │ ┌────────────────────────────────────────────────────┐  │  │
│  │ │ POST /api/predict                                  │  │  │
│  │ │                                                    │  │  │
│  │ │ 1. Receive uploaded MRI image file                │  │  │
│  │ │    └─ File saved to: app/static/uploads/         │  │  │
│  │ │                                                    │  │  │
│  │ │ 2. Image Validation (is_valid_mri)               │  │  │
│  │ │    ├─ Check minimum size (150x150)               │  │  │
│  │ │    ├─ Check aspect ratio                         │  │  │
│  │ │    ├─ Check pixel brightness                     │  │  │
│  │ │    ├─ Check image contrast                       │  │  │
│  │ │    └─ Returns: is_valid=True/False              │  │  │
│  │ │                                                    │  │  │
│  │ │ 3. Call InferenceService.predict_image()         │  │  │
│  │ │    module: app/services/inference.py             │  │  │
│  │ └────────────────────────────────────────────────────┘  │  │
│  │                                                          │  │
│  │ ┌────────────────────────────────────────────────────┐  │  │
│  │ │ InferenceService.predict_image()                  │  │  │
│  │ │                                                    │  │  │
│  │ │ 1. Load image from file                          │  │  │
│  │ │    └─ PIL.Image                                  │  │  │
│  │ │                                                    │  │  │
│  │ │ 2. Preprocess Image (ImageProcessor)             │  │  │
│  │ │    ├─ Convert to RGB                             │  │  │
│  │ │    ├─ Resize to 150x150 pixels                   │  │  │
│  │ │    ├─ Normalize to [0, 1]                        │  │  │
│  │ │    └─ Output shape: (1, 150, 150, 3)            │  │  │
│  │ │                                                    │  │  │
│  │ │ 3. Load Trained Model                            │  │  │
│  │ │    └─ TensorFlow/Keras CNN model                 │  │  │
│  │ │       app/models/brain_tumor_model.h5            │  │  │
│  │ │                                                    │  │  │
│  │ │ 4. Run Prediction                                │  │  │
│  │ │    ├─ model.predict(preprocessed_image)         │  │  │
│  │ │    ├─ Output: [prob_glioma, prob_meningioma,   │  │  │
│  │ │    │            prob_no_tumor, prob_pituitary]  │  │  │
│  │ │    └─ Sum = 1.0 (softmax probabilities)         │  │  │
│  │ │                                                    │  │  │
│  │ │ 5. Get Medical Analysis                          │  │  │
│  │ │    ├─ Determine top prediction class            │  │  │
│  │ │    ├─ Fetch from MEDICAL_ANALYSIS_DB            │  │  │
│  │ │    └─ Return: {description, advantages,         │  │  │
│  │ │       disadvantages, recommendations, severity}  │  │  │
│  │ │                                                    │  │  │
│  │ │ 6. Format Response                               │  │  │
│  │ │    └─ Return PredictionResponse JSON             │  │  │
│  │ └────────────────────────────────────────────────────┘  │  │
│  │                                                          │  │
│  └──────────────────────────────────────────────────────────┘  │
└─────────────┬──────────────────────────────────────────────────┘
              │
              │ HTTP Response (JSON)
              │ {
              │   "predictions": [...],
              │   "top_prediction": {...},
              │   "medical_analysis": {...},
              │   "status": "success"
              │ }
              │
              ▼
┌─────────────────────────────────────────────────────────────────┐
│                    BROWSER (Frontend)                            │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ Parse JSON Response                                      │  │
│  │ ├─ Extract top_prediction                               │  │
│  │ ├─ Extract predictions array                            │  │
│  │ ├─ Extract medical_analysis                             │  │
│  │ └─ Update component state                               │  │
│  │                                                          │  │
│  │ Display Results:                                         │  │
│  │ ├─ ResultPanel: Shows predictions & confidence         │  │
│  │ └─ MedicalAnalysis: Shows medical details              │  │
│  │                                                          │  │
│  │ User sees beautiful formatted results! 🎉               │  │
│  └──────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
```

---

## Data Flow Sequence

```
Timeline of Process
═══════════════════════════════════════════════════════════════════

[User] 
  │
  ├─ Selects brain MRI image file
  │  └─ File: brain_mri_001.jpg (1.2 MB)
  │
  └─ Drags to upload area or clicks
     │
     ▼
[Frontend: UploadCard.jsx]
  │
  ├─ Create FormData with file
  │  └─ form.append('file', file)
  │
  ├─ POST to http://localhost:8000/api/predict
  │  └─ Header: Content-Type: multipart/form-data
  │
  ├─ Show upload progress (0% → 100%)
  │  └─ Passes through: onUploadProgress event
  │
  └─ Wait for response...
     │ (Takes 1-3 seconds typically)
     │
     ▼
[Backend: app/api/routes/predict.py]
  │
  ├─ Receive file upload
  │  └─ file: UploadFile = File(...)
  │
  ├─ Validate file
  │  ├─ Check: filename exists
  │  ├─ Check: content_type contains 'image'
  │  └─ Check: file_size < MAX_UPLOAD_SIZE (10 MB)
  │
  ├─ Save file to disk
  │  └─ app/static/uploads/brain_mri_001.jpg
  │
  ├─ Load image from bytes
  │  └─ PIL.Image.open(BytesIO(file_contents))
  │
  ├─ Validate MRI (is_valid_mri)
  │  ├─ Check: image dimensions >= 150x150
  │  ├─ Check: aspect ratio 0.6-1.67
  │  ├─ Check: image mode valid (L, RGB, RGBA, 1)
  │  ├─ Check: brightness (mean intensity 3-252)
  │  ├─ Check: contrast (std_dev > 5)
  │  └─ If invalid → Return error response immediately
  │
  ├─ Call InferenceService.predict_image()
  │  │
  │  ▼ [app/services/inference.py]
  │  │
  │  ├─ Load image from file path
  │  │  └─ ImageProcessor.load_image(file_path)
  │  │
  │  ├─ Validate brain image (again)
  │  │  └─ InferenceService.validate_brain_image()
  │  │
  │  ├─ Preprocess image
  │  │  ├─ Convert to RGB
  │  │  ├─ Resize to 150x150 pixels
  │  │  ├─ Normalize to [0, 1]
  │  │  └─ Add batch dim: (150,150,3) → (1,150,150,3)
  │  │
  │  ├─ Load TensorFlow model
  │  │  ├─ ModelLoader.get_model()
  │  │  └─ Load from: app/models/brain_tumor_model.h5
  │  │
  │  ├─ Run prediction
  │  │  ├─ model.predict(preprocessed_image, verbose=0)
  │  │  └─ Output: [[p0, p1, p2, p3]] where sum=1.0
  │  │     p0 = Glioma probability
  │  │     p1 = Meningioma probability
  │  │     p2 = No Tumor probability
  │  │     p3 = Pituitary probability
  │  │
  │  ├─ Sort predictions by confidence (desc)
  │  │  └─ [1] Highest confidence first
  │  │     [2] Second highest
  │  │     [3] Third
  │  │     [4] Lowest
  │  │
  │  ├─ Get top prediction
  │  │  └─ predictions[0] = highest confidence
  │  │
  │  ├─ Get medical analysis
  │  │  ├─ Look up tumor type in MEDICAL_ANALYSIS_DB
  │  │  └─ Get: description, advantages, disadvantages,
  │  │     key_characteristics, recommended_next_steps,
  │  │     severity_level
  │  │
  │  └─ Return complete prediction response
  │     │
  │     ▼ [Response JSON Structure]
  │     └─ {
  │         "status": "success",
  │         "is_valid_brain_image": true,
  │         "top_prediction": {
  │           "class_index": 2,
  │           "label": "No Tumor",
  │           "confidence": 0.7234,
  │           "percentage": 72.34
  │         },
  │         "predictions": [
  │           {"label": "No Tumor", "confidence": 0.7234, ...},
  │           {"label": "Glioma", "confidence": 0.1523, ...},
  │           {"label": "Pituitary", "confidence": 0.0891, ...},
  │           {"label": "Meningioma", "confidence": 0.0352, ...}
  │         ],
  │         "medical_analysis": {
  │           "tumor_type": "No Tumor",
  │           "description": "...",
  │           "severity_level": "None",
  │           "advantages": [...],
  │           "disadvantages": [...],
  │           "key_characteristics": [...],
  │           "recommended_next_steps": [...]
  │         },
  │         "image_path": "app/static/uploads/brain_mri_001.jpg",
  │         "model_name": "brain_tumor_model.h5"
  │       }
  │
  └─ Send HTTP response (JSON)
     │ Status 200 OK
     │
     ▼
[Frontend: UploadCard.jsx gets response]
  │
  ├─ Stop progress indicator
  ├─ Parse response JSON
  │  └─ res.data = prediction response
  │
  ├─ Emit custom event
  │  ├─ Event: 'predictionUpdated'
  │  └─ Detail: res.data (full response)
  │
  ├─ Store globally
  │  ├─ window.latestPrediction = res.data
  │  └─ window.latestUploadedImage = previewUrl
  │
  └─ Components listen to event
     │
     ▼
[App.jsx listens to event]
  │
  ├─ Receives 'predictionUpdated' event
  ├─ Updates state:
  │  └─ setPredictionResult(event.detail)
  │
  └─ Re-renders with new prediction
     │
     ▼
[ResultPanel.jsx - Shows Predictions]
  │
  ├─ Shows result.top_prediction
  │  ├─ Displays label/name
  │  ├─ Shows confidence as %
  │  └─ Renders circular progress indicator
  │
  ├─ Shows confidence breakdown
  │  └─ Bar chart for all 4 classes
  │
  └─ Shows severity level with color
     │ 🟢 None (Green)
     │ 🔵 Low (Blue)
     │ 🟡 Medium (Yellow)
     │ 🔴 High (Red)
     │
     ▼
[MedicalAnalysis.jsx - Shows Medical Info]
  │
  ├─ Shows result.medical_analysis
  │  ├─ Description of tumor type
  │  ├─ Key characteristics
  │  ├─ Advantages (positive aspects)
  │  ├─ Disadvantages (risks)
  │  ├─ Recommended next steps
  │  └─ Specialist recommendations
  │
  └─ User sees complete analysis!
     │
     ▼
[User sees beautiful formatted results]
  │
  ├─ 🧠 Prediction: "No Tumor"
  ├─ 📊 Confidence: 72.34%
  ├─ 🟢 Severity: None
  ├─ 📈 Breakdown chart
  └─ 📋 Medical analysis

═══════════════════════════════════════════════════════════════════
Total Time: 1-3 seconds
═══════════════════════════════════════════════════════════════════
```

---

## File & Component Interaction Map

```
Frontend Components
═════════════════════════════════════════════════════════════════

React App
  │
  ├─ App.jsx (Main component)
  │  │
  │  ├─ Listens to: predictionUpdated event
  │  ├─ Stores: predictionResult (state)
  │  ├─ Renders: UploadCard, ResultPanel, MedicalAnalysis
  │  └─ Emits: Custom events
  │
  │
  ├─ UploadCard.jsx
  │  ├─ Shows: File upload UI
  │  ├─ Calls: POST /api/predict
  │  ├─ Uses: axios library
  │  ├─ Emits: predictionUpdated event
  │  └─ Stores: window.latestPrediction
  │
  │
  ├─ ResultPanel.jsx
  │  ├─ Receives: predictionResult prop
  │  ├─ Shows: Top prediction
  │  ├─ Displays: Confidence percentage
  │  ├─ Renders: Confidence breakdown chart
  │  ├─ Shows: Severity level
  │  └─ Status: success/error/invalid_image
  │
  │
  ├─ MedicalAnalysis.jsx
  │  ├─ Receives: predictionResult prop
  │  ├─ Shows: Medical description
  │  ├─ Lists: Characteristics, symptoms
  │  ├─ Shows: Advantages/disadvantages
  │  └─ Displays: Recommendations
  │
  │
  └─ config/api.js
     └─ Exports: API_BASE_URL (http://localhost:8000)


Backend Components
═════════════════════════════════════════════════════════════════

FastAPI App
  │
  ├─ main.py (Entry point)
  │  ├─ Initializes: FastAPI app
  │  ├─ Adds: CORS middleware
  │  ├─ Includes: predict router
  │  ├─ Includes: chat router
  │  └─ Health checks: /health, /
  │
  │
  ├─ api/routes/predict.py
  │  └─ Endpoint: POST /api/predict
  │     ├─ Receives: File upload
  │     ├─ Calls: is_valid_mri() for validation
  │     ├─ Calls: InferenceService.predict_image()
  │     └─ Returns: PredictionResponse JSON
  │
  │
  ├─ services/inference.py
  │  └─ InferenceService class
  │     ├─ Methods:
  │     │  ├─ predict_image(image_path)
  │     │  ├─ validate_brain_image(image)
  │     │  ├─ get_medical_analysis(class_idx, conf)
  │     │  └─ batch_predict(image_paths)
  │     │
  │     └─ Uses:
  │        ├─ ImageProcessor (preprocessing)
  │        ├─ ModelLoader (load model)
  │        └─ MEDICAL_ANALYSIS_DB (medical info)
  │
  │
  ├─ core/model_loader.py
  │  └─ ModelLoader class
  │     ├─ Loads: TensorFlow/Keras model
  │     ├─ From: app/models/brain_tumor_model.h5
  │     └─ Caches: Model in memory
  │
  │
  ├─ core/image_utils.py
  │  └─ ImageProcessor class
  │     ├─ Methods:
  │     │  ├─ load_image(file_path)
  │     │  ├─ preprocess_image(image)
  │     │  ├─ get_image_info(image)
  │     │  └─ get_class_name(class_index)
  │     │
  │     └─ Features:
  │        ├─ Resize to 150x150
  │        ├─ Normalize to [0,1]
  │        ├─ Convert to RGB
  │        └─ Add batch dimension
  │
  │
  ├─ core/mri_validator.py
  │  └─ is_valid_mri(image)
  │     ├─ Checks: Size, format, contrast
  │     └─ Returns: (is_valid, reason)
  │
  │
  ├─ models/
  │  └─ brain_tumor_model.h5
  │     ├─ Type: CNN (Convolutional Neural Network)
  │     ├─ Input: 150x150x3 image
  │     ├─ Output: [p_glioma, p_meningioma, p_no_tumor, p_pituitary]
  │     └─ Uses: Softmax (probabilities sum to 1)
  │
  │
  ├─ schemas/prediction.py
  │  └─ PredictionResponse (Pydantic model)
  │     ├─ status: "success" | "error" | "invalid_image"
  │     ├─ predictions: List[Dict]
  │     ├─ top_prediction: Dict
  │     ├─ medical_analysis: Dict
  │     └─ image_path: str
  │
  │
  └─ config.py
     └─ Settings class
        ├─ IMAGE_SIZE: 150
        ├─ MAX_UPLOAD_SIZE: 10 MB
        ├─ UPLOAD_DIR: app/static/uploads/
        └─ MODEL_NAME: brain_tumor_model.h5


File System Storage
═════════════════════════════════════════════════════════════════

app/
├─ models/
│  └─ brain_tumor_model.h5  (Trained CNN model)
│
└─ static/
   └─ uploads/
      ├─ brain_mri_001.jpg  (Your uploaded images)
      ├─ brain_mri_002.jpg
      └─ brain_mri_003.jpg
```

---

## Prediction Confidence Levels

```
Confidence Scale
═════════════════════════════════════════════════════════════════

100% ┌─────────────────────────────────────────────┐
     │  ████████████████ VERY HIGH CONFIDENCE      │
     │  Model almost certain. Prediction reliable. │
 95% │                                             │
     │  ████████████████ HIGH CONFIDENCE           │
 85% │  Model very confident. Usually accurate.   │
     │                                             │
 75% ├─────────────────────────────────────────────┤ ← Good threshold
     │  ████████████░░░░ GOOD CONFIDENCE          │
 65% │  Model is confident. Prediction reasonable. │
     │                                             │
 55% ├─────────────────────────────────────────────┤ ← Fair threshold
     │  ████████░░░░░░░░ FAIR CONFIDENCE          │
 45% │  Model has some doubt. Verify recommended. │
     │                                             │
 35% ├─────────────────────────────────────────────┤ ← Low threshold
     │  ████░░░░░░░░░░░░ LOW CONFIDENCE           │
 25% │  Model is uncertain. Seek specialist.      │
     │                                             │
 15% ├─────────────────────────────────────────────┤
     │  ██░░░░░░░░░░░░░░ VERY LOW CONFIDENCE      │
     │  Model is guessing. Don't rely on result.  │
  0% └─────────────────────────────────────────────┘

Recommendation by Confidence:
  > 75%  → Likely accurate, general guidance ok
  50-75% → Reasonably confident, consider specialist
  < 50%  → Model uncertain, definitely seek specialist
```

---

## JSON Response Structure

```json
{
  "status": "success",
  "is_valid_brain_image": true,
  "image_validation_confidence": 0.92,
  "validation_reason": "✅ Image suitable for analysis",
  "image_path": "app/static/uploads/brain_mri_001.jpg",
  "model_name": "brain_tumor_model.h5",
  
  "top_prediction": {
    "class_index": 2,
    "label": "No Tumor",
    "confidence": 0.7234,
    "percentage": 72.34
  },
  
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
  
  "medical_analysis": {
    "tumor_type": "No Tumor",
    "description": "No brain tumor detected. The MRI scan appears normal...",
    "severity_level": "None",
    
    "advantages": [
      "Indicates healthy brain tissue",
      "No immediate neurological threat",
      "No need for urgent neurosurgical intervention",
      "Allows continued normal lifestyle",
      "Peace of mind regarding brain health"
    ],
    
    "disadvantages": [
      "If symptoms persist, requires investigation of other causes",
      "Small lesions may not be detected on standard imaging",
      "Does not rule out other neurological conditions"
    ],
    
    "key_characteristics": [
      "Normal brain parenchyma without masses",
      "Intact ventricles without dilatation",
      "No midline shift or mass effect",
      "Normal gray-white matter differentiation",
      "No abnormal enhancement with contrast"
    ],
    
    "recommended_next_steps": [
      "No urgent intervention needed for brain pathology",
      "If symptoms persist, consult neurologist",
      "Consider follow-up imaging only if new symptoms",
      "Maintain regular health checkups",
      "Address any other medical concerns with PCP"
    ]
  }
}
```

---

**Last Updated**: February 2026
