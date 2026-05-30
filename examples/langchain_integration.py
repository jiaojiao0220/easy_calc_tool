#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author : jiaojiao
# @Time : 2026/5/30
"""
LangChain integration example - Agent Mode.
Demonstrates how to use easy-calc-tool with LangChain Agent.
"""

import sys
import os

# 将项目根目录添加到 Python 路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from easy_calc_tool import EasyCalc
from easy_calc_tool.integration_langchain import get_langchain_tools

# ============================================================
# 在这里配置你的参数（直接修改即可）
# ============================================================

# OpenAI API 配置
OPENAI_API_KEY = MIMO_API_KEY  # 你的 API Key
OPENAI_API_BASE = base_url  # API 地址（默认 OpenAI）
OPENAI_MODEL = MIMO_V  # 模型名称（可选: gpt-4, gpt-3.5-turbo, 等等）

# 运行模式
# "demo": 运行预设示例
# "interactive": 交互式对话
# "test": 测试模式（不需要 API）
RUN_MODE = "interactive"


# ============================================================


def create_agent_with_tools(api_key=None, api_base=None, model=None):
    """
    Create a LangChain agent with easy-calc-tool tools.

    Args:
            api_key: OpenAI API key
            api_base: OpenAI API base URL
            model: Model name
    """
    from langchain.agents import create_agent
    from langchain_openai import ChatOpenAI

    # 使用传入的参数或全局配置
    key = api_key or OPENAI_API_KEY
    base = api_base or OPENAI_API_BASE
    mdl = model or OPENAI_MODEL

    if key == "your-api-key-here":
        print("⚠️  Warning: Please set your OpenAI API key in the OPENAI_API_KEY variable")
        print("   Open the file and replace 'your-api-key-here' with your actual API key")
        return None, None

    # Initialize calculator
    calc = EasyCalc()

    # Get LangChain tools
    tools = get_langchain_tools(calc)
    print(f"Loaded {len(tools)} tools:")
    for tool in tools:
        print(f"  - {tool.name}: {tool.description[:50]}...")

    # Create LLM with custom configuration
    llm_kwargs = {
        "model": mdl,
        "temperature": 0,
        "api_key": key,
    }

    # 如果 API base 不是默认的 OpenAI 地址，则设置
    if base != "https://api.openai.com/v1":
        llm_kwargs["base_url"] = base
        print(f"📡 Using custom API base: {base}")

    llm = ChatOpenAI(**llm_kwargs)
    print(f"🤖 Using model: {mdl}")

    # Create agent
    agent = create_agent(model=llm, tools=tools)

    return agent, tools


def run_demo():
    """Run preset examples."""
    print("=" * 60)
    print("LangChain Agent Demo")
    print("=" * 60)

    # Create agent
    agent, tools = create_agent_with_tools()

    if agent is None:
        return

    examples = [
        ("Basic Arithmetic", "Calculate 12345 * 67890"),
        ("Unit Conversion", "Convert 100 kilometers to miles"),
        ("Date Calculation", "How many days between 2024-01-01 and 2024-12-31?"),
        ("Statistics", "Analyze this sales data: [100, 200, 150, 300], calculate sum and average"),
    ]

    for title, question in examples:
        print(f"\n📊 {title}")
        print("-" * 40)
        print(f"🧑 User: {question}")

        response = agent.invoke({"messages": [{"role": "user", "content": question}]})
        print(f"🤖 Agent: {response['messages'][-1].content}")


def run_interactive():
    """Run in interactive mode (chat loop)."""
    print("\n" + "=" * 60)
    print("🤖 Interactive Agent Mode")
    print("Type 'quit' or 'exit' to stop")
    print("=" * 60)

    # Create agent
    agent, tools = create_agent_with_tools()

    if agent is None:
        return

    messages = []

    while True:
        user_input = input("\n🧑 You: ").strip()

        if user_input.lower() in ["quit", "exit", "q"]:
            print("Goodbye! 👋")
            break

        if not user_input:
            continue

        messages.append({"role": "user", "content": user_input})
        response = agent.invoke({"messages": messages})
        assistant_message = response["messages"][-1]
        messages.append({"role": "assistant", "content": assistant_message.content})

        print(f"🤖 Agent: {assistant_message.content}")


def run_test():
    """Quick test without API (manual tool calling)."""
    print("=" * 60)
    print("Quick Test (Manual Tool Calling)")
    print("=" * 60)

    calc = EasyCalc()
    tools = get_langchain_tools(calc)

    # Test calculator
    calc_tool = next((t for t in tools if t.name == "calculator"), None)
    if calc_tool:
        result = calc_tool.invoke({"expression": "12345 * 67890"})
        print(f"\n🧮 Calculator: 12345 * 67890 = {result}")

    # Test statistics
    stats_tool = next((t for t in tools if t.name == "statistics"), None)
    if stats_tool:
        data = '[{"sales":100},{"sales":200},{"sales":300}]'
        result = stats_tool.invoke({"data": data, "columns": "sales", "operations": "sum,mean"})
        print(f"\n📊 Statistics Result:\n{result}")

    print("\n" + "-" * 40)
    print("💡 To run full agent mode, set your configuration in the code:")
    print("   OPENAI_API_KEY = 'your-api-key'")
    print("   RUN_MODE = 'demo' or 'interactive'")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="LangChain Integration Demo")
    parser.add_argument(
        "--mode", choices=["demo", "interactive", "test"], default=RUN_MODE, help="Run mode"
    )
    parser.add_argument("--api-key", help="OpenAI API key")
    parser.add_argument("--api-base", help="OpenAI API base URL")
    parser.add_argument("--model", help="Model name")

    args = parser.parse_args()

    # 命令行参数优先于配置文件
    if args.api_key:
        OPENAI_API_KEY = args.api_key
    if args.api_base:
        OPENAI_API_BASE = args.api_base
    if args.model:
        OPENAI_MODEL = args.model

    if args.mode == "test":
        run_test()
    elif args.mode == "demo":
        run_demo()
    elif args.mode == "interactive":
        run_interactive()
