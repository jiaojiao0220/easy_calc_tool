#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author : jiaojiao
# @Time : 2026/5/29 17:47
"""
Advanced analysis examples for easy-calc-tool.
"""
# 将项目根目录添加到 Python 路径
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from easy_calc_tool import EasyCalc
import pandas as pd


def correlation_analysis():
    """Demonstrate correlation analysis."""
    calc = EasyCalc()

    # Sample data with relationships
    data = [
        {"temperature": 20, "sales": 100, "advertising": 50},
        {"temperature": 22, "sales": 120, "advertising": 60},
        {"temperature": 24, "sales": 140, "advertising": 70},
        {"temperature": 26, "sales": 160, "advertising": 80},
        {"temperature": 28, "sales": 180, "advertising": 90},
    ]

    # Calculate correlations
    result = calc.calculate("correlation", data, method="pearson")
    print("Correlation Matrix:")
    for var, corrs in result["correlation_matrix"].items():
        print(f"  {var}: {corrs}")


def pivot_table_analysis():
    """Demonstrate pivot table creation."""
    calc = EasyCalc()

    # Sales data by product and region
    data = [
        {"product": "A", "region": "North", "quarter": "Q1", "sales": 100},
        {"product": "A", "region": "South", "quarter": "Q1", "sales": 150},
        {"product": "B", "region": "North", "quarter": "Q1", "sales": 200},
        {"product": "B", "region": "South", "quarter": "Q1", "sales": 250},
        {"product": "A", "region": "North", "quarter": "Q2", "sales": 120},
        {"product": "A", "region": "South", "quarter": "Q2", "sales": 180},
        {"product": "B", "region": "North", "quarter": "Q2", "sales": 220},
        {"product": "B", "region": "South", "quarter": "Q2", "sales": 280},
    ]

    # Pivot by product and region
    result = calc.calculate(
        "pivot", data, index="product", columns="region", values="sales", aggfunc="sum"
    )
    print("\nPivot Table (Product × Region):")
    print(result["pivot_table"])


def comprehensive_data_analysis():
    """Demonstrate end-to-end data analysis."""
    calc = EasyCalc()

    # Create sample dataset
    data = pd.DataFrame(
        {
            "date": pd.date_range("2024-01-01", periods=100, freq="D"),
            "sales": np.random.normal(1000, 100, 100),
            "customers": np.random.poisson(50, 100),
            "region": np.random.choice(["North", "South", "East", "West"], 100),
            "product": np.random.choice(["A", "B", "C"], 100),
        }
    )

    print("Comprehensive Data Analysis")
    print("=" * 50)

    # 1. Overall statistics
    print("\n1. Overall Statistics:")
    result = calc.calculate(
        "statistics", data, columns=["sales", "customers"], operations=["mean", "std", "min", "max"]
    )
    for col, stats in result["statistics"].items():
        print(f"   {col}: {stats}")

    # 2. Group by analysis
    print("\n2. Sales by Region:")
    result = calc.calculate(
        "statistics", data, columns="sales", operations=["sum", "mean"], group_by="region"
    )
    for region, stats in result["grouped"].items():
        print(f"   {region}: {stats}")

    # 3. Time series analysis
    print("\n3. Time Series Trends:")
    result = calc.calculate(
        "timeseries", data, date_col="date", value_col="sales", operation="moving_average", window=7
    )
    print(f"   Calculated 7-day moving average for {len(result['result'])} days")

    # 4. Filtered analysis
    print("\n4. High Sales Analysis (>1200):")
    result = calc.calculate("filter_calc", data, condition="sales > 1200", calculate="sales总和")
    print(f"   High sales days: {result['filtered_count']}")
    if "statistics" in result:
        print(f"   Total high sales: {result['statistics']['sales']['sum']:.0f}")

    # 5. Correlation
    print("\n5. Sales vs Customers Correlation:")
    result = calc.calculate("correlation", data, columns=["sales", "customers"])
    corr = result["correlation_matrix"]["sales"]["customers"]
    print(f"   Correlation coefficient: {corr:.3f}")


def export_results():
    """Demonstrate result formatting and export."""
    calc = EasyCalc()

    data = [
        {"product": "A", "sales": 100, "profit": 20},
        {"product": "B", "sales": 200, "profit": 40},
        {"product": "C", "sales": 300, "profit": 60},
    ]

    result = calc.calculate("statistics", data, columns="sales", operations=["sum", "mean"])

    # Access individual values
    total_sales = result["statistics"]["sales"]["sum"]
    avg_sales = result["statistics"]["sales"]["mean"]

    print(f"\nSales Analysis Results:")
    print(f"  Total Sales: {total_sales}")
    print(f"  Average Sales: {avg_sales}")

    # The result is already serializable to JSON
    import json

    json_str = json.dumps(result, indent=2)
    print(f"\nJSON Export (first 200 chars): {json_str[:200]}...")


if __name__ == "__main__":
    correlation_analysis()
    pivot_table_analysis()
    comprehensive_data_analysis()
    export_results()
