#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author : jiaojiao
# @Time : 2026/5/29 18:37

"""
LangChain integration for easy-calc-tool.

Provides adapters to wrap EasyCalc tools as LangChain-compatible tools.
This module is optional and only needed when using LangChain framework.
"""

from typing import List, Optional, Dict, Any  # 添加 Any
from langchain_core.tools import StructuredTool
from pydantic import BaseModel, Field

from core import EasyCalc
from tools import get_tools


# ========== Pydantic Models for Parameter Validation ==========

class ArithmeticInput(BaseModel):
    expression: Optional[str] = Field(None, description="数学表达式，如 '2+3*4'")
    a: Optional[float] = Field(None, description="二元运算第一个数")
    b: Optional[float] = Field(None, description="二元运算第二个数")
    operation: Optional[str] = Field(None, description="操作符: +, -, *, /, **, %")


class StatisticsInput(BaseModel):
    data: str = Field(description="数据，CSV格式或JSON数组")
    columns: Optional[str] = Field(None, description="列名，逗号分隔")
    operations: Optional[str] = Field("mean,sum", description="操作，逗号分隔")
    group_by: Optional[str] = Field(None, description="分组字段")


class AggregateInput(BaseModel):
    data: str = Field(description="数据")
    what: Optional[str] = Field(None, description="自然语言描述")
    columns: Optional[str] = Field(None, description="列名")
    operations: Optional[str] = Field(None, description="操作")
    group_by: Optional[str] = Field(None, description="分组字段")


class FilterCalcInput(BaseModel):
    data: str = Field(description="数据")
    condition: str = Field(description="筛选条件，如 'sales > 1000'")
    calculate: Optional[str] = Field(None, description="要计算的内容")


class TimeseriesInput(BaseModel):
    data: str = Field(description="时间序列数据")
    date_col: Optional[str] = Field(None, description="日期列名")
    value_col: Optional[str] = Field(None, description="数值列名")
    operation: str = Field(description="操作类型")
    window: Optional[int] = Field(3, description="移动窗口大小")


class UnitConvertInput(BaseModel):
    value: float = Field(description="数值")
    from_unit: str = Field(description="原始单位")
    to_unit: str = Field(description="目标单位")


class DateCalcInput(BaseModel):
    start: Optional[str] = Field(None, description="开始日期")
    end: Optional[str] = Field(None, description="结束日期")
    date: Optional[str] = Field(None, description="基准日期")
    days: Optional[int] = Field(None, description="天数")
    birth_date: Optional[str] = Field(None, description="出生日期")


class DescribeInput(BaseModel):
    data: str = Field(description="数据")
    percentiles: Optional[str] = Field("0.25,0.5,0.75", description="分位数")


class CorrelationInput(BaseModel):
    data: str = Field(description="数据")
    method: str = Field("pearson", description="方法: pearson, spearman")
    columns: Optional[str] = Field(None, description="列名")


class PivotInput(BaseModel):
    data: str = Field(description="数据")
    index: str = Field(description="行索引")
    columns: Optional[str] = Field(None, description="列字段")
    values: str = Field(description="值字段")
    aggfunc: str = Field("mean", description="聚合函数")
    fill_value: float = Field(0, description="填充值")


# ========== Tool Creation ==========

def _call_calc(calc: EasyCalc, tool: str, data: Any, **kwargs) -> str:
    """Helper to call calc and format result."""
    import json

    result = calc.calculate(tool, data, **kwargs)

    if result.get("success", True) is False:
        return f"Error: {result.get('error', 'Unknown error')}"

    return _format_result(result)


def _format_result(result: Dict) -> str:
    """Format result dictionary into readable string."""
    import json

    # Remove metadata
    if "_metadata" in result:
        result = {k: v for k, v in result.items() if k != "_metadata"}

    # Special handling for different result types
    if "result" in result and isinstance(result["result"], (int, float, str)):
        return str(result["result"])

    if "statistics" in result:
        return json.dumps(result["statistics"], ensure_ascii=False, indent=2)

    if "grouped_result" in result:
        return json.dumps(result["grouped_result"], ensure_ascii=False, indent=2)

    if "correlation_matrix" in result:
        return json.dumps(result["correlation_matrix"], ensure_ascii=False, indent=2)

    return json.dumps(result, ensure_ascii=False, indent=2)


def _parse_list(value: Optional[str]) -> Optional[List[str]]:
    """Parse comma-separated string into list."""
    if value is None:
        return None
    if isinstance(value, list):
        return value
    return [v.strip() for v in value.split(",") if v.strip()]


# 定义包装函数（避免 lambda 的潜在问题）
def _arithmetic_wrapper(calc: EasyCalc, expression=None, a=None, b=None, operation=None):
    return _call_calc(calc, "arithmetic", None,
                      expression=expression, a=a, b=b, operation=operation)


def _statistics_wrapper(calc: EasyCalc, data: str, columns=None, operations="mean,sum", group_by=None):
    return _call_calc(calc, "statistics", data,
                      columns=_parse_list(columns),
                      operations=_parse_list(operations),
                      group_by=group_by)


def _aggregate_wrapper(calc: EasyCalc, data: str, what=None, columns=None, operations=None, group_by=None):
    return _call_calc(calc, "aggregate", data,
                      what=what,
                      columns=_parse_list(columns),
                      operations=_parse_list(operations) if operations else None,
                      group_by=group_by)


def _filter_calc_wrapper(calc: EasyCalc, data: str, condition: str,
                         calculate=None, columns=None, operations=None):
    return _call_calc(calc, "filter_calc", data,
                      condition=condition,
                      calculate=calculate,
                      columns=_parse_list(columns),
                      operations=_parse_list(operations))


