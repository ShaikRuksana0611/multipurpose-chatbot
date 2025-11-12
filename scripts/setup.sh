#!/bin/bash

echo "🚀 Setting up Multi-Purpose Chatbot..."

# Create virtual environment
python3 -m venv chatbot_env
source chatbot_env/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create necessary directories
mkdir -p backend/data backend/logs backend/models tests/fixtures

# Download NLTK data
python -c "import nltk; nltk.download('punkt'); nltk.download('wordnet')"

# Initialize data file
cp config/default_data.json backend/data/chatbot_data.json

echo "✅ Setup completed successfully!"
echo "🎯 To start the application:"
echo "   source chatbot_env/bin/activate"
echo "   python backend/app.py"