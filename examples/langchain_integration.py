#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author : jiaojiao
# @Time : 2026/5/29 17:46
"""
LangChain integration example.
"""
import sys
import os

# 将项目根目录添加到 Python 路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from easy_calc_tool import EasyCalc
from easy_calc_tool.integration_langchain import get_langchain_tools


def create_langchain_agent():
    """
    Create a LangChain agent with easy-calc-tool.

    Note: This example requires langchain and openai packages.
    Install with: pip install easy-calc-tool[langchain]
    """
    # from langchain.agents import create_agent
    # from langchain_openai import ChatOpenAI

    # Initialize calculator
    calc = EasyCalc()

    # Get LangChain tools
    tools = get_langchain_tools(calc)
    print(f"Loaded {len(tools)} tools:")
    for tool in tools:
        print(f"  - {tool.name}: {tool.description[:50]}...")

    # Create agent (requires API key)
    # llm = ChatOpenAI(model="gpt-4", temperature=0)
    # agent = create_agent(model=llm, tools=tools)

    return tools


def manual_tool_calling():
    """Demonstrate manual tool calling without agent."""
    calc = EasyCalc()
    tools = get_langchain_tools(calc)

    # Find the calculator tool
    calc_tool = next((t for t in tools if t.name == "calculator"), None)
    if calc_tool:
        result = calc_tool.invoke({"expression": "12345 * 67890"})
        print(f"Calculator result: {result}")

    # Find statistics tool
    stats_tool = next((t for t in tools if t.name == "statistics"), None)
    if stats_tool:
        data = '[{"sales":100},{"sales":200},{"sales":300}]'
        result = stats_tool.invoke({
            "data": data,
            "columns": "sales",
            "operations": "sum,mean"
        })
        print(f"Statistics result: {result}")


if __name__ == "__main__":
    print("LangChain Integration Examples")
    print("=" * 40)

    tools = create_langchain_agent()
    print(f"\nCreated {len(tools)} LangChain tools")

    print("\nManual tool calling:")
    manual_tool_calling()