# Easy Calc Tool

[![PyPI version](https://badge.fury.io/py/easy-calc-tool.svg)](https://badge.fury.io/py/easy-calc-tool)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Codecov](https://codecov.io/gh/easy-calc-tool/easy-calc-tool/branch/main/graph/badge.svg)](https://codecov.io/gh/easy-calc-tool/easy-calc-tool)
[![CI](https://github.com/easy-calc-tool/easy-calc-tool/actions/workflows/ci.yml/badge.svg)](https://github.com/easy-calc-tool/easy-calc-tool/actions/workflows/ci.yml)

> 🚀 A flexible calculation toolbox designed specifically for LLM Function Calling

## ✨ Features

- 🎯 **LLM-Optimized**: Natural language parameter parsing, making it easier for LLMs to call
- 📊 **All-in-One**: Basic arithmetic, statistical analysis, time series, unit conversion, and more
- 🔌 **LangChain Ready**: Out-of-the-box LangChain tool integration
- 🛡️ **Secure**: Safe expression evaluation, preventing injection attacks
- 📦 **Lightweight**: Core dependencies only (pandas, numpy)
- 🚀 **High Performance**: Built-in caching, batch computation support
- 🌍 **Multi-format Support**: CSV, JSON, DataFrame, file paths

## 📦 Installation

```bash
# Basic installation
pip install easy-calc-tool

# With LangChain support
pip install easy-calc-tool[langchain]

# Full installation (includes development tools)
pip install easy-calc-tool[all]
```

## 🚀 Quick Start
###Basic Usage
```bash
from easy_calc_tool import EasyCalc

calc = EasyCalc()

# 基础算术
result = calc.calculate("arithmetic", None, expression="100 * 2 + 5")
print(result["result"])  # 205

# 统计分析
data = [
    {"sales": 100, "profit": 20},
    {"sales": 200, "profit": 40},
    {"sales": 300, "profit": 60}
]
result = calc.calculate("statistics", data, columns="sales", operations=["sum", "mean"])
print(result["statistics"]["sales"]["sum"])  # 600
```
### Natural Language Interface
```bash
# Natural language aggregation
result = calc.calculate("aggregate", data, 
                       what="group by profit and sum sales")
print(result["grouped_result"])
````
### 🛠️ LangChain Integration
```bash
from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from easy_calc_tool.langchain import get_tools

llm = ChatOpenAI(model="gpt-4")
tools = get_tools()  # 一键获取所有工具

agent = create_agent(model=llm, tools=tools)
response = agent.invoke({
    "messages": [{"role": "user", "content": "计算 12345 * 67890"}]
})
```
## 📚 Supported Scenarios
1. Basic Calculations
- Arithmetic operations (+, -, *, /, **, %)
- Trigonometric functions (sin, cos, tan)
- Logarithmic and exponential functions
- Percentage calculations
- Rounding operations
2. Statistical Analysis
- Descriptive statistics (mean, median, mode, std, var)

- Group statistics (GroupBy operations)

- Correlation analysis

- Regression analysis

- Hypothesis testing

3. Data Processing
- Aggregation (sum, mean, count, min, max)

- Data filtering

- Pivot tables

- Data transformation (normalization, standardization)

4. Time Series
- Moving averages

- Growth rates (MoM, YoY)

- Cumulative sums

- Lag/Difference operations

- Date arithmetic

5. Other Features
- Unit conversion (length, weight, temperature, currency)

- Date calculations (age, date differences)

- Financial calculations (loans, IRR, NPV)

- Matrix operations
## 🔧 Configuration
```python
from easy_calc_tool import EasyCalc

# Custom configuration
calc = EasyCalc(config={
    "cache_enabled": True,      # Enable result caching
    "precision": 2,              # Floating point precision
    "timeout": 30,              # Computation timeout (seconds)
    "max_data_size": 1000000,    # Maximum data rows
    "safe_mode": True,          # Enable safe evaluation mode
})
```
## 📖 Documentation
Full documentation is available at https://easy-calc-tool.readthedocs.io

- Installation Guide

- Usage Examples

- API Reference

- Contributing Guide

## 🤝 Contributing
We welcome contributions! Please see our Contributing Guide for details.

## Development Setup
```bash
# Clone the repository
git clone https://github.com/easy-calc-tool/easy-calc-tool.git
cd easy-calc-tool

# Install development dependencies
make install-dev

# Run tests
make test

# Run linting
make lint

# Format code
make format
```

## 📊 Benchmarks
| Operation | Data Size | Time |
| ---------- | -------- |------|
| Basic arithmetic | N/A | < 0.1ms |
| Statistics (mean, sum) | 1M rows | ~50ms |
| Group by aggregation | 1M rows, 10 groups | ~100ms |
| Time series (moving average) | 100K rows | ~30ms |

## 🗺️ Roadmap
- v0.2.0 - More statistical functions (ANOVA, chi-square)

- v0.3.0 - Machine learning predictions

- v0.4.0 - Visualization support

- v0.5.0 - GPU acceleration

- v1.0.0 - Stable release with full documentation

## 🙏 Acknowledgments
- Built with pandas and numpy

- Inspired by the needs of LLM function calling applications

- Thanks to all contributors and users

## 📄 License
 MIT License - see LICENSE file for details.

##📧 Contact
Issues: GitHub Issues

Email: team@easy-calc-tool.com

Discord: Join our Discord
