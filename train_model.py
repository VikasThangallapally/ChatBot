"""
Train Brain Tumor Detection Model using Testing folder images.
This script trains a CNN model on the 4 tumor classes and saves it for deployment.
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
from tensorflow.keras.callbacks import EarlyStopping
from pathlib import Path

# Configuration
IMAGE_SIZE = 150
BASE_PATH = r"app\static\Brain Folders\Testing"
MODEL_SAVE_PATH = r"app\models\brain_tumor_model.h5"

# Class labels (must match the folder names)
CLASS_LABELS = {
    'glioma_tumor': 0,
    'meningioma_tumor': 1,
    'no_tumor': 2,
    'pituitary_tumor': 3
}

CLASS_NAMES = ['Glioma Tumor', 'Meningioma Tumor', 'No Tumor', 'Pituitary Tumor']

print("=" * 80)
print("🧠 BRAIN TUMOR DETECTION - MODEL TRAINING")
print("=" * 80)
print(f"📁 Data folder: {BASE_PATH}")
print(f"💾 Model will be saved to: {MODEL_SAVE_PATH}")
print("=" * 80)

# Create model directory
os.makedirs(os.path.dirname(MODEL_SAVE_PATH), exist_ok=True)

# Load images from Testing folder
print("\n📁 Loading images from Testing folder...")
X_train = []
Y_train = []

# Check if data path exists
if not os.path.exists(BASE_PATH):
    print(f"❌ Error: Data path not found: {BASE_PATH}")
    exit(1)

# Load images from each class folder
for folder_name, class_index in CLASS_LABELS.items():
    class_path = os.path.join(BASE_PATH, folder_name)
    
    if not os.path.isdir(class_path):
        print(f"⚠️  Folder not found: {class_path}")
        continue
    
    print(f"\n📂 {CLASS_NAMES[class_index]} ({folder_name})", end=' ')
    image_count = 0
    
    for filename in os.listdir(class_path):
        img_path = os.path.join(class_path, filename)
        
        # Skip if not a file
        if not os.path.isfile(img_path):
            continue
        
        try:
            # Read image
            img = cv2.imread(img_path)
            
            if img is None:
                continue
            
            # Resize to standard size
            img = cv2.resize(img, (IMAGE_SIZE, IMAGE_SIZE))
            
            # Append to training data
            X_train.append(img)
            Y_train.append(class_index)
            image_count += 1
            
        except Exception as e:
            print(f"⚠️  Error loading {filename}: {str(e)}")
            continue
    
    if image_count > 0:
        print(f"✅ Loaded {image_count} images")
    else:
        print(f"❌ No images found")

# Convert to numpy arrays
X_train = np.array(X_train)
Y_train = np.array(Y_train)

print(f"\n📊 Total images loaded: {len(X_train)}")

if len(X_train) == 0:
    print("❌ No images found! Please check the Testing folder.")
    exit(1)

print(f"📊 Data shape: {X_train.shape}")

# Shuffle data
print("\n🔀 Shuffling data...")
X_train, Y_train = shuffle(X_train, Y_train, random_state=42)

# Normalize images (convert to float and scale to [0, 1])
print("🎨 Normalizing images...")
X_train = X_train.astype(np.float32) / 255.0

# Train-test split (80/20)
print("📌 Splitting data: 80% train, 20% test...")
X_train_set, X_test_set, y_train_set, y_test_set = train_test_split(
    X_train, Y_train, test_size=0.2, stratify=Y_train, random_state=42
)

# Convert labels to categorical
print("🏷️  Converting labels to categorical...")
y_train_categorical = tf.keras.utils.to_categorical(y_train_set, num_classes=4)
y_test_categorical = tf.keras.utils.to_categorical(y_test_set, num_classes=4)

print(f"   Train set: {X_train_set.shape} - {len(y_train_set)} samples")
print(f"   Test set: {X_test_set.shape} - {len(y_test_set)} samples")

# Build CNN Model
print("\n🏗️  Building CNN model...")
model = Sequential([
    # Block 1
    Conv2D(32, (3, 3), activation='relu', padding='same', input_shape=(IMAGE_SIZE, IMAGE_SIZE, 3)),
    Conv2D(32, (3, 3), activation='relu', padding='same'),
    MaxPooling2D((2, 2)),
    Dropout(0.25),
    
    # Block 2
    Conv2D(64, (3, 3), activation='relu', padding='same'),
    Conv2D(64, (3, 3), activation='relu', padding='same'),
    MaxPooling2D((2, 2)),
    Dropout(0.25),
    
    # Block 3
    Conv2D(128, (3, 3), activation='relu', padding='same'),
    Conv2D(128, (3, 3), activation='relu', padding='same'),
    MaxPooling2D((2, 2)),
    Dropout(0.25),
    
    # Block 4
    Conv2D(256, (3, 3), activation='relu', padding='same'),
    Conv2D(256, (3, 3), activation='relu', padding='same'),
    MaxPooling2D((2, 2)),
    Dropout(0.25),
    
    # Fully connected layers
    Flatten(),
    Dense(512, activation='relu'),
    Dropout(0.5),
    Dense(512, activation='relu'),
    Dropout(0.5),
    Dense(4, activation='softmax')  # 4 classes
])

# Compile model
print("⚙️  Compiling model...")
model.compile(
    loss='categorical_crossentropy',
    optimizer=Adam(learning_rate=0.001),
    metrics=['accuracy']
)

# Print model summary
print("\n📋 Model Summary:")
model.summary()

# Train model
print("\n🚀 Training model...")
early_stop = EarlyStopping(
    monitor='val_loss',
    patience=5,
    restore_best_weights=True,
    verbose=1
)

history = model.fit(
    X_train_set, y_train_categorical,
    validation_data=(X_test_set, y_test_categorical),
    epochs=30,
    batch_size=32,
    callbacks=[early_stop],
    verbose=1
)

# Evaluate model
print("\n📊 Evaluating model...")
test_loss, test_accuracy = model.evaluate(X_test_set, y_test_categorical, verbose=0)
print(f"   Test Loss: {test_loss:.4f}")
print(f"   Test Accuracy: {test_accuracy:.4f} ({test_accuracy*100:.2f}%)")

# Save model
print(f"\n💾 Saving model to {MODEL_SAVE_PATH}...")
model.save(MODEL_SAVE_PATH)
print("✅ Model saved successfully!")

# Print class predictions
print("\n🔍 Making predictions on test set...")
predictions = model.predict(X_test_set, verbose=0)
predicted_classes = np.argmax(predictions, axis=1)

# Show sample predictions
print("\n📈 Sample predictions:")
for i in range(min(10, len(predicted_classes))):
    true_class = CLASS_NAMES[y_test_set[i]]
    pred_class = CLASS_NAMES[predicted_classes[i]]
    confidence = predictions[i][predicted_classes[i]]
    status = "✅" if y_test_set[i] == predicted_classes[i] else "❌"
    print(f"   {status} True: {true_class:20s} | Predicted: {pred_class:20s} ({confidence:.2%})")

print("\n" + "=" * 80)
print("🎉 Training Complete!")
print(f"📁 Model location: {MODEL_SAVE_PATH}")
print("You can now run predictions on the web interface!")
print("=" * 80)