def _timeseries_wrapper(calc: EasyCalc, data: str, operation: str,
                        date_col=None, value_col=None, window=3):
    return _call_calc(calc, "timeseries", data,
                      date_col=date_col, value_col=value_col,
                      operation=operation, window=window)


def _unit_convert_wrapper(calc: EasyCalc, value: float, from_unit: str, to_unit: str):
    return _call_calc(calc, "unit_convert", None,
                      value=value, from_unit=from_unit, to_unit=to_unit)


def _date_calc_wrapper(calc: EasyCalc, start=None, end=None, date=None,
                       days=None, birth_date=None, date_for_dow=None, reference_date=None):
    return _call_calc(calc, "date_calc", None,
                      start=start, end=end, date=date, days=days,
                      birth_date=birth_date, date_for_dow=date_for_dow,
                      reference_date=reference_date)


def _describe_wrapper(calc: EasyCalc, data: str, percentiles="0.25,0.5,0.75", include="all"):
    return _call_calc(calc, "describe", data,
                      percentiles=[float(p) for p in percentiles.split(",")],
                      include=include)


def _correlation_wrapper(calc: EasyCalc, data: str, method="pearson", columns=None):
    return _call_calc(calc, "correlation", data,
                      method=method,
                      columns=_parse_list(columns))


def _pivot_wrapper(calc: EasyCalc, data: str, index: str, values: str,
                   columns=None, aggfunc="mean", fill_value=0):
    return _call_calc(calc, "pivot", data,
                      index=[index] if isinstance(index, str) else index,
                      columns=[columns] if columns else None,
                      values=values, aggfunc=aggfunc, fill_value=fill_value)


def create_langchain_tools(calc: Optional[EasyCalc] = None) -> List[StructuredTool]:
    """
    Create LangChain tools from the EasyCalc instance.

    Args:
        calc: EasyCalc instance. If None, creates a new one.

    Returns:
        List of LangChain StructuredTool objects.
    """
    if calc is None:
        calc = EasyCalc()

    tools = []

    # Arithmetic tool
    tools.append(StructuredTool.from_function(
        func=lambda expression=None, a=None, b=None, operation=None:
            _arithmetic_wrapper(calc, expression, a, b, operation),
        name="calculator",
        description="执行数学计算。输入数学表达式如'2+3*4'，或提供a,b,operation进行二元运算。",
        args_schema=ArithmeticInput
    ))

    # Statistics tool
    tools.append(StructuredTool.from_function(
        func=lambda data, columns=None, operations="mean,sum", group_by=None:
            _statistics_wrapper(calc, data, columns, operations, group_by),
        name="statistics",
        description="对数据进行统计分析，计算均值、总和、标准差等。支持分组统计。",
        args_schema=StatisticsInput
    ))

    # Aggregate tool
    tools.append(StructuredTool.from_function(
        func=lambda data, what=None, columns=None, operations=None, group_by=None:
            _aggregate_wrapper(calc, data, what, columns, operations, group_by),
        name="aggregate",
        description="对数据进行聚合计算，支持自然语言描述如'按部门求和销售额'。",
        args_schema=AggregateInput
    ))

    # Filter calc tool
    tools.append(StructuredTool.from_function(
        func=lambda data, condition, calculate=None, columns=None, operations=None:
            _filter_calc_wrapper(calc, data, condition, calculate, columns, operations),
        name="filter_calc",
        description="筛选数据并计算统计值。",
        args_schema=FilterCalcInput
    ))

    # Timeseries tool
    tools.append(StructuredTool.from_function(
        func=lambda data, operation, date_col=None, value_col=None, window=3:
            _timeseries_wrapper(calc, data, operation, date_col, value_col, window),
        name="timeseries",
        description="时间序列分析：移动平均、增长率、累计和、同比环比。",
        args_schema=TimeseriesInput
    ))

    # Unit convert tool
    tools.append(StructuredTool.from_function(
        func=lambda value, from_unit, to_unit:
            _unit_convert_wrapper(calc, value, from_unit, to_unit),
        name="unit_convert",
        description="单位转换，支持长度、重量、温度。",
        args_schema=UnitConvertInput
    ))

    # Date calc tool
    tools.append(StructuredTool.from_function(
        func=lambda start=None, end=None, date=None, days=None, birth_date=None,
               date_for_dow=None, reference_date=None:
            _date_calc_wrapper(calc, start, end, date, days, birth_date, date_for_dow, reference_date),
        name="date_calc",
        description="日期计算：日期差、日期加减、年龄、星期几。",
        args_schema=DateCalcInput
    ))

    # Describe tool
    tools.append(StructuredTool.from_function(
        func=lambda data, percentiles="0.25,0.5,0.75", include="all":
            _describe_wrapper(calc, data, percentiles, include),
        name="describe",
        description="生成数据的描述性统计摘要。",
        args_schema=DescribeInput
    ))

    # Correlation tool
    tools.append(StructuredTool.from_function(
        func=lambda data, method="pearson", columns=None:
            _correlation_wrapper(calc, data, method, columns),
        name="correlation",
        description="计算变量之间的相关系数矩阵。",
        args_schema=CorrelationInput
    ))

    # Pivot tool
    tools.append(StructuredTool.from_function(
        func=lambda data, index, values, columns=None, aggfunc="mean", fill_value=0:
            _pivot_wrapper(calc, data, index, values, columns, aggfunc, fill_value),
        name="pivot",
        description="创建数据透视表。",
        args_schema=PivotInput
    ))

    return tools


def get_langchain_tools(calc: Optional[EasyCalc] = None) -> List[StructuredTool]:
    """Get all LangChain tools (alias for create_langchain_tools)."""
    return create_langchain_tools(calc)