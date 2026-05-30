#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author : jiaojiao
# @Time : 2026/5/29 17:43

"""
Tests for DataHandler.
"""
import sys
import os

# 将项目根目录添加到 Python 路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import pytest
import pandas as pd
import numpy as np
from easy_calc_tool.data_handler import DataHandler
from easy_calc_tool.exceptions import DataParseError


class TestDataHandler:
	"""Test DataHandler functionality."""

	def setup_method(self):
		self.handler = DataHandler()

	def test_parse_dataframe(self, sample_dataframe):
		"""Test parsing DataFrame."""
		result = self.handler.parse(sample_dataframe)
		assert isinstance(result, pd.DataFrame)
		assert len(result) == 8

	def test_parse_json_string(self, sample_data_json):
		"""Test parsing JSON string."""
		result = self.handler.parse(sample_data_json)
		assert isinstance(result, pd.DataFrame)
		assert len(result) == 5

	def test_parse_csv_string(self, sample_data_csv):
		"""Test parsing CSV string."""
		result = self.handler.parse(sample_data_csv)
		assert isinstance(result, pd.DataFrame)
		assert len(result) == 5
		assert list(result.columns) == ["name", "value", "category"]

	def test_parse_list_of_dicts(self, sample_data_list):
		"""Test parsing list of dictionaries."""
		result = self.handler.parse(sample_data_list)
		assert isinstance(result, pd.DataFrame)
		assert len(result) == 5

	def test_parse_single_dict(self):
		"""Test parsing single dictionary."""
		data = {"name": "A", "value": 10}
		result = self.handler.parse(data)
		assert isinstance(result, pd.DataFrame)
		assert len(result) == 1

	def test_parse_single_value(self):
		"""Test parsing single value."""
		result = self.handler.parse(42)
		assert isinstance(result, pd.DataFrame)
		assert len(result) == 1
		assert result["value"][0] == 42

	def test_parse_empty_list(self):
		"""Test parsing empty list."""
		result = self.handler.parse([])
		assert isinstance(result, pd.DataFrame)
		assert len(result) == 0

	def test_parse_none(self):
		"""Test parsing None."""
		with pytest.raises(DataParseError):
			self.handler.parse(None)

	def test_parse_invalid_string(self):
		"""Test parsing invalid string."""
		with pytest.raises(DataParseError):
			self.handler.parse("not valid csv or json")

	def test_parse_invalid_type(self):
		"""Test parsing invalid type."""
		with pytest.raises(DataParseError):
			self.handler.parse(object())

	def test_file_parsing_csv(self, temp_csv_file):
		"""Test parsing CSV file."""
		result = self.handler.parse(temp_csv_file)
		assert isinstance(result, pd.DataFrame)
		assert len(result) == 3

	def test_file_parsing_json(self, temp_json_file):
		"""Test parsing JSON file."""
		result = self.handler.parse(temp_json_file)
		assert isinstance(result, pd.DataFrame)
		assert len(result) == 2

	def test_file_not_found(self):
		"""Test parsing non-existent file."""
		with pytest.raises(DataParseError):
			self.handler.parse("nonexistent_file.csv")

	def test_max_data_size_limit(self):
		"""Test max data size limit."""
		handler = DataHandler({"max_data_size": 10})
		large_data = [{"i": i} for i in range(100)]
		with pytest.raises(DataParseError):
			handler.parse(large_data)

	def test_to_json(self, sample_dataframe):
		"""Test DataFrame to JSON conversion."""
		json_str = self.handler.to_json(sample_dataframe)
		assert isinstance(json_str, str)
		assert "name" in json_str

	def test_to_csv(self, sample_dataframe):
		"""Test DataFrame to CSV conversion."""
		csv_str = self.handler.to_csv(sample_dataframe)
		assert isinstance(csv_str, str)
		assert "name,value,category" in csv_str

	def test_preview(self, sample_dataframe):
		"""Test data preview."""
		preview = self.handler.preview(sample_dataframe, n=3)
		assert "head" in preview
		assert len(preview["head"]) == 3
		assert "shape" in preview
		assert preview["shape"] == (8, 4)
		assert "columns" in preview
		assert "dtypes" in preview
