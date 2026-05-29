#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author : jiaojiao
# @Time : 2026/5/29 17:21

"""
Function Call tool definitions for LLM integration.
Provides OpenAI-compatible tool schemas for all calculation tools.
"""

from typing import List, Dict, Any

# Complete tool schemas for OpenAI/Anthropic function calling
TOOLS_SCHEMA: List[Dict[str, Any]] = [
    {
        "type": "function",
        "function": {
            "name": "arithmetic",
            "description": "执行基础数学计算。支持表达式计算（如 '2+3*4'）或二元运算（如 a=10, b=3, operation='*'）。",
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {
                        "type": "string",
                        "description": "数学表达式，例如 '100 * 2 + 5'、'sqrt(16)'、'sin(30)'"
                    },
                    "a": {
                        "type": "number",
                        "description": "二元运算的第一个操作数"
                    },
                    "b": {
                        "type": "number",
                        "description": "二元运算的第二个操作数"
                    },
                    "operation": {
                        "type": "string",
                        "enum": ["+", "-", "*", "/", "**", "%"],
                        "description": "二元运算的操作符"
                    }
                },
                "additionalProperties": False
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "statistics",
            "description": "对数据进行统计分析。支持单列、多列或全部数值列的统计计算，支持分组统计。",
            "parameters": {
                "type": "object",
                "properties": {
                    "data": {
                        "type": "string",
                        "description": "数据，支持CSV格式字符串、JSON数组字符串、或文件路径"
                    },
                    "columns": {
                        "anyOf": [
                            {"type": "string"},
                            {"type": "array", "items": {"type": "string"}},
                            {"type": "null"}
                        ],
                        "description": "要分析的列名，可以是单列名、列名列表，或不填(表示全部数值列)",
                        "default": None
                    },
                    "operations": {
                        "anyOf": [
                            {"type": "string"},
                            {"type": "array", "items": {"type": "string"}},
                            {"type": "null"}
                        ],
                        "description": "要计算的操作，支持: sum, mean, count, std, var, min, max, median, skew, kurt",
                        "default": "all"
                    },
                    "group_by": {
                        "anyOf": [
                            {"type": "string"},
                            {"type": "array", "items": {"type": "string"}},
                            {"type": "null"}
                        ],
                        "description": "分组字段，用于分组统计",
                        "default": None
                    }
                },
                "required": ["data"],
                "additionalProperties": False
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "aggregate",
            "description": "对数据进行聚合计算。支持自然语言描述，如'按部门求和销售额'、'计算平均利润'。",
            "parameters": {
                "type": "object",
                "properties": {
                    "data": {
                        "type": "string",
                        "description": "数据，支持CSV格式字符串、JSON数组字符串、或文件路径"
                    },
                    "what": {
                        "type": "string",
                        "description": "自然语言描述要计算什么，例如 '按部门求和销售额'、'计算每个产品的平均销量'"
                    },
                    "columns": {
                        "anyOf": [
                            {"type": "string"},
                            {"type": "array", "items": {"type": "string"}},
                            {"type": "null"}
                        ],
                        "description": "要聚合的列名",
                        "default": None
                    },
                    "operations": {
                        "anyOf": [
                            {"type": "string"},
                            {"type": "array", "items": {"type": "string"}},
                            {"type": "null"}
                        ],
                        "description": "聚合操作: sum, mean, count, min, max",
                        "default": None
                    },
                    "group_by": {
                        "anyOf": [
                            {"type": "string"},
                            {"type": "array", "items": {"type": "string"}},
                            {"type": "null"}
                        ],
                        "description": "分组字段",
                        "default": None
                    }
                },
                "required": ["data"],
                "additionalProperties": False
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "filter_calc",
            "description": "筛选数据并计算统计值。支持条件筛选和筛选后的计算。",
            "parameters": {
                "type": "object",
                "properties": {
                    "data": {
                        "type": "string",
                        "description": "数据，支持CSV格式字符串、JSON数组字符串、或文件路径"
                    },
                    "condition": {
                        "type": "string",
                        "description": "筛选条件，如 '销售额 > 1000'、'部门 == \"销售部\"'"
                    },
                    "calculate": {
                        "type": "string",
                        "description": "要计算的内容，如 '利润总和'、'平均销售额'"
                    },
                    "columns": {
                        "anyOf": [
                            {"type": "string"},
                            {"type": "array", "items": {"type": "string"}},
                            {"type": "null"}
                        ],
                        "description": "要计算的列名",
                        "default": None
                    },
                    "operations": {
                        "anyOf": [
                            {"type": "string"},
                            {"type": "array", "items": {"type": "string"}},
                            {"type": "null"}
                        ],
                        "description": "计算操作: sum, mean, count, min, max",
                        "default": None
                    }
                },
                "required": ["data", "condition"],
                "additionalProperties": False
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "timeseries",
            "description": "时间序列计算。支持移动平均、增长率、累计和、同比、环比等。",
            "parameters": {
                "type": "object",
                "properties": {
                    "data": {
                        "type": "string",
                        "description": "时间序列数据，支持CSV格式字符串或JSON数组字符串"
                    },
                    "date_col": {
                        "type": "string",
                        "description": "日期列名，如不提供将自动检测"
                    },
                    "value_col": {
                        "type": "string",
                        "description": "数值列名，如不提供将自动检测"
                    },
                    "operation": {
                        "type": "string",
                        "enum": ["moving_average", "growth_rate", "cumulative", "yoy", "mom"],
                        "description": "操作类型: moving_average(移动平均), growth_rate(增长率), cumulative(累计和), yoy(同比增长), mom(环比增长)"
                    },
                    "window": {
                        "type": "integer",
                        "description": "移动窗口大小（仅用于moving_average）",
                        "default": 3
                    }
                },
                "required": ["data", "operation"],
                "additionalProperties": False
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "unit_convert",
            "description": "单位转换。支持长度、重量、温度等单位的转换。",
            "parameters": {
                "type": "object",
                "properties": {
                    "value": {
                        "type": "number",
                        "description": "要转换的数值"
                    },
                    "from_unit": {
                        "type": "string",
                        "description": "原始单位，支持: km, m, mile, ft, cm, inch, kg, g, lb, oz, c, f, k",
                        "examples": ["km", "kg", "c"]
                    },
                    "to_unit": {
                        "type": "string",
                        "description": "目标单位",
                        "examples": ["mile", "lb", "f"]
                    }
                },
                "required": ["value", "from_unit", "to_unit"],
                "additionalProperties": False
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "date_calc",
            "description": "日期计算。支持日期差、日期加减、年龄计算、星期几查询等。",
            "parameters": {
                "type": "object",
                "properties": {
                    "start": {
                        "type": "string",
                        "description": "开始日期，格式: YYYY-MM-DD"
                    },
                    "end": {
                        "type": "string",
                        "description": "结束日期，格式: YYYY-MM-DD"
                    },
                    "date": {
                        "type": "string",
                        "description": "基准日期，格式: YYYY-MM-DD"
                    },
                    "days": {
                        "type": "integer",
                        "description": "要增加或减少的天数"
                    },
                    "birth_date": {
                        "type": "string",
                        "description": "出生日期，用于计算年龄，格式: YYYY-MM-DD"
                    },
                    "date_for_dow": {
                        "type": "string",
                        "description": "要查询星期几的日期"
                    },
                    "reference_date": {
                        "type": "string",
                        "description": "参考日期，用于年龄计算（默认为今天）"
                    }
                },
                "additionalProperties": False
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "describe",
            "description": "生成数据的描述性统计摘要，包括计数、均值、标准差、分位数等。",
            "parameters": {
                "type": "object",
                "properties": {
                    "data": {
                        "type": "string",
                        "description": "数据，支持CSV格式字符串、JSON数组字符串、或文件路径"
                    },
                    "percentiles": {
                        "type": "array",
                        "items": {"type": "number"},
                        "description": "要计算的分位数，默认 [0.25, 0.5, 0.75]",
                        "default": [0.25, 0.5, 0.75]
                    },
                    "include": {
                        "type": "string",
                        "enum": ["all", "number", "object"],
                        "description": "要包含的列类型",
                        "default": "all"
                    }
                },
                "required": ["data"],
                "additionalProperties": False
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "correlation",
            "description": "计算变量之间的相关系数矩阵。支持皮尔逊相关系数。",
            "parameters": {
                "type": "object",
                "properties": {
                    "data": {
                        "type": "string",
                        "description": "数据，支持CSV格式字符串或JSON数组字符串"
                    },
                    "method": {
                        "type": "string",
                        "enum": ["pearson", "spearman"],
                        "description": "相关系数计算方法",
                        "default": "pearson"
                    },
                    "columns": {
                        "anyOf": [
                            {"type": "string"},
                            {"type": "array", "items": {"type": "string"}},
                            {"type": "null"}
                        ],
                        "description": "要计算相关性的列名列表",
                        "default": None
                    }
                },
                "required": ["data"],
                "additionalProperties": False
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "pivot",
            "description": "创建数据透视表，进行交叉分析。",
            "parameters": {
                "type": "object",
                "properties": {
                    "data": {
                        "type": "string",
                        "description": "数据，支持CSV格式字符串或JSON数组字符串"
                    },
                    "index": {
                        "anyOf": [
                            {"type": "string"},
                            {"type": "array", "items": {"type": "string"}}
                        ],
                        "description": "透视表的行索引字段"
                    },
                    "columns": {
                        "anyOf": [
                            {"type": "string"},
                            {"type": "array", "items": {"type": "string"}},
                            {"type": "null"}
                        ],
                        "description": "透视表的列字段",
                        "default": None
                    },
                    "values": {
                        "type": "string",
                        "description": "要聚合的值字段"
                    },
                    "aggfunc": {
                        "type": "string",
                        "enum": ["sum", "mean", "count", "min", "max"],
                        "description": "聚合函数",
                        "default": "mean"
                    },
                    "fill_value": {
                        "type": "number",
                        "description": "填充空值的数值",
                        "default": 0
                    }
                },
                "required": ["data", "index", "values"],
                "additionalProperties": False
            }
        }
    }
]


def get_tools() -> List[Dict[str, Any]]:
    """Get all tool schemas for function calling."""
    return TOOLS_SCHEMA


def get_tool_by_name(name: str) -> Dict[str, Any]:
    """Get a specific tool schema by name."""
    for tool in TOOLS_SCHEMA:
        if tool["function"]["name"] == name:
            return tool
    raise ValueError(f"Tool '{name}' not found")