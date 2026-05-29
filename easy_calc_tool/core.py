#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author : jiaojiao
# @Time : 2026/5/29 17:39


import logging
import hashlib
import re
from collections import OrderedDict
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional, Union
import warnings

import pandas as pd
import numpy as np

from .exceptions import CalculationError, InvalidParameterError, ToolNotFoundError
from .config import settings
from .data_handler import DataHandler
from .parser import parser

logger = logging.getLogger(__name__)


class EasyCalc:
	"""
	Flexible calculation toolbox designed for LLM Function Calling.

	This class provides a unified interface for various calculation operations,
	with support for natural language parameters and multiple data formats.

	Examples:
		>>> calc = EasyCalc()
		>>> result = calc.calculate("arithmetic", None, expression="2+3")
		>>> print(result["result"])
		5
	"""

	def __init__(self, config: Optional[Dict] = None):
		"""
		Initialize the calculator.

		Args:
			config: Configuration options (cache_enabled, precision, timeout, etc.)
		"""
		self.config = {**settings.to_dict(), **(config or {})}
		self.data_handler = DataHandler(self.config)
		self._cache = OrderedDict()

		# Register all available tools
		self._tools = {
			"arithmetic": self._arithmetic,
			"statistics": self._statistics,
			"aggregate": self._aggregate,
			"filter_calc": self._filter_calc,
			"timeseries": self._timeseries,
			"unit_convert": self._unit_convert,
			"date_calc": self._date_calc,
			"describe": self._describe,
			"correlation": self._correlation,
			"pivot": self._pivot,
		}
		# core.py 第 60-70 行左右

		# Setup logging
		log_level = self.config.get("log_level", "INFO")
		log_format = self.config.get("log_format", "%(asctime)s - %(name)s - %(levelname)s - %(message)s")

		logging.basicConfig(
			level=getattr(logging, log_level),
			format=log_format
		)

		logger.info(f"EasyCalc initialized with {len(self._tools)} tools")

	@property
	def available_tools(self) -> List[str]:
		"""Return list of available tool names."""
		return list(self._tools.keys())

	def calculate(self, tool: str, data: Any, **kwargs) -> Dict:
		"""Main calculation entry point."""
		if tool not in self._tools:
			raise ToolNotFoundError(f"Unknown tool: {tool}. Available: {self.available_tools}")

		try:
			# Check cache
			cache_key = None
			if self.config["cache_enabled"]:
				cache_key = self._generate_cache_key(tool, data, kwargs)
				if cache_key in self._cache:
					logger.debug(f"Cache hit for {tool}")
					result = self._cache[cache_key]
					self._cache.move_to_end(cache_key)
					return result

			# Parse data (if needed)
			df = None
			if tool not in ["arithmetic", "unit_convert", "date_calc"]:
				df = self.data_handler.parse(data)

			# Execute tool
			result = self._tools[tool](df, **kwargs)

			# 确保 result 是字典
			if result is None:
				result = {"success": False, "error": f"Tool {tool} returned None"}

			# 如果结果中没有 success 字段，默认成功
			if "success" not in result:
				result["success"] = True

			# 只在成功时添加 metadata
			if result.get("success", True):
				result["_metadata"] = {
					"tool": tool,
					"success": True,
					"timestamp": datetime.now().isoformat(),
					"config": {k: v for k, v in self.config.items() if not callable(v)}
				}

			# Cache result
			if self.config["cache_enabled"] and cache_key and result.get("success", True):
				self._add_to_cache(cache_key, result)

			logger.info(f"Successfully executed {tool}")
			return result

		except (InvalidParameterError, CalculationError) as e:
			logger.error(f"Error in {tool}: {str(e)}")
			return {
				"success": False,
				"error": str(e),
				"error_type": type(e).__name__,
				"tool": tool
			}
		except Exception as e:
			logger.exception(f"Unexpected error in {tool}")
			return {
				"success": False,
				"error": f"Unexpected error: {str(e)}",
				"error_type": "UnexpectedError",
				"tool": tool
			}

	def execute_tool(tool_name: str, arguments: dict) -> dict:
		"""Execute a tool call (convenience function)."""
		calc = EasyCalc()
		return calc.calculate(tool_name, **arguments)

	def _generate_cache_key(self, tool: str, data: Any, kwargs: Dict) -> str:
		"""Generate cache key from tool name, data, and parameters."""
		import hashlib

		data_str = ""
		if data is not None:
			if isinstance(data, pd.DataFrame):
				# 修复：使用 pandas 2.0+ 兼容的方式
				try:
					# pandas 2.0+ 方式
					from pandas.util import hash_pandas_object
					data_str = hashlib.md5(hash_pandas_object(data).values.tobytes()).hexdigest()
				except ImportError:
					# 降级方案
					data_str = hashlib.md5(str(data.shape).encode() +
					                       str(data.columns.tolist()).encode()).hexdigest()
			else:
				data_str = str(data)

		key_str = f"{tool}_{data_str}_{str(sorted(kwargs.items()))}"
		return hashlib.md5(key_str.encode()).hexdigest()

	def _add_to_cache(self, key: str, value: Dict):
		"""Add item to cache with LRU eviction."""
		if key in self._cache:
			self._cache.move_to_end(key)
		else:
			if len(self._cache) >= self.config["cache_max_size"]:
				self._cache.popitem(last=False)
			self._cache[key] = value

	def get_cache_size(self) -> int:
		"""Get current cache size."""
		return len(self._cache)

	def clear_cache(self):
		"""Clear all cached results."""
		self._cache.clear()
		logger.info("Cache cleared")

	def get_stats(self) -> Dict:
		"""Get statistics about the calculator instance."""
		return {
			"tools_count": len(self._tools),
			"cache_size": len(self._cache),
			"cache_max_size": self.config["cache_max_size"],
			"cache_enabled": self.config["cache_enabled"],
			"available_tools": self.available_tools,
		}

	# ========== Tool Implementations ==========

	def _arithmetic(self, df: Optional[pd.DataFrame] = None, **kwargs) -> Dict:
		"""Basic arithmetic operations."""
		import numexpr as ne

		expression = kwargs.get('expression')
		a = kwargs.get('a')
		b = kwargs.get('b')
		operation = kwargs.get('operation')

		# 处理表达式
		if expression:
			try:
				# 预检查除零
				if '/0' in expression.replace(' ', ''):
					return {
						"result": float('inf'),
						"expression": expression,
						"type": "float"
					}

				result = ne.evaluate(expression)
				if hasattr(result, 'item'):
					result = result.item()

				# 应用精度
				if isinstance(result, float):
					result = round(result, self.config.get("precision", 2))
					if result.is_integer():
						result = int(result)

				return {
					"result": result,
					"expression": expression,
					"type": type(result).__name__
				}
			except Exception as e:
				# 检查是否是除零错误
				if 'division by zero' in str(e):
					return {
						"result": float('inf'),
						"expression": expression,
						"type": "float"
					}
				# 返回错误信息而不是抛出异常
				return {
					"success": False,
					"error": f"Invalid expression: {expression}, error: {str(e)}",
					"error_type": "CalculationError"
				}

		# 处理二元运算
		if a is not None and b is not None and operation:
			ops = {
				'+': lambda x, y: x + y,
				'-': lambda x, y: x - y,
				'*': lambda x, y: x * y,
				'/': lambda x, y: x / y if y != 0 else float('inf'),
				'**': lambda x, y: x ** y,
				'%': lambda x, y: x % y,
			}

			if operation not in ops:
				return {
					"success": False,
					"error": f"Unsupported operation: {operation}",
					"error_type": "InvalidParameterError"
				}

			result = ops[operation](a, b)
			if isinstance(result, float):
				result = round(result, self.config.get("precision", 2))
				if result.is_integer():
					result = int(result)

			return {
				"result": result,
				"operation": f"{a}{operation}{b}",
				"type": type(result).__name__
			}

		# 参数不足
		return {
			"success": False,
			"error": "Need either 'expression' or ('a', 'b', 'operation')",
			"error_type": "InvalidParameterError"
		}


	def _statistics(self, df: pd.DataFrame, **kwargs) -> Dict:
		"""Statistical analysis."""
		result = {}

		columns = kwargs.get('columns', 'all')
		operations = kwargs.get('operations', 'all')
		group_by = kwargs.get('group_by')

		# Parse natural language if needed
		if isinstance(operations, str) and any(c in operations for c in ['和', '平均', '总']):
			parsed = parser.parse_calculation(operations)
			operations = parsed.get("operations", ["mean", "sum"])
			if not group_by and parsed.get("group_by"):
				group_by = parsed["group_by"]

		# Select numeric columns
		if columns == 'all' or columns is None:
			columns = df.select_dtypes(include=[np.number]).columns.tolist()
			if not columns:
				raise InvalidParameterError("No numeric columns found")
		elif isinstance(columns, str):
			columns = [columns] if columns in df.columns else self._find_similar_columns(df, columns)
		elif isinstance(columns, list):
			columns = [c for c in columns if c in df.columns]

		# Parse operations
		if operations == 'all' or operations is None:
			operations = ['count', 'mean', 'std', 'min', 'max']
		elif isinstance(operations, str):
			operations = self._parse_operation_string(operations)

		# Compute statistics
		if group_by:
			if isinstance(group_by, str):
				group_by = [group_by]
			result = self._grouped_statistics(df, columns, operations, group_by)
		else:
			result = self._overall_statistics(df, columns, operations)

		result["summary"] = self._generate_summary(result, columns, operations, group_by)
		return result

	def _overall_statistics(self, df: pd.DataFrame, columns: List, operations: List) -> Dict:
		"""Compute overall statistics."""
		stats = {}
		for col in columns:
			col_stats = {}
			for op in operations:
				try:
					if op == 'count':
						col_stats['count'] = int(df[col].count())
					elif op == 'mean':
						col_stats['mean'] = float(df[col].mean())
					elif op == 'sum':
						col_stats['sum'] = float(df[col].sum())
					elif op == 'std':
						col_stats['std'] = float(df[col].std())
					elif op == 'var':
						col_stats['var'] = float(df[col].var())
					elif op == 'min':
						col_stats['min'] = float(df[col].min())
					elif op == 'max':
						col_stats['max'] = float(df[col].max())
					elif op == 'median':
						col_stats['median'] = float(df[col].median())
					elif op == 'skew':
						col_stats['skew'] = float(df[col].skew())
					elif op == 'kurt':
						col_stats['kurtosis'] = float(df[col].kurtosis())
				except Exception as e:
					col_stats[op] = None
					logger.warning(f"Failed to compute {op} for {col}: {e}")

			# Apply precision
			for k, v in col_stats.items():
				if isinstance(v, float):
					col_stats[k] = round(v, self.config["precision"])

			stats[col] = col_stats

		return {"statistics": stats}

	def _grouped_statistics(self, df: pd.DataFrame, columns: List,
	                        operations: List, group_by: List) -> Dict:
		"""Compute grouped statistics."""
		grouped = df.groupby(group_by)
		result = {}

		for name, group in grouped:
			# 将元组转换为字符串
			if isinstance(name, tuple):
				group_name = '_'.join(str(x) for x in name)
			else:
				group_name = str(name)

			stats = {}
			for col in columns:
				col_stats = {}
				for op in operations:
					if op == 'count':
						col_stats['count'] = int(group[col].count())
					elif op == 'mean':
						col_stats['mean'] = float(group[col].mean())
					elif op == 'sum':
						col_stats['sum'] = float(group[col].sum())
					elif op == 'std':
						col_stats['std'] = float(group[col].std())
					elif op == 'min':
						col_stats['min'] = float(group[col].min())
					elif op == 'max':
						col_stats['max'] = float(group[col].max())
					elif op == 'median':
						col_stats['median'] = float(group[col].median())

				for k, v in col_stats.items():
					if isinstance(v, float):
						col_stats[k] = round(v, self.config["precision"])

				stats[col] = col_stats
			result[group_name] = stats

		return {"grouped": result, "group_by": group_by}

	def _aggregate(self, df: pd.DataFrame, **kwargs) -> Dict:
		"""Flexible aggregation."""
		what = kwargs.get('what')
		columns = kwargs.get('columns')
		operations = kwargs.get('operations')
		group_by = kwargs.get('group_by')

		# Natural language parsing
		if what and not columns and not operations:
			parsed = parser.parse_calculation(what)
			columns = parsed.get("columns") or "all"
			operations = parsed.get("operations") or ["sum"]
			if not group_by and parsed.get("group_by"):
				group_by = parsed["group_by"]

		# Parse columns
		if columns == 'all' or columns is None:
			columns = df.select_dtypes(include=[np.number]).columns.tolist()
		elif isinstance(columns, str):
			columns = [columns]

		# Parse operations
		if operations is None:
			operations = ['sum']
		elif isinstance(operations, str):
			operations = self._parse_operation_string(operations)

		# Build aggregation dictionary
		agg_dict = {}
		for col in columns:
			for op in operations:
				col_name = f"{col}_{op}" if len(operations) > 1 else col
				agg_dict[col_name] = (col, op)

		# Execute aggregation
		if group_by:
			if isinstance(group_by, str):
				group_by = [group_by]
			result_df = df.groupby(group_by).agg(**agg_dict).reset_index()
			return {
				"grouped_result": result_df.to_dict(orient='records'),
				"group_by": group_by,
				"shape": result_df.shape
			}
		else:
			# result_df = df.agg(**agg_dict).to_frame().T
			result_df = pd.DataFrame(df.agg(**agg_dict)).T
			# Convert numpy types to Python types
			record = result_df.to_dict(orient='records')[0]
			for k, v in record.items():
				if hasattr(v, 'item'):
					record[k] = v.item()
			return {"result": record, "shape": result_df.shape}

	def _filter_calc(self, df: pd.DataFrame, **kwargs) -> Dict:
		"""Filter data and compute statistics."""
		condition = kwargs.get('condition')
		calculate = kwargs.get('calculate')
		columns = kwargs.get('columns')

		if not condition:
			raise InvalidParameterError("'condition' is required for filter_calc")

		# Apply filter
		try:
			filtered_df = df.query(condition)
		except Exception as e:
			raise InvalidParameterError(f"Invalid filter condition: {condition}, error: {str(e)}")

		result = {
			"filtered_count": len(filtered_df),
			"original_count": len(df),
			"filter_condition": condition,
			"filtered_preview": filtered_df.head(10).to_dict(orient='records')
		}

		# Compute statistics on filtered data
		if calculate or columns:
			if calculate and isinstance(calculate, str):
				parsed = parser.parse_calculation(calculate)
				columns = parsed.get("columns") or (columns if columns else "all")
				operations = parsed.get("operations") or ["sum"]
			else:
				operations = kwargs.get('operations', ['sum'])

			# Get statistics
			stats_result = self._statistics(filtered_df, columns=columns, operations=operations)
			result["statistics"] = stats_result.get("statistics", stats_result)

		return result

	def _timeseries(self, df: pd.DataFrame, **kwargs) -> Dict:
		"""Time series analysis."""
		date_col = kwargs.get('date_col')
		value_col = kwargs.get('value_col')
		operation = kwargs.get('operation')

		if not date_col:
			# Auto-detect date column
			for col in df.columns:
				try:
					pd.to_datetime(df[col])
					date_col = col
					break
				except:
					continue
			if not date_col:
				raise InvalidParameterError("No date column found")

		if not value_col:
			# Auto-detect numeric column
			numeric_cols = df.select_dtypes(include=[np.number]).columns
			if len(numeric_cols) == 0:
				raise InvalidParameterError("No numeric column found")
			value_col = numeric_cols[0]

		# Ensure date column is datetime
		df[date_col] = pd.to_datetime(df[date_col])
		df = df.sort_values(date_col)

		result = {"operation": operation, "date_col": date_col, "value_col": value_col}

		if operation == 'moving_average':
			window = kwargs.get('window', 3)
			df['moving_avg'] = df[value_col].rolling(window=window).mean()
			result['result'] = df[[date_col, value_col, 'moving_avg']].dropna().to_dict(orient='records')
			result['window'] = window

		elif operation == 'growth_rate':
			df['growth_rate'] = df[value_col].pct_change() * 100
			result['result'] = df[[date_col, value_col, 'growth_rate']].to_dict(orient='records')
			result['average_growth'] = float(df['growth_rate'].mean())

		elif operation == 'cumulative':
			df['cumulative'] = df[value_col].cumsum()
			result['result'] = df[[date_col, value_col, 'cumulative']].to_dict(orient='records')
			result['total'] = float(df['cumulative'].iloc[-1])

		elif operation == 'yoy':
			df['year'] = df[date_col].dt.year
			df['month'] = df[date_col].dt.month
			df['yoy'] = df.groupby('month')[value_col].pct_change() * 100
			result['result'] = df.dropna(subset=['yoy'])[[date_col, value_col, 'yoy']].to_dict(orient='records')

		elif operation == 'mom':
			df['mom'] = df[value_col].pct_change() * 100
			result['result'] = df[[date_col, value_col, 'mom']].to_dict(orient='records')

		else:
			raise InvalidParameterError(f"Unsupported operation: {operation}. "
			                            f"Supported: moving_average, growth_rate, cumulative, yoy, mom")

		return result

	def _unit_convert(self, df: Optional[pd.DataFrame] = None, **kwargs) -> Dict:
		"""Unit conversion for length, weight, and temperature."""
		value = kwargs.get('value')
		from_unit = kwargs.get('from_unit', '').lower()
		to_unit = kwargs.get('to_unit', '').lower()

		if value is None:
			raise InvalidParameterError("'value' is required")

		# 定义温度转换函数
		def c_to_f(c):
			return c * 9 / 5 + 32

		def f_to_c(f):
			return (f - 32) * 5 / 9

		def c_to_k(c):
			return c + 273.15

		def k_to_c(k):
			return k - 273.15

		# 转换映射表 - 使用 lambda 函数
		conversions = {
			# ========== Length ==========
			('km', 'm'): lambda v: v * 1000,
			('m', 'km'): lambda v: v * 0.001,
			('km', 'mile'): lambda v: v * 0.621371,
			('mile', 'km'): lambda v: v * 1.60934,
			('m', 'ft'): lambda v: v * 3.28084,
			('ft', 'm'): lambda v: v * 0.3048,
			('cm', 'inch'): lambda v: v * 0.393701,
			('inch', 'cm'): lambda v: v * 2.54,
			('km', 'ft'): lambda v: v * 3280.84,
			('ft', 'km'): lambda v: v * 0.0003048,
			('m', 'inch'): lambda v: v * 39.3701,
			('inch', 'm'): lambda v: v * 0.0254,

			# ========== Weight ==========
			('kg', 'g'): lambda v: v * 1000,
			('g', 'kg'): lambda v: v * 0.001,
			('kg', 'lb'): lambda v: v * 2.20462,
			('lb', 'kg'): lambda v: v * 0.453592,
			('g', 'oz'): lambda v: v * 0.035274,
			('oz', 'g'): lambda v: v * 28.3495,
			('kg', 'oz'): lambda v: v * 35.274,
			('oz', 'kg'): lambda v: v * 0.0283495,
			('lb', 'oz'): lambda v: v * 16,
			('oz', 'lb'): lambda v: v * 0.0625,

			# ========== Temperature ==========
			('c', 'f'): c_to_f,
			('f', 'c'): f_to_c,
			('c', 'k'): c_to_k,
			('k', 'c'): k_to_c,
		}

		key = (from_unit, to_unit)
		if key in conversions:
			try:
				result_value = conversions[key](value)
			except Exception as e:
				return {
					"success": False,
					"error": f"Conversion failed: {str(e)}",
					"from_unit": from_unit,
					"to_unit": to_unit
				}

			# 应用精度
			result_value = round(result_value, self.config.get("precision", 2))

			# 格式化结果（如果是整数，去掉 .0）
			if isinstance(result_value, float) and result_value.is_integer():
				result_value = int(result_value)

			return {
				"success": True,
				"result": result_value,
				"conversion": f"{value} {from_unit} = {result_value} {to_unit}",
				"from_unit": from_unit,
				"to_unit": to_unit
			}

		# 尝试反向转换（仅适用于线性转换）
		reverse_key = (to_unit, from_unit)
		if reverse_key in conversions:
			# 对于非线性转换（如温度），不进行反向
			if from_unit in ['c', 'f', 'k'] and to_unit in ['c', 'f', 'k']:
				return {
					"success": False,
					"error": f"Unsupported conversion: {from_unit} -> {to_unit}. Please use forward direction.",
					"from_unit": from_unit,
					"to_unit": to_unit
				}

			try:
				# 对于线性转换，可以用 1/因子 反向
				conv = conversions[reverse_key]
				# 简化：直接返回不支持，让用户使用正向
				return {
					"success": False,
					"error": f"Unsupported conversion: {from_unit} -> {to_unit}. Try {to_unit} -> {from_unit} instead.",
					"from_unit": from_unit,
					"to_unit": to_unit
				}
			except:
				pass

		return {
			"success": False,
			"error": f"Unsupported conversion: {from_unit} -> {to_unit}. Supported units: km, m, mile, ft, cm, inch, kg, g, lb, oz, c, f, k",
			"from_unit": from_unit,
			"to_unit": to_unit
		}
	def _date_calc(self, df: Optional[pd.DataFrame] = None, **kwargs) -> Dict:
		"""Date calculations."""
		result = {}

		# Date difference
		start = kwargs.get('start')
		end = kwargs.get('end')
		if start and end:
			start_date = pd.to_datetime(start)
			end_date = pd.to_datetime(end)
			delta = end_date - start_date
			result['days_diff'] = delta.days
			result['weeks_diff'] = delta.days / 7
			result['months_diff'] = delta.days / 30.44

		# Date addition/subtraction
		date = kwargs.get('date')
		days = kwargs.get('days')
		if date and days:
			date_obj = pd.to_datetime(date)
			new_date = date_obj + timedelta(days=days)
			result['new_date'] = new_date.strftime(self.config["default_date_format"])

		# Age calculation
		birth_date = kwargs.get('birth_date')
		if birth_date:
			birth = pd.to_datetime(birth_date)
			today = kwargs.get('reference_date')
			if today:
				today = pd.to_datetime(today)
			else:
				today = pd.Timestamp.now()
			age = today.year - birth.year - ((today.month, today.day) < (birth.month, birth.day))
			result['age'] = age

		# Day of week
		date_str = kwargs.get('date_for_dow')
		if date_str:
			date_obj = pd.to_datetime(date_str)
			result['day_of_week'] = date_obj.strftime('%A')
			result['day_of_week_number'] = date_obj.dayofweek

		if not result:
			raise InvalidParameterError("Need at least one of: (start,end), (date,days), birth_date")

		return result

	def _describe(self, df: pd.DataFrame, **kwargs) -> Dict:
		"""Generate descriptive statistics summary."""
		percentiles = kwargs.get('percentiles', [.25, .5, .75])
		include = kwargs.get('include', 'all')

		if include == 'all':
			include = None

		description = df.describe(percentiles=percentiles, include=include)

		# 直接返回描述性统计，metadata 会在 calculate 中添加
		return description.to_dict()

	def _correlation(self, df: pd.DataFrame, **kwargs) -> Dict:
		"""Calculate correlation matrix."""
		method = kwargs.get('method', 'pearson')
		columns = kwargs.get('columns')

		if columns:
			if isinstance(columns, str):
				columns = [columns]
			df = df[columns]

		# Select only numeric columns
		numeric_df = df.select_dtypes(include=[np.number])

		if numeric_df.empty:
			raise InvalidParameterError("No numeric columns for correlation")

		corr_matrix = numeric_df.corr(method=method)

		return {
			"correlation_matrix": corr_matrix.to_dict(),
			"method": method,
			"variables": numeric_df.columns.tolist()
		}

	def _pivot(self, df: pd.DataFrame, **kwargs) -> Dict:
		"""Create pivot table."""
		index = kwargs.get('index')
		columns = kwargs.get('columns')
		values = kwargs.get('values')
		aggfunc = kwargs.get('aggfunc', 'mean')

		if not index or not values:
			raise InvalidParameterError("'index' and 'values' are required")

		pivot_table = pd.pivot_table(
			df,
			values=values,
			index=index,
			columns=columns,
			aggfunc=aggfunc,
			fill_value=kwargs.get('fill_value', 0)
		)

		return {
			"pivot_table": pivot_table.to_dict(),
			"index": index,
			"columns": columns,
			"values": values,
			"aggfunc": aggfunc,
			"shape": pivot_table.shape
		}

	# ========== Helper Methods ==========

	def _find_similar_columns(self, df: pd.DataFrame, keyword: str) -> List[str]:
		"""Find columns similar to keyword."""
		keyword_lower = keyword.lower()
		matches = [col for col in df.columns if keyword_lower in col.lower()]
		if matches:
			return matches
		raise InvalidParameterError(f"Column '{keyword}' not found. Available: {df.columns.tolist()}")

	def _parse_operation_string(self, ops_str: str) -> List[str]:
		"""Parse operation string like 'mean,sum,std'."""
		ops_map = {
			'sum': 'sum', '总和': 'sum', '合计': 'sum',
			'mean': 'mean', '平均': 'mean', '平均值': 'mean',
			'count': 'count', '计数': 'count',
			'std': 'std', '标准差': 'std',
			'var': 'var', '方差': 'var',
			'min': 'min', '最小': 'min',
			'max': 'max', '最大': 'max',
			'median': 'median', '中位数': 'median',
		}

		# Split by common separators
		parts = re.split(r'[,，\s]+', ops_str)
		result = []
		for part in parts:
			if part in ops_map:
				result.append(ops_map[part])
			elif part in ops_map.values():
				result.append(part)

		return result if result else ['mean', 'sum']

	def _generate_summary(self, result: Dict, columns: List, operations: List, group_by: Any) -> str:
		"""Generate human-readable summary."""
		parts = []
		if group_by:
			parts.append(f"Grouped by {group_by}")
		parts.append(f"Analyzed {len(columns)} column(s)")
		parts.append(f"Computed {len(operations)} statistic(s)")
		return " | ".join(parts)

if __name__ == "__main__":
	calc = EasyCalc()
	print(calc.calculate("123 + 456"))