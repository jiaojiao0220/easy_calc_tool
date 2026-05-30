#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author : jiaojiao
# @Time : 2026/5/29 17:43

"""
Tests for natural language parser.
"""
import sys
import os

# 将项目根目录添加到 Python 路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import pytest
from easy_calc_tool.parser import NaturalLanguageParser


class TestNaturalLanguageParser:
    """Test natural language parsing functionality."""

    def setup_method(self):
        self.parser = NaturalLanguageParser()

    def test_parse_calculation_sum(self):
        """Test parsing sum operation."""
        result = self.parser.parse_calculation("计算销售额的总和")
        assert "sum" in result["operations"]

    def test_parse_calculation_mean(self):
        """Test parsing mean operation."""
        result = self.parser.parse_calculation("计算平均工资")
        assert "mean" in result["operations"]

    def test_parse_calculation_multiple_ops(self):
        """Test parsing multiple operations."""
        result = self.parser.parse_calculation("计算平均工资和总工资")
        assert "mean" in result["operations"]
        assert "sum" in result["operations"]

    def test_parse_calculation_count(self):
        """Test parsing count operation."""
        result = self.parser.parse_calculation("统计员工数量")
        assert "count" in result["operations"]

    def test_parse_calculation_max_min(self):
        """Test parsing max and min operations."""
        result = self.parser.parse_calculation("找出最大销售额和最小利润")
        assert "max" in result["operations"]
        assert "min" in result["operations"]

    def test_parse_calculation_with_groupby_chinese(self):
        """Test parsing group by in Chinese."""
        result = self.parser.parse_calculation("按部门统计平均工资")
        assert result["group_by"] == ["部门"]

    def test_parse_calculation_with_groupby_english(self):
        """Test parsing group by in English."""
        result = self.parser.parse_calculation("group by department average salary")
        assert result["group_by"] == ["department"]

    def test_parse_calculation_with_each_pattern(self):
        """Test parsing 'each' pattern."""
        result = self.parser.parse_calculation("each product total sales")
        assert result["group_by"] == ["product"]

    def test_parse_calculation_with_column_extraction(self):
        """Test column name extraction."""
        result = self.parser.parse_calculation("计算销售额的总和")
        assert "销售额" in result["columns"]

    def test_parse_calculation_with_quoted_columns(self):
        """Test extraction of quoted column names."""
        result = self.parser.parse_calculation("计算'sales'的总和")
        assert "sales" in result["columns"]

    def test_parse_calculation_default_operation(self):
        """Test default operation when none specified."""
        result = self.parser.parse_calculation("计算数据")
        assert "sum" in result["operations"]  # default

    def test_parse_calculation_with_filter(self):
        """Test filter extraction."""
        result = self.parser.parse_calculation("销售额大于1000的数据 where sales > 1000")
        assert result["filters"] is not None

    def test_parse_expression_safe(self):
        """Test safe expression detection."""
        result = self.parser.parse_expression("2+3*4")
        assert result["safe"] is True
        assert result["has_numbers"] is True
        assert result["has_operators"] is True

    def test_parse_expression_with_functions(self):
        """Test expression with mathematical functions."""
        result = self.parser.parse_expression("sqrt(16) + abs(-5)")
        assert result["safe"] is True
        assert "sqrt" in result["identifiers"]
        assert "abs" in result["identifiers"]

    def test_parse_expression_unsafe_import(self):
        """Test unsafe import detection."""
        result = self.parser.parse_expression("__import__('os')")
        assert result["safe"] is False
        assert "reason" in result

    def test_parse_expression_unsafe_eval(self):
        """Test unsafe eval detection."""
        result = self.parser.parse_expression("eval('2+3')")
        assert result["safe"] is False

    def test_parse_expression_unsafe_open(self):
        """Test unsafe file open detection."""
        result = self.parser.parse_expression("open('file.txt')")
        assert result["safe"] is False

    def test_parse_expression_dunder_methods(self):
        """Test dunder method detection."""
        result = self.parser.parse_expression("obj.__dict__")
        assert result["safe"] is False

    def test_parse_expression_no_operators(self):
        """Test expression with no operators."""
        result = self.parser.parse_expression("123")
        assert result["safe"] is True
        assert result["has_operators"] is False
        assert result["has_numbers"] is True

    def test_parse_expression_identifiers_only(self):
        """Test expression with only identifiers."""
        result = self.parser.parse_expression("x + y")
        assert result["safe"] is True
        assert "x" in result["identifiers"]
        assert "y" in result["identifiers"]
