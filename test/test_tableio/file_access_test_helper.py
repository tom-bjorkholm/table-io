#! /usr/bin/env python3
"""Helpers for testing defensive FileAccess validation paths."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from tableio import FileAccess


def unsupported_file_access() -> FileAccess:
    """Return a future FileAccess-style value unsupported by helpers."""
    access = int.__new__(FileAccess, 99)
    setattr(access, '_name_', 'UNKNOWN')
    setattr(access, '_value_', 99)
    return access
