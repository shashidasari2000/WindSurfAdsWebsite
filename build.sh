#!/bin/bash
set -e

echo "🐍 Python version check..."
python --version

echo "📦 Upgrading pip..."
pip install --upgrade pip

echo "📦 Installing requirements..."
pip install -r requirements.txt

echo "🗄️ Database initialization will run on startup..."
echo "✅ Build completed successfully!"