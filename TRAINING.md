# 🧠 Brain Tumor Detection - Training Guide

## Overview

This project uses a **Convolutional Neural Network (CNN)** trained on brain MRI images to classify tumors into 4 categories:
- **Glioma Tumor** (Index 0)
- **Meningioma Tumor** (Index 1)
- **No Tumor** (Index 2)
- **Pituitary Tumor** (Index 3)

The training script automatically loads images from your uploaded folder and trains the model.

---

## 📁 Folder Structure

Your images should be organized in the following structure:

```
app/static/uploads/brain tumor/
├── glioma_tumor/
│   ├── image1.jpg
│   ├── image2.jpg
│   └── ...
├── meningioma_tumor/
│   ├── image1.jpg
│   ├── image2.jpg
│   └── ...
├── no_tumor/
│   ├── image1.jpg
│   ├── image2.jpg
│   └── ...
└── pituitary_tumor/
    ├── image1.jpg
    ├── image2.jpg
    └── ...
```

**Important**: The folder names MUST match exactly as shown above.

---

## 🚀 Quick Start

### Step 1: Prepare Images

Organize your brain MRI images into the folder structure above with the exact folder names.

### Step 2: Train the Model

Run the training script from the project root directory:

```bash
python training/train_on_uploads.py
```

This will:
- ✅ Load all images from the upload folder
- ✅ Resize images to 150×150 pixels
- ✅ Normalize pixel values to [0, 1]
- ✅ Split data: 90% training, 10% testing
- ✅ Train CNN for 10 epochs
- ✅ Generate training history plots
- ✅ Create confusion matrix
- ✅ Save trained model to `app/models/brain_tumor_model.h5`

### Step 3: Run the Application

After training completes, start the backend:

```bash
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

In another terminal, start the frontend:

```bash
cd frontend
npm run dev
```

Access the application at: **http://localhost:5174**

---

## 🏗️ Model Architecture

The CNN model consists of:

```
Input (150×150×3)
    ↓
Conv2D (32 filters) → Conv2D (64 filters) → MaxPooling → Dropout(0.3)
    ↓
Conv2D (64) → Conv2D (64) → Dropout(0.3) → MaxPooling → Dropout(0.3)
    ↓
Conv2D (128) → Conv2D (128) → Conv2D (128) → MaxPooling → Dropout(0.3)
    ↓
Conv2D (128) → Conv2D (256) → MaxPooling → Dropout(0.3)
    ↓
Flatten
    ↓
Dense (512, ReLU) → Dense (512, ReLU) → Dropout(0.3)
    ↓
Dense (4, Softmax) - Output (4 classes)
```

**Training Details:**
- **Loss Function**: Categorical Crossentropy
- **Optimizer**: Adam
- **Epochs**: 10
- **Batch Size**: 32
- **Image Size**: 150×150 (RGB)
- **Classes**: 4

---

## 📊 Training Output

After training completes, you'll see:

### Console Output
```
✅ Final Training Accuracy: 95.50%
✅ Final Training Loss: 0.1234
✅ Test Accuracy: 92.80%
✅ Test Loss: 0.3456

📋 Classification Report:
              precision    recall  f1-score   support
  glioma_tumor       0.95      0.94      0.94       120
meningioma_tumor     0.92      0.93      0.93       100
      no_tumor       0.98      0.98      0.98        80
 pituitary_tumor     0.91      0.92      0.91        90
```

### Generated Files
- **confusion_matrix.png** - Visual representation of model predictions vs actual
- **training_history.png** - Accuracy and loss curves over epochs
- **app/models/brain_tumor_model.h5** - Trained model file

---

## ✅ Model Validation

The application includes validation to:

1. **Detect Non-Brain Images**: Checks if uploaded image is actually a brain MRI
2. **Provide Confidence Scores**: Shows probability for each class
3. **Handle Invalid Images**: Rejects corrupted or non-image files

---

## 🔧 Troubleshooting

### Issue: "No images found" error

**Solution**: Ensure folder names are exactly:
- `glioma_tumor`
- `meningioma_tumor`
- `no_tumor`
- `pituitary_tumor`

(Case-sensitive on Linux/Mac, but always use lowercase)

### Issue: Low training accuracy

**Possible causes**:
- Too few images (need minimum 50+ per class)
- Poor image quality
- Images are not brain MRIs

**Solution**: 
- Increase training data
- Ensure images are clear brain scans
- Remove corrupted images

### Issue: Model file not found

**Solution**: Run training script first to generate `brain_tumor_model.h5`

---

## 📈 Tips for Better Results

1. **More Data**: Train with 200+ images per class for better accuracy
2. **Data Variety**: Include images from different brain scan angles/orientations
3. **Image Quality**: Use clear, properly labeled medical images
4. **Regular Updates**: Retrain model as you gather more labeled data
5. **Validation**: Always test with labeled images to verify accuracy

---

## 🎯 Expected Accuracy

With a good quality dataset of brain MRI images:
- **Training Accuracy**: 90-98%
- **Test Accuracy**: 85-95%
- **Per-class Performance**: Varies by tumor type and data quality

---

## 📝 Notes

- Images are automatically normalized to [0, 1] range
- Model uses data augmentation via random train-test split
- 10% of data reserved for testing
- Adam optimizer with default learning rate
- Early stopping not implemented (you can add if needed)

---

## 🚀 Next Steps

1. Upload your brain MRI images to the correct folder structure
2. Run `python training/train_on_uploads.py`
3. Wait for training to complete
4. Start the application
5. Upload new brain images to get predictions

**Enjoy accurate brain tumor detection!** 🧠✨
