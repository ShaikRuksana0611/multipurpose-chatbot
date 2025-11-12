#!/usr/bin/env python3
"""
Quick start script for Multi-Purpose Chatbot
"""

import os
import sys
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def setup_environment():
    """Setup the required environment"""
    logger.info("🚀 Setting up Multi-Purpose Chatbot...")
    
    # Create necessary directories
    directories = [
        'backend/data',
        'backend/logs', 
        'backend/models',
        'backend/utils',
        'backend/api',
        'templates',
        'static/css',
        'static/js',
        'static/images',
        'config'
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        logger.info(f"✅ Created directory: {directory}")
    
    # Check if all required files exist
    required_files = [
        'backend/app.py',
        'backend/chatbot_core.py',
        'backend/models/__init__.py',
        'backend/models/context_manager.py',
        'backend/models/intent_classifier.py',
        'backend/utils/__init__.py',
        'backend/utils/text_preprocessor.py',
        'backend/data/__init__.py',
        'backend/data/training_data.py',
        'backend/api/__init__.py',
        'templates/index.html',
        'config/__init__.py',
        'config/config_loader.py'
    ]
    
    missing_files = []
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)
    
    if missing_files:
        logger.warning(f"⚠️ Missing files: {missing_files}")
        logger.info("Please create the missing files before running the chatbot.")
        return False
    
    logger.info("✅ Environment setup completed")
    return True

def main():
    """Main function to run the chatbot"""
    if not setup_environment():
        logger.error("❌ Setup failed. Please check the missing files.")
        return
    
    try:
        # Import and run the Flask app
        from backend.app import create_app
        
        app = create_app()
        logger.info("🎉 Chatbot is starting...")
        logger.info("🌐 Access the chatbot at: http://localhost:5000")
        
        app.run(host='0.0.0.0', port=5000, debug=True)
        
    except Exception as e:
        logger.error(f"❌ Failed to start chatbot: {e}")
        logger.info("💡 Try running: python backend/app.py directly")

if __name__ == '__main__':
    main()