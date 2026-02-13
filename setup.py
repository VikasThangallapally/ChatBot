#!/usr/bin/env python
"""
Quick setup script to verify dataset structure and install dependencies.
Run this before training the model.
"""

import os
import sys
from pathlib import Path
import subprocess

def check_dataset_structure():
    """Check if brain_tumor dataset has correct folder structure."""
    print("\n" + "="*70)
    print("CHECKING BRAIN TUMOR DATASET STRUCTURE")
    print("="*70)
    
    root = Path(__file__).parent.parent / "brain_tumor"
    required_folders = {
        "Training": ["Glioma", "Meningioma", "Pituitary", "NoTumor"],
        "Testing": ["Glioma", "Meningioma", "Pituitary", "NoTumor"]
    }
    
    all_good = True
    
    for split, classes in required_folders.items():
        split_path = root / split
        print(f"\n{split} Dataset:")
        print(f"  Path: {split_path}")
        
        if not split_path.exists():
            print(f"  ❌ MISSING - Please create this folder")
            all_good = False
            continue
        
        print(f"  ✓ Found")
        
        for class_name in classes:
            class_path = split_path / class_name
            if class_path.exists():
                count = len(list(class_path.glob("*.jpg"))) + len(list(class_path.glob("*.png")))
                if count > 0:
                    print(f"    ✓ {class_name:12} - {count:4} images")
                else:
                    print(f"    ⚠ {class_name:12} - EMPTY (0 images)")
                    all_good = False
            else:
                print(f"    ❌ {class_name:12} - MISSING folder")
                all_good = False
    
    return all_good


def install_dependencies():
    """Install Python dependencies from requirements.txt."""
    print("\n" + "="*70)
    print("INSTALLING DEPENDENCIES")
    print("="*70)
    
    req_file = Path(__file__).parent.parent / "requirements.txt"
    
    print(f"\nInstalling packages from {req_file}...")
    try:
        subprocess.run(
            [sys.executable, "-m", "pip", "install", "-r", str(req_file), "-q"],
            check=True
        )
        print("✓ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False


def main():
    """Main setup routine."""
    print("\n" + "="*70)
    print("BRAIN TUMOR CHATBOT - SETUP")
    print("="*70)
    print("\nThis script will:")
    print("  1. Check your dataset structure")
    print("  2. Install Python dependencies")
    print("  3. Show you how to train the model")
    
    # Check dataset
    dataset_ok = check_dataset_structure()
    
    # Install dependencies
    deps_ok = install_dependencies()
    
    # Final instructions
    print("\n" + "="*70)
    print("NEXT STEPS")
    print("="*70)
    
    if not dataset_ok:
        print("\n❌ Dataset structure incomplete. Please:")
        print("   1. Download the brain tumor dataset")
        print("   2. Organize it as follows:")
        print("""
   brain_tumor/
   ├── Training/
   │   ├── Glioma/
   │   ├── Meningioma/
   │   ├── Pituitary/
   │   └── NoTumor/
   └── Testing/
       ├── Glioma/
       ├── Meningioma/
       ├── Pituitary/
       └── NoTumor/
        """)
    else:
        print("\n✓ Dataset structure verified!")
    
    if deps_ok and dataset_ok:
        print("\n✓ All checks passed! Ready to train the model.")
        print("\nTo train the model, run:")
        print("   python training/train_model.py")
        print("\nThis will:")
        print("   - Load all training images from brain_tumor/Training/")
        print("   - Build a CNN neural network with 4 output classes")
        print("   - Train for 20 epochs with validation")
        print("   - Save the trained model to app/models/brain_tumor_model.h5")
        print("\nEstimated training time: 10-30 minutes (depends on dataset size)")
    
    print("\n" + "="*70)


if __name__ == "__main__":
    main()
