#!/bin/bash
# Build script for easy-calc-tool

set -e  # Exit on error

echo "🔨 Building easy-calc-tool..."

# Clean previous builds
echo "🧹 Cleaning previous builds..."
rm -rf build/
rm -rf dist/
rm -rf *.egg-info

# Install build dependencies
echo "📦 Installing build dependencies..."
pip install build twine

# Build package
echo "🏗️ Building package..."
python -m build

# Check package
echo "✅ Checking package..."
twine check dist/*

echo "🎉 Build complete! Packages are in dist/ directory"
ls -la dist/