#!/bin/bash

echo "Creating python directory..."
mkdir -p ./python

echo "Installing dependencies..."
pip install --target ./python -r requirements.txt --no-deps

echo "Cleaning up unnecessary files..."
find ./python -type d -name "tests" -exec rm -rf {} +
find ./python -type d -name "__pycache__" -exec rm -rf {} +
find ./python -type d -name "*.dist-info" -exec rm -rf {} +

echo "Checking size..."
du -sh ./python