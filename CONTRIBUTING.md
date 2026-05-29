# Contributing to Easy Calc Tool

> 🎉 First off, thank you for considering contributing to Easy Calc Tool! 🎉

We welcome all kinds of contributions, including but not limited to:
- Reporting bugs
- Submitting feature requests
- Improving documentation
- Submitting code fixes
- Adding new features

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Code Style](#code-style)
- [Testing](#testing)
- [Documentation](#documentation)
- [Pull Request Process](#pull-request-process)
- [Reporting Bugs](#reporting-bugs)
- [Feature Requests](#feature-requests)
- [Release Process](#release-process)
- [License](#license)

## Code of Conduct

### Our Pledge

In the interest of fostering an open and welcoming environment, we as contributors and maintainers pledge to make participation in our project and our community a harassment-free experience for everyone, regardless of age, body size, disability, ethnicity, sex characteristics, gender identity and expression, level of experience, education, socio-economic status, nationality, personal appearance, race, religion, or sexual identity and orientation.

### Our Standards

Examples of behavior that contributes to creating a positive environment include:

- Using welcoming and inclusive language
- Being respectful of differing viewpoints and experiences
- Gracefully accepting constructive criticism
- Focusing on what is best for the community
- Showing empathy towards other community members

### Enforcement

Instances of abusive, harassing, or otherwise unacceptable behavior may be reported by contacting the project team at [team@easy-calc-tool.com](mailto:team@easy-calc-tool.com). All complaints will be reviewed and investigated and will result in a response that is deemed necessary and appropriate to the circumstances.

## Getting Started

### Prerequisites

- Python 3.8 or higher
- Git
- Make (optional, but recommended)

### First Time Contributors

If you're new to open source or this project, here are some good first issues:

1. Look for issues labeled `good-first-issue` or `help-wanted`
2. Comment on the issue that you'd like to work on it
3. Follow the setup instructions below

## Development Setup

### 1. Fork the Repository

Click the "Fork" button on the top right of the [GitHub repository page](https://github.com/easy-calc-tool/easy-calc-tool).

### 2. Clone Your Fork

```bash
git clone https://github.com/YOUR_USERNAME/easy-calc-tool.git
cd easy-calc-tool
```
### 3. Set Up Development Environment

```bash
# Install development dependencies
make install-dev

# Or manually
pip install -e ".[dev]"
```

### 4. Install Pre-commit Hooks

```bash
pre-commit install
This will automatically run code formatting and linting on every commit.
```

### 5. Verify Setup

```bash
# Run all checks
make test
make lint
```

## Code Style

We use several tools to maintain consistent code style:

| Tool |	Purpose |	Configuration |
| ---- | -------- | ------------- |
| Black | Code formatting | Line length: 100 characters |
| isort | Import sorting | Compatible with Black |
| flake8 | Style guide enforcement | Follows PEP 8 |
| mypy | Type checking | Strict type annotations |
| ruff | Fast linting | Combined functionality |

## Formatting Code
```bash
# Format all code
make format

# Or run individually
black easy_calc_tool tests
isort easy_calc_tool tests
```

## Linting Code
```bash
# Run all checks
make lint

# Or run individually
flake8 easy_calc_tool tests
mypy easy_calc_tool
ruff check easy_calc_tool tests
```

## Type Hints
All new code should include proper type hints:

```python
from typing import List, Dict, Optional

def calculate_mean(values: List[float]) -> Optional[float]:
    """Calculate the mean of a list of values."""
    if not values:
        return None
    return sum(values) / len(values)
```
    
## Naming Conventions
| Element | Convention |	Example |
| ------- | --------- | -------- |
| Classes |	PascalCase |	EasyCalc |
| Functions/Methods | snake_case | calculate_statistics |
| Variables | snake_case | result_data |
| Constants | UPPER_SNAKE_CASE | MAX_DATA_SIZE |
| Private Members | Leading underscore | _internal_method |

## Docstrings
Use Google-style docstrings:

```python
def calculate_statistics(
    data: pd.DataFrame,
    columns: List[str],
    operations: List[str]
) -> Dict[str, Any]:
    """
    Calculate statistics for specified columns.

    Args:
        data: Input DataFrame containing the data
        columns: List of column names to analyze
        operations: List of statistical operations to perform

    Returns:
        Dictionary containing the calculated statistics

    Raises:
        InvalidParameterError: If columns don't exist in data

    Example:
        >>> df = pd.DataFrame({'x': [1, 2, 3]})
        >>> result = calculate_statistics(df, ['x'], ['mean', 'sum'])
        >>> print(result['x']['mean'])
        2.0
    """
```
## Testing
- Test Requirements
- Every new feature must include tests

- Bug fixes should include regression tests

- Aim for >90% code coverage

- Critical paths should have >95% coverage

## Test Structure
```
tests/
├── __init__.py
├── conftest.py          # Shared fixtures
├── test_core.py         # Core functionality tests
├── test_data_handler.py # Data parsing tests
├── test_parser.py       # Natural language parser tests
├── test_integration.py  # Integration tests
└── fixtures/            # Test data files
    ├── sample_data.csv
    └── sample_data.json
```
## Writing Tests
```python
import pytest
from easy_calc_tool import EasyCalc

class TestStatistics:
    """Test statistical calculations."""
    
    @pytest.fixture
    def calc(self):
        """Create calculator instance for testing."""
        return EasyCalc(config={"cache_enabled": False})
    
    def test_mean_calculation(self, calc):
        """Test mean calculation."""
        data = [{"value": 10}, {"value": 20}, {"value": 30}]
        result = calc.calculate("statistics", data, 
                                columns="value", 
                                operations=["mean"])
        
        assert result["statistics"]["value"]["mean"] == 20.0
    
    @pytest.mark.slow
    def test_large_dataset(self, calc):
        """Test with large dataset (marked as slow)."""
        data = [{"value": i} for i in range(100000)]
        result = calc.calculate("statistics", data,
                                columns="value",
                                operations=["sum"])
        
        assert result["statistics"]["value"]["sum"] == sum(range(100000))
    
    @pytest.mark.parametrize("data,expected", [
        ([1, 2, 3], 2.0),
        ([10, 20, 30, 40], 25.0),
        ([5], 5.0),
    ])
    def test_mean_with_parameterized_data(self, calc, data, expected):
        """Test mean with various inputs."""
        result = calc.calculate("statistics", data,
                                columns="value",
                                operations=["mean"])
        
        assert result["statistics"]["value"]["mean"] == expected
```

## Running Tests
```# Run all tests
make test

# Run specific test file
pytest tests/test_core.py

# Run specific test function
pytest tests/test_core.py -k test_mean_calculation

# Run tests with coverage report
make test-coverage

# View coverage report
open htmlcov/index.html

# Run only slow tests
pytest tests/ -m slow

# Run only fast tests (exclude slow)
pytest tests/ -m "not slow"

# Run tests in parallel (requires pytest-xdist)
pytest tests/ -n auto
```

## Test Coverage Expectations
```bash
# Check coverage
pytest tests/ --cov=easy_calc_tool --cov-report=term

# Expected output:
# Name                           Stmts   Miss  Cover
# --------------------------------------------------
# easy_calc_tool/__init__.py        12      0   100%
# easy_calc_tool/core.py            245     12    95%
# easy_calc_tool/data_handler.py     67      3    96%
# easy_calc_tool/parser.py           45      2    96%
# easy_calc_tool/tools.py            89      0   100%
# --------------------------------------------------
# TOTAL                             458     17    96%
```

## Documentation
### Building Documentation

```bash
# Build documentation
make docs

# Serve documentation locally
make docs-serve

# View at http://127.0.0.1:8000
```
### Documentation Structure
```text
docs/
├── index.md              # Home page
├── installation.md       # Installation guide
├── usage.md              # Usage examples
├── api.md                # API reference
├── examples.md           # More examples
└── contributing.md       # Contributing guide
```

## Docstring Guidelines
- Public APIs: Always include docstrings

- Private methods: Optional but encouraged for complex logic

- Include examples for non-trivial functions

- Keep docstrings up to date with code changes

## Pull Request Process
### Branch Naming
#### Use descriptive branch names:

```bash
# Features
git checkout -b feature/add-matrix-operations

# Bug fixes
git checkout -b fix/handle-division-by-zero

# Documentation
git checkout -b docs/update-api-reference

# Refactoring
git checkout -b refactor/optimize-data-parsing

# Tests
git checkout -b test/add-coverage-for-timeseries
```

### Commit Message Guidelines
#### Follow Conventional Commits:

```text
<type>(<scope>): <subject>

<body>

<footer>
```
#### Types:

- feat: New feature

- fix: Bug fix

- docs: Documentation only changes

- style: Code style changes (formatting, etc.)

- refactor: Code changes that neither fix bugs nor add features

- perf: Performance improvements

- test: Adding or fixing tests

- chore: Changes to build process or auxiliary tools

#### Examples:

```bash
feat(statistics): add correlation matrix calculation

fix(arithmetic): handle division by zero gracefully

docs(api): update function signatures in API docs

test(core): increase coverage for edge cases

perf(data_handler): optimize large dataframe parsing
```

### Pre-commit Checklist
#### Before committing, ensure:

```bash
# 1. Format code
make format

# 2. Run linters
make lint

# 3. Run tests
make test

# 4. Check coverage
make test-coverage
```

### Creating a Pull Request
1. Push your changes:
```bash
git push origin feature/your-feature-name
```
2. Open a Pull Request on GitHub

3. Fill out the PR template (automatically loaded)

4. Request review from maintainers

5. Respond to feedback and make requested changes

6. Wait for CI checks to pass

7. Get approval from at least one maintainer

8. Merge (maintainers will handle this)

### PR Template
```markdown
## Pull Request Checklist

- [ ] I have read the [contributing guidelines](CONTRIBUTING.md)
- [ ] I have followed the code style guidelines
- [ ] I have added tests for my changes
- [ ] I have updated the documentation
- [ ] I have updated the CHANGELOG.md

## Type of Change

- [ ] Bug fix (non-breaking change that fixes an issue)
- [ ] New feature (non-breaking change that adds functionality)
- [ ] Breaking change (fix or feature that would cause existing functionality to not work as expected)
- [ ] Documentation update
- [ ] Performance improvement
- [ ] Code refactoring

## Description

<!-- Provide a clear and concise description of your changes -->

## Related Issues

<!-- Link to any related issues using #issue-number -->
Fixes #123
Closes #456

## Testing

<!-- Describe how you tested your changes -->

- [ ] Unit tests added/updated
- [ ] Integration tests added/updated
- [ ] Manual testing performed

## Screenshots

<!-- If applicable, add screenshots to help explain your changes -->

## Additional Context

<!-- Add any other context about the pull request here -->
```
### Reporting Bugs
We use GitHub Issues to track public bugs. Report a bug by opening a new issue.

### Bug Report Template
```markdown
**Describe the Bug**
A clear and concise description of what the bug is.

**To Reproduce**
Steps to reproduce the behavior:
1. Create data '...'
2. Call method '...'
3. See error

**Expected Behavior**
A clear and concise description of what you expected to happen.

**Actual Behavior**
A clear and concise description of what actually happened.

**Code Example**
```python
from easy_calc_tool import EasyCalc

calc = EasyCalc()
data = [...]
result = calc.calculate(...)  # This fails
```
#### Environment

- Python version: [e.g., 3.11.0]

- easy-calc-tool version: [e.g., 0.1.0]

- Operating system: [e.g., macOS 14.0, Ubuntu 22.04]

- Installation method: [e.g., pip, from source]

#### Additional Context
Add any other context about the problem here.

#### Possible Solution
If you have ideas on how to fix the issue, please share them.

```text

## Feature Requests

Feature requests are also submitted via Issues. Please use the feature request template:

```markdown
**Problem Statement**
What problem are you trying to solve? What's the use case?

**Proposed Solution**
How would you like this feature to work?

**Alternative Solutions**
What alternatives have you considered?

**Example Usage**
```python
# How would users use this feature?
result = calc.calculate("new_feature", data, ...)
Additional Context
Add any other context or screenshots about the feature request here.

text

## Release Process

Only maintainers can publish new releases.

### Version Numbering

We follow [Semantic Versioning](https://semver.org/):

- **MAJOR**: Incompatible API changes
- **MINOR**: Backward-compatible new functionality
- **PATCH**: Backward-compatible bug fixes

### Release Steps

1. **Update CHANGELOG.md**
   - Add new version section
   - Document all changes

2. **Update version.py**
   ```python
   __version__ = "1.2.3"

3. **Create Release PR**
    - Title: chore(release): prepare for v1.2.3
    - Include version bump and changelog updates

4. **After merge, create GitHub Release**

    - Tag: v1.2.3

    - Title: Version 1.2.3

    - Description: Copy from CHANGELOG

5. **CI will automatically publish to PyPI**
```
## Getting Help
### Where to Ask Questions
- GitHub Discussions: For questions and general discussion

- Issues: For bug reports and feature requests

- Discord: For real-time chat (link coming soon)

### What to Include When Asking for Help
- What you're trying to achieve

- What you've tried

- Code examples or error messages

- Your environment details

### Recognition
Contributors will be recognized in:

- README.md contributors section

- CHANGELOG.md for significant contributions

- GitHub profile on the contributors page

### License
By contributing, you agree that your contributions will be licensed under the same MIT License that covers the project.

### Quick Reference Card
#### Common Commands
```bash
# Setup
make install-dev          # Install development dependencies
pre-commit install        # Install git hooks

# Development
make format               # Format code
make lint                 # Run linters
make test                 # Run tests
make test-coverage        # Run tests with coverage

# Building
make build                # Build distribution packages
make publish-test         # Publish to Test PyPI
make publish              # Publish to PyPI

# Documentation
make docs                 # Build docs
make docs-serve           # Serve docs locally

# Cleanup
make clean                # Clean build artifacts

```

#### File Locations
| File            | Purpose                          |
|-----------------|----------------------------------|
| easy_calc_tool/ | Main package code                |
| tests/          | Test files                       |
| docs/           | Documentation                    |
| examples/       | Example scripts                  |
| .github/        | 	GitHub templates and workflows  |
#### Thank you for contributing! 🚀

Every contribution, no matter how small, is valuable. Together we're building something great.
