#!/bin/bash

# BFHL API Deployment Script
# Supports multiple deployment platforms

set -e

echo "🚀 BFHL API Deployment Script"
echo "================================"

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 is not installed. Please install Python 3.7+ first."
    exit 1
fi

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 is not installed. Please install pip first."
    exit 1
fi

# Install dependencies
echo "📦 Installing dependencies..."
pip3 install -r requirements.txt

# Run tests
echo "🧪 Running tests..."
python3 test_api.py

# Check if tests passed
if [ $? -eq 0 ]; then
    echo "✅ Tests passed successfully!"
else
    echo "❌ Tests failed. Please fix issues before deployment."
    exit 1
fi

# Start the application
echo "🚀 Starting BFHL API..."
echo "📍 API will be available at: http://localhost:5000"
echo "🔗 Main endpoint: http://localhost:5000/bfhl"
echo "📖 API info: http://localhost:5000/bfhl (GET)"
echo "🔄 Health check: http://localhost:5000/"
echo ""
echo "Press Ctrl+C to stop the server"
echo "================================"

# Start the Flask application
python3 app.py
