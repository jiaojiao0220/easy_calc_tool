.PHONY: help install install-dev install-all uninstall clean \
        test test-slow test-coverage test-benchmark \
        lint format type-check \
        build build-check publish publish-test \
        docs docs-serve \
        pre-commit

# Colors for output
GREEN := \033[0;32m
RED := \033[0;31m
NC := \033[0m # No Color

help:
	@echo "$(GREEN)Easy Calc Tool - Available Commands$(NC)"
	@echo ""
	@echo "Installation:"
	@echo "  make install        - Install basic package"
	@echo "  make install-dev    - Install with development dependencies"
	@echo "  make install-all    - Install with all dependencies"
	@echo "  make uninstall      - Uninstall the package"
	@echo ""
	@echo "Testing:"
	@echo "  make test           - Run all tests"
	@echo "  make test-slow      - Run slow tests"
	@echo "  make test-coverage  - Run tests with coverage report"
	@echo "  make test-benchmark - Run performance benchmarks"
	@echo ""
	@echo "Code Quality:"
	@echo "  make lint           - Run linters"
	@echo "  make format         - Format code"
	@echo "  make type-check     - Run type checking"
	@echo ""
	@echo "Building:"
	@echo "  make build          - Build distribution packages"
	@echo "  make build-check    - Check distribution packages"
	@echo "  make publish        - Publish to PyPI"
	@echo "  make publish-test   - Publish to Test PyPI"
	@echo ""
	@echo "Documentation:"
	@echo "  make docs           - Build documentation"
	@echo "  make docs-serve     - Serve documentation locally"
	@echo ""
	@echo "Other:"
	@echo "  make clean          - Clean build artifacts"
	@echo "  make pre-commit     - Run pre-commit hooks"
	@echo ""

# Installation
install:
	pip install -e .

install-dev:
	pip install -e ".[dev]"

install-all:
	pip install -e ".[all]"

uninstall:
	pip uninstall easy-calc-tool -y

# Testing
test:
	pytest tests/ -v

test-slow:
	pytest tests/ -v -m slow

test-coverage:
	pytest tests/ -v --cov=easy_calc_tool --cov-report=html --cov-report=term-missing
	@echo "$(GREEN)Coverage report generated in htmlcov/index.html$(NC)"

test-benchmark:
	pytest tests/ --benchmark-only

# Code Quality
lint:
	@echo "$(GREEN)Running flake8...$(NC)"
	flake8 easy_calc_tool tests --count --statistics
	@echo "$(GREEN)Running ruff...$(NC)"
	ruff check easy_calc_tool tests
	@echo "$(GREEN)Running mypy...$(NC)"
	mypy easy_calc_tool

format:
	@echo "$(GREEN)Running black...$(NC)"
	black easy_calc_tool tests
	@echo "$(GREEN)Running isort...$(NC)"
	isort easy_calc_tool tests
	@echo "$(GREEN)Running ruff fix...$(NC)"
	ruff check --fix easy_calc_tool tests

type-check:
	mypy easy_calc_tool

# Building
build: clean
	@echo "$(GREEN)Building distribution packages...$(NC)"
	python -m build

build-check: build
	@echo "$(GREEN)Checking distribution packages...$(NC)"
	twine check dist/*

publish: build-check
	@echo "$(GREEN)Publishing to PyPI...$(NC)"
	twine upload dist/*

publish-test: build-check
	@echo "$(GREEN)Publishing to Test PyPI...$(NC)"
	twine upload --repository testpypi dist/*

# Documentation
docs:
	@echo "$(GREEN)Building documentation...$(NC)"
	mkdocs build

docs-serve:
	@echo "$(GREEN)Serving documentation at http://127.0.0.1:8000$(NC)"
	mkdocs serve

# Other
clean:
	@echo "$(GREEN)Cleaning build artifacts...$(NC)"
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info
	rm -rf .eggs/
	rm -rf .pytest_cache/
	rm -rf .mypy_cache/
	rm -rf .ruff_cache/
	rm -rf htmlcov/
	rm -rf .coverage
	rm -rf coverage.xml
	rm -rf site/
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.so" -delete

pre-commit:
	pre-commit run --all-files

# Development convenience
dev: install-dev pre-commit
	@echo "$(GREEN)Development environment ready!$(NC)"

.PHONY: help install install-dev install-all uninstall clean \
        test test-slow test-coverage test-benchmark \
        lint format type-check \
        build build-check publish publish-test \
        docs docs-serve \
        pre-commit