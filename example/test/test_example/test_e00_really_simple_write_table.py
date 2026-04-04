#! /usr/local/bin/python3
"""Tests for really simple write table example."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

import pytest
from tableio import Value
from example.e00_really_simple_write_table import e00_really_simple_write_table
from .example_checkers import Example, check_example_spreadsheet, \
    check_example_md_csv
from .spreadsheet_checkers import SheetContentExpectation


SHEET_ROW_FRAGMENTS: list[list[Value]] = [
    ['English', 'German', 'Swedish'],
    ['Hello', 'Hallo', 'Hej'],
    ['World', 'Welt', 'Värld'],
    [3.14159, True]
]

EXPECTED_SHEET_FRAGMENTS: list[SheetContentExpectation] = [
    SheetContentExpectation(sheet_name='Sheet1',
                            row_fragments=SHEET_ROW_FRAGMENTS),
]

EXPECTED_CSV_FRAGMENTS: list[str] = [
    '"English","German","Swedish"',
    '"Hello","Hallo","Hej"',
    '"World","Welt","Värld"',
    '"3.14159","True"'
]

EXPECTED_MD_FRAGMENTS: list[str] = [
    '| English | German | Swedish |',
    '|---------|--------|---------|',
    '| Hello   | Hallo  | Hej     |',
    '| World   | Welt   | Värld   |',
    '| 3.14159 | True   |'
]


@pytest.mark.parametrize('fmt,impl',
                         [('ods', 'odfdo'),
                          ('excel', 'openpyxl'),
                          ('excel', 'XlsxWriter'),
                          ('excel', 'pylightxl')])
def test_e00_write_table(capsys: pytest.CaptureFixture[str],
                         fmt: str, impl: str) -> None:
    """Test 00_really_simple_write_table example."""
    example = Example(example_function=e00_really_simple_write_table,
                      format_name=fmt,
                      implementation_name=impl)
    check_example_spreadsheet(example, capture=capsys,
                              expected_fragments=EXPECTED_SHEET_FRAGMENTS)


@pytest.mark.parametrize('fmt, exp',
                         [('csv', EXPECTED_CSV_FRAGMENTS),
                          ('md', EXPECTED_MD_FRAGMENTS)])
def test_e00_write_table_md_csv(capsys: pytest.CaptureFixture[str],
                                fmt: str, exp: list[str]) -> None:
    """Test 00_really_simple_write_table example for markdown and CSV."""
    example = Example(example_function=e00_really_simple_write_table,
                      format_name=fmt, implementation_name=None)
    check_example_md_csv(example, capture=capsys,
                         expected_fragments=exp)
