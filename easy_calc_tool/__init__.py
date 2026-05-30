#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author : jiaojiao
# @Time : 2026/5/29 17:22

"""
Easy Calc Tool - A flexible calculation toolbox designed for LLM Function Calling.

This package provides a comprehensive set of calculation tools that can be easily
integrated with LLM applications through function calling interfaces.

Example:
    >>> from easy_calc_tool import EasyCalc
    >>> calc = EasyCalc()
    >>> result = calc.calculate("arithmetic", None, expression="2+3")
    >>> print(result["result"])
    5
"""

from .core import EasyCalc
from .exceptions import (
	EasyCalcError,
	CalculationError,
	DataParseError,
	InvalidParameterError,
	ToolNotFoundError,
	SecurityError,
)
from .version import __version__, __version_info__

# LangChain integration (optional)
try:
	from .integration_langchain import get_langchain_tools, create_langchain_tools

	__all__ = [
		"EasyCalc",
		"EasyCalcError",
		"CalculationError",
		"DataParseError",
		"InvalidParameterError",
		"ToolNotFoundError",
		"SecurityError",
		"get_langchain_tools",
		"create_langchain_tools",
		"__version__",
		"__version_info__",
	]
except ImportError:
	# LangChain dependencies not installed
	__all__ = [
		"EasyCalc",
		"EasyCalcError",
		"CalculationError",
		"DataParseError",
		"InvalidParameterError",
		"ToolNotFoundError",
		"SecurityError",
		"__version__",
		"__version_info__",
	]
