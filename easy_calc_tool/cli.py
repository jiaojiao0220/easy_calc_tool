#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author : jiaojiao
# @Time : 2026/5/29 18:38

"""
Command-line interface for easy-calc-tool.
"""

import argparse
import json
import sys
from typing import Dict, Any

from .core import EasyCalc
from .version import __version__


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Easy Calc Tool - Flexible calculation toolbox for LLMs"
    )
    parser.add_argument("--version", action="version", version=f"easy-calc-tool {__version__}")

    subparsers = parser.add_subparsers(dest="command", help="Commands")

    # Calculate command
    calc_parser = subparsers.add_parser("calc", help="Perform calculation")
    calc_parser.add_argument(
        "--tool",
        required=True,
        choices=[
            "arithmetic",
            "statistics",
            "aggregate",
            "filter_calc",
            "timeseries",
            "unit_convert",
            "date_calc",
        ],
        help="Tool to use",
    )
    calc_parser.add_argument("--data", help="Input data (file path or JSON string)")
    calc_parser.add_argument("--params", help="JSON string of parameters")

    # Tools list command
    subparsers.add_parser("tools", help="List available tools")

    # Stats command
    subparsers.add_parser("stats", help="Show calculator statistics")

    # Cache command
    cache_parser = subparsers.add_parser("cache", help="Manage cache")
    cache_parser.add_argument("action", choices=["clear", "stats"], help="Cache action")

    args = parser.parse_args()

    if args.command == "calc":
        _run_calc(args)
    elif args.command == "tools":
        _list_tools()
    elif args.command == "stats":
        _show_stats()
    elif args.command == "cache":
        _manage_cache(args.action)
    else:
        parser.print_help()


def _run_calc(args):
    """Execute calculation."""
    calc = EasyCalc()

    # Parse data
    data = None
    if args.data:
        try:
            # Try as JSON
            data = json.loads(args.data)
        except json.JSONDecodeError:
            # Treat as file path
            data = args.data

    # Parse params
    params = {}
    if args.params:
        params = json.loads(args.params)

    # Execute
    result = calc.calculate(args.tool, data, **params)

    # Output result
    if result.get("success", True) is False:
        print(f"Error: {result.get('error')}", file=sys.stderr)
        sys.exit(1)

    print(json.dumps(result, ensure_ascii=False, indent=2))


def _list_tools():
    """List available tools."""
    calc = EasyCalc()
    print("Available tools:")
    for tool in calc.available_tools:
        print(f"  - {tool}")


def _show_stats():
    """Show calculator statistics."""
    calc = EasyCalc()
    stats = calc.get_stats()
    print(json.dumps(stats, indent=2))


def _manage_cache(action: str):
    """Manage cache."""
    calc = EasyCalc()
    if action == "clear":
        calc.clear_cache()
        print("Cache cleared")
    elif action == "stats":
        # 使用公共方法而不是直接访问私有属性
        print(f"Cache size: {calc.get_cache_size()} / {calc.config['cache_max_size']}")


if __name__ == "__main__":
    main()
