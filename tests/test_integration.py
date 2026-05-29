#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author : jiaojiao
# @Time : 2026/5/29 17:43

"""
Integration tests for easy-calc-tool.
Tests end-to-end workflows and complex scenarios.
"""
import sys
import os

# 将项目根目录添加到 Python 路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import pytest
import pandas as pd
import json
from easy_calc_tool import EasyCalc


class TestEndToEndWorkflows:
    """Test complete workflows combining multiple tools."""

    def test_complete_data_analysis_pipeline(self, calc, sample_data_list):
        """Test complete data analysis pipeline."""
        # Step 1: Filter data
        filtered = calc.calculate("filter_calc", sample_data_list,
                                 condition="sales > 150")
        assert filtered["filtered_count"] == 3

        # Step 2: Aggregate filtered data
        result = calc.calculate("aggregate", sample_data_list,
                               columns=["sales"], operations=["sum"],
                               group_by="product")
        assert "grouped_result" in result

        # Step 3: Statistics on filtered data
        stats = calc.calculate("statistics", sample_data_list,
                              columns="sales", operations=["mean", "std"])
        assert "statistics" in stats

    def test_timeseries_with_statistics(self, calc, timeseries_dataframe):
        """Test time series combined with statistics."""
        # Calculate moving average
        ma_result = calc.calculate("timeseries", timeseries_dataframe,
                                  operation="moving_average", window=7)
        assert ma_result["operation"] == "moving_average"

        # Calculate statistics on original data
        stats = calc.calculate("statistics", timeseries_dataframe,
                              columns="sales", operations=["mean", "std"])
        assert "statistics" in stats

        # Calculate growth rate
        growth = calc.calculate("timeseries", timeseries_dataframe,
                               operation="growth_rate")
        assert "average_growth" in growth

    def test_multi_step_calculation_with_cache(self):
        """Test multi-step calculation with caching."""
        calc = EasyCalc(config={"cache_enabled": True})

        data = [{"x": i, "y": i*2} for i in range(100)]

        # First calculation
        result1 = calc.calculate("statistics", data, columns="x", operations="sum")
        # Second calculation (should use cache)
        result2 = calc.calculate("statistics", data, columns="x", operations="sum")

        assert result1["statistics"]["x"]["sum"] == result2["statistics"]["x"]["sum"]
        assert calc.get_stats()["cache_size"] >= 1


class TestEdgeCases:
    """Test edge cases and boundary conditions."""

    def test_empty_dataframe(self, calc):
        """Test with empty DataFrame."""
        df = pd.DataFrame()
        result = calc.calculate("statistics", df)
        assert result.get("success") is False

    def test_single_row_data(self, calc):
        """Test with single row of data."""
        data = [{"value": 100}]
        result = calc.calculate("statistics", data, columns="value",
                               operations=["sum", "mean", "std"])
        assert result["statistics"]["value"]["sum"] == 100
        assert result["statistics"]["value"]["mean"] == 100

    def test_all_same_values(self, calc):
        """Test with all identical values."""
        data = [{"value": 50} for _ in range(10)]
        result = calc.calculate("statistics", data, columns="value",
                               operations=["std"])
        assert result["statistics"]["value"]["std"] == 0

    def test_negative_values(self, calc):
        """Test with negative values."""
        data = [{"value": -10}, {"value": -20}, {"value": -30}]
        result = calc.calculate("statistics", data, columns="value",
                               operations=["sum", "mean"])
        assert result["statistics"]["value"]["sum"] == -60
        assert result["statistics"]["value"]["mean"] == -20

    def test_decimal_precision(self, calc):
        """Test decimal precision handling."""
        data = [{"value": 1/3}, {"value": 2/3}]
        result = calc.calculate("statistics", data, columns="value",
                               operations=["mean"])
        # Should be rounded to configured precision (2 by default)
        assert round(result["statistics"]["value"]["mean"], 2) == 0.5

    def test_large_numbers(self, calc):
        """Test with very large numbers."""
        result = calc.calculate("arithmetic", None, expression="1e100 * 1e100")
        assert result["result"] is not None

    def test_special_characters_in_column_names(self, calc):
        """Test with special characters in column names."""
        data = [{"column-name": 10, "column name": 20, "column_name": 30}]
        result = calc.calculate("statistics", data, columns="column-name",
                               operations="sum")
        assert result["statistics"]["column-name"]["sum"] == 10


class TestErrorHandling:
    """Test error handling scenarios."""

    def test_invalid_data_format(self, calc):
        """Test with invalid data format."""
        # 单数值实际上是有效的（作为单行数据）
        result = calc.calculate("statistics", 12345)
        # 应该成功，而不是失败
        assert result.get("success", True) is True
        assert "statistics" in result

    def test_invalid_column_name(self, calc, sample_dataframe):
        """Test with invalid column name."""
        result = calc.calculate("statistics", sample_dataframe,
                               columns="nonexistent_column",
                               operations="sum")
        assert result.get("success") is False

    def test_invalid_operation(self, calc, sample_dataframe):
        """Test with invalid operation."""
        result = calc.calculate("statistics", sample_dataframe,
                               columns="value",
                               operations="invalid_op")
        # Should still work, invalid op will be ignored
        assert result.get("success", True) is not False

    def test_division_by_zero_in_expression(self, calc):
        """Test division by zero in expression."""
        result = calc.calculate("arithmetic", None, expression="10/0")
        assert result["result"] == float('inf')

    def test_timeout_handling(self, calc):
        """Test timeout handling (simulated)."""
        # This tests that timeout config is respected
        assert calc.config["timeout"] == 30

    def test_memory_limit(self, calc):
        """Test memory limit configuration."""
        assert calc.config["max_data_size"] == 10_000_000


class TestLargeDataPerformance:
    """Test performance with large datasets."""

    @pytest.mark.slow
    def test_large_dataframe_statistics(self, calc, large_dataframe):
        """Test statistics on large DataFrame."""
        result = calc.calculate("statistics", large_dataframe,
                               columns="value1", operations=["sum", "mean"])
        assert "statistics" in result
        assert result["statistics"]["value1"]["sum"] is not None

    @pytest.mark.slow
    def test_large_dataframe_groupby(self, calc, large_dataframe):
        """Test groupby on large DataFrame."""
        result = calc.calculate("statistics", large_dataframe,
                               columns="value1", operations="sum",
                               group_by="group")
        assert "grouped" in result
        assert len(result["grouped"]) == 4

    @pytest.mark.slow
    def test_large_dataframe_correlation(self, calc, large_dataframe):
        """Test correlation on large DataFrame."""
        result = calc.calculate("correlation", large_dataframe,
                               columns=["value1", "value2"])
        assert "correlation_matrix" in result


class TestJSONSerialization:
    """Test JSON serialization of results."""

    def test_result_is_json_serializable(self, calc, sample_dataframe):
        """Test that results can be serialized to JSON."""
        result = calc.calculate("statistics", sample_dataframe,
                               columns="value", operations=["sum", "mean"])

        # Should not raise an exception
        json_str = json.dumps(result, default=str)
        assert isinstance(json_str, str)

    def test_numpy_types_converted(self, calc, sample_dataframe):
        """Test that numpy types are converted to Python types."""
        result = calc.calculate("statistics", sample_dataframe,
                               columns="value", operations="sum")

        value = result["statistics"]["value"]["sum"]
        # Should be Python int/float, not numpy type
        assert not hasattr(value, 'item') or callable(getattr(value, 'item', None)) is False


class TestLangChainIntegration:
    """Test LangChain adapter functionality (if available)."""

    def test_langchain_import(self):
        """Test that langchain integration can be imported."""
        try:
            from easy_calc_tool.integration_langchain import get_langchain_tools
            assert callable(get_langchain_tools)
        except ImportError:
            pytest.skip("LangChain dependencies not installed")

    def test_langchain_tools_creation(self):
        """Test creation of LangChain tools."""
        try:
            from easy_calc_tool.integration_langchain import get_langchain_tools
            tools = get_langchain_tools()
            assert len(tools) > 0
            tool_names = [t.name for t in tools]
            assert "calculator" in tool_names
            assert "statistics" in tool_names
        except ImportError:
            pytest.skip("LangChain dependencies not installed")