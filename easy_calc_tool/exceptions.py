#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author : jiaojiao
# @Time : 2026/5/29 17:40

"""Custom exceptions for easy-calc-tool."""


class EasyCalcError(Exception):
	"""Base exception for all easy-calc-tool errors."""
	pass


class CalculationError(EasyCalcError):
	"""Raised when a calculation fails."""

	pass


class DataParseError(EasyCalcError):
	"""Raised when data parsing fails."""

	pass


class InvalidParameterError(EasyCalcError):
	"""Raised when invalid parameters are provided."""
	pass


class ToolNotFoundError(EasyCalcError):
	"""Raised when a requested tool is not found."""

	pass


class SecurityError(EasyCalcError):
	"""Raised when a security violation occurs (e.g., expression injection)."""

	pass