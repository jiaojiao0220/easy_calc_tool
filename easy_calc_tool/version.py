"""
Version information for easy-calc-tool
"""

import re

__version__ = "0.1.1.dev11+g652acf942.d20260530"


def _parse_version(ver_str):
    parts = []
    for part in ver_str.split(".")[:3]:
        match = re.search(r"^\d+", part)
        parts.append(int(match.group()) if match else 0)
    return tuple(parts)


__version_info__ = _parse_version(__version__)
