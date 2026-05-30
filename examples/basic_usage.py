#!/usr/bin/python3
# @Author : jiaojiao
# @Time : 2026/5/29 17:46
"""
Basic usage examples for easy-calc-tool.
"""
import os
import sys

# 将项目根目录添加到 Python 路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from easy_calc_tool import EasyCalc


def basic_arithmetic():
    """Demonstrate basic arithmetic operations."""
    calc = EasyCalc()

    # Expression evaluation
    result = calc.calculate("arithmetic", None, expression="100 * 2 + 5")
    print(f"100 * 2 + 5 = {result['result']}")

    # Binary operation
    result = calc.calculate("arithmetic", None, a=10, b=3, operation="**")
    print(f"10 ** 3 = {result['result']}")

    # Complex expression
    result = calc.calculate(
        "arithmetic", None, expression="sqrt(16) + sin(30)"
    )
    print(f"sqrt(16) + sin(30) = {result['result']}")


def statistical_analysis():
    """Demonstrate statistical analysis."""
    calc = EasyCalc()

    # Sample data
    data = [
        {"department": "Sales", "revenue": 1000, "profit": 200},
        {"department": "Sales", "revenue": 1500, "profit": 300},
        {"department": "Marketing", "revenue": 800, "profit": 150},
        {"department": "Marketing", "revenue": 1200, "profit": 250},
        {"department": "Engineering", "revenue": 2000, "profit": 500},
    ]

    # Overall statistics
    result = calc.calculate(
        "statistics",
        data,
        columns=["revenue", "profit"],
        operations=["sum", "mean", "std"],
    )
    print("\nOverall Statistics:")
    print(result["statistics"])

    # Grouped statistics
    result = calc.calculate(
        "statistics",
        data,
        columns="revenue",
        operations=["sum", "mean"],
        group_by="department",
    )
    print("\nGrouped Statistics:")
    for dept, stats in result["grouped"].items():
        print(f"  {dept}: {stats}")


def natural_language_aggregation():
    """Demonstrate natural language aggregation."""
    calc = EasyCalc()

    data = [
        {"product": "A", "sales": 100, "region": "North"},
        {"product": "B", "sales": 200, "region": "South"},
        {"product": "A", "sales": 150, "region": "North"},
        {"product": "C", "sales": 300, "region": "East"},
    ]

    # Natural language query
    result = calc.calculate("aggregate", data, what="按product分组求和sales")
    print("\nNatural Language Result:")
    print(result["grouped_result"])


def time_series_analysis():
    """Demonstrate time series analysis."""
    calc = EasyCalc()

    # Create time series data
    import pandas as pd

    dates = pd.date_range("2024-01-01", periods=30, freq="D")
    data = pd.DataFrame(
        {
            "date": dates,
            "sales": [100 + i * 2 + (i % 7) * 5 for i in range(30)],
        }
    )

    # Moving average
    result = calc.calculate(
        "timeseries", data, operation="moving_average", window=7
    )
    print("\nMoving Average (7-day):")
    print(f"Calculated for {len(result['result'])} days")

    # Growth rate
    result = calc.calculate("timeseries", data, operation="growth_rate")
    print(f"\nAverage daily growth: {result['average_growth']:.2f}%")


def unit_conversion():
    """Demonstrate unit conversion."""
    calc = EasyCalc()

    conversions = [
        (10, "km", "mile"),
        (100, "kg", "lb"),
        (100, "c", "f"),
        (5, "m", "ft"),
    ]

    print("\nUnit Conversions:")
    for value, from_unit, to_unit in conversions:
        result = calc.calculate(
            "unit_convert",
            None,
            value=value,
            from_unit=from_unit,
            to_unit=to_unit,
        )

        # 安全地获取结果
        if isinstance(result, dict):
            if result.get("success") is False:
                print(
                    f"  ✗ {value} {from_unit} to {to_unit}: {result.get('error')}"
                )
            elif "result" in result:
                print(
                    f"  ✓ {value} {from_unit} = {result['result']:.2f} {to_unit}"
                )
            elif "conversion" in result:
                print(f"  ✓ {result['conversion']}")
            else:
                print(f"  ? {value} {from_unit} to {to_unit}: {result}")
        else:
            print(f"  ? {value} {from_unit} to {to_unit}: {result}")


def date_calculations():
    """Demonstrate date calculations."""
    calc = EasyCalc()

    # Date difference
    result = calc.calculate(
        "date_calc", None, start="2024-01-01", end="2024-12-31"
    )
    print(f"\nDays in 2024: {result['days_diff']}")

    # Age calculation
    result = calc.calculate(
        "date_calc", None, birth_date="1990-05-15", reference_date="2024-01-01"
    )
    print(f"Age: {result['age']} years")

    # Day of week
    result = calc.calculate("date_calc", None, date_for_dow="2024-12-25")
    print(f"Christmas 2024 is on {result['day_of_week']}")


if __name__ == "__main__":
    print("=" * 50)
    print("Easy Calc Tool - Basic Examples")
    print("=" * 50)

    basic_arithmetic()
    statistical_analysis()
    natural_language_aggregation()
    time_series_analysis()
    unit_conversion()
    date_calculations()
