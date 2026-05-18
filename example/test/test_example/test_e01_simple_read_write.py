#! /usr/bin/env python3
"""Tests for simple read and write example."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

import pytest
from tableio import Value
from example.e01_simple_read_write import e01_simple_read_write
from .spreadsheet_checkers import SheetContentExpectation
from .example_checkers import check_example_md_csv, \
    check_example_spreadsheet, Example


SHEET_ROW_FRAGMENTS1: list[list[Value]] = [
    ['Example of how to use the tableio package.'],
    ['A subheading.'],
    ['Hello', 'World'],
    [1, 3.14],
    ['Writer information:'],
    ['Attribute', 'Value', 'Requested value'],
]

# pylint: disable=duplicate-code
SHEET_OPX: SheetContentExpectation = SheetContentExpectation(
    sheet_name='Sheet',
    row_fragments=SHEET_ROW_FRAGMENTS1 + [
        ['Implementation', 'OpenPyXL', 'openpyxl']
    ])

SHEET_PYXL: SheetContentExpectation = SheetContentExpectation(
    sheet_name='Sheet1',
    row_fragments=SHEET_ROW_FRAGMENTS1 + [
        ['Implementation', 'pylightxl', 'pylightxl']
    ])

SHEET_ODS: SheetContentExpectation = SheetContentExpectation(
    sheet_name='Sheet1',
    row_fragments=SHEET_ROW_FRAGMENTS1 + [
        ['Implementation', 'odfdo', 'odfdo']
    ])
# pylint: enable=duplicate-code


CSV_FRAGMENTS: list[str] = [
    '# Example of how to use the tableio package.',
    '## A subheading.',
    '"Hello","World"',
    '1,3.14',
    '## Writer information:',
    '"Attribute","Value","Requested value"',
    '"Type name","CSV","csv"',
    '"Implementation","csv","(none)"'
]


@pytest.mark.parametrize('fmt, impl, expected',
                         [('ods', 'odfdo', SHEET_ODS),
                          ('excel', 'openpyxl', SHEET_OPX),
                          ('excel', 'pylightxl', SHEET_PYXL)])
def test_e01_spreadsheet(capsys: pytest.CaptureFixture[str], fmt: str,
                         impl: str, expected: SheetContentExpectation) -> None:
    """Test e01 for spreadsheet formats and implementations."""
    example = Example(example_function=e01_simple_read_write, format_name=fmt,
                      implementation_name=impl)
    check_example_spreadsheet(example, capture=capsys,
                              expected_fragments=[expected])


@pytest.mark.parametrize('fmt, expected', [('csv', CSV_FRAGMENTS)])
def test_e01_simple_read_write_text(capsys: pytest.CaptureFixture[str],
                                    fmt: str, expected: list[str]) \
        -> None:
    """Test e01 for md and csv text formats."""
    example = Example(example_function=e01_simple_read_write, format_name=fmt)
    check_example_md_csv(example, capture=capsys, expected_fragments=expected)
