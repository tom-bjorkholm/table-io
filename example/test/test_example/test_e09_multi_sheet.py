#! /usr/bin/env python3
"""Tests for multi-sheet example."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

import pytest
from tableio import Value
from example.e09_multi_sheet import e09_multi_sheet
from .spreadsheet_checkers import SheetContentExpectation
from .example_checkers import check_example_spreadsheet, Example


MAIN_SHEET_ROWS: list[list[Value]] = [
    ['Name', 'Role', 'Hours'],
    ['Alice', 'Developer', 38],
    ['Bob', 'Tester', 35],
    ['Carla', 'Project manager', 40]
]


def build_summary_rows(first_sheet_name: str) -> list[list[Value]]:
    """Build expected summary-sheet row fragments for one backend."""
    return [
        ['Information about the workbook sheets.'],
        ['Property', 'Value'],
        ['First sheet name', first_sheet_name],
        ['Current sheet after select_sheet()', 'Summary'],
        ['Sheets in workbook', f'{first_sheet_name}, Summary'],
        ['Data read back from the first sheet.'],
        ['Name', 'Role', 'Hours'],
        ['Alice', 'Developer', 38],
        ['Bob', 'Tester', 35],
        ['Carla', 'Project manager', 40]
    ]


SHEETS_SHEET: list[SheetContentExpectation] = [
    SheetContentExpectation(sheet_name='Sheet', row_fragments=MAIN_SHEET_ROWS),
    SheetContentExpectation(sheet_name='Summary',
                            row_fragments=build_summary_rows('Sheet'))
]

SHEETS_SHEET1: list[SheetContentExpectation] = [
    SheetContentExpectation(sheet_name='Sheet1',
                            row_fragments=MAIN_SHEET_ROWS),
    SheetContentExpectation(sheet_name='Summary',
                            row_fragments=build_summary_rows('Sheet1'))
]


@pytest.mark.parametrize('example, expected_fragments',
                         [(Example(example_function=e09_multi_sheet,
                                   format_name='ods',
                                   implementation_name='odfdo'),
                           SHEETS_SHEET1),
                          (Example(example_function=e09_multi_sheet,
                                   format_name='excel',
                                   implementation_name='openpyxl'),
                           SHEETS_SHEET),
                          (Example(example_function=e09_multi_sheet,
                                   format_name='excel',
                                   implementation_name='pylightxl'),
                           SHEETS_SHEET1)])
def test_e09_multi_sheet_spreadsheet(
        capsys: pytest.CaptureFixture[str], example: Example,
        expected_fragments: list[SheetContentExpectation]) -> None:
    """Test e09 for spreadsheet formats and implementations."""
    check_example_spreadsheet(example=example, capture=capsys,
                              expected_fragments=expected_fragments)
