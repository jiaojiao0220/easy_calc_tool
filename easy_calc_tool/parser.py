#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author : jiaojiao
# @Time : 2026/5/29 17:39

"""
Natural language parser for flexible parameter handling.
"""

import re
from typing import Dict, List, Optional, Any, Tuple


class NaturalLanguageParser:
	"""Parse natural language expressions for calculations."""

	# 更新 OP_MAPPINGS
	OP_MAPPINGS = {
		'sum': ['sum', '总和', '合计', '总计', '加起来', '总'],
		'mean': ['mean', 'average', 'avg', '平均', '均值', '平均数'],
		'count': ['count', '计数', '数量', '个数', '统计'],
		'max': ['max', 'maximum', '最大', '最高', '最大值'],
		'min': ['min', 'minimum', '最小', '最低', '最小值'],
		'std': ['std', 'standard deviation', '标准差', '标准偏差'],
		'var': ['var', 'variance', '方差'],
		'median': ['median', '中位数', '中值'],
	}

	# 更新 AGGREGATION_PATTERNS
	AGGREGATION_PATTERNS = [
		r'按\s*(\w+)\s*分组',
		r'按\s*(\w+)\s*统计',
		r'group\s+by\s+(\w+)',
		r'each\s+(\w+)',
		r'per\s+(\w+)',
		r'(\w+)\s*分组',
	]

	# 更新 COLUMN_PATTERNS
	COLUMN_PATTERNS = [
		r'计算\s*(\w+)的',  # 添加 "计算" 前缀
		r'(\w+)的',
		r'列\s*["\']?(\w+)["\']?',
		r'column\s*["\']?(\w+)["\']?',
		r'字段\s*["\']?(\w+)["\']?',
	]
	def parse_calculation(self, text: str) -> Dict[str, Any]:
		"""
		Parse natural language calculation request.

		Examples:
			"计算销售额的总和" -> {"columns": ["销售额"], "operations": ["sum"]}
			"按部门统计平均工资和总工资" ->
				{"columns": ["工资"], "operations": ["mean", "sum"], "group_by": ["部门"]}

		Args:
			text: Natural language description

		Returns:
			Parsed parameters dictionary
		"""
		result = {
			"columns": [],
			"operations": [],
			"group_by": None,
			"filters": None,
		}

		# Extract operations
		result["operations"] = self._extract_operations(text)
		if not result["operations"]:
			result["operations"] = ["sum"]  # default

		# Extract columns
		result["columns"] = self._extract_columns(text)

		# Extract group by
		result["group_by"] = self._extract_group_by(text)

		# Extract filters
		result["filters"] = self._extract_filters(text)

		return result

	def _extract_operations(self, text: str) -> List[str]:
		"""Extract operation names from text."""
		operations = []
		text_lower = text.lower()

		for op, keywords in self.OP_MAPPINGS.items():
			for keyword in keywords:
				if keyword in text_lower:
					operations.append(op)
					break

		# Remove duplicates while preserving order
		seen = set()
		return [op for op in operations if not (op in seen or seen.add(op))]

	def _extract_columns(self, text: str) -> List[str]:
		"""Extract column names from text."""
		columns = []

		# Look for patterns like "销售额的" or "列'销售额'"
		for pattern in self.COLUMN_PATTERNS:
			matches = re.findall(pattern, text)
			columns.extend(matches)

		# Also look for quoted column names
		quoted = re.findall(r'["\'](\w+)["\']', text)
		columns.extend(quoted)

		# Remove duplicates
		return list(dict.fromkeys(columns))

	def _extract_group_by(self, text: str) -> Optional[List[str]]:
		"""Extract group by fields from text."""
		for pattern in self.AGGREGATION_PATTERNS:
			match = re.search(pattern, text.lower())
			if match:
				field = match.group(1)
				return [field] if field else None

		# Look for "each X" pattern
		each_match = re.search(r'each\s+(\w+)', text.lower())
		if each_match:
			return [each_match.group(1)]

		return None

	def _extract_filters(self, text: str) -> Optional[str]:
		"""Extract filter conditions from text."""
		# Look for patterns like "where X > Y" or "X大于Y"
		patterns = [
			r'where\s+([^.,;]+)',
			r'filter\s+([^.,;]+)',
			r'条件\s*[:：]\s*([^.,;]+)',
		]

		for pattern in patterns:
			match = re.search(pattern, text.lower())
			if match:
				return match.group(1).strip()

		return None

	def parse_expression(self, expression: str) -> Dict[str, Any]:
		"""
		Parse mathematical expression for safety checking.

		Args:
			expression: Mathematical expression string

		Returns:
			Parsed expression info
		"""
		# Check for dangerous patterns
		dangerous_patterns = [
			r'__',  # dunder methods
			r'import',  # imports
			r'eval',  # eval
			r'exec',  # exec
			r'compile',  # compile
			r'open\(',  # file operations
			r'__import__',  # import
		]

		for pattern in dangerous_patterns:
			if re.search(pattern, expression.lower()):
				return {"safe": False, "reason": f"Dangerous pattern: {pattern}"}

		# Extract all identifiers
		identifiers = re.findall(r'\b[a-zA-Z_][a-zA-Z0-9_]*\b', expression)

		return {
			"safe": True,
			"identifiers": list(set(identifiers)),
			"has_numbers": bool(re.search(r'\d+', expression)),
			"has_operators": bool(re.search(r'[+\-*/%]', expression)),
		}


# Global parser instance
parser = NaturalLanguageParser()