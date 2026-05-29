#!/bin/bash
# Clean build artifacts

echo "🧹 Cleaning build artifacts..."

# Python build artifacts
rm -rf build/
rm -rf dist/
rm -rf *.egg-info
rm -rf .eggs/

# Test artifacts
rm -rf .pytest_cache/
rm -rf .coverage
rm -rf coverage.xml
rm -rf htmlcov/
rm -rf .benchmarks/

# Type checking artifacts
rm -rf .mypy_cache/
rm -rf .pytype/

# Documentation artifacts
rm -rf site/
rm -rf docs/_build/

# Cache directories
find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
find . -type f -name "*.pyc" -delete
find . -type f -name "*.pyo" -delete
find . -type f -name "*.so" -delete

# IDE artifacts
rm -rf .vscode/
rm -rf .idea/
rm -rf *.swp
rm -rf *.swo

# OS artifacts
find . -type f -name ".DS_Store" -delete
find . -type f -name "Thumbs.db" -delete

echo "✅ Clean complete!"