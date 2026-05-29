#!/bin/bash
# Publish script for easy-calc-tool

set -e

echo "📦 Publishing easy-calc-tool to PyPI..."

# Check version
VERSION=$(python -c "from easy_calc_tool.version import __version__; print(__version__)")
echo "Current version: $VERSION"

# Confirm
read -p "Continue with publish? (y/n) " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    exit 1
fi

# Run tests
echo "🧪 Running tests..."
./scripts/test.sh

# Build package
echo "🔨 Building package..."
./scripts/build.sh

# Publish to PyPI
echo "🚀 Publishing to PyPI..."
twine upload dist/*

echo "🎉 Published version $VERSION to PyPI!"

# Create git tag
echo "🏷️ Creating git tag v$VERSION"
git tag "v$VERSION"
git push origin "v$VERSION"

echo "✅ Done!"