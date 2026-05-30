#!/usr/bin/python3
# @Author : jiaojiao
# @Time : 2026/5/29 17:40

"""
Configuration management for easy-calc-tool.
"""

import os
from dataclasses import dataclass, field
from typing import Any, Dict


@dataclass
class Config:
    """Configuration class for EasyCalc."""

    # Cache settings
    cache_enabled: bool = True
    cache_max_size: int = 1000

    # Performance settings
    timeout: int = 30  # seconds
    max_data_size: int = 10_000_000  # max rows
    chunk_size: int = 100_000  # chunk size for large data

    # Precision settings
    precision: int = 6
    float_format: str = "float64"

    # Security settings
    safe_mode: bool = True
    allowed_functions: list = field(
        default_factory=lambda: [
            "abs",
            "round",
            "min",
            "max",
            "sum",
            "len",
            "int",
            "float",
            "str",
            "bool",
        ]
    )

    # Logging settings
    log_level: str = "INFO"
    log_format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

    # Data handling
    default_date_format: str = "%Y-%m-%d"
    encoding: str = "utf-8"

    def to_dict(self) -> Dict[str, Any]:
        """Convert config to dictionary."""
        return {
            "cache_enabled": self.cache_enabled,
            "cache_max_size": self.cache_max_size,
            "timeout": self.timeout,
            "max_data_size": self.max_data_size,
            "chunk_size": self.chunk_size,
            "precision": self.precision,
            "float_format": self.float_format,
            "safe_mode": self.safe_mode,
            "allowed_functions": self.allowed_functions,
            "log_level": self.log_level,
            "default_date_format": self.default_date_format,
            "encoding": self.encoding,
        }

    @classmethod
    def from_env(cls) -> "Config":
        """Create config from environment variables."""
        config = cls()

        # Override with environment variables
        config.cache_enabled = (
            os.getenv("EASY_CALC_CACHE_ENABLED", "true").lower() == "true"
        )
        config.cache_max_size = int(
            os.getenv("EASY_CALC_CACHE_MAX_SIZE", "1000")
        )
        config.timeout = int(os.getenv("EASY_CALC_TIMEOUT", "30"))
        config.max_data_size = int(
            os.getenv("EASY_CALC_MAX_DATA_SIZE", "10000000")
        )
        config.precision = int(os.getenv("EASY_CALC_PRECISION", "6"))
        config.safe_mode = (
            os.getenv("EASY_CALC_SAFE_MODE", "true").lower() == "true"
        )
        config.log_level = os.getenv("EASY_CALC_LOG_LEVEL", "INFO")

        return config


# Default configuration instance
settings = Config()
