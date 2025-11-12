#!/usr/bin/env python3
"""
Dependency installation script for Multi-Purpose Chatbot
"""

import subprocess
import sys
import os

def run_command(command, description):
    """Run a shell command and handle errors"""
    print(f"📦 {description}...")
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ {description} completed successfully")
            return True
        else:
            print(f"❌ {description} failed:")
            print(f"Error: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ {description} failed with exception: {e}")
        return False

def main():
    """Main installation function"""
    print("🚀 Installing Multi-Purpose Chatbot Dependencies...")
    
    # Upgrade pip first
    if not run_command(f"{sys.executable} -m pip install --upgrade pip", "Upgrading pip"):
        print("⚠️  Pip upgrade failed, but continuing...")
    
    # Install compatible packages one by one
    packages = [
        "flask==2.3.3",
        "flask-cors==4.0.0", 
        "numpy==1.24.3",
        "scikit-learn==1.2.2",
        "nltk==3.8.1",
        "python-dotenv==1.0.0",
        "joblib==1.2.0"
    ]
    
    all_success = True
    for package in packages:
        if not run_command(f"{sys.executable} -m pip install {package}", f"Installing {package}"):
            all_success = False
            print(f"⚠️  Failed to install {package}, but continuing...")
    
    if all_success:
        print("🎉 All dependencies installed successfully!")
    else:
        print("⚠️  Some dependencies may not have installed correctly, but let's try to run anyway...")
    
    # Download NLTK data
    print("📥 Downloading NLTK data...")
    try:
        import nltk
        nltk.download('punkt_tab', quiet=False)
        nltk.download('wordnet', quiet=False) 
        nltk.download('omw-1.4', quiet=False)
        print("✅ NLTK data downloaded successfully")
    except Exception as e:
        print(f"⚠️  NLTK download warning: {e}")
    
    print("\n🎯 Setup completed! Run: python backend/app.py")

if __name__ == "__main__":
    main()