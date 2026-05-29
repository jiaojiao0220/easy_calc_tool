#!/bin/bash
# Format code for easy-calc-tool

set -e

echo "🎨 Formatting code..."

# Format with black
echo "Running black..."
black easy_calc_tool tests examples

# Sort imports
echo "Running isort..."
isort easy_calc_tool tests examples

# Lint with ruff
echo "Running ruff..."
ruff check --fix easy_calc_tool tests examples

echo "✅ Code formatting complete!"