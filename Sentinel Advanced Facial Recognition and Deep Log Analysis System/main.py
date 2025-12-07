import sys
import os

def check_environment():
    print("Checking environment setup for Sentinel System...")
    
    try:
        import tensorflow as tf
        print(f"TensorFlow version: {tf.__version__}")
    except ImportError:
        print("Warning: TensorFlow not found.")

    try:
        import torch
        print(f"PyTorch version: {torch.__version__}")
    except ImportError:
        print("Warning: PyTorch not found.")

    try:
        import cv2
        print(f"OpenCV version: {cv2.__version__}")
    except ImportError:
        print("Warning: OpenCV not found.")

    print("Environment check complete.")

if __name__ == "__main__":
    check_environment()
    print("Sentinel System Initialized.")
