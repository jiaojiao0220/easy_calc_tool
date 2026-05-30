#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author : jiaojiao
# @Time : 2026/5/29 17:22
# examples.py
import sys
import os

# 将项目根目录添加到 Python 路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from easy_calc_tool import execute_tool

# 1. 基础统计 - 单列
result = execute_tool(
    "statistics",
    {
        "data": [
            {"name": "张三", "sales": 1000, "profit": 200},
            {"name": "李四", "sales": 1500, "profit": 300},
            {"name": "王五", "sales": 800, "profit": 150},
        ],
        "columns": "sales",
        "operations": ["sum", "mean"],
    },
)
print(result)

# 2. 分组统计 - 多列
result = execute_tool(
    "statistics",
    {
        "data": "sales_data.csv",
        "columns": ["sales", "profit"],
        "operations": ["sum", "mean", "std"],
        "group_by": "department",
    },
)

# 3. 自然语言调用
result = execute_tool(
    "aggregate",
    {"data": sales_data, "what": "按部门求和销售额，计算平均利润", "group_by": "department"},
)

# 4. 筛选后计算
result = execute_tool(
    "filter_calc", {"data": sales_data, "condition": "sales > 1000", "calculate": "利润总和"}
)

# 5. 时间序列
result = execute_tool(
    "timeseries", {"data": daily_sales, "operation": "moving_average", "window": 7}
)

# 6. 基础算术
result = execute_tool("arithmetic", {"expression": "100 * 2 + 5 * 3"})
