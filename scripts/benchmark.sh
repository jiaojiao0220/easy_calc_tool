#!/bin/bash
# Benchmark script for easy-calc-tool

set -e

echo "📊 Running benchmarks..."

# Run benchmark tests
pytest tests/ --benchmark-only --benchmark-json=benchmark_results.json

# Display results
echo ""
echo "Benchmark Results:"
echo "=================="
python -c "
import json
with open('benchmark_results.json', 'r') as f:
    data = json.load(f)
    for benchmark in data['benchmarks']:
        name = benchmark['name']
        mean = benchmark['stats']['mean'] * 1000
        print(f'{name}: {mean:.2f} ms')
"

echo "✅ Benchmarks complete!"