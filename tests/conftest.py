#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author : jiaojiao
# @Time : 2026/5/29 17:45

"""
Pytest configuration and shared fixtures.
"""

import json
import os
import sys
import tempfile
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

# 将项目根目录添加到 Python 路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from easy_calc_tool import EasyCalc


# ========== Basic Fixtures ==========


@pytest.fixture
def calc():
    """Create EasyCalc instance for testing."""
    return EasyCalc(config={"cache_enabled": False, "log_level": "ERROR", "precision": 2})


@pytest.fixture
def calc_with_cache():
    """Create EasyCalc instance with cache enabled."""
    return EasyCalc(config={"cache_enabled": True, "cache_max_size": 10, "log_level": "ERROR"})


# ========== Data Fixtures ==========


@pytest.fixture
def sample_dataframe():
    """Create sample DataFrame for testing."""
    return pd.DataFrame(
        {
            "name": ["A", "B", "A", "C", "B", "D", "E", "A"],
            "value": [10, 20, 30, 40, 50, 60, 70, 80],
            "category": ["X", "Y", "X", "Z", "Y", "X", "Z", "Y"],
            "score": [1.5, 2.3, 3.1, 4.2, 5.0, 6.1, 7.2, 8.3],
        }
    )


@pytest.fixture
def sample_data_json():
    """Create sample data as JSON string."""
    return json.dumps(
        [
            {"name": "A", "value": 10, "category": "X"},
            {"name": "B", "value": 20, "category": "Y"},
            {"name": "A", "value": 30, "category": "X"},
            {"name": "C", "value": 40, "category": "Z"},
            {"name": "B", "value": 50, "category": "Y"},
        ]
    )


@pytest.fixture
def sample_data_csv():
    """Create sample data as CSV string."""
    return "name,value,category\nA,10,X\nB,20,Y\nA,30,X\nC,40,Z\nB,50,Y"


@pytest.fixture
def sample_data_list():
    """Create sample data as list of dicts."""
    return [
        {"product": "A", "sales": 100, "region": "North", "profit": 20},
        {"product": "B", "sales": 200, "region": "South", "profit": 40},
        {"product": "A", "sales": 150, "region": "North", "profit": 30},
        {"product": "C", "sales": 300, "region": "East", "profit": 60},
        {"product": "B", "sales": 250, "region": "West", "profit": 50},
    ]


@pytest.fixture
def timeseries_dataframe():
    """Create time series DataFrame for testing."""
    dates = pd.date_range("2024-01-01", periods=30, freq="D")
    return pd.DataFrame(
        {
            "date": dates,
            "sales": [100 + i * 2 + (i % 7) * 3 for i in range(30)],
            "value": [50 + i * 1.5 for i in range(30)],
        }
    )


@pytest.fixture
def correlation_dataframe():
    """Create data with strong correlation for testing."""
    np.random.seed(42)
    x = np.random.randn(50) * 10 + 50
    return pd.DataFrame(
        {"x": x, "y": x * 0.8 + np.random.randn(50) * 5, "z": np.random.randn(50) * 10 + 100}
    )


# ========== File Fixtures ==========


@pytest.fixture
def temp_csv_file():
    """Create temporary CSV file for testing."""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as f:
        f.write("name,value\nA,10\nB,20\nC,30")
        temp_path = f.name

    yield temp_path
    Path(temp_path).unlink()


@pytest.fixture
def temp_json_file():
    """Create temporary JSON file for testing."""
    data = [{"name": "A", "value": 10}, {"name": "B", "value": 20}]
    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
        json.dump(data, f)
        temp_path = f.name

    yield temp_path
    Path(temp_path).unlink()


# ========== Large Data Fixtures ==========


@pytest.fixture
def large_dataframe():
    """Create large DataFrame for performance testing."""
    np.random.seed(42)
    return pd.DataFrame(
        {
            "group": np.random.choice(["A", "B", "C", "D"], 10000),
            "value1": np.random.randn(10000) * 100,
            "value2": np.random.randn(10000) * 50,
        }
    )
