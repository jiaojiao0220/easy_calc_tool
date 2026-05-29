# Easy Calc Tool - 智能计算工具箱

[![PyPI version](https://badge.fury.io/py/easy-calc-tool.svg)](https://badge.fury.io/py/easy-calc-tool)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> 🚀 专为大模型 Function Call 设计的灵活计算工具箱

## ✨ 特性

- 🎯 **LLM优化**: 支持自然语言参数解析，让大模型更容易调用
- 📊 **功能全面**: 基础计算、统计分析、时间序列、单位转换等
- 🔌 **LangChain集成**: 开箱即用的LangChain工具支持
- 🛡️ **安全可靠**: 安全的表达式求值，防止注入攻击
- 📦 **轻量级**: 核心依赖仅 pandas 和 numpy
- 🚀 **高性能**: 内置缓存，支持批量计算

## 📦 安装

```bash
# 基础安装
pip install easy-calc-tool

# 安装LangChain支持
pip install easy-calc-tool[langchain]

```
## 🚀 快速开始
```PYTHON
from easy_calc_tool import EasyCalc

# 初始化
calc = EasyCalc()

# 基础算术
result = calc.calculate("arithmetic", None, expression="100 * 2 + 5")
print(result["result"])  # 205

# 统计分析
data = [
    {"销售额": 100, "利润": 20},
    {"销售额": 200, "利润": 40},
    {"销售额": 300, "利润": 60}
]
result = calc.calculate("statistics", data, columns="销售额", operations=["总和", "平均"])
print(result["statistics"]["销售额"]["总和"])  # 600
```
## 📚 支持的场景
| 类别 |	功能 |
| --- | --- |
| 基础计算 | 四则运算、幂运算、三角函数、对数 |
| 统计分析 | 均值、方差、标准差、相关性、回归 |
| 表格处理 | 聚合、筛选、透视表、分组统计 |
| 时间序列 | 移动平均、增长率、累计和 |
| 单位转换 | 长度、重量、温度、货币 |
| 日期计算 | 日期差、年龄、工作日 |
