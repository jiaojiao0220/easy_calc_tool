#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Version information for easy-calc-tool
"""

import re

__version__ = "{version}"


def _parse_version(ver_str):
    parts = []
    for part in ver_str.split(".")[:3]:
        match = re.search(r'^\d+', part)
        parts.append(int(match.group()) if match else 0)
    return tuple(parts)


__version_info__ = _parse_version(__version__)