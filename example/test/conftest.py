#! /usr/bin/env python3
"""Pytest configuration for example tests."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from pathlib import Path
import sys

SOURCE_PATH = Path(__file__).resolve().parents[1] / 'src'
if str(SOURCE_PATH) not in sys.path:
    sys.path.insert(0, str(SOURCE_PATH))
# Makes the shared helpers in test/test_tableio importable as test_tableio.
TEST_PATH = Path(__file__).resolve().parents[2] / 'test'
if str(TEST_PATH) not in sys.path:
    sys.path.insert(0, str(TEST_PATH))
