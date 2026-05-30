#!/usr/bin/python3
# @Author : jiaojiao
# @Time : 2026/5/29 17:40

"""
Version information for easy-calc-tool
"""

__version__ = "0.1.0"

# 安全解析版本号
def _parse_version(ver_str):
    try:
        # 提取数字部分
        parts = []
        for part in ver_str.split(".")[:3]:
            # 只取数字部分
            import re
            match = re.search(r'^\d+', part)
            if match:
                parts.append(int(match.group()))
            else:
                parts.append(0)
        return tuple(parts)
    except:
        return (0, 1, 0)

__version_info__ = _parse_version(__version__)