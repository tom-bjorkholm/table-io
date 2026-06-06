#! /usr/bin/env python3
"""Tests for the TableIO speed test command-line helper."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from pathlib import Path

from pytest import CaptureFixture

from . import speed_test
from .check_capsys import check_capsys


def test_excel_read_uses_reader(tmp_path: Path,
                                capsys: CaptureFixture[str]) -> None:
    """Excel input mode chooses an implementation that supports reading."""
    file_name = tmp_path / 'sample'
    assert speed_test.main([
        '-f', 'excel', '-o', str(file_name), '-r', '3', '-c', '2']) == 0
    capsys.readouterr()

    assert speed_test.main(['-f', 'excel', '-l', '2',
                            '-i', str(file_name)]) == 0

    captured = capsys.readouterr()
    assert 'operation: read' in captured.out
    assert 'implementation: XlsxWriter' not in captured.out
    assert 'rows: 3' in captured.out
    assert 'columns: 2' in captured.out
    check_capsys(capsys)
