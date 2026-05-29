#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author : jiaojiao
# @Time : 2026/5/29 17:39

"""
Data handling utilities for parsing various input formats.
"""

import json
import pandas as pd
import numpy as np
from typing import Any, Union, Optional, Dict, List
from io import StringIO
from pathlib import Path

from .exceptions import DataParseError


class DataHandler:
	"""Handle data parsing from various formats."""

	def __init__(self, config: Optional[Dict] = None):
		self.config = config or {}
		self.max_data_size = self.config.get("max_data_size", 10_000_000)

	def parse(self, data: Any) -> pd.DataFrame:
		"""Parse data from various formats."""
		if data is None:
			raise DataParseError("Data cannot be None")

		# Already a DataFrame
		if isinstance(data, pd.DataFrame):
			return self._validate_dataframe(data)

		# String data
		if isinstance(data, str):
			# 先判断是否是文件路径（以常见扩展名结尾或包含路径分隔符）
			if self._looks_like_file_path(data):
				try:
					return self._parse_file(data)
				except DataParseError:
					pass  # 不是有效文件，继续尝试解析内容

			# 然后尝试解析内容
			return self._parse_string(data)

		# Path object
		if isinstance(data, Path):
			return self._parse_file(data)

		# List or dict
		if isinstance(data, (list, dict)):
			return self._parse_structured(data)

		# Single value
		if isinstance(data, (int, float, bool)):
			return pd.DataFrame({"value": [data]})

		raise DataParseError(f"Unsupported data type: {type(data)}")

	def _looks_like_file_path(self, data: str) -> bool:
		"""Check if string looks like a file path."""
		# 以常见扩展名结尾
		extensions = ('.csv', '.json', '.xlsx', '.xls', '.parquet', '.txt')
		if data.lower().endswith(extensions):
			return True

		# 包含路径分隔符
		if any(c in data for c in '/\\'):
			return True

		return False
	def _parse_string(self, data: str) -> pd.DataFrame:
		"""Parse string data (CSV or JSON)."""
		data = data.strip()

		# 1. 优先尝试 JSON 解析
		try:
			import json
			json_data = json.loads(data)
			return self._parse_structured(json_data)
		except json.JSONDecodeError:
			pass

		# 2. 尝试 CSV 解析（必须有换行符和逗号）
		if '\n' in data and ',' in data:
			try:
				from io import StringIO
				return pd.read_csv(StringIO(data))
			except Exception:
				pass

		# 3. 最后尝试作为文件路径
		if len(data) < 255 and any(c in data for c in '/\\:') and '\n' not in data:
			try:
				return self._parse_file(data)
			except DataParseError:
				pass  # 如果文件不存在，继续抛出最终错误

		raise DataParseError(f"Unable to parse string as CSV, JSON, or file path: {data[:100]}...")

	def _validate_dataframe(self, df: pd.DataFrame) -> pd.DataFrame:
		"""Validate and optionally truncate large dataframes."""
		if len(df) > self.max_data_size:
			raise DataParseError(
				f"Data size ({len(df)}) exceeds maximum allowed ({self.max_data_size})"
			)
		return df

	def _parse_file(self, path: Union[str, Path]) -> pd.DataFrame:
		"""Parse data from a file."""
		path = Path(path)

		if not path.exists():
			raise DataParseError(f"File not found: {path}")

		try:
			if path.suffix.lower() == '.csv':
				return pd.read_csv(path, encoding=self.config.get("encoding", "utf-8"))
			elif path.suffix.lower() in ['.xlsx', '.xls']:
				return pd.read_excel(path)
			elif path.suffix.lower() == '.json':
				return pd.read_json(path)
			elif path.suffix.lower() == '.parquet':
				return pd.read_parquet(path)
			else:
				raise DataParseError(f"Unsupported file type: {path.suffix}")
		except Exception as e:
			raise DataParseError(f"Failed to read file {path}: {str(e)}")

	def _parse_string(self, data: str) -> pd.DataFrame:
		"""Parse string data (CSV or JSON)."""
		data = data.strip()

		# 1. 优先尝试 JSON 解析（因为 JSON 字符串可能包含冒号等字符）
		try:
			import json
			json_data = json.loads(data)
			# 成功解析为 JSON，直接返回
			return self._parse_structured(json_data)
		except json.JSONDecodeError:
			pass  # 不是有效的 JSON，继续尝试其他格式

		# 2. 尝试 CSV 解析（必须有换行符和逗号，看起来像 CSV）
		if '\n' in data and ',' in data:
			try:
				from io import StringIO
				return pd.read_csv(StringIO(data))
			except Exception:
				pass

		# 3. 尝试作为文件路径（包含路径分隔符，且看起来不像数据内容）
		if any(c in data for c in '/\\') and '\n' not in data and len(data) < 255:
			# 检查是否是常见的数据格式开头（避免误判 JSON）
			if not data.lstrip().startswith(('[', '{', '{"', '[{')):
				try:
					return self._parse_file(data)
				except DataParseError:
					pass

		raise DataParseError(f"Unable to parse string as CSV, JSON, or file path: {data[:100]}...")

	def _parse_structured(self, data: Union[List, Dict]) -> pd.DataFrame:
		"""Parse structured data (list of dicts or single dict)."""
		if isinstance(data, list):
			if not data:
				return pd.DataFrame()

			# 检查数据大小
			if len(data) > self.max_data_size:
				raise DataParseError(
					f"Data size ({len(data)}) exceeds maximum allowed ({self.max_data_size})"
				)

			if all(isinstance(item, dict) for item in data):
				return pd.DataFrame(data)
			return pd.DataFrame({"value": data})

		if isinstance(data, dict):
			return pd.DataFrame([data])

		raise DataParseError(f"Unsupported structured data type: {type(data)}")

	def to_json(self, df: pd.DataFrame, orient: str = 'records') -> str:
		"""Convert DataFrame to JSON string."""
		return df.to_json(orient=orient, force_ascii=False)

	def to_csv(self, df: pd.DataFrame) -> str:
		"""Convert DataFrame to CSV string."""
		return df.to_csv(index=False)

	def preview(self, df: pd.DataFrame, n: int = 5) -> Dict:
		"""Get preview of DataFrame."""
		return {
			"head": df.head(n).to_dict(orient='records'),
			"shape": df.shape,
			"columns": df.columns.tolist(),
			"dtypes": df.dtypes.astype(str).to_dict()
		}