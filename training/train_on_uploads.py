"""
Brain Tumor Detection Model Training
Based on CNN architecture from Kaggle notebook
Trains on images from app/static/uploads/brain tumor folder
"""

import os
import numpy as np
import cv2
import tensorflow as tf
from sklearn.model_selection import train_test_split
from sklearn.utils import shuffle
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout
from tensorflow.keras.optimizers import Adam
from sklearn.metrics import classification_report, confusion_matrix
from pathlib import Path

# Optional matplotlib imports - skip if not available
try:
    import matplotlib.pyplot as plt
    import seaborn as sns
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False
    print("⚠️  matplotlib not available - skipping visualization plots")

# Configuration
IMAGE_SIZE = 150
DATA_PATH = r"C:\Users\vikas\OneDrive\Desktop\BN\brain-tumor-chatbot\app\static\uploads\brain tumor"
MODEL_SAVE_PATH = r"C:\Users\vikas\OneDrive\Desktop\BN\brain-tumor-chatbot\app\models\brain_tumor_model.h5"

# Supported label mappings (handles different folder naming conventions)
LABEL_MAPPINGS = {
    'glioma_tumor': 0,
    'glioma': 0,
    'meningioma_tumor': 1,
    'meningioma': 1,
    'no_tumor': 2,
    'notumor': 2,
    'pituitary_tumor': 3,
    'pituitary': 3,
}

LABELS = ['glioma_tumor', 'meningioma_tumor', 'no_tumor', 'pituitary_tumor']

print("=" * 80)
print("🧠 BRAIN TUMOR DETECTION - MODEL TRAINING")
print("=" * 80)

# Create model directory if it doesn't exist
os.makedirs(os.path.dirname(MODEL_SAVE_PATH), exist_ok=True)

# Load images from folder
print("\n📁 Loading images from uploads folder...")
X_train = []
Y_train = []

# Check if data path exists
if not os.path.exists(DATA_PATH):
    print(f"❌ Error: Data path not found: {DATA_PATH}")
    print(f"Please check that you have images in: {DATA_PATH}")
    exit(1)

# List all subdirectories
subdirs = os.listdir(DATA_PATH)
print(f"📂 Found subdirectories: {subdirs}")

# Process both Training and Testing folders
data_folders = ['Training', 'Testing']

for data_folder in data_folders:
    data_folder_path = os.path.join(DATA_PATH, data_folder)
    
    if not os.path.isdir(data_folder_path):
        print(f"   ⚠️  Skipping {data_folder} folder (not found)")
        continue
    
    print(f"\n📂 Processing {data_folder} data...")
    category_dirs = os.listdir(data_folder_path)
    
    for folder_name in category_dirs:
        category_path = os.path.join(data_folder_path, folder_name)
        
        # Skip if not a directory
        if not os.path.isdir(category_path):
            continue
        
        # Map folder name to label index
        if folder_name.lower() not in LABEL_MAPPINGS:
            print(f"      ⚠️  Skipping unknown category: {folder_name}")
            continue
        
        label_index = LABEL_MAPPINGS[folder_name.lower()]
        label_name = LABELS[label_index]
        
        print(f"   📂 {data_folder}/{folder_name} → {label_name}", end=' ')
        image_count = 0
        
        for filename in os.listdir(category_path):
            img_path = os.path.join(category_path, filename)
            
            # Skip if not a file
            if not os.path.isfile(img_path):
                continue
            
            try:
                # Read image
                img = cv2.imread(img_path)
                
                if img is None:
                    continue
                
                # Resize image
                img = cv2.resize(img, (IMAGE_SIZE, IMAGE_SIZE))
                
                # Append to training data with standardized label name
                X_train.append(img)
                Y_train.append(label_name)
                image_count += 1
                
            except Exception as e:
                continue
        
        if image_count == 0:
            print(f"❌ (0 images)")
        else:
            print(f"✅ ({image_count} images)")

# Convert to numpy arrays
X_train = np.array(X_train)
Y_train = np.array(Y_train)

print(f"\n📊 Total images loaded: {len(X_train)}")
print(f"📊 Data shape: {X_train.shape}")

if len(X_train) == 0:
    print("❌ No images found! Please upload images to the folder.")
    exit(1)

# Shuffle data
print("\n🔀 Shuffling data...")
X_train, Y_train = shuffle(X_train, Y_train, random_state=101)

# Normalize images
print("🎨 Normalizing images...")
X_train = X_train / 255.0

# Train-test split
print("📌 Splitting data into train/test sets...")
X_train, X_test, y_train, y_test = train_test_split(
    X_train, Y_train, test_size=0.1, random_state=101
)

# Convert labels to numeric indices
print("🏷️  Converting labels to categorical...")
y_train_indices = np.array([LABELS.index(label) for label in y_train])
y_test_indices = np.array([LABELS.index(label) for label in y_test])

y_train = tf.keras.utils.to_categorical(y_train_indices)
y_test = tf.keras.utils.to_categorical(y_test_indices)

print(f"   Train set: {X_train.shape}")
print(f"   Test set: {X_test.shape}")

# Build CNN Model
print("\n🏗️  Building CNN model...")
model = Sequential()
model.add(Conv2D(32, (3, 3), activation='relu', input_shape=(IMAGE_SIZE, IMAGE_SIZE, 3)))
model.add(Conv2D(64, (3, 3), activation='relu'))
model.add(MaxPooling2D(2, 2))
model.add(Dropout(0.3))

model.add(Conv2D(64, (3, 3), activation='relu'))
model.add(Conv2D(64, (3, 3), activation='relu'))
model.add(Dropout(0.3))
model.add(MaxPooling2D(2, 2))
model.add(Dropout(0.3))

model.add(Conv2D(128, (3, 3), activation='relu'))
model.add(Conv2D(128, (3, 3), activation='relu'))
model.add(Conv2D(128, (3, 3), activation='relu'))
model.add(MaxPooling2D(2, 2))
model.add(Dropout(0.3))

model.add(Conv2D(128, (3, 3), activation='relu'))
model.add(Conv2D(256, (3, 3), activation='relu'))
model.add(MaxPooling2D(2, 2))
model.add(Dropout(0.3))

model.add(Flatten())
model.add(Dense(512, activation='relu'))
model.add(Dense(512, activation='relu'))
model.add(Dropout(0.3))
model.add(Dense(4, activation='softmax'))

# Compile model
print("⚙️  Compiling model...")
model.compile(
    loss='categorical_crossentropy',
    optimizer=Adam(),
    metrics=['accuracy']
)

# Print model summary
print("\n📋 Model Summary:")
model.summary()

# Train model
print("\n🚀 Training model...")
print("=" * 80)
history = model.fit(
    X_train, y_train,
    epochs=10,
    validation_split=0.1,
    batch_size=32,
    verbose=1
)

# Evaluate on test set
print("\n" + "=" * 80)
print("📊 Evaluating on test set...")
test_loss, test_accuracy = model.evaluate(X_test, y_test, verbose=0)

print(f"\n✅ Final Training Accuracy: {history.history['accuracy'][-1] * 100:.2f}%")
print(f"✅ Final Training Loss: {history.history['loss'][-1]:.4f}")
print(f"✅ Test Accuracy: {test_accuracy * 100:.2f}%")
print(f"✅ Test Loss: {test_loss:.4f}")

# Make predictions
print("\n🔮 Making predictions on test set...")
y_pred = model.predict(X_test, verbose=0)
y_pred_classes = np.argmax(y_pred, axis=1)
y_true = np.argmax(y_test, axis=1)

# Classification report
print("\n📋 Classification Report:")
print(classification_report(y_true, y_pred_classes, target_names=LABELS))

# Confusion Matrix
print("\n📊 Generating confusion matrix...")
cm = confusion_matrix(y_true, y_pred_classes)

if MATPLOTLIB_AVAILABLE:
    plt.figure(figsize=(10, 8))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
                xticklabels=LABELS, yticklabels=LABELS,
                cbar_kws={'label': 'Count'})
    plt.xlabel('Predicted Label')
    plt.ylabel('True Label')
    plt.title('Confusion Matrix - Brain Tumor Classification')
    plt.tight_layout()
    plt.savefig('confusion_matrix.png', dpi=100, bbox_inches='tight')
    print("💾 Confusion matrix saved as 'confusion_matrix.png'")
    plt.close()
else:
    print("📊 Confusion Matrix (text format):")
    print(cm)

# Plot training history
print("\n📈 Generating training history plots...")

if MATPLOTLIB_AVAILABLE:
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    # Accuracy
    axes[0].plot(history.history['accuracy'], 'r-', label='Training Accuracy', linewidth=2)
    axes[0].plot(history.history['val_accuracy'], 'b-', label='Validation Accuracy', linewidth=2)
    axes[0].set_title('Model Accuracy', fontsize=14, fontweight='bold')
    axes[0].set_xlabel('Epoch')
    axes[0].set_ylabel('Accuracy')
    axes[0].legend(loc='lower right')
    axes[0].grid(True, alpha=0.3)

    # Loss
    axes[1].plot(history.history['loss'], 'r-', label='Training Loss', linewidth=2)
    axes[1].plot(history.history['val_loss'], 'b-', label='Validation Loss', linewidth=2)
    axes[1].set_title('Model Loss', fontsize=14, fontweight='bold')
    axes[1].set_xlabel('Epoch')
    axes[1].set_ylabel('Loss')
    axes[1].legend(loc='upper right')
    axes[1].grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('training_history.png', dpi=100, bbox_inches='tight')
    print("💾 Training history saved as 'training_history.png'")
    plt.close()
else:
    print("⚠️  Skipping plot generation (matplotlib not available)")

# Save model
print(f"\n💾 Saving model to: {MODEL_SAVE_PATH}")
model.save(MODEL_SAVE_PATH)
print(f"✅ Model saved successfully!")

print("\n" + "=" * 80)
print("✨ TRAINING COMPLETE!")
print("=" * 80)
print(f"\n📁 Model location: {MODEL_SAVE_PATH}")
print(f"📚 Classes: {', '.join(LABELS)}")
print(f"\n🚀 To use the model:")
print(f"   1. Start backend: python -m uvicorn app.main:app --reload")
print(f"   2. Start frontend: cd frontend && npm run dev")
print(f"   3. Upload brain MRI images at http://localhost:5174")
print("=" * 80)
