#!/bin/bash
# Test script for easy-calc-tool

set -e

echo "🧪 Running tests..."

# Install development dependencies
pip install -e ".[dev]"

# Run tests with coverage
pytest tests/ \
    --cov=easy_calc_tool \
    --cov-report=html \
    --cov-report=term-missing \
    --cov-report=xml \
    -v

# Check coverage threshold
COVERAGE=$(pytest tests/ --cov=easy_calc_tool --cov-report=term 2>&1 | grep "TOTAL" | awk '{print $4}' | sed 's/%//')

echo "📊 Coverage: ${COVERAGE}%"

if (( $(echo "$COVERAGE < 90" | bc -l) )); then
    echo "❌ Coverage is below 90%!"
    exit 1
else
    echo "✅ Coverage meets threshold (>=90%)"
fi

echo "🎉 All tests passed!"