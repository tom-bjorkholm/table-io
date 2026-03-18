#! /usr/bin/env python3
"""Highlight colors for the tableio package."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from enum import IntEnum


class Color(IntEnum):
    """Highlight colors for the tableio package."""

    NONE = 0
    """No hightlight color."""
    RED = 1
    """Red highlight color."""
    GREEN = 2
    """Green highlight color."""
    YELLOW = 3
    """Yellow highlight color."""
